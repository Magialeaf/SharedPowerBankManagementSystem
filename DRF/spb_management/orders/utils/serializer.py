import math

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from orders.models import PowerBankRentalInfo, PowerBankReturnInfo, PowerBankFeeInfo
from power_bank.models import PowerBankInfo
from users.models import UserInfo
from django.utils import timezone


class PowerBankRentalSerializer(serializers.ModelSerializer):
    power_bank = serializers.PrimaryKeyRelatedField(queryset=PowerBankInfo.objects.all(), error_messages={'null': "充电宝不能为空"})
    user = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), error_messages={'null': "用户不能为空"})
    rental_date = serializers.DateTimeField(default=timezone.now(), error_messages={'null': "开始时间不能为空"})
    returned = serializers.BooleanField(default=False)

    class Meta:
        model = PowerBankRentalInfo
        fields = "__all__"

    def create(self, validated_data):
        return PowerBankRentalInfo.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        returned = validated_data.get('returned', False)
        if returned:
            instance.returned = True

            # 创建归还记录，这里不使用try-except，因为如果约束失败事务会自动回滚
            PowerBankReturnInfo.objects.create(
                power_bank=instance.power_bank,
                user=instance.user,
                return_date=timezone.now()
            )

            # 更新或创建费用记录
            fee_count = instance.power_bank.hourly_fee * math.ceil((timezone.now() - instance.rental_date).total_seconds() / 3600)
            PowerBankFeeInfo.objects.create(
                power_bank=instance.power_bank,
                user=instance.user,
                fee=fee_count,
                paid=False
            )

        instance.save()  # 明确指定更新字段
        return instance

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['power_bank_name'] = instance.power_bank.name
        res['user_name'] = instance.user.username
        return res


class PowerBankReturnSerializer(serializers.ModelSerializer):
    power_bank = serializers.PrimaryKeyRelatedField(queryset=PowerBankInfo.objects.all(), error_messages={'null': "充电宝不能为空"})
    user = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), error_messages={'null': "用户不能为空"})
    return_date = serializers.DateTimeField(default=timezone.now(), error_messages={'null': "归还时间不能为空"})

    class Meta:
        model = PowerBankReturnInfo
        fields = "__all__"

    def create(self, validated_data):
        return PowerBankReturnInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['power_bank_name'] = instance.power_bank.name
        res['user_name'] = instance.user.username
        return res


class PowerBankFeeSerializer(serializers.ModelSerializer):
    power_bank = serializers.PrimaryKeyRelatedField(queryset=PowerBankInfo.objects.all(), error_messages={'null': "充电宝不能为空"})
    user = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), error_messages={'null': "用户不能为空"})
    fee = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, error_messages={'null': "费用不能为空"})
    paid = serializers.BooleanField(default=False)

    class Meta:
        model = PowerBankFeeInfo
        fields = "__all__"

    def create(self, validated_data):
        try:
            # 尝试获取关联的已归还的租赁实例
            rental_instance = PowerBankRentalInfo.objects.get(
                user=validated_data['user'],
                power_bank=validated_data['power_bank'],
                returned=True
            )
        except ObjectDoesNotExist:
            # 如果找不到对应的已归还的租赁实例，则抛出异常
            raise serializers.ValidationError("没有找到与该用户和充电宝匹配的已归还的租赁记录。")

        hourly_fee = rental_instance.power_bank.hourly_fee
        rental_date = rental_instance.rental_date
        return_date = validated_data.get('return_date')  # 确保return_date存在

        if return_date is None:
            raise serializers.ValidationError("归还时间不存在")

        hours_diff = math.ceil((return_date - rental_date).total_seconds() / 3600)
        fee = hourly_fee * hours_diff
        validated_data['fee'] = fee

        return PowerBankFeeInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.paid = validated_data.get('paid', instance.paid)
        instance.save()
        return instance

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['power_bank_name'] = instance.power_bank.name
        res['user_name'] = instance.user.username
        return res
