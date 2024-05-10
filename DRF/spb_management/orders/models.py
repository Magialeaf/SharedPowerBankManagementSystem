from django.db import models

from orders.utils.orders import generate_unique_order_number


class PowerBankRentalInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    number = models.CharField(verbose_name="订单号", unique=True, max_length=35)
    power_bank = models.ForeignKey("power_bank.PowerBankInfo", verbose_name="充电宝", on_delete=models.CASCADE)
    user = models.ForeignKey("users.UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    returned = models.BooleanField(verbose_name="是否归还", default=False)
    rental_date = models.DateTimeField(verbose_name="开始时间", auto_now_add=True)


class PowerBankReturnInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    rental = models.ForeignKey("orders.PowerBankRentalInfo", verbose_name="租赁记录", on_delete=models.CASCADE)
    return_date = models.DateTimeField(verbose_name="归还时间", auto_now_add=True)


class PowerBankFeeInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    rental = models.ForeignKey("orders.PowerBankRentalInfo", verbose_name="租赁记录", on_delete=models.CASCADE)
    pay_date = models.DateTimeField(verbose_name="支付时间", null=True)
    fee = models.DecimalField(verbose_name="费用", decimal_places=2, max_digits=10)
    paid = models.BooleanField(verbose_name="是否支付", default=False)
