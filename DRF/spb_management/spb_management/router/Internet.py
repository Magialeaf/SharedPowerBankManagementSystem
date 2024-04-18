from django.core.cache import caches
from spb_management.utils.my_crypto import HashFunc
from django.utils import timezone
from users.models import Identity, AccountInfo, UserInfo
import jwt
import datetime
from spb_management import settings


def get_real_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]  # 当有多级代理时，取第一个IP
    else:
        ip = request.META.get('REMOTE_ADDR')

    # 检查IP地址是否为空值，如果为空值则设置为默认值
    if not ip:
        ip = 'Unknown'  # 设置为一个特殊的默认值
    return ip


def create_jwt_token(aid, timeout: int = 1):
    secret_key = settings.SECRET_KEY

    payload = AccountInfo.objects.filter(id=aid).values("id", "identity").first()
    user_query = UserInfo.objects.filter(aid=aid).values("id").first()
    payload['uid'] = user_query['id']
    payload['aid'] = payload.pop('id')
    headers = {
        "typ": "jwt",
        "alg": "HS256"
    }

    payload["exp"] = timezone.now() + datetime.timedelta(minutes=timeout)

    token = "Bearer " + jwt.encode(payload=payload, key=secret_key, algorithm="HS256", headers=headers)

    return token


def set_jwt_token(data, token):
    data["jwt_token"] = token
    return data


def get_internet_data(request):
    conditions = {}
    data = {}

    if request.method == 'GET':
        data = request.GET.getlist('data[]', ' ')
        for key, value in request.GET.items():
            if key.startswith('conditions[') and key.endswith(']'):
                clean_key = key[11:-1]
                conditions[clean_key] = value

    elif request.method == 'POST':
        for key, value in request.data.items():
            if key.startswith('data[') and key.endswith(']'):
                clean_key = key[5:-1]
                data[clean_key] = value
            elif key.startswith('conditions[') and key.endswith(']'):
                clean_key = key[11:-1]
                conditions[clean_key] = value

    return conditions, data
