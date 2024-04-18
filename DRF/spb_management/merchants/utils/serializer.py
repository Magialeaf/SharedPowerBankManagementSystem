import re
from rest_framework import serializers
from merchants.models import MerchantInfo
from spb_management.router.image_operation import ImgAPI

shopNameLen = 20
addressLen = 30
liaisonLen = 20
phoneLen = 11

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantInfo
        fields = ('id', 'shop_name', 'area', 'address', 'liaison', 'phone', 'shop_img')
        read_only_fields = ('id',)

    # 定义自定义验证方法
    def validate_shop_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('商户名称不能为空')

        if len(value) > 20:
            raise serializers.ValidationError(f"商户名称不能超过{shopNameLen}个字符")

        return value

    def validate_area(self, value):
        if not value:
            raise serializers.ValidationError('所属区域不能为空')
        return value

    def validate_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('详细地址不能为空')

        if len(value) > 30:
            raise serializers.ValidationError(f"详细地址不能超过{addressLen}个字符")

        return value

    def validate_liaison(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('联系人不能为空')

        if len(value) > 20:
            raise serializers.ValidationError(f"联系人不能超过{liaisonLen}个字符")

        return value

    def validate_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('联系电话不能为空')

        numeric_regex = r'^\d{1,11}$'
        if not re.match(numeric_regex, value):
            raise serializers.ValidationError(f"联系电话是纯数字且不能超过{phoneLen}位")

        return value

    def validate_shop_img(self, value):
        if not value:
            raise serializers.ValidationError('商户图片不能为空')
        return value

    def create(self, validated_data):
        save_data = MerchantInfo.objects.create(**validated_data)
        save_data = {
            'id': save_data.id,
            'shop_name': save_data.shop_name,
            'area': save_data.area,
            'address': save_data.address,
            'liaison': save_data.liaison,
            'phone': save_data.phone,
            'shop_img': ImgAPI.get_merchant_img(save_data.shop_img)
        }
        return save_data





