from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError

from orders.models import PowerBankRentalInfo, PowerBankReturnInfo, PowerBankFeeInfo
from orders.utils.serializer import PowerBankRentalSerializer, PowerBankReturnSerializer, PowerBankFeeSerializer

from orders.utils.throttle import PowerBankRentalThrottle, PowerBankReturnThrottle, PowerBankFeeThrottle
from spb_management.base_class.CRUDInterface import UnknownActionError, CRUDInterface
from spb_management.router import Internet
from spb_management.router.permission import MoreAndMaintainerPermission
from spb_management.router.response_data import response, ResponseCode
from spb_management.utils.my_exception import validation_exception
from spb_management.utils.page_operation import set_extra_page

# Create your views here.
"""
订单的创建、查询、支付、取消、完成等全生命周期管理。
订单费用计算、优惠活动处理、退款退货等操作。
"""


""" —————————————————————————————— """
""" |    PowerBankRentalInfo     | """
""" —————————————————————————————— """


class PowerBankRentalView(CRUDInterface):
    permission_classes = [MoreAndMaintainerPermission, ]
    throttle_classes = [PowerBankRentalThrottle, ]

    def get_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        query = PowerBankRentalInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "租赁信息不存在", {})
        else:
            data = PowerBankRentalSerializer(query).data
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
            power_bank = conditions.get("power_bank", None)
            if power_bank:
                base_query &= Q(power_bank=power_bank)

            user = conditions.get("user", None)
            if user:
                base_query &= Q(user=user)

            query = PowerBankRentalInfo.objects.filter(base_query).all()[
                    start_index:start_index + items_per_page]
            total = PowerBankRentalInfo.objects.filter(base_query).count()
        else:
            query = PowerBankRentalInfo.objects.all()[start_index:start_index + items_per_page]
            total = PowerBankRentalInfo.objects.count()

        data = PowerBankRentalSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)

        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def create_info(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)
        serializer = PowerBankRentalSerializer(data=data)
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
            instance = PowerBankRentalInfo.objects.filter(id=id_).first()
        except PowerBankRentalInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "租赁记录不存在", {})

        ser = PowerBankRentalSerializer(instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "更新租赁记录成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        try:
            PowerBankRentalInfo.objects.filter(id=id_).delete()
            return response(ResponseCode.SUCCESS, "删除成功", {})
        except PowerBankRentalInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "租赁记录不存在", {})


""" —————————————————————————————— """
""" |    PowerBankReturnInfo     | """
""" —————————————————————————————— """


class PowerBankReturnView(CRUDInterface):
    permission_classes = [MoreAndMaintainerPermission, ]
    throttle_classes = [PowerBankReturnThrottle, ]

    def get_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        query = PowerBankReturnInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "租赁信息不存在", {})
        else:
            data = PowerBankReturnSerializer(query).data
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
            power_bank = conditions.get("power_bank", None)
            if power_bank:
                base_query &= Q(power_bank=power_bank)

            user = conditions.get("user", None)
            if user:
                base_query &= Q(user=user)

            query = PowerBankReturnInfo.objects.filter(base_query).all()[
                    start_index:start_index + items_per_page]
            total = PowerBankReturnInfo.objects.filter(base_query).count()
        else:
            query = PowerBankReturnInfo.objects.all()[start_index:start_index + items_per_page]
            total = PowerBankReturnInfo.objects.count()

        data = PowerBankReturnSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)

        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def create_info(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)
        serializer = PowerBankReturnSerializer(data=data)
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
            instance = PowerBankReturnInfo.objects.filter(id=id_).first()
        except PowerBankReturnInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "租赁记录不存在", {})

        ser = PowerBankReturnSerializer(instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "更新租赁记录成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        try:
            PowerBankReturnInfo.objects.filter(id=id_).delete()
            return response(ResponseCode.SUCCESS, "删除成功", {})
        except PowerBankReturnInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "租赁记录不存在", {})


""" —————————————————————————————— """
""" |      PowerBankFeeInfo      | """
""" —————————————————————————————— """


class PowerBankFeeView(CRUDInterface):
    permission_classes = [MoreAndMaintainerPermission, ]
    throttle_classes = [PowerBankFeeThrottle, ]

    def get_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        query = PowerBankFeeInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "租赁信息不存在", {})
        else:
            data = PowerBankFeeSerializer(query).data
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
            power_bank = conditions.get("power_bank", None)
            if power_bank:
                base_query &= Q(power_bank=power_bank)

            user = conditions.get("user", None)
            if user:
                base_query &= Q(user=user)

            query = PowerBankFeeInfo.objects.filter(base_query).all()[
                    start_index:start_index + items_per_page]
            total = PowerBankFeeInfo.objects.filter(base_query).count()
        else:
            query = PowerBankFeeInfo.objects.all()[start_index:start_index + items_per_page]
            total = PowerBankFeeInfo.objects.count()

        data = PowerBankFeeSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)

        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def create_info(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)
        serializer = PowerBankFeeSerializer(data=data)
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
            instance = PowerBankFeeInfo.objects.filter(id=id_).first()
        except PowerBankFeeInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "租赁记录不存在", {})

        ser = PowerBankFeeSerializer(instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "更新租赁记录成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        try:
            PowerBankFeeInfo.objects.filter(id=id_).delete()
            return response(ResponseCode.SUCCESS, "删除成功", {})
        except PowerBankFeeInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "租赁记录不存在", {})



