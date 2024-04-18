import datetime
from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from areas.models import AreaInfo
from spb_management.router.image_operation import ImgAPI


class Identity(Enum):
    SUPER_ADMIN = 0, _("超级管理员")
    ADMIN = 1, _("管理员")
    MAINTAINER = 10, _("运维人员")
    USER = 11, _("普通用户")
    ANON = 100, _("匿名用户")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj

    @classmethod
    def get_display_name(cls, identity):
        return cls(identity).display_name

    @classmethod
    def is_valid_identity_code(cls, code):
        return code in cls._value2member_map_



class AccountInfo(models.Model):
    """ 用户表 """
    IDENTITY_CHOICES = tuple((identity.value, identity.display_name) for identity in Identity)

    id = models.AutoField(verbose_name="aid", primary_key=True)
    account = models.CharField(verbose_name="账号", max_length=15, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    email = models.EmailField(verbose_name="邮箱", unique=True)
    identity = models.SmallIntegerField(verbose_name="身份", choices=IDENTITY_CHOICES, default=Identity.USER.value)
    last_login_time = models.DateTimeField(verbose_name="上次登录时间", null=True, blank=True, auto_now_add=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def get_identity_display(self):
        return Identity.get_display_name(int(self.identity))

    @staticmethod
    def get_field_name(field_name):
        return AccountInfo._meta.get_field(field_name).verbose_name


class UserInfo(models.Model):
    """ 用户详细信息表 """
    GENDER_CHOICES = (
        (0, "男"),
        (1, "女"),
        (2, "保密"),
    )
    id = models.AutoField(verbose_name="uid", primary_key=True)
    aid = models.OneToOneField(AccountInfo, verbose_name='aid', on_delete=models.CASCADE,
                               related_name='user_info', unique=True)
    username = models.CharField(verbose_name="用户名", max_length=20, default="新用户")
    profile = models.CharField(verbose_name="个人简介", max_length=100, default="这个用户很懒，什么也没有写")
    avatar = models.ImageField(verbose_name="头像", upload_to=ImgAPI.user_avatar_path, default="default.png")
    sex = models.SmallIntegerField(verbose_name="性别", choices=GENDER_CHOICES, default=2)
    birthday = models.DateField(verbose_name="生日", blank=False, null=False, default=datetime.datetime(2001, 1, 1))
    # phone = models.CharField(verbose_name="电话号码", max_length=15, blank=False, null=False, default='0')

    def get_sex_display(self):
        return dict(self.GENDER_CHOICES)[self.sex]

    @property
    def age(self):
        if self.birthday:
            today = datetime.datetime.now(datetime.timezone.utc).date()
            try:
                age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
                return age
            except ValueError:
                pass  # 处理日期格式错误的情况
        return None

    @staticmethod
    def get_field_name(field_name):
        return UserInfo._meta.get_field(field_name).verbose_name


class MaintainInfo(UserInfo):
    maintain_areas = models.ManyToManyField(AreaInfo, verbose_name="维护区域", related_name="maintain_info")
