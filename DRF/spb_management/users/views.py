import datetime
import re
from django.core.cache import caches
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.router.Internet import create_jwt_token, set_jwt_token
from spb_management.router.image_operation import UploadImage, ImgAPI
from spb_management.router.permission import MoreAndAdminPermission, NotAnonPermission
from spb_management.router.response_data import ResponseCode, response, response_data
from spb_management.router import Internet
from users.utils.throttle import EnterThrottle, UserThrottle, AccountThrottle, UserAvatarThrottle
from spb_management.utils.captcha import destroy_captcha, set_captcha, generate_captcha, send_captcha_email
from spb_management.utils.my_exception import validation_exception
from users.models import UserInfo, AccountInfo, Identity
from users.utils.serializer import LoginByAccountSerializer, RegisterSerializer, UserSerializer, AccountSerializer
from users.utils.base_views import OneUserBase, TOKEN_TIME


"""
负责用户账号的注册、登录、密码重置、个人信息修改等功能。
用户角色权限管理，如普通用户、商户用户、管理员角色等。
"""

""" —————————————————————————————— """
""" |        用户登录注册           | """
""" —————————————————————————————— """


class EnterView(GetAndPostAPIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [EnterThrottle]

    def post(self, request, version, **kwargs):
        action = request.POST.get("action", "")
        if action == "login":
            return self.login(request)
        elif action == "register":
            return self.register(request)

        return response(ResponseCode.ERROR, "请求参数错误", {})

    def login(self, request):
        conditions, data = Internet.get_internet_data(request)
        ip = Internet.get_real_ip(request)
        if "login" in conditions and conditions["login"] == 'account':
            serializer = LoginByAccountSerializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    res_tuple = self.authenticate_user(serializer.validated_data)
                    if res_tuple[0]:
                        data = set_jwt_token({}, create_jwt_token(res_tuple[2], TOKEN_TIME))
                        return response(ResponseCode.SUCCESS, res_tuple[1], data)
                    else:
                        return response(ResponseCode.ERROR, res_tuple[1], {})
            except ValidationError as e:
                return validation_exception(e)
        elif "login" in conditions and conditions["login"] == 'email':
            res_tuple = self.authenticate_user(data)
            if res_tuple[0]:
                data = set_jwt_token({}, create_jwt_token(res_tuple[2], TOKEN_TIME))
                return response(ResponseCode.SUCCESS, res_tuple[1], data)
            else:
                return response(ResponseCode.ERROR, res_tuple[1], {})

        return response(ResponseCode.ERROR, "登录失败", {})

    def register(self, request):
        conditions, data = Internet.get_internet_data(request)
        ip = Internet.get_real_ip(request)

        serializer = RegisterSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                new_data = serializer.validated_data
                post_captcha = int(data['captcha'])

                # 检查验证码有效期
                captcha_key = f"captcha:{new_data['email']}"
                captcha_value = caches['user_captcha'].get(captcha_key)

                if not captcha_value:
                    return response(ResponseCode.ERROR, "验证码已获取，请在5分钟内使用", {})

                if captcha_value != post_captcha:
                    return response(ResponseCode.ERROR, "验证码已过期，请重新获取", {})

                # 注册并保存用户信息
                aid = serializer.save()

                destroy_captcha(new_data["email"], ip)

                # 处理注册逻辑
                data = set_jwt_token({}, create_jwt_token(aid, TOKEN_TIME))
                return response(ResponseCode.SUCCESS, "注册成功", data)

        except ValidationError as e:
            return validation_exception(e)

        return response(ResponseCode.ERROR, "注册", {})


    def authenticate_user(self, data):
        if "account" in data:
            query = AccountInfo.objects.filter(account=data["account"], password=data["password"]).values('id').first()
            if query:
                AccountInfo.objects.filter(id=query['id']).update(last_login_time=timezone.now())
                return True, "登录成功", query['id']
            else:
                return False, "账号或密码错误", None
        elif "email" in data:
            captcha_key = f"captcha:{data['email']}"
            captcha_value = str(caches['user_captcha'].get(captcha_key))
            if captcha_value == data['captcha']:
                query = AccountInfo.objects.filter(email=data["email"]).values('id').first()
                if query:
                    return True, "登录成功", query['id']
                else:
                    return False, "验证码错误", None
            else:
                return False, "验证码错误", None

        return False, "登录失败", None


""" —————————————————————————————— """
""" |         验证码管理            | """
""" —————————————————————————————— """


class CaptchaView(GetAndPostAPIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, version, **kwargs):
        action = request.GET.get("action", " ")
        email = kwargs.get('pk', '')
        if action == "getCaptcha":
            return self.get_captcha(request, email)
        elif action == "getCaptchaCache":
            return self.get_captcha_cache(request)

        return response(ResponseCode.ERROR, "请求参数错误", {})

    def get_captcha(self, request, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return response(ResponseCode.ERROR, '邮箱格式错误', {})

        # 检验验证码是否阻塞
        blocked_key = f'blocked:{email}'
        if caches['user_captcha'].get(blocked_key):
            return response(ResponseCode.ERROR, '请求过于频繁，请稍后再试', {})

        # # 检查验证码有效期
        # captcha_key = f'captcha:{email}'
        # captcha_value = caches['user_captcha'].get(captcha_key)
        # if captcha_value:
        #     return response(ResponseCode.ERROR, '验证码已获取，请在5分钟内使用', {})

        # 生成验证码并存储
        captcha_value = generate_captcha()
        # 发送验证码到用户邮箱
        send_captcha_email(email, captcha_value)

        # 发送成功后设置阻塞时间和有效时间
        ip = Internet.get_real_ip(request)

        set_captcha(email, ip, captcha_value)

        return response(ResponseCode.SUCCESS, "发送成功，请在5分钟内使用", {"cooling_time": 60})

    def get_captcha_cache(self, request):
        ip = Internet.get_real_ip(request)
        blocked_ip = f'blocked:{ip}'
        cooling_time = caches['user_captcha'].ttl(blocked_ip)
        if cooling_time:
            return response(ResponseCode.SUCCESS, "",{"cooling_time": cooling_time})
        return response(ResponseCode.SUCCESS, "获取验证码", {})


""" —————————————————————————————— """
""" |        UserInfo            | """
""" —————————————————————————————— """


class UserView(GetAndPostAPIView):
    permission_classes = [MoreAndAdminPermission, ]
    throttle_classes = [UserThrottle, ]

    def get(self, request, version, **kwargs):
        action = request.GET.get("action", " ")
        if action == "getList":
            conditions, data = Internet.get_internet_data(request)
            page = kwargs.get('pk', 1)
            conditions['page'] = page
            print(conditions)
            return self.get_user_info(conditions, "all")
        # todo：暂时没用
        if action == "getOne":
            id = kwargs.get('pk', '')
            return self.get_user_info(id,"one")
        return response(ResponseCode.ERROR, "请求参数错误", {})

    def post (self, request, version, **kwargs):
        return super().post(request, version, **kwargs)

    def get_user_info(self, param:dict | int = None, type="all"):
        if type == "all":
            page = int(param['page']) if param.get("page", 0) > 0 else 1
            identity = param.get("identity", Identity.ANON.value)
            items_per_page = 10
            start_index = (page - 1) * items_per_page

            aid_values = list(AccountInfo.objects.filter(identity=identity).values_list('id', flat=True)[start_index:start_index + items_per_page])
            user_query = UserInfo.objects.filter(aid__in=aid_values)
            res = []
            for user in user_query:
                serializer = UserSerializer(user)
                structured_data = serializer.to_representation(user)
                res.append(structured_data)
            return response(ResponseCode.SUCCESS, "获取成功", res)
        elif type == "one":
            user_query = UserInfo.objects.filter(aid=param).first()
            if user_query:
                serializer = UserSerializer(user_query)
                structured_data = serializer.to_representation(user_query)
                return response(ResponseCode.SUCCESS, "获取成功", structured_data)
        return response(ResponseCode.ERROR, "获取失败", {})


""" —————————————————————————————— """
""" |       AccountInfo          | """
""" —————————————————————————————— """


class AccountView(GetAndPostAPIView):
    permission_classes = [MoreAndAdminPermission, ]
    throttle_classes = [AccountThrottle, ]

    def get(self, request, version, **kwargs):
        action = request.GET.get("action", " ")
        # todo：暂时没用
        if action == "getByJwt":
            aid = request.user.get('aid', '')
            return self.get_account_info(aid)
        # todo：暂时没用
        elif action == "getOne":
            aid = kwargs.get('pk', '')
            return self.get_account_info(aid)

    def post(self, request, version, **kwargs):
        return super().post(request, version, **kwargs)

    def get_account_info(self, id):
        account_query = AccountInfo.objects.filter(aid=id).first()
        if account_query:
            serializer = AccountSerializer(account_query)
            structured_data = serializer.to_representation(account_query)
            return response(ResponseCode.SUCCESS, "获取成功", structured_data)
        return response(ResponseCode.ERROR, "获取失败", {})


""" —————————————————————————————— """
""" |         MyInfo             | """
""" —————————————————————————————— """


class MyInfoView(OneUserBase):
    def get(self, request, version, **kwargs):
        aid = request.user.get("aid", "")
        return self.get_user_and_account(aid)

    def post(self, request, version, **kwargs):
        action = request.POST.get("action", " ")
        if action == "update":
            conditions, data = Internet.get_internet_data(request)
            table = conditions.get("table", "")
            if table == "user":
                id_ = request.user.get("uid", "")
                return self.update(id_, request)
            elif table == "account":
                id_ = request.user.get("aid", "")
                return self.update(id_, request)
            return response(ResponseCode.ERROR, "请求参数错误", {})
        return response(ResponseCode.ERROR, "请求参数错误", {})


""" —————————————————————————————— """
""" |         OneInfo            | """
""" —————————————————————————————— """


class OneInfoView(OneUserBase):
    permission_classes = [MoreAndAdminPermission, ]

    def get(self, request, version, **kwargs):
        uid = kwargs.get('pk', '')
        aid = UserInfo.objects.filter(id=uid).values("aid").first().get("aid", "")
        return self.get_user_and_account(aid)

    def post(self, request, version, **kwargs):
        action = request.POST.get("action", " ")
        if action == "update":
            id_ = kwargs.get('pk', '')
            return self.update(id_, request)
        return response(ResponseCode.ERROR, "请求参数错误", {})


""" —————————————————————————————— """
""" |         UserAvatar         | """
""" —————————————————————————————— """


class UserAvatarView(GetAndPostAPIView):
    permission_classes = [NotAnonPermission,]
    throttle_classes = [UserAvatarThrottle, ]

    def post(self, request, version, **kwargs):
        res = UploadImage.upload_image(request, ImgAPI.user_avatar_path)
        if res[0] == UploadImage.IMG_ERROR:
            return response(ResponseCode.ERROR, res[1], {})
        elif res[0] == UploadImage.IMG_NEW:
            return response(ResponseCode.SUCCESS, "上传成功", {"avatar": res[1]})
        elif res[0] == UploadImage.IMG_EXIST:
            return response(ResponseCode.SUCCESS, "头像已存在", {"avatar": res[1]})





