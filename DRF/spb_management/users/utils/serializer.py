import os

from django.core.cache import caches
from django.utils import timezone
import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from spb_management.router.image_operation import ImgAPI
from spb_management.utils.my_crypto import HashFunc, RSAFunc
from spb_management.utils.my_exception import validation_exception
from users.models import AccountInfo, UserInfo, Identity


class RegisterSerializer(serializers.ModelSerializer):
    account = serializers.CharField(error_messages={'required': "缺少账号"})

    password = serializers.CharField(max_length=350, error_messages={'required': "缺少密码",
                                                                     'max_length': '密码长度不能超过 350 个字符。'})
    email = serializers.EmailField(error_messages={'required': "缺少邮箱"})
    class Meta:
        model = AccountInfo
        fields = ['account', 'password', 'email']

    def validate_account(self, value):
        if not re.match('^[a-zA-Z]\w{2,14}$', value):
            raise serializers.ValidationError('账号必须以字母开头且是3-15位')

        if AccountInfo.objects.filter(account=value).exists():
            raise serializers.ValidationError('账号已被注册')

        return value

    def validate_password(self, value):
        rsa = RSAFunc()
        value = rsa.decode(value)

        if not re.match('^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{6,18}$', value):
            raise serializers.ValidationError('密码必须是6-18位且包含字母和数字')

        value = HashFunc.hash256(value)
        return value

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', value):
            raise serializers.ValidationError('邮箱格式不正确')

        if AccountInfo.objects.filter(email=value).exists():
            raise serializers.ValidationError('邮箱已被注册.')

        return value

    def create(self, validated_data):
        # 在创建时设置默认值或自定义值
        validated_data['identity'] = Identity.USER.value  # 根据实际情况设置
        validated_data['last_login_time'] = timezone.now()
        validated_data['create_time'] = timezone.now()

        instance = super().create(validated_data)

        # 执行额外操作（如：UserInfoOpera.register_database）
        UserInfo.objects.create(aid=instance)

        return instance.id


class LoginByAccountSerializer(serializers.ModelSerializer):
    account = serializers.CharField(max_length=15, error_messages={'required': "缺少账号", 'max_length': '账号长度不能超过 15 个字符。'})
    password = serializers.CharField(max_length=350, error_messages={'required': "缺少密码", 'max_length': '密码长度不能超过 350 个字符。'})
    class Meta:
        model = AccountInfo
        fields = ['account', 'password']

    def validate(self, attrs):
        rsa_func = RSAFunc()
        attrs['password'] = HashFunc.hash256(rsa_func.decode(attrs['password']))
        return attrs


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(allow_blank=True)

    class Meta:
        model = UserInfo
        fields = ('id', 'username', 'sex', 'profile', 'avatar', 'birthday')

    def validate_avatar(self, value):
        url = ImgAPI.get_avatar(value)
        name = os.path.basename(url)

        try:
            ImgAPI.check_img(ImgAPI.user_avatar_path, name)
            return value
        except ValueError as e:
            raise validation_exception(e)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.profile = validated_data.get('profile', instance.profile)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.save()
        res = {
            'id': instance.id,
            'sex': instance.get_sex_display(),
            'username': instance.username,
            'profile': instance.profile,
            'avatar': instance.avatar.name,
            'birthday': instance.birthday
        }
        res["avatar"] = ImgAPI.get_avatar(res["avatar"])
        return res


    def to_representation(self, instance):
        avatar = instance.avatar
        structured_data = super().to_representation(instance)
        structured_data['sex'] = instance.get_sex_display()
        structured_data['avatar'] = ImgAPI.get_avatar(avatar)

        return structured_data


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=350, error_messages={'max_length': '密码长度不能超过 350 个字符。'})
    identity = serializers.CharField(error_messages={'required': "缺少身份"})
    captcha = serializers.CharField(write_only=True)  # 添加captcha字段，仅用于写入（更新）

    class Meta:
        model = AccountInfo
        fields = ('id', 'account', 'password', 'email', 'identity', 'last_login_time', 'create_time', 'captcha')  # 添加captcha到fields列表

    def validate_account(self, value):
        if not re.match('^[a-zA-Z]\w{2,14}$', value):
            raise serializers.ValidationError('账号必须以字母开头且是3-15位')

        current_account = self.instance.account if self.instance else None  # 获取当前用户（正在更新的用户）的账户名

        if current_account and current_account == value:  # 如果当前用户账户名与提交的新账户名相同
            raise serializers.ValidationError('新账户名和老账户名一致')

        # 检查是否有其他用户使用了相同的账户名
        if AccountInfo.objects.exclude(id=self.instance.id).filter(account=value).exists():  # 排除当前用户（如果存在）
            raise serializers.ValidationError('账户名已存在')

        return value

    def validate_password(self, value):
        rsa = RSAFunc()
        value = rsa.decode(value)

        if not re.match('^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{6,18}$', value):
            raise serializers.ValidationError('密码必须是6-18位且包含字母和数字')

        value = HashFunc.hash256(value)

        # 检查密码是否和原来的一样
        query = AccountInfo.objects.filter(id=self.instance.id).values('password').first()
        if query and query['password'] == value:
            raise serializers.ValidationError('新密码和原密码一致')

        return value

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', value):
            raise serializers.ValidationError('邮箱格式不正确')

        if AccountInfo.objects.filter(email=value).exists():
            raise serializers.ValidationError('邮箱已被注册.')

        return value

    def validate_identity(self, value):
        if not Identity.is_valid_identity_code(value):
            serializers.ValidationError(f'{value}是无效的身份')
        return value

    def validate(self, attrs):
        email = attrs.get("email", None)
        if email:
            captcha_key = f"captcha:{email}"
            captcha_value = caches['user_captcha'].get(captcha_key)
            captcha = int(attrs.get("captcha", None))
            if not (captcha_value and captcha_value == captcha):
                raise serializers.ValidationError({"captcha": "验证码错误"})

        return attrs

    def update(self, instance, validated_data):
        res = {'id': instance.id}
        updated_fields = []

        # 检查并更新用户名（如果存在）
        if 'account' in validated_data:
            instance.account = validated_data['account']
            updated_fields.append('account')
            res['account'] = instance.account

        # 检查并更新密码（如果存在且处理密码加密等逻辑）
        if 'password' in validated_data:
            instance.password = validated_data['password']
            updated_fields.append('password')

        # 检查并更新邮箱（如果存在）
        if 'email' in validated_data:
            instance.email = validated_data['email']
            updated_fields.append('email')
            res['email'] = instance.email

        # 检查并更新身份（如果存在，假设身份字段为 `identity`）
        if 'identity' in validated_data:
            instance.identity = validated_data['identity']
            updated_fields.append('identity')
            res['identity'] = instance.get_identity_display()

        # 如果有字段被更新，则保存实例
        if updated_fields:
            instance.save(update_fields=updated_fields)

        return res

    def to_representation(self, instance):
        structured_data = super().to_representation(instance)
        structured_data['identity'] = Identity.get_display_name(instance.identity)

        return structured_data
