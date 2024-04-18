from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from spb_management.router.response_data import ResponseCode, response_data
from users.models import Identity


""" —————————————————————————————— """
""" |            基类             | """
""" —————————————————————————————— """


class MyBasePermission(BasePermission):
    # 自定义错误信息返回
    message = response_data(ResponseCode.NOT_AUTH, '无权访问', {})

    def __init__(self, target_identity: tuple):
        super().__init__()
        self.target_identity = target_identity

    # 校验函数
    def has_permission(self, request, view):
        # 匿名用户无权访问
        if isinstance(request.user, AnonymousUser):
            raise AuthenticationFailed(detail=MyBasePermission.message)

        identity = request.user.get("identity", "")
        if identity in self.target_identity:
            return True

        return False


""" —————————————————————————————— """
""" |           具体类             | """
""" —————————————————————————————— """


class NotAnonPermission(BasePermission):
    # 自定义错误信息返回
    message = response_data(ResponseCode.NOT_AUTH, '无权访问', {})

    def __init__(self):
        super().__init__()

    # 校验函数
    def has_permission(self, request, view):
        # 匿名用户无权访问
        if isinstance(request.user, AnonymousUser):
            raise AuthenticationFailed(detail=NotAnonPermission.message)

        identity = request.user.get("identity", "")
        if identity is not Identity.ANON:
            return True

        return False


class SuperAdminPermission(MyBasePermission):
    def __init__(self):
        super().__init__((Identity.SUPER_ADMIN.value, ))


class AdminPermission(MyBasePermission):
    def __init__(self):
        super().__init__((Identity.ADMIN.value, ))


class MaintainerPermission(MyBasePermission):
    def __init__(self):
        super().__init__((Identity.MAINTAINER.value, ))


class UserPermission(MyBasePermission):
    def __init__(self):
        super().__init__((Identity.USER.value, ))


class MoreAndAdminPermission(MyBasePermission):
    def __init__(self):
        super().__init__((Identity.SUPER_ADMIN.value, Identity.ADMIN.value))


class MoreAndMaintainerPermission(MyBasePermission):
    def __init__(self):
        super().__init__((Identity.SUPER_ADMIN.value, Identity.ADMIN.value, Identity.MAINTAINER.value))