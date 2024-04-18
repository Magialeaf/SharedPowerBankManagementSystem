import abc
from django.core.cache import caches
from rest_framework.exceptions import Throttled
from rest_framework.throttling import SimpleRateThrottle

from spb_management.router import Internet
from spb_management.router.response_data import ResponseCode,response_data


""" —————————————————————————————— """
""" |          基类               | """
""" —————————————————————————————— """


class BaseThrottle(SimpleRateThrottle):
    scope = "base"
    THROTTLE_RATES = {"base": "5/h"}
    cache = caches["throttle"]

    @abc.abstractmethod
    def get_cache_key(self, request, view):
        """Abstract method for defining the cache key generation logic."""
        pass

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        if period[0] in 'smhd':
            duration = time_units[period[0]]
        else:
            duration = int(period[:-1]) * time_units[period[-1]]
        return (num_requests, duration)

    def throttle_failure(self):
        minutes_to_wait = int(self.wait() / 60) + 1
        raise Throttled(detail=response_data(ResponseCode.ERROR, f"请求过于频繁，请{minutes_to_wait}分钟后再试", {}))


class AnonThrottle(BaseThrottle):
    def get_cache_key(self, request, view):
        ip = Internet.get_real_ip(request)
        return self.cache_format % {'scope': self.scope, 'ident': ip}


class AuthThrottle(BaseThrottle):
    def get_cache_key(self, request, view):
        aid = str(request.user.get("aid", ""))
        ip = Internet.get_real_ip(request)
        return self.cache_format % {'scope': self.scope, 'ident': aid + "|" + ip}


# class LoginThrottle(UserThrottle):
#     scope = "login"
#     THROTTLE_RATES = {"login": "5/m"}
#     cache = caches["throttle"]
#
#     def allow_request(self, request, view):
#         # 获取请求中的动作
#         if request.method == 'POST':
#             action = request.POST.get('action', '')
#         else:
#             action = ""
#
#         # 检查是否针对特定动作进行限流
#         if action == 'login' or action == "register":
#             return super().allow_request(request, view)
#
#         # 如果不是特定动作，则不执行此限流策略
#         return True
