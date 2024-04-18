# from django.db import models
#
# # Create your models here.
#
# ### admin (system_administration) 应用
# # 根据实际情况定义所需的系统管理相关模型，这里假设有一个简单的日志模型
#
# class SystemLog(models.Model):
#     action_time = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
#     action_type = models.CharField(max_length=50)
#     message = models.TextField()
#
# # 注意：以上代码仅为示例，实际建模时需根据业务需求调整字段类型、长度、约束条件等细节