from django.db import models


class PowerBankRentalInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    power_bank = models.ForeignKey("power_bank.PowerBankInfo", verbose_name="充电宝", on_delete=models.CASCADE)
    user = models.ForeignKey("users.UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    returned = models.BooleanField(verbose_name="是否归还", default=False)
    rental_date = models.DateTimeField(verbose_name="开始日期", auto_now_add=True)


class PowerBankReturnInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    power_bank = models.ForeignKey("power_bank.PowerBankInfo", verbose_name="充电宝", on_delete=models.CASCADE)
    user = models.ForeignKey("users.UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    return_date = models.DateTimeField(verbose_name="归还日期", auto_now_add=True)


class PowerBankFeeInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    power_bank = models.ForeignKey("power_bank.PowerBankInfo", verbose_name="充电宝", on_delete=models.CASCADE)
    user = models.ForeignKey("users.UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    fee = models.DecimalField(verbose_name="费用", decimal_places=2, max_digits=10)
    paid = models.BooleanField(verbose_name="是否支付", default=False)
