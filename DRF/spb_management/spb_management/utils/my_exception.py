from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import exception_handler
from spb_management.router.response_data import ResponseCode, response, response_data


# 序列化异常处理
def validation_exception(e):
    # print(e)
    first_key = next(iter(e.detail.keys()))
    first_error_message = e.detail[first_key][0]
    return response(ResponseCode.ERROR, first_error_message, {})


# 全局异常处理
def common_exception_handler(exc, context):
    err_response = exception_handler(exc, context)
    if err_response is None:
        if isinstance(exc, (Http404, NotFound)):
            err_response = JsonResponse(
                response_data(ResponseCode.NOT_FOUND, "API不存在", {}),
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            view = context['view']
            print(f'[{view}]: {exc}')
            # 可以考虑在这里添加对其他异常类型的处理

    return err_response
