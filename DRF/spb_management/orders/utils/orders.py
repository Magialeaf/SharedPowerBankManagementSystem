import random
import threading
from datetime import datetime

from orders.utils.redis_operation import increment_and_get_sequence

# 全局流水号，初始为0
global_sequence = 0
# 使用锁确保线程安全
sequence_lock = threading.Lock()


def generate_unique_order_number(prefix='SPB#'):
    """
    生成唯一订单号
    :param prefix: 订单号前缀，如'SPB#'
    :return: 唯一订单号字符串
    """
    # 获取当前时间（精确到微秒）
    current_time = datetime.now()
    timestamp_str = current_time.strftime('%Y%m%d%H%M%S%f')

    # 随机数（增加序列的随机性，可以调整范围）
    random_part_1 = random.randint(0, 99)
    random_part_2 = random.randint(0, 999)

    # 获取流水号
    sequence = str(increment_and_get_sequence()).zfill(6)

    # 结合前缀、日期、随机码和流水号生成订单号
    order_number = f"{prefix}{timestamp_str}{random_part_1}{sequence}{random_part_2}"
    return order_number

