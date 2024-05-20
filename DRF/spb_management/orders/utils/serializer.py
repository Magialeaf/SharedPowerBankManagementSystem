import math
from sqlite3 import IntegrityError

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from orders.models import PowerBankRentalInfo, PowerBankReturnInfo, PowerBankFeeInfo
from orders.utils.orders import generate_unique_order_number
from power_bank.models import PowerBankInfo, StatusDescription
from users.models import UserInfo
from django.utils import timezone


class PowerBankRentalSerializer(serializers.ModelSerializer):
    power_bank = serializers.PrimaryKeyRelatedField(
        queryset=PowerBankInfo.objects.all(), error_messages={'required': '请选择充电宝', 'null': "充电宝不能为空"})
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserInfo.objects.all(), error_messages={'required': '请选择用户', 'null': "用户不能为空"}),
    rental_date = serializers.DateTimeField(
        default=timezone.now(), error_messages={'null': "开始时间不能为空"})
    returned = serializers.BooleanField(default=False),

    class Meta:
        model = PowerBankRentalInfo
        fields = "__all__"
        read_only_fields = ['number']

    @transaction.atomic
    def create(self, validated_data):
        try:
            if validated_data.get('power_bank').status != StatusDescription.free and validated_data.get('power_bank').status != StatusDescription.charging:
                raise ValidationError("充电宝不可使用")
            elif validated_data.get('power_bank').electricity_percentage <= 5:
                raise ValidationError("充电宝电量不足")

            validated_data['number'] = generate_unique_order_number()
            instance = PowerBankRentalInfo.objects.create(**validated_data)
            instance.power_bank.status = StatusDescription.borrowed
            instance.power_bank.save()

            from my_celery.orders.tasks import check_charging_status, cancel_charging_task_by_power_bank_id
            cancel_charging_task_by_power_bank_id(instance.power_bank.id)
            check_charging_status.delay(instance.power_bank.id)
            return instance
        except IntegrityError as e:
            raise ValidationError(e)

    @transaction.atomic
    def update(self, instance, validated_data):
        returned = validated_data.get('returned', False)
        if returned:
            instance.returned = True

            # 创建归还记录，这里不使用try-except，因为如果约束失败事务会自动回滚
            PowerBankReturnInfo.objects.create(
                rental=instance,
                return_date=timezone.now()
            )

            # 更新或创建费用记录
            fee_count = instance.power_bank.hourly_fee * math.ceil((timezone.now() - instance.rental_date).total_seconds() / 3600)
            PowerBankFeeInfo.objects.create(
                rental=instance,
                fee=fee_count,
                paid=False
            )

            instance.power_bank.status = StatusDescription.charging
            instance.power_bank.save()
            instance.save()  # 明确指定更新字段

            from my_celery.orders.tasks import charge_power_bank,cancel_charging_task_by_power_bank_id
            cancel_charging_task_by_power_bank_id(instance.power_bank.id)
            charge_power_bank.delay(instance.power_bank.id)
            return instance

        raise serializers.ValidationError("更新失败")

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['power_bank_name'] = instance.power_bank.name
        res['user_name'] = instance.user.username
        return res


class PowerBankReturnSerializer(serializers.ModelSerializer):
    return_date = serializers.DateTimeField(default=timezone.now(), error_messages={'null': "归还时间不能为空"})

    class Meta:
        model = PowerBankReturnInfo
        fields = "__all__"

    # def create(self, validated_data):
    #     return PowerBankReturnInfo.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.save()
    #     return instance

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['number'] = instance.rental.number
        res['power_bank'] = instance.rental.power_bank.id
        res['user'] = instance.rental.user.id
        res['power_bank_name'] = instance.rental.power_bank.name
        res['user_name'] = instance.rental.user.username
        return res


class PowerBankFeeSerializer(serializers.ModelSerializer):
    fee = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, error_messages={'null': "费用不能为空"})
    paid = serializers.BooleanField(default=False)

    class Meta:
        model = PowerBankFeeInfo
        fields = "__all__"

    # def create(self, validated_data):
    #     try:
    #         # 尝试获取关联的已归还的租赁实例
    #         rental_instance = PowerBankRentalInfo.objects.get(
    #             user=validated_data['user'],
    #             power_bank=validated_data['power_bank'],
    #             returned=True
    #         )
    #     except ObjectDoesNotExist:
    #         # 如果找不到对应的已归还的租赁实例，则抛出异常
    #         raise serializers.ValidationError("没有找到与该用户和充电宝匹配的已归还的租赁记录。")
    #
    #     hourly_fee = rental_instance.power_bank.hourly_fee
    #     rental_date = rental_instance.rental_date
    #     return_date = validated_data.get('return_date')  # 确保return_date存在
    #
    #     if return_date is None:
    #         raise serializers.ValidationError("归还时间不存在")
    #
    #     hours_diff = math.ceil((return_date - rental_date).total_seconds() / 3600)
    #     fee = hourly_fee * hours_diff
    #     validated_data['fee'] = fee
    #
    #     return PowerBankFeeInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        paid = validated_data.get('paid', False)
        if paid:
            instance.paid = True
            instance.pay_date = timezone.now()
            instance.save()
            return instance
        raise serializers.ValidationError("更新失败")


    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['number'] = instance.rental.number
        res['power_bank'] = instance.rental.power_bank.id
        res['user'] = instance.rental.user.id
        res['power_bank_name'] = instance.rental.power_bank.name
        res['user_name'] = instance.rental.user.username
        return res


class OrderUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerBankRentalInfo
        fields = '__all__'

    def to_representation(self, instance):
        return_query = PowerBankReturnInfo.objects.filter(rental=instance).first()
        fee_query = PowerBankFeeInfo.objects.filter(rental=instance).first()

        result = {
            'rental': instance.id,
            'number': instance.number,
            'power_bank': instance.power_bank.id,
            'power_bank_name': instance.power_bank.name,
            'rental_date': instance.rental_date,
            'returned': instance.returned,
            'return_date': return_query.return_date if return_query else None,
            'pay_date': fee_query.pay_date if fee_query else None,
            'fee': fee_query.fee if fee_query else None,
            'paid': fee_query.paid if fee_query else None,
        }

        return result