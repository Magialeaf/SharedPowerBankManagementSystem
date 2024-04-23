import re
from rest_framework import serializers

from areas.models import AreaInfo
from merchants.models import MerchantInfo
from spb_management.router.image_operation import ImgAPI

shopNameLen = 20
addressLen = 30
liaisonLen = 20
phoneLen = 11


class MerchantSerializer(serializers.ModelSerializer):
    shop_img = serializers.CharField(max_length=64, error_messages={
        'required': "缺少图片",
        'blank': '图片不能为空',
        'max_length': '图片名字太长。',
    })
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
            'area': save_data.area.code + '|' + save_data.area.name,
            'address': save_data.address,
            'liaison': save_data.liaison,
            'phone': save_data.phone,
            'shop_img': ImgAPI.get_merchant_img(save_data.shop_img)
        }
        return save_data

    def update(self, instance, validated_data):
        instance.shop_name = validated_data.get('shop_name', instance.shop_name)
        instance.area = validated_data.get('area', instance.area)
        instance.address = validated_data.get('address', instance.address)
        instance.liaison = validated_data.get('liaison', instance.liaison)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.shop_img = validated_data.get('shop_img', instance.shop_img)
        instance.save()

        res = {
            'id': instance.id,
            'shop_name': instance.shop_name,
            'area': instance.area_id,
            'address': instance.address,
            'liaison': instance.liaison,
            'phone': instance.phone,
            'shop_img': ImgAPI.get_merchant_img(instance.shop_img)
        }

        area_info = AreaInfo.objects.filter(id=instance.area_id).values("code", "name").first()
        if not area_info:
            res['area_data'] = "000000" + "|" + ''
        else:
            res['area_data'] = area_info['code'] + '|' + area_info['name']
        return res

    def to_representation(self, data):
        if isinstance(data, dict):
            res = {
                'id': data['id'],
                'shop_name': data['shop_name'],
                'area': data['area_id'],
                'address': data['address'],
                'liaison': data['liaison'],
                'phone': data['phone'],
                'shop_img': ImgAPI.get_merchant_img(data['shop_img'])
            }

            area_info = AreaInfo.objects.filter(id=data['area_id']).values("code", "name").first()
            if not area_info:
                res['area_data'] = "000000" + "|" + ''
            else:
                res['area_data'] = area_info['code'] + '|' + area_info['name']
        else:
            res = {
                'id': data.id,
                'area': data.area_id,
                'shop_name': data.shop_name,
                'address': data.address,
                'liaison': data.liaison,
                'phone': data.phone,
                'shop_img': ImgAPI.get_merchant_img(data.shop_img)
            }

            area_info = AreaInfo.objects.filter(id=data.area_id).values("code", "name").first()
            if not area_info:
                res['area_data'] = "000000" + "|" + ''
            else:
                res['area_data'] = area_info['code'] + '|' + area_info['name']

        return res


