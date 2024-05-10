# tasks.py
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from my_celery.main import app
from power_bank.models import PowerBankInfo, StatusDescription
from orders.models import PowerBankRentalInfo
from orders.utils.serializer import PowerBankRentalSerializer
from celery import signals
import time

import logging

# 配置日志支持中文输出
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
log = logging.getLogger("django")

log.addHandler(handler)
log.setLevel(logging.INFO)

# 假设PowerBankInfo模型有一个名为`current_charge`的字段表示当前电量
# 如果没有这个字段，你需要添加一个或修改现有字段来存储电量

# 每小时执行一次
# unit = 60 * 60
unit = 10

@app.task
def start_check_charging_status():
    print("任务初始化了喵")
    # 删除历史遗留任务防止里面的任务直接被运行
    # 清空当前数据库
    import redis
    r = redis.Redis(host="127.0.0.1", port=6379, db=14)
    r.flushdb()

    r = redis.Redis(host="127.0.0.1", port=6379, db=15)
    r.flushdb()

    # 获取所有未归还的充电宝
    orders = PowerBankRentalInfo.objects.filter(returned=False)

    # 对每个充电宝执行任务
    for order in orders:
        # 超过12小时直接归还
        hold_time = timezone.now() - order.rental_date
        if hold_time >= timezone.timedelta(hours=unit * 12):
            # 准备更新数据，假设标记为已归还
            data = {"returned": True}
            serializer = PowerBankRentalSerializer(instance=order, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                log.info(f"编号为 {order.power_bank.id} 的充电宝超过12小时未归还，已自动归还。")
            else:
                log.error(f"归还失败: {serializer.errors}")
        else:
            # 计算下一次检查时间
            next_time = unit - hold_time.total_seconds() % unit
            check_charging_status.apply_async((order.power_bank.id,), countdown=next_time)

    print("初始化结束了喵")


@app.task
def check_charging_status(power_bank: int):
    print(f"开始检查编号为 {power_bank} 的充电宝的电量。")
    power_bank = PowerBankInfo.objects.filter(id=power_bank).first()
    if not power_bank:
        log.error(f"编号为 {power_bank} 的充电宝不存在。")
        return

    try:
        # 查询与该充电宝关联的未归还租赁信息
        rental_info = PowerBankRentalInfo.objects.filter(power_bank=power_bank, returned=False).first()

        if rental_info:
            # 更新电量，假设每个充电宝初始电量为100%
            if power_bank.electricity_percentage > 5:
                power_bank.electricity_percentage -= 5
                power_bank.save(update_fields=["electricity_percentage"])
                check_charging_status.apply_async((power_bank.id,), countdown=unit)
            else:
                power_bank.electricity_percentage = 0
                power_bank.save(update_fields=["electricity_percentage"])

                # 准备更新数据，假设标记为已归还
                data = {"returned": True}
                serializer = PowerBankRentalSerializer(instance=rental_info, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    log.error(f"更新租赁信息时发生错误: {serializer.errors}")
        else:
            log.warning(f"未找到编号为 {power_bank.id} 的充电宝的租赁信息以进行更新。")

        # 记录日志
        log.info(f"充电宝 {power_bank.id} 的电量检查完成。剩余电量: {power_bank.electricity_percentage}%")

        print(f"power_bank：{power_bank}结束")

    except ObjectDoesNotExist:
        log.error(f"编号为 {power_bank.id} 的充电宝不存在。")
    except Exception as e:
        log.error(f"检查充电状态时出现错误: {e}")


@app.task
def charge_power_bank(power_bank: int):
    print(f"开始充电编号为 {power_bank} 的充电宝。")
    power_bank = PowerBankInfo.objects.filter(id=power_bank).first()
    if not power_bank:
        log.error(f"编号为 {power_bank} 的充电宝不存在。")
        return

    try:
        # 更新电量，假设每个充电宝初始电量为100%
        if power_bank.electricity_percentage < 100:
            power_bank.electricity_percentage = min(power_bank.electricity_percentage + 15, 100)
            power_bank.save(update_fields=["electricity_percentage"])
            charge_power_bank.apply_async((power_bank.id,), countdown=unit)
            log.info(f"充电宝 {power_bank.id} 充电一次完成。剩余电量: {power_bank.electricity_percentage}%")
        else:
            power_bank.status = StatusDescription.free
            power_bank.save(update_fields=["status"])
            log.warning(f"编号为 {power_bank.id} 的充电宝已满电，无法充电。")

        # 记录日志
        log.info(f"充电宝 {power_bank.id} 的单次充电完成。剩余电量: {power_bank.electricity_percentage}%")
        print(f"power_bank：{power_bank}结束")

    except ObjectDoesNotExist:
        log.error(f"编号为 {power_bank.id} 的充电宝不存在。")
    except Exception as e:
        log.error(f"检查充电状态时出现错误: {e}")