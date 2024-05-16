# tasks.py
from celery.result import AsyncResult
from django.core.cache import caches
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
    print("任务初始化了")
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
            schedule_and_store_task_id(check_charging_status, order.power_bank.id, next_time)
            check_charging_status.apply_async((order.power_bank.id,), countdown=next_time)

    # 获取所有在充电的充电宝
    charging_power_banks = PowerBankInfo.objects.filter(status=StatusDescription.charging)
    for power_bank in charging_power_banks:
        schedule_and_store_task_id(charge_power_bank, power_bank.id, unit)

    print("初始化结束了")


@app.task(bind=True)
def check_charging_status(self, power_bank: int):
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
                schedule_and_store_task_id(check_charging_status, power_bank.id, unit)
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


@app.task(bind=True)
def charge_power_bank(self, power_bank: int):
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
            schedule_and_store_task_id(charge_power_bank, power_bank.id, unit)
            log.info(f"充电宝 {power_bank.id} 充电一次完成。剩余电量: {power_bank.electricity_percentage}%")
            if power_bank.electricity_percentage == 100:
                power_bank.status = StatusDescription.free
                power_bank.save(update_fields=["status"])
                log.warning(f"编号为 {power_bank.id} 的充电宝已满电，无法充电。")
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


# 新建celery任务存储到redis中
def schedule_and_store_task_id(func, power_bank_id, countdown=unit):
    task = func.apply_async((power_bank_id,), countdown=countdown)
    cache_key = f'task:{power_bank_id}'
    caches['power_bank'].set(cache_key, task.id, unit * 2)  # 存储任务ID到缓存
    return task


# 取消celery任务
def cancel_charging_task_by_power_bank_id(power_bank_id):
    cache_key = f'task:{power_bank_id}'
    task_id = caches['power_bank'].get(cache_key)  # 从缓存中获取任务ID
    if task_id:
        task = AsyncResult(task_id)
        if not task.ready():  # 检查任务是否已完成
            task.revoke(terminate=True)  # 取消任务
            log.info(f"成功取消了编号为 {power_bank_id} 的充电宝的任务。")
        else:
            log.info(f"编号为 {power_bank_id} 的充电宝的任务已经完成或不存在。")
    else:
        log.warning(f"没有找到编号为 {power_bank_id} 的充电宝的任务ID。")