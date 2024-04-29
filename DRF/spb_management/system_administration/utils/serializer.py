from django.utils import timezone
from rest_framework import serializers


from spb_management.router.image_operation import ImgAPI
from system_administration.models import CarouselChartInfo, NoticeInfo


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


# class NoticeInfo(models.Model):
#     id = models.AutoField(verbose_name="id", primary_key=True)
#     title = models.CharField(verbose_name="标题", max_length=20)
#     content = models.CharField(verbose_name="内容", max_length=100)
#     type = models.SmallIntegerField(verbose_name="类型", choices=((0, "管理员公告"), (1, "维护人员公告"), (2, "全体公告")))
#     create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#     update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

class NoticeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=20, error_messages={'null': "标题不能为空", "max_length": "标题长度不能超过20个字符"})
    content = serializers.CharField(max_length=100, error_messages={'null': "内容不能为空", "max_length": "内容长度不能超过100个字符"})
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
        res = super().to_representation(instance)
        return res



