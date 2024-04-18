from rest_framework.exceptions import ValidationError

from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.router import Internet
from spb_management.router.Internet import create_jwt_token, set_jwt_token
from spb_management.router.response_data import response, ResponseCode, response_data
from spb_management.utils.captcha import destroy_captcha
from spb_management.utils.my_exception import validation_exception
from users.models import AccountInfo, UserInfo, Identity
from users.utils.serializer import AccountSerializer, UserSerializer
from users.utils.throttle import OneThrottle

# Create your views here.
# 分 * 时 * 天
TOKEN_TIME = 60 * 1 * 1


""" —————————————————————————————— """
""" |      OneUserBase           | """
""" —————————————————————————————— """


class OneUserBase(GetAndPostAPIView):
    throttle_classes = [OneThrottle]
    def get_user_and_account(self, aid):
        account_query = AccountInfo.objects.filter(id=aid).first()
        user_query = UserInfo.objects.filter(aid=aid).first()
        if account_query and user_query:
            account_serializer = AccountSerializer(account_query)
            user_serializer = UserSerializer(user_query)
            account_data = account_serializer.to_representation(account_query)
            user_data = user_serializer.to_representation(user_query)
            return response(ResponseCode.SUCCESS, "获取成功",[account_data, user_data])
        return response(ResponseCode.ERROR, "获取失败", {})

    def update(self, id_, request):
        conditions, data = Internet.get_internet_data(request)
        table = conditions.get("table", "")
        if table == "user":
            return self.update_user(id_, data)
        elif table == "account":
            res = self.validate_identity(request)
            if not res[0]:
                return response(ResponseCode.ERROR, res[1], {})

            ip = Internet.get_real_ip(request)
            now_aid = request.user.get("aid", "")
            return self.update_account(id_, now_aid, data, ip)

        return response(ResponseCode.ERROR, "更新失败", {})

    def validate_identity(self, request):
        user_identity = request.user.get("identity", "")
        if user_identity == Identity.SUPER_ADMIN.value:
            return True, ''
        elif user_identity == Identity.ADMIN.value:
            return True, ''
        else:
            return False, '权限不够'

    def update_user(self, uid, data):
        try:
            user_instance = UserInfo.objects.get(id=uid)
        except UserInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "用户不存在", {})

        ser = UserSerializer(user_instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            user_data = ser.save()  # 使用序列化器的save方法更新实例并触发缓存操作
            return response(ResponseCode.SUCCESS, "更新用户成功", user_data)
        except ValidationError as e:
            return validation_exception(e)

    def update_account(self, aid, now_aid, data, ip):
        try:
            account_instance = AccountInfo.objects.get(id=aid)
        except AccountInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "账户不存在", {})

        data['id'] = aid
        ser = AccountSerializer(account_instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            account_data = ser.save()
            if account_data.get("identity", False) and now_aid == aid:
                data = set_jwt_token(data, create_jwt_token(data['id'], TOKEN_TIME))

            email = account_data.get("email", False)
            if email:
                destroy_captcha(email, ip)

            return response(ResponseCode.SUCCESS, "更新账户成功", data)
        except ValidationError as e:
            return validation_exception(e)

