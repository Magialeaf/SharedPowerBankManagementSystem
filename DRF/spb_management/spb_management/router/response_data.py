from enum import Enum
from django.http import JsonResponse


class ResponseCode(Enum):
    SUCCESS = 20000
    ERROR = 40000
    NOT_AUTH = 40001
    REDIRECT = 40003
    NOT_FOUND = 40004

    @classmethod
    def get_description(cls, code: 'ResponseCode') -> str:
        return code.name.title().replace('_', ' ')


def response(code: 'ResponseCode', message: str, data: dict | list, **kwargs) -> JsonResponse:
    return JsonResponse({
        'code': code.value,
        'message': message,
        'data': data,
        **kwargs
    })

def response_data(code: 'ResponseCode', message: str, data: dict | list, **kwargs) -> dict:
    return {
        'code': code.value,
        'message': message,
        'data': data,
        **kwargs
    }