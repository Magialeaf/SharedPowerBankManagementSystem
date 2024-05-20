from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from my_celery.orders.tasks import charge_power_bank, cancel_charging_task_by_power_bank_id
from merchants.models import MerchantInfo
from power_bank.models import PowerBankInfo, PowerBankMaintenanceInfo, StatusDescription
from spb_management.router.image_operation import ImgAPI
from users.models import UserInfo, AccountInfo


class PowerBankSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20, default="新充电宝", allow_blank=True, error_messages={'max_length': "名称长度不能超过20个字符"})
    img = serializers.CharField(max_length=100, default="default.png", allow_blank=True, error_messages={'max_length': "图片地址长度不能超过100个字符"})
    status = serializers.IntegerField(default=0, error_messages={'required': "缺少状态"})
    hourly_fee = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), error_messages={'required': "缺少每小时费用", 'max_digits': "最多两位小数", 'decimal_places': "最多两位小数"})
    electricity_percentage = serializers.IntegerField(default=100, error_messages={'required': "缺少电量百分比", 'max_value': "电量百分比不能超过100", 'min_value': "电量百分比不能小于0"})

    class Meta:
        model = PowerBankInfo
        fields = "__all__"

    def validate_name(self, value):
        if value == '':
            return '新充电宝'
        return value

    def validate_img(self, value):
        if value == '':
            return 'default.png'
        return value

    def create(self, validated_data):
        return PowerBankInfo.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        if instance.status == StatusDescription.scrap or instance.status == StatusDescription.error:
            query = PowerBankMaintenanceInfo.objects.filter(power_bank=instance, finished=False)
            if query.exists():
                raise serializers.ValidationError("该充电宝正在维修中，请等待维修完成")
        elif status == StatusDescription.charging:
            instance.status = status
            charge_power_bank.delay(instance.id)
        elif instance.status == StatusDescription.charging:
            cancel_charging_task_by_power_bank_id(instance.id)
            instance.status = validated_data.get('status', instance.status)
        elif status == StatusDescription.scrap or status == StatusDescription.error:
            # 产生一条维护记录（如果已经有且未完成，修改状态，如果没有，创建）
            query = PowerBankMaintenanceInfo.objects.filter(power_bank=instance, finished=False)
            if query.exists():
                query.update(status=status)
            else:
                PowerBankMaintenanceInfo.objects.create(power_bank=instance, status=status)
            instance.status = validated_data.get('status', instance.status)
        else:
            instance.status = validated_data.get('status', instance.status)

        instance.name = validated_data.get('name', instance.name)
        instance.img = validated_data.get('img', instance.img)
        instance.area = validated_data.get('area', instance.area)
        try:
            query = set(MerchantInfo.objects.filter(area=instance.area.id).values_list("id", flat=True))
        except AttributeError as e:
            query = set()

        temp_merchant = validated_data.get('merchant', instance.merchant)
        if temp_merchant and temp_merchant.id not in query:
            instance.merchant = None
        else:
            instance.merchant = temp_merchant

        instance.hourly_fee = validated_data.get('hourly_fee', instance.hourly_fee)
        instance.electricity_percentage = validated_data.get('electricity_percentage', instance.electricity_percentage)
        instance.save()
        return instance

    def to_representation(self, instance):
        img = instance.img
        structured_data = super().to_representation(instance)
        structured_data['area_code'] = instance.area.code if instance.area else ''
        structured_data['area_name'] = instance.area.name if instance.area else ''
        structured_data['area_data'] = structured_data['area_code'] + "|" + structured_data['area_name']
        structured_data['merchant_address'] = instance.merchant.address if instance.merchant else None
        structured_data['merchant_name'] = instance.merchant.shop_name if instance.merchant else None
        structured_data['img'] = ImgAPI.get_power_bank_img(img)
        return structured_data


class PowerBankMaintenanceSerializer(serializers.ModelSerializer):
    power_bank = serializers.PrimaryKeyRelatedField(queryset=PowerBankInfo.objects.all(), error_messages={'null': "充电宝不能为空"})
    status = serializers.IntegerField(default=3, error_messages={'required': "缺少状态"})
    date = serializers.CharField(max_length=20, default="", allow_blank=True, error_messages={'max_length': "处理日期长度不能超过20个字符"})
    question_description = serializers.CharField(max_length=50, default="", allow_blank=True, error_messages={'max_length': "问题描述长度不能超过50个字符"})
    maintenance_result = serializers.CharField(max_length=50, default="", allow_blank=True, error_messages={'max_length': "处理结果长度不能超过50个字符"})
    new_status = serializers.IntegerField(default=0, error_messages={'required': "缺少状态"})

    class Meta:
        model = PowerBankMaintenanceInfo
        fields = "__all__"
        extra_kwargs = {
            'new_status': {'read_only': True},
        }

    def validate_date(self, value):
        if value == '':
            return None
        return value

    @transaction.atomic
    def create(self, validated_data):
        power_bank = validated_data.get('power_bank', None)
        query = PowerBankMaintenanceInfo.objects.filter(power_bank=power_bank, finished=False).first()
        if query:
            raise serializers.ValidationError("该充电宝已有未完成的维护记录")
        return PowerBankMaintenanceInfo.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.finished == 1:
            raise serializers.ValidationError("该记录已被处理，无法修改")

        instance.power_bank.status = validated_data.get('new_status', instance.power_bank.status)
        instance.power_bank.save()

        instance.status = validated_data.get('status', instance.status)
        instance.maintainer_account = validated_data.get('maintainer_account', instance.maintainer_account)
        instance.finished = validated_data.get('finished', instance.finished)
        instance.date = validated_data.get('date', instance.date)
        instance.question_description = validated_data.get('question_description', instance.question_description)
        instance.maintenance_result = validated_data.get('maintenance_result', instance.maintenance_result)
        instance.save()
        return instance

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['power_bank_name'] = instance.power_bank.name if instance.power_bank else None
        try:
            query = UserInfo.objects.filter(aid=instance.maintainer_account.id).values("username").first()
            res['maintainer_account_name'] = query['username']
        except AttributeError:
            res['maintainer_account_name'] = None
        return res


