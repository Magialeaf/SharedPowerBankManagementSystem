# check_result.py
from celery.result import AsyncResult
from my_celery.main import app

'''验证任务的执行状态的'''


def check_task_status(task_id):
    '''
    任务的执行状态：
        PENDING :等待执行
        STARTED :开始执行
        RETRY   :重新尝试执行
        SUCCESS :执行成功
        FAILURE :执行失败
    :param task_id:
    :return:
    '''
    result = AsyncResult(id=task_id, app=app)
    dic = {
        'code': 400,
        'type': result.status,
        'message': '',
        'data': '',

    }
    if result.status == 'PENDING':
        dic['message'] = '任务等待中'
    elif result.status == 'STARTED':
        dic['message'] = '任务开始执行'
    elif result.status == 'RETRY':
        dic['message'] = '任务重新尝试执行'
    elif result.status == 'FAILURE':
        dic['message'] = '任务执行失败了'
    elif result.status == 'SUCCESS':
        result = result.get()
        dic['message'] = '任务执行成功'
        dic['data'] = result
        dic['code'] = 200
        # result.forget() # 将结果删除
        # async.revoke(terminate=True)  # 无论现在是什么时候，都要终止
        # async.revoke(terminate=False) # 如果任务还没有开始执行呢，那么就可以终止。
    return dic

print(check_task_status('9540f047-88fb-4869-b762-d7c13f499556'))