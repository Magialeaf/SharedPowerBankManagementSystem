import datetime
import re
from django.core.cache import caches
from django.db import transaction
from django.db.models import Q, QuerySet
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.router.Internet import create_jwt_token, set_jwt_token
from spb_management.router.image_operation import UploadImage, ImgAPI
from spb_management.router.permission import MoreAndAdminPermission, NotAnonPermission, MoreAndMaintainerPermission
from spb_management.router.response_data import ResponseCode, response, response_data
from spb_management.router import Internet
from users.utils.throttle import EnterThrottle, UserThrottle, AccountThrottle, UserAvatarThrottle, MaintainThrottle
from spb_management.utils.captcha import destroy_captcha, set_captcha, generate_captcha, send_captcha_email
from spb_management.utils.my_exception import validation_exception
from users.models import UserInfo, AccountInfo, Identity, MaintainInfo
from users.utils.serializer import LoginByAccountSerializer, RegisterSerializer, UserSerializer, AccountSerializer, \
    MaintainSerializer
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
    throttle_classes = [UserThrottle, ]

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.permission_classes = [MoreAndMaintainerPermission, ]
        else:
            self.permission_classes = [MoreAndAdminPermission, ]
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, version, **kwargs):
        action = request.GET.get("action", " ")
        if action == "getList":
            page = kwargs.get('pk', 1)
            return self.get_user_list(page, request)
        elif action == "getNameList":
            return self.get_name_list()
        elif action == "getMaintainNameList":
            return self.get_maintain_name_list()

        return response(ResponseCode.ERROR, "请求参数错误", {})

    def post(self, request, version, **kwargs):
        return super().post(request, version, **kwargs)

    def get_user_list(self, page, request):
        conditions, data = Internet.get_internet_data(request)
        page = page if page > 0 else 1
        identity = int(conditions.get('identity', Identity.ANON.value))
        items_per_page = 10
        start_index = (page - 1) * items_per_page

        aid_values = set(AccountInfo.objects.filter(identity=identity).values_list('id', flat=True))
        user_query = QuerySet()
        if identity == Identity.USER.value:
            base_query = Q()
            if keyword := conditions.get('keyword', None):
                match_fields = ['username', 'profile']

                for field in match_fields:
                    base_query |= Q(**{f'{field}__icontains': keyword})
            if sex := conditions.get('sex', None):
                base_query &= Q(sex=sex)

            base_query &= Q(aid__in=aid_values)
            user_query = UserInfo.objects.filter(base_query)[start_index:start_index + items_per_page]
            total = UserInfo.objects.filter(base_query).count()

        if identity == Identity.MAINTAINER.value:
            base_query = Q()

            if keyword := conditions.get('keyword', None):
                match_fields = ['username', 'profile']
                for field in match_fields:
                    base_query |= Q(**{f'{field}__icontains': keyword})

            if area_id := conditions.get('areaId', None):
                maintainers_in_area = set(MaintainInfo.objects.filter(area_id_id=area_id,aid_id__identity=identity).values_list('aid', flat=True))
                base_query &= Q(aid__in=maintainers_in_area)
            else:
                base_query &= Q(aid__in=aid_values)

            if sex := conditions.get('sex', None):
                base_query &= Q(sex=sex)
            user_query = UserInfo.objects.filter(base_query)[start_index:start_index + items_per_page]
            total = UserInfo.objects.filter(base_query).count()

        serializer = UserSerializer(user_query, many=True)
        structured_data = serializer.to_representation(user_query)
        extra = {
            "total": total,
            "pageSize": items_per_page,
        }

        def set_default_areas(item):
            item['areas'] = ["000000|", "000000|", "000000|"]

        if identity == Identity.MAINTAINER.value:
            for item in structured_data:
                aid_id = item.get('aid_id', None)
                if aid_id:
                    areas = MaintainInfo.objects.filter(aid_id=aid_id).values_list('area_id__code', 'area_id__name')
                    if areas:
                        item['areas'] = [f"{area[0] or '000000'}|{area[1] or ''}" for area in areas]
                    else:
                        set_default_areas(item)
                else:
                    set_default_areas(item)
        return response(ResponseCode.SUCCESS, "获取成功", structured_data, extra=extra)

    def get_name_list(self):
        query = UserInfo.objects.filter().values("id", "username")
        data = [{"id": item["id"], "name": item["username"]} for item in query]
        return response(ResponseCode.SUCCESS, "获取成功", data)

    def get_maintain_name_list(self):
        query = UserInfo.objects.filter(aid__identity=Identity.MAINTAINER.value).values("id", "username")
        data = [{"id": item["id"], "name": item["username"]} for item in query]

        return response(ResponseCode.SUCCESS, "获取成功", data)


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
        elif action == "delete":
            id_ = request.user.get("uid", "")
            return self.delete(id_)
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
        if action == "create":
            return self.create(request)
        elif action == "update":
            id_ = kwargs.get('pk', '')
            return self.update(id_, request)
        elif action == "delete":
            id_ = kwargs.get('pk', '')
            return self.delete(id_)
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


""" —————————————————————————————— """
""" |        MaintainInfo        | """
""" —————————————————————————————— """


class MaintainView(GetAndPostAPIView):
    permission_classes = [MoreAndMaintainerPermission, ]
    throttle_classes = [MaintainThrottle, ]

    def get(self, request, version, **kwargs):
        action = request.GET.get("action", " ")
        if action == "get":
            id_ = kwargs.get('pk', '')
            return self.get_maintain_info(id_)
        return response(ResponseCode.ERROR, "请求参数错误", {})

    def post(self, request, version, **kwargs):
        action = request.POST.get("action", " ")
        if action == "update":
            id_ = kwargs.get('pk', '')
            return self.update_maintain_info(id_, request)
        return response(ResponseCode.ERROR, "请求参数错误", {})

    def get_maintain_info(self, aid):
        maintain_query = MaintainInfo.objects.filter(aid=aid).order_by("id")
        if maintain_query:
            serializer = MaintainSerializer(maintain_query, many=True)
            structured_data = serializer.to_representation(maintain_query)
            return response(ResponseCode.SUCCESS, "获取成功", structured_data)
        else:
            res = [
                {'id': 0, 'aid_id': aid, 'area_id': None, 'code': '000000'},
                {'id': 0, 'aid_id': aid, 'area_id': None, 'code': '000000'},
                {'id': 0, 'aid_id': aid, 'area_id': None, 'code': '000000'}
            ]
            return response(ResponseCode.SUCCESS, "获取成功", res)

    def update_maintain_info(self, aid, request):
        conditions, data = Internet.get_internet_data(request)
        maintain_query = MaintainInfo.objects.filter(aid=aid).order_by("id")

        with transaction.atomic():
            if maintain_query:
                res = []
                try:
                    idx = '0'
                    for query in maintain_query:
                        value = None if int(data[idx]) == 0 else int(data[idx])
                        area_data = {"aid": aid, "area_id": value}
                        serializer = MaintainSerializer(query, data=area_data)

                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        res.append(serializer.data)
                        idx = str(int(idx) + 1)
                    return response(ResponseCode.SUCCESS, "更新成功", res)
                except ValidationError as e:
                    return validation_exception(e)
            else:
                try:
                    for key, value in data.items():
                        value = int(value)
                        value = None if value == 0 else value
                        area_data = {"aid": aid, "area_id": value}
                        serializer = MaintainSerializer(data=area_data)

                        serializer.is_valid(raise_exception=True)
                        new_maintain_info = serializer.save()

                        query = MaintainInfo.objects.filter(aid=aid).order_by("id")
                        serializer = MaintainSerializer(data=query, many=True)
                        data = serializer.to_representation(query)

                        return response(ResponseCode.SUCCESS, "创建成功", data)
                except ValidationError as e:
                    return validation_exception(e)



