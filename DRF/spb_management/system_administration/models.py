from django.db import models
from spb_management.router.image_operation import ImgAPI


class NoticeInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=20)
    content = models.CharField(verbose_name="内容", max_length=100)
    type = models.SmallIntegerField(verbose_name="类型", choices=((0, "管理员公告"), (1, "维护人员公告"), (2, "全体公告")))
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)


class CarouselChartInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    img = models.ImageField(verbose_name='轮播图', upload_to=ImgAPI.carousel_chart_path)
    title = models.CharField(max_length=20, verbose_name='标题')
    active = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)



