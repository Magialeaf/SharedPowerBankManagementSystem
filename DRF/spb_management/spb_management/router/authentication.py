import jwt
from spb_management import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from spb_management.router.response_data import ResponseCode, response_data


""" —————————————————————————————— """
""" |          具体类              | """
""" —————————————————————————————— """


class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization", "")
        token = token.replace("Bearer ", "")

        secret_key = settings.SECRET_KEY

        try:
            # 使用 secret_key 替换原本的 SALT 变量
            payload = jwt.decode(token, secret_key, algorithms=["HS256"], options={"verify_exp": True})

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(detail=response_data(ResponseCode.NOT_AUTH, "token已失效", {}))

        except jwt.DecodeError:
            raise AuthenticationFailed(detail=response_data(ResponseCode.NOT_AUTH, "token认证失败", {}))

        except jwt.InvalidTokenError:
            raise AuthenticationFailed(detail=response_data(ResponseCode.NOT_AUTH, "非法的toekn", {}))

        return payload, token