from django.http import HttpResponseNotFound


# 异常中间件
class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        res = self.get_response(request)
        if res.status_code == 404:
            return HttpResponseNotFound('API不存在')
        return res
