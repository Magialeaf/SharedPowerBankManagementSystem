from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError

from power_bank.models import PowerBankInfo, PowerBankMaintenanceInfo
from power_bank.utils.throttle import PowerBankImgThrottle, PowerBankThrottle, PowerBankMaintenanceThrottle
from power_bank.utils.serializer import PowerBankSerializer, PowerBankMaintenanceSerializer
from spb_management.base_class.CRUDInterface import CRUDInterface, UnknownActionError
from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.base_class.UploadImgAPI import UploadImgAPI
from spb_management.router import Internet
from spb_management.router.image_operation import ImgAPI
from spb_management.router.permission import MoreAndMaintainerPermission, MoreAndAdminPermission, NotAnonPermission
from spb_management.router.response_data import response, ResponseCode
from spb_management.utils.my_exception import validation_exception
from spb_management.utils.page_operation import set_extra_page
from users.models import Identity

# Create your views here.
"""
充电宝设备的基础信息管理，包括充电宝ID、型号、状态等。
充电宝的位置管理，关联到区域管理，记录充电宝所在的具体商户和地点。
充电宝使用情况跟踪，如电量变化、故障报告等。

"""


""" —————————————————————————————— """
""" |       PowerBankInfo        | """
""" —————————————————————————————— """


class PowerBankView(CRUDInterface):
    throttle_classes = [PowerBankThrottle, ]

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.permission_classes = [NotAnonPermission, ]
        else:
            self.permission_classes = [MoreAndMaintainerPermission, ]
        return super().dispatch(request, *args, **kwargs)

    def extra_get(self, request, version, kwargs):
        action = request.GET.get("action", None)
        if action == "getNameList":
            return self.get_name_list(request, version, kwargs)

        raise UnknownActionError()

    def get_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        query = PowerBankInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "充电宝不存在", {})
        else:
            data = PowerBankSerializer(query).data
            return response(ResponseCode.SUCCESS, "获取成功", data)

    def get_list(self, request, version, kwargs):
        page = kwargs.get("pk", None)
        if page is None or page < 1:
            page = 1

        conditions, data = Internet.get_internet_data(request)

        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if conditions:
            base_query = Q()
            if keyword := conditions.get("keyword", None):
                match_fields = ['name', 'merchant__shop_name']
                for field in match_fields:
                    base_query |= Q(**{f'{field}__icontains': keyword})
            if keycode := conditions.get("keyAreaId", None):
                base_query &= Q(area=keycode)

            if status := conditions.get("status", None):
                base_query &= Q(status=status)

            if not (order_by := conditions.get("order_by", None)):
                order_by = []

            query = PowerBankInfo.objects.filter(base_query).all().order_by(*order_by)[start_index:start_index + items_per_page]
            total = PowerBankInfo.objects.filter(base_query).count()
        else:
            query = PowerBankInfo.objects.all()[start_index:start_index + items_per_page]
            total = PowerBankInfo.objects.count()

        data = PowerBankSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)

        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def get_name_list(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)

        if merchant := conditions.get("merchant", None):
            query = PowerBankInfo.objects.filter(merchant=merchant).values('id','name')
        else:
            query = PowerBankInfo.objects.values('id','name')
        data = [{'id': item['id'], 'name': item['name']} for item in query]

        return response(ResponseCode.SUCCESS, "获取成功", data)

    def create_info(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)
        serializer = PowerBankSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.to_representation(serializer.instance)
            return response(ResponseCode.SUCCESS, "创建成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def update_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        conditions, data = Internet.get_internet_data(request)
        try:
            instance = PowerBankInfo.objects.filter(id=id_).first()
        except PowerBankInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "充电宝不存在", {})

        ser = PowerBankSerializer(instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "更新充电宝成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        try:
            PowerBankInfo.objects.filter(id=id_).delete()
            return response(ResponseCode.SUCCESS, "删除成功", {})
        except PowerBankInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "充电宝不存在", {})


""" —————————————————————————————— """
""" |       PowerBankImg         | """
""" —————————————————————————————— """


class PowerBankImgView(UploadImgAPI):
    throttle_classes = [PowerBankImgThrottle, ]
    def __init__(self):
        super().__init__(ImgAPI.power_bank_img_path)


""" —————————————————————————————— """
""" |    PowerBankMaintenance    | """
""" —————————————————————————————— """


class PowerBankMaintenanceView(CRUDInterface):
    permission_classes = [MoreAndMaintainerPermission, ]
    throttle_classes = [PowerBankMaintenanceThrottle, ]

    def get_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        query = PowerBankMaintenanceInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "充电宝维护记录不存在", {})
        else:
            data = PowerBankMaintenanceSerializer(query).data
            return response(ResponseCode.SUCCESS, "获取成功", data)

    def get_list(self, request, version, kwargs):
        page = kwargs.get("pk", None)
        if page is None or page < 1:
            page = 1

        conditions, data = Internet.get_internet_data(request)

        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if conditions:
            base_query = Q()
            if power_bank := conditions.get("power_bank", None):
                base_query &= Q(power_bank=power_bank)

            if maintainer_account := conditions.get("maintainer_account", None):
                base_query &= Q(maintainer_account=maintainer_account)

            if status := conditions.get("status", None):
                base_query &= Q(status=status)

            if finished := conditions.get("finished", None):
                base_query &= Q(finished=finished)

            if new_status := conditions.get("new_status", None):
                base_query &= Q(new_status=new_status)

            if not (order_by := conditions.get("order_by", None)):
                order_by = []

            query = PowerBankMaintenanceInfo.objects.filter(base_query).all().order_by(*order_by)[start_index:start_index + items_per_page]
            total = PowerBankMaintenanceInfo.objects.filter(base_query).count()
        else:
            query = PowerBankMaintenanceInfo.objects.all()[start_index:start_index + items_per_page]
            total = PowerBankMaintenanceInfo.objects.count()

        data = PowerBankMaintenanceSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)

        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def create_info(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)
        account = int(data["maintainer_account"])
        identity = request.user.get("identity", -1)
        if identity == Identity.MAINTAINER.value and request.user.get("aid", -2) != account:
            return response(ResponseCode.ERROR, "您不是该维护人员", {})

        serializer = PowerBankMaintenanceSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.to_representation(serializer.instance)
            return response(ResponseCode.SUCCESS, "创建成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def update_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        conditions, data = Internet.get_internet_data(request)
        account = int(data["maintainer_account"])
        identity = request.user.get("identity", -1)
        if identity == Identity.MAINTAINER.value and request.user.get("aid", -2) != account:
            return response(ResponseCode.ERROR, "您不是该维护人员", {})

        try:
            instance = PowerBankMaintenanceInfo.objects.filter(id=id_).first()
        except PowerBankMaintenanceInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "充电宝维护记录不存在", {})

        ser = PowerBankMaintenanceSerializer(instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "更新充电宝维护记录成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        try:
            PowerBankMaintenanceInfo.objects.filter(id=id_).delete()
            return response(ResponseCode.SUCCESS, "删除成功", {})
        except PowerBankMaintenanceInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "充电宝不存在", {})


""" —————————————————————————————— """
""" |      HotPowerBankView      | """
""" —————————————————————————————— """


class HotPowerBankView(GetAndPostAPIView):
    throttle_classes = [PowerBankThrottle, ]
    permission_classes = [NotAnonPermission, ]

    def get(self, request, version, **kwargs):
        action = request.GET.get("action")
        if action == "getList":
             return self.get_hot_power_bank()

        return response(ResponseCode.ERROR, "请求参数错误", {})

    def get_hot_power_bank(self):
        query = PowerBankInfo.objects.all()[:6]
        data = PowerBankSerializer(query, many=True).data
        return response(ResponseCode.SUCCESS, "获取热门商户成功", data)