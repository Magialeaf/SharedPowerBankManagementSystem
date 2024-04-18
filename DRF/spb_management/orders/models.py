# from django.db import models
#
# # Create your models here.
# ### orders 应用
# class Order(models.Model):
#     user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
#     charge_pile = models.ForeignKey('charge_piles.ChargePile', on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(null=True, blank=True)  # 结束时间可能为空，表示未结束的订单
#     total_amount = models.DecimalField(max_digits=..., decimal_places=...)
#     status = models.CharField(max_length=20)  # 订单状态（如：待支付、已支付、已完成、已取消等）