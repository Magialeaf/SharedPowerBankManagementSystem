from django.core.cache import caches
from django.core.mail import send_mail
from spb_management.settings import global_studio_name
from django.conf import settings
import random


def generate_captcha():
    captcha = random.randrange(100000,1000000)
    return captcha


# 发送验证码的函数
def send_captcha_email(email, captcha):
    subject = global_studio_name + '注册验证码'  # 邮件主题
    # 邮件内容
    message = f"""
    尊敬的用户你好！
    感谢你注册本网站。
    您的验证码是: {captcha}
    请在五分钟内使用
    """

    # 发送邮件
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


def set_captcha(email, ip, captcha_value):
    # 验证码缓存
    caches['user_captcha'].set(f"captcha:{email}", captcha_value, 300)
    # 阻塞邮箱
    caches['user_captcha'].set(f'blocked:{email}', True, 60)
    # 阻塞IP
    caches['user_captcha'].set(f'blocked:{ip}', email, 60)


def destroy_captcha(email, ip):
    # 登录成功后销毁验证码
    caches['user_captcha'].delete(f"captcha:{email}")
    caches['user_captcha'].delete(f'blocked:{ip}')
    caches['user_captcha'].delete(f'blocked:{email}')

