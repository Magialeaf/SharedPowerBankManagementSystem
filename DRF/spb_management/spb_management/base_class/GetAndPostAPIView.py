from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView

from spb_management.router.response_data import *


class GetAndPostAPIView(APIView):
    """
    基础API视图类，只允许GET和POST方法。
    对于不支持的方法，返回统一的错误响应。
    """
    versioning_class = URLPathVersioning

    def get(self, request, version, **kwargs):
        return response(ResponseCode.ERROR, "请求方法不支持", None)

    def post(self, request, version, **kwargs):
        return response(ResponseCode.ERROR, "请求方法不支持", None)

    def options(self, request, *args, **kwargs):
        allowed_methods = ['GET', 'POST']
        return JsonResponse({'Allow': ', '.join(allowed_methods)}, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, MethodNotAllowed):
            return response(ResponseCode.ERROR, "请求方法不支持", None)

        # 其他异常情况仍按照DRF默认方式处理
        return super().handle_exception(exc)
