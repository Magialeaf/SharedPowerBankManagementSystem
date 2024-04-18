from django.db import models

from spb_management.router.image_operation import ImgAPI


class MerchantInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    shop_name = models.CharField(max_length=20, verbose_name='商户名称')
    area = models.ForeignKey('areas.AreaInfo', verbose_name='所属区域', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=30, verbose_name='详细地址')
    liaison = models.CharField(max_length=20, verbose_name='联系人')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    shop_img = models.ImageField(verbose_name='商户图片', upload_to=ImgAPI.merchant_img_path)