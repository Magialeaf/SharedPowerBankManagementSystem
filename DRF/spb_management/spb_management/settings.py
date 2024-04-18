"""
Django settings for spb_management project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mzlf_w#-&o-i$&optx83sarx@6=(4o6##mnm@c+v+x+xv_fmux'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 增加：server 地址
drf_ip = "127.0.0.1"
drf_port = "8000"
drf_url = f"http://{drf_ip}:{drf_port}"


ALLOWED_HOSTS = [drf_ip]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'areas.apps.AreasConfig',
    'merchants.apps.MerchantsConfig',
    'orders.apps.OrdersConfig',
    'power_bank.apps.PowerBankConfig',
    'system_administration.apps.SystemAdministrationConfig',
    'users.apps.UsersConfig',
    'rest_framework',
    'corsheaders'
]

MIDDLEWARE = [
    'spb_management.utils.my_middleware.CustomExceptionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spb_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spb_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
sql_port = 3306

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spb_management',
        'USER': 'root',
        'PASSWORD': 'nyanyanya',
        'HOST': drf_ip,
        'PORT': sql_port,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


""" 添加代码 """

# 自定义名字
global_studio_name = '共享充电宝管理系统'


# 跨域
vue_url = "http://127.0.0.1:5173"

CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True  # 允许所有host访
# CORS_ALLOW_METHODS = ['GET',]
CORS_ALLOWED_ORIGINS = [vue_url]
CORS_ALLOW_HEADERS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
# 匹配静态文件路径
CORS_URLS_REGEX = r'^/media/.*$'

# CSRF跨域
CSRF_TRUSTED_ORIGINS = [vue_url]


# 缓存是redis
# 添加缓存
redis_port = 6379

CACHES = {
    # 设置数据库名
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 网址，可以是多个
        "LOCATION": f"redis://{drf_ip}:{redis_port}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
    "user_captcha": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 网址，可以是多个
        "LOCATION": f"redis://{drf_ip}:{redis_port}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
    "throttle": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 网址，可以是多个
        "LOCATION": f"redis://{drf_ip}:{redis_port}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
    "area": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 网址，可以是多个
        "LOCATION": f"redis://{drf_ip}:{redis_port}/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
    "merchant": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 网址，可以是多个
        "LOCATION": f"redis://{drf_ip}:{redis_port}/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    }
}

# 邮箱验证
# 发送邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'mugi831@163.com'
# 在邮箱中设置的授权密码
EMAIL_HOST_PASSWORD = 'ENCFWJBUYPOSDMQI'
# 收件人看到的发件人
DEFAULT_FROM_EMAIL = global_studio_name + '<mugi831@163.com>'


# 配置文件存储目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'spb_management/media')
# 配置浏览器访问文件的地址：http://127.0.0.1:8000/media/...
MEDIA_URL = '/media/'
# 以上表示浏览器传来的url以media开头的，django统一到MEDIA_ROOT配置的目录下去找


# 配置版本信息
REST_FRAMEWORK = {
    # 默认可以匿名访问
    "DEFAULT_AUTHENTICATION_CLASSES": ["spb_management.router.authentication.JwtQueryParamsAuthentication", ],
    # 默认匿名的权限
    "DEFAULT_PERMISSION_CLASSES": ["spb_management.router.permission.NotAnonPermission", ],

    # 404异常处理
    'EXCEPTION_HANDLER': 'spb_management.utils.my_exception.common_exception_handler',

    # 请求的参数名
    "VERSION_PARAM": "version",
    # 不传参数时默认的版本值
    "DEFAULT_VERSION": "v1",
    # 合法的版本值
    "ALLOWED_VERSIONS": ["v1", "v2", "v3"],
    # 默认传递方式
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning"
}