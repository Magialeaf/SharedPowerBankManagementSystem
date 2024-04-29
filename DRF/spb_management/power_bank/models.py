from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from spb_management.router.image_operation import ImgAPI

POWER_BANK_STATUS_CHOICES = (
    (0, "空闲"),
    (1, "充电中"),
    (2, "已借出"),
    (3, "已损坏"),
    (4, "已报废"),
)

POWER_BANK_ERROR_STATUS_CHOICES = (
    (3, "已损坏"),
    (4, "已报废"),
)


class PowerBankInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    name = models.CharField(verbose_name="名称", max_length=20, default="新充电宝")
    img = models.ImageField(verbose_name="图片", upload_to=ImgAPI.power_bank_img_path, default="default.png", blank=True)
    status = models.SmallIntegerField(verbose_name="状态", choices=POWER_BANK_STATUS_CHOICES, default=0)
    area = models.ForeignKey("areas.AreaInfo", verbose_name="区域", on_delete=models.SET_NULL, null=True)
    merchant = models.ForeignKey("merchants.MerchantInfo", verbose_name="商户", on_delete=models.SET_NULL, null=True)
    hourly_fee = models.DecimalField(verbose_name="每小时费用", decimal_places=2, max_digits=10, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    electricity_percentage = models.IntegerField(verbose_name="电量百分比", validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)

    def get_status_display(self):
        return POWER_BANK_STATUS_CHOICES[self.status][1]


class PowerBankMaintenanceInfo(models.Model):
    id = models.AutoField(verbose_name="id", primary_key=True)
    power_bank = models.ForeignKey(PowerBankInfo, verbose_name="充电宝", on_delete=models.CASCADE)
    status = models.SmallIntegerField(verbose_name="状态", choices=POWER_BANK_ERROR_STATUS_CHOICES, default=3)
    maintainer_account = models.ForeignKey("users.AccountInfo", verbose_name="运维人员", on_delete=models.CASCADE, null=True)
    finished = models.BooleanField(verbose_name="是否完成", default=False)
    date = models.DateTimeField(verbose_name="处理日期", null=True, blank=True)
    question_description = models.CharField(verbose_name="问题描述", max_length=50)
    maintenance_result = models.CharField(verbose_name="处理结果", max_length=50)
