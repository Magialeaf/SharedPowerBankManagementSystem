from django.db import models


class AreaInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    code = models.CharField(max_length=6, verbose_name='地图编号')
    name = models.CharField(max_length=30, verbose_name='地图名称')
    description = models.CharField(max_length=100, verbose_name='简介', blank=True)
    latitude = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='纬度')
    longitude = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='经度')

    # 定义经纬度联合唯一约束
    class Meta:
        unique_together = [['latitude', 'longitude']]
