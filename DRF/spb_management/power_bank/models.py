# from django.db import models
#
# # Create your models here.
# class ChargePile(models.Model):
#     id = models.CharField(max_length=50, primary_key=True)  # 充电宝ID
#     model = models.CharField(max_length=50)  # 充电宝型号
#     status = models.CharField(max_length=20)  # 充电宝状态（如：空闲、使用中、故障等）
#     location = models.ForeignKey('areas.Location', on_delete=models.CASCADE)  # 关联具体的地理位置信息
#
# class DeviceHistory(models.Model):
#     charge_pile = models.ForeignKey(ChargePile, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     status_before = models.CharField(max_length=20)
#     status_after = models.CharField(max_length=20)
#     # 其他变动记录字段...
