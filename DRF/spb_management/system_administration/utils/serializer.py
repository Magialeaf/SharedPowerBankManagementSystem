from django.utils import timezone
from rest_framework import serializers


from spb_management.router.image_operation import ImgAPI
from system_administration.models import CarouselChartInfo, NoticeInfo
from users.models import AccountInfo, UserInfo


# class CarouselChart(models.Model):
#     id = models.AutoField(verbose_name="id", primary_key=True)
#     img = models.ImageField(verbose_name='轮播图', upload_to=ImgAPI.carousel_chart_path)
#     title = models.CharField(max_length=20, verbose_name='标题')
#     active = models.BooleanField(default=True, verbose_name='是否启用')


class CarouselChartSerializer(serializers.ModelSerializer):
    img = serializers.CharField(max_length=64)
    active = serializers.IntegerField()

    class Meta:
        model = CarouselChartInfo
        fields = '__all__'

    def validated_active(self, value):
        value = int(value)
        if value == 1:
            value = True
        elif value == 0:
            value = False
        else:
            raise serializers.ValidationError('active参数错误')
        return value

    def create(self, validated_data):
        return CarouselChartInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.img = validated_data.get('img', instance.img)
        instance.active = validated_data.get('active', instance.active)
        instance.update_time = timezone.now()
        instance.save()
        return instance

    def to_representation(self, instance):
        if isinstance(instance, dict):
            img = instance['img']
        else:
            img = instance.img
        res = super().to_representation(instance)

        res['img'] = ImgAPI.get_carousel_chart(img)
        return res


class CarouselChartImgSerializer(serializers.Serializer):
    img = serializers.CharField(max_length=64)

    class Meta:
        model = CarouselChartInfo
        fields = ('id', 'img')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['img'] = ImgAPI.get_carousel_chart(res['img'])
        return res


class NoticeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20, error_messages={'null': "标题不能为空", "max_length": "标题长度不能超过20个字符"})
    content = serializers.CharField(max_length=100, error_messages={'null': "内容不能为空", "max_length": "内容长度不能超过100个字符"})
    uid = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), error_messages={'null': "发布者不能为空"})
    img = serializers.CharField(max_length=64, allow_null=True, default='default.png', error_messages={"max_length": "图片地址长度不能超过64个字符"})
    type = serializers.IntegerField(error_messages={'null': "类型不能为空"})

    class Meta:
        model = NoticeInfo
        fields = '__all__'

    def create(self, validated_data):
        return NoticeInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.type = validated_data.get('type', instance.type)
        instance.update_time = timezone.now()
        instance.save()
        return instance

    def to_representation(self, instance):
        img = instance.img
        res = super().to_representation(instance)
        res['uid_name'] = instance.uid.username
        res['img'] = ImgAPI.get_notice_img(img)
        return res



