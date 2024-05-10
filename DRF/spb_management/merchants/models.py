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


class MerchantCommentInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    merchant = models.ForeignKey(
        'MerchantInfo',
        verbose_name='商户',
        on_delete=models.CASCADE,
        related_name='comments'  # 为商户的评论提供反向查询
    )
    user = models.ForeignKey(
        'users.UserInfo',
        verbose_name='用户',
        on_delete=models.SET_NULL,
        null=True,
        related_name='merchant_comments'  # 为用户的评论提供反向查询
    )
    parent_comment = models.ForeignKey(
        'self',
        verbose_name='父评论',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='replies'  # 为评论的回复提供反向查询
    )
    comment = models.CharField(max_length=100, verbose_name='评论内容')
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        ordering = ['-comment_date']  # 按评论时间降序排列
