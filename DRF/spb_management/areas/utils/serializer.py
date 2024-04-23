from django.core.cache import caches
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from areas.models import AreaInfo
from areas.utils.redis_operation import AreaDataRedis


class AreaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, error_messages={
        'required': "缺少名称",
        'blank': '名字不能为空',
        'max_length': '名称长度不能超过 30 个字符。',
    })
    description = serializers.CharField(required=False, max_length=100, allow_blank=True, error_messages={
        'max_length': '简介长度不能超过 100 个字符。',
    })

    class Meta:
        model = AreaInfo
        fields = ('id', 'code', 'name', 'description', 'latitude', 'longitude')
        validators = [
            UniqueTogetherValidator(
                queryset=AreaInfo.objects.all(),
                fields=['latitude', 'longitude'],
                message='该经纬度已存在对应区域！'
            )
        ]

    def validate(self, attrs):
        # 验证传入的lat和lon是否符合预期条件
        lat = attrs.get('latitude')
        lng = attrs.get('longitude')

        # 假设有一个简单的条件：经纬度均不为None且在[-90, 90]和[-180, 180]范围内
        if lat is not None and lng is not None and 2 <= lat <= 54 and 72 <= lng <= 136:
            return attrs
        else:
            raise serializers.ValidationError("经纬度输入不合法")

    def to_representation(self, instance):
        return super().to_representation(instance)

    def create(self, validated_data):
        save_data = AreaInfo.objects.create(**validated_data)
        save_data = {
            "id": save_data.id,
            "code": save_data.code,
            "name": save_data.name,
            "description": save_data.description,
            "latitude": save_data.latitude,
            "longitude": save_data.longitude,
        }
        AreaDataRedis.set_area_data(save_data)
        return save_data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        old_cache_key = {
            "id": instance.id,
            "latitude": instance.latitude,
            "longitude": instance.longitude,
        }

        instance.code = validated_data.get('code', instance.code)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()

        AreaDataRedis.delete_area_data(old_cache_key)

        # 构建要缓存的字典数据
        cache_data = {
            "id": instance.id,
            "code": instance.code,
            "name": instance.name,
            "description": instance.description,
            "latitude": instance.latitude,
            "longitude": instance.longitude,
            # 添加其他需要缓存的字段（如果有）
        }

        AreaDataRedis.set_area_data(cache_data)
        return instance


class AreaNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaInfo
        fields = ('id', 'name')

