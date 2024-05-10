# main.py
# 主程序
import os
from datetime import timedelta

from celery import Celery
from spb_management.settings import TIME_ZONE

# 把celery和django进行组合，识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spb_management.settings')

import redis

# 清空当前数据库
r = redis.Redis(host="127.0.0.1", port=6379, db=14)
r.flushdb()

r = redis.Redis(host="127.0.0.1", port=6379, db=15)
r.flushdb()

# 创建celery实例对象
app = Celery("orders")

# 通过app对象加载配置
app.config_from_object("my_celery.config")

# 加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称（因此名称必须是tasks.py）
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["my_celery.orders",])


# 初始化执行某个任务
app.send_task('my_celery.orders.tasks.start_check_charging_status')
# 启动Celery的命令
# 强烈建议切换目录到my_celery的根目录下启动（不是my_celery里面）
# celery -A my_celery.main beat
# celery -A my_celery.main worker --loglevel=info