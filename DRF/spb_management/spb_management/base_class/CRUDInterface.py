from abc import abstractmethod

from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.router.response_data import ResponseCode, response


class UnknownActionError(Exception):
    def __init__(self, message="请求参数错误"):
        self.message = message
        super().__init__(self.message)


class CRUDInterface(GetAndPostAPIView):
    def get(self, request, version, **kwargs):
        try:
            action = request.GET.get("action", "")
            if action == "get":
                return self.get_info(request, version, kwargs)
            elif action == "getList":
                return self.get_list(request, version, kwargs)
            else:
                return self.extra_get(request, version, kwargs)
        except UnknownActionError as e:
            return response(ResponseCode.ERROR, e.message, {})

    def post(self, request, version, **kwargs):
        try:
            action = request.POST.get("action", "")
            if action == "create":
                return self.create_info(request, version, kwargs)
            elif action == "update":
                return self.update_info(request, version, kwargs)
            elif action == "delete":
                return self.delete_info(request, version, kwargs)
            else:
                return self.extra_post(request, version, kwargs)
        except UnknownActionError as e:
            return response(ResponseCode.ERROR, e.message, {})

    def extra_get(self, request, version, kwargs):
        raise UnknownActionError()

    def extra_post(self, request, version, kwargs):
        raise UnknownActionError()

    @abstractmethod
    def get_info(self, request, version, kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_list(self, request, version, kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_info(self, request, version, kwargs):
        raise NotImplementedError
    @abstractmethod
    def update_info(self, request, version, kwargs):
        raise NotImplementedError
    @abstractmethod
    def delete_info(self, request, version, kwargs):
        raise NotImplementedError




