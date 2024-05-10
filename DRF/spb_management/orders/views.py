from django.db.models import Q, Subquery, OuterRef
from django.shortcuts import render
from rest_framework.exceptions import ValidationError

from orders.models import PowerBankRentalInfo, PowerBankReturnInfo, PowerBankFeeInfo
from orders.utils.serializer import PowerBankRentalSerializer, PowerBankReturnSerializer, PowerBankFeeSerializer, \
    OrderUserSerializer

from orders.utils.throttle import PowerBankRentalThrottle, PowerBankReturnThrottle, PowerBankFeeThrottle, \
    UserOrderOperationThrottle
from spb_management.base_class.CRUDInterface import UnknownActionError, CRUDInterface
from spb_management.router import Internet
from spb_management.router.permission import MoreAndMaintainerPermission, NotAnonPermission, MoreAndAdminPermission
from spb_management.router.response_data import response, ResponseCode
from spb_management.utils.my_exception import validation_exception
from spb_management.utils.page_operation import set_extra_page
from users.models import Identity
from my_celery.orders.tasks import check_charging_status

# Create your views here.
"""
订单的创建、查询、支付、取消、完成等全生命周期管理。
订单费用计算、优惠活动处理、退款退货等操作。
"""


""" —————————————————————————————— """
""" |    PowerBankRentalInfo     | """
""" —————————————————————————————— """


class PowerBankRentalView(CRUDInterface):
    throttle_classes = [PowerBankRentalThrottle, ]

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.permission_classes = [NotAnonPermission, ]
        else:
            self.permission_classes = [MoreAndAdminPermission, ]
        return super().dispatch(request, *args, **kwargs)

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
        identity = request.user.get("identity", None)

        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if identity == Identity.SUPER_ADMIN.value or identity == Identity.ADMIN.value:
            if conditions:
                base_query = Q()
                if power_bank := conditions.get("power_bank", None):
                    base_query &= Q(power_bank=power_bank)

                if user := conditions.get("user", None):
                    base_query &= Q(user=user)

                if returned := conditions.get("returned", None):
                    if returned == "true":
                        base_query &= Q(returned=True)
                    else:
                        base_query &= Q(returned=False)

                if not (order_by := conditions.get("order_by", None)):
                    order_by = []

                query = PowerBankRentalInfo.objects.filter(base_query).all().order_by(*order_by)[
                        start_index:start_index + items_per_page]
                total = PowerBankRentalInfo.objects.filter(base_query).count()
            else:
                query = PowerBankRentalInfo.objects.all()[start_index:start_index + items_per_page]
                total = PowerBankRentalInfo.objects.count()
        else:
            base_query = Q()
            user = request.user.get("uid", None)
            base_query &= Q(user=user)
            if conditions:
                if returned := conditions.get("returned", None):
                    if returned == "True":
                        base_query &= Q(returned=True)
                    else:
                        base_query &= Q(returned=False)

            if not (order_by := conditions.get("order_by", None)):
                order_by = []

            query = PowerBankRentalInfo.objects.filter(base_query).all().order_by(*order_by)[start_index:start_index + items_per_page]
            total = PowerBankRentalInfo.objects.filter(base_query).count()

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
            check_charging_status.delay([data["power_bank"]])
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
    throttle_classes = [PowerBankReturnThrottle, ]

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.permission_classes = [NotAnonPermission, ]
        else:
            self.permission_classes = [MoreAndAdminPermission, ]
        return super().dispatch(request, *args, **kwargs)

    def get_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        query = PowerBankReturnInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "归还信息不存在", {})
        else:
            data = PowerBankReturnSerializer(query).data
            return response(ResponseCode.SUCCESS, "获取成功", data)

    def get_list(self, request, version, kwargs):
        page = kwargs.get("pk", None)
        if page is None or page < 1:
            page = 1

        conditions, data = Internet.get_internet_data(request)
        identity = request.user.get("identity", None)

        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if identity == Identity.SUPER_ADMIN.value or identity == Identity.ADMIN.value:
            if conditions:
                base_query = Q()
                if power_bank := conditions.get("power_bank", None):
                    base_query &= Q(rental__power_bank=power_bank)

                if user := conditions.get("user", None):
                    base_query &= Q(rental__user=user)

                if not (order_by := conditions.get("order_by", None)):
                    order_by = []

                query = PowerBankReturnInfo.objects.filter(base_query).all().order_by(*order_by)[
                        start_index:start_index + items_per_page]
                total = PowerBankReturnInfo.objects.filter(base_query).count()
            else:
                query = PowerBankReturnInfo.objects.all()[start_index:start_index + items_per_page]
                total = PowerBankReturnInfo.objects.count()
        else:
            base_query = Q()
            user = request.user.get("uid", None)
            base_query &= Q(rental__user=user)

            if not (order_by := conditions.get("order_by", None)):
                order_by = []

            query = PowerBankReturnInfo.objects.filter(base_query).all().order_by(*order_by)[start_index:start_index + items_per_page]
            total = PowerBankReturnInfo.objects.filter(base_query).count()

        data = PowerBankReturnSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)

        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def create_info(self, request, version, kwargs):
        # conditions, data = Internet.get_internet_data(request)
        # serializer = PowerBankReturnSerializer(data=data)
        # try:
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     data = serializer.to_representation(serializer.instance)
        #     return response(ResponseCode.SUCCESS, "创建成功", data)
        # except ValidationError as e:
        #     return validation_exception(e)
        raise UnknownActionError("不支持此操作")

    def update_info(self, request, version, kwargs):
        # id_ = kwargs.get("pk", None)
        # conditions, data = Internet.get_internet_data(request)
        # try:
        #     instance = PowerBankReturnInfo.objects.filter(id=id_).first()
        # except PowerBankReturnInfo.DoesNotExist:
        #     return response(ResponseCode.ERROR, "归还记录不存在", {})
        #
        # ser = PowerBankReturnSerializer(instance, data=data, partial=True)
        # try:
        #     ser.is_valid(raise_exception=True)
        #     res = ser.save()
        #     data = ser.to_representation(res)
        #     return response(ResponseCode.SUCCESS, "更新归还记录成功", data)
        # except ValidationError as e:
        #     return validation_exception(e)
        raise UnknownActionError("不支持此操作")

    def delete_info(self, request, version, kwargs):
        # id_ = kwargs.get("pk", None)
        # try:
        #     PowerBankReturnInfo.objects.filter(id=id_).delete()
        #     return response(ResponseCode.SUCCESS, "删除成功", {})
        # except PowerBankReturnInfo.DoesNotExist:
        #     return response(ResponseCode.ERROR, "归还记录不存在", {})
        raise UnknownActionError("不支持此操作")


""" —————————————————————————————— """
""" |      PowerBankFeeInfo      | """
""" —————————————————————————————— """


class PowerBankFeeView(CRUDInterface):
    throttle_classes = [PowerBankFeeThrottle, ]
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            self.permission_classes = [NotAnonPermission, ]
        else:
            self.permission_classes = [MoreAndAdminPermission, ]
        return super().dispatch(request, *args, **kwargs)

    def get_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        query = PowerBankFeeInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "费用信息不存在", {})
        else:
            data = PowerBankFeeSerializer(query).data
            return response(ResponseCode.SUCCESS, "获取成功", data)

    def get_list(self, request, version, kwargs):
        page = kwargs.get("pk", None)
        if page is None or page < 1:
            page = 1

        conditions, data = Internet.get_internet_data(request)
        identity = request.user.get("identity", None)

        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if identity == Identity.SUPER_ADMIN.value or identity == Identity.ADMIN.value:
            if conditions:
                base_query = Q()
                if power_bank := conditions.get("power_bank", None):
                    base_query &= Q(rental__power_bank=power_bank)

                if user := conditions.get("user", None):
                    base_query &= Q(rental__user=user)

                if paid := conditions.get("paid", None):
                    if paid == "true":
                        base_query &= Q(paid=True)
                    else:
                        base_query &= Q(paid=False)

                if not (order_by := conditions.get("order_by", None)):
                    order_by = []

                query = PowerBankFeeInfo.objects.filter(base_query).all().order_by(*order_by)[
                        start_index:start_index + items_per_page]
                total = PowerBankFeeInfo.objects.filter(base_query).count()
            else:
                query = PowerBankFeeInfo.objects.all()[start_index:start_index + items_per_page]
                total = PowerBankFeeInfo.objects.count()
        else:
            base_query = Q()
            user = request.user.get("uid", None)
            base_query &= Q(rental__user=user)

            if not (order_by := conditions.get("order_by", None)):
                order_by = []

            query = PowerBankFeeInfo.objects.filter(base_query).all().order_by(*order_by)[start_index:start_index + items_per_page]
            total = PowerBankFeeInfo.objects.filter(base_query).count()

        data = PowerBankFeeSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)

        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def create_info(self, request, version, kwargs):
        # conditions, data = Internet.get_internet_data(request)
        # serializer = PowerBankFeeSerializer(data=data)
        # try:
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     data = serializer.to_representation(serializer.instance)
        #     return response(ResponseCode.SUCCESS, "创建成功", data)
        # except ValidationError as e:
        #     return validation_exception(e)
        raise UnknownActionError("不支持此操作")

    def update_info(self, request, version, kwargs):
        id_ = kwargs.get("pk", None)
        conditions, data = Internet.get_internet_data(request)
        try:
            instance = PowerBankFeeInfo.objects.filter(id=id_).first()
        except PowerBankFeeInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "费用记录不存在", {})

        ser = PowerBankFeeSerializer(instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "更新费用记录成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_info(self, request, version, kwargs):
        # id_ = kwargs.get("pk", None)
        # try:
        #     PowerBankFeeInfo.objects.filter(id=id_).delete()
        #     return response(ResponseCode.SUCCESS, "删除成功", {})
        # except PowerBankFeeInfo.DoesNotExist:
        #     return response(ResponseCode.ERROR, "费用记录不存在", {})
        raise UnknownActionError("不支持此操作")


""" —————————————————————————————— """
""" |      UserOrderOperation    | """
""" —————————————————————————————— """


class UserOrderOperationView(CRUDInterface):
    permission_classes = [NotAnonPermission, ]
    throttle_classes = [UserOrderOperationThrottle, ]

    def get_info(self, request, version, kwargs):
        raise UnknownActionError("不支持此操作")

    def get_list(self, request, version, kwargs):
        page = kwargs.get("pk", None)
        if page is None or page < 1:
            page = 1
        uid = request.user.get("uid", None)
        if uid is None:
            return response(ResponseCode.ERROR, "用户不存在", {})

        conditions, data = Internet.get_internet_data(request)
        items_per_page = 10
        start_index = (page - 1) * items_per_page

        order_by = conditions.get("order_by", None) or ["-rental_date"]

        # 共享的过滤条件
        common_filter = Q(user=uid)

        # 根据排序字段动态构建查询
        if order_by[0] in ("-fee", "fee", "pay_date", "-pay_date"):
            subquery = PowerBankFeeInfo.objects.filter(rental=OuterRef('pk')).order_by(*order_by)
            query = (
                PowerBankRentalInfo.objects
                .filter(common_filter)
                .annotate(fee=Subquery(subquery.values('fee')[:1]), pay_date=Subquery(subquery.values('pay_date')[:1]))
                .order_by(order_by[0])
            )
        elif order_by[0] in ("-return_date", "return_date"):
            subquery = PowerBankReturnInfo.objects.filter(rental=OuterRef('pk')).order_by(*order_by)

            query = (
                PowerBankRentalInfo.objects
                .filter(common_filter)
                .annotate(return_date=Subquery(subquery.values('return_date')[:1]))
                .order_by(order_by[0])
            )
        else:
            query = PowerBankRentalInfo.objects.filter(common_filter).order_by(*order_by)
        total_query = PowerBankRentalInfo.objects.filter(user=uid)

        # 应用分页
        query = query[start_index:start_index + items_per_page]
        total = total_query.count()

        # 序列化数据并返回
        data = OrderUserSerializer(query, many=True).data
        extra = set_extra_page(total, items_per_page)
        return response(ResponseCode.SUCCESS, "获取成功", data, extra=extra)

    def create_info(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)
        power_bank = data.get("power_bank", None)
        if power_bank is None:
            return response(ResponseCode.ERROR, "缺少充电宝", {})

        data = {
            'power_bank': power_bank,
            'user': request.user.get("uid", None),
        }
        serializer = PowerBankRentalSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.to_representation(serializer.instance)
            check_charging_status.delay(data["power_bank"])
            return response(ResponseCode.SUCCESS, "租用成功", data)
        except ValidationError as e:
            return validation_exception(e)


    def update_info(self, request, version, kwargs):
        conditions, data = Internet.get_internet_data(request)
        uid = request.user.get("uid", None)
        rental = kwargs.get("pk", None)

        type_ = conditions.get("type", None)
        if type_ == 'return':
            query = PowerBankRentalInfo.objects.filter(id=rental).first()

            if query is None:
                return response(ResponseCode.ERROR, "租赁记录不存在", {})

            if query.user.id != uid:
                return response(ResponseCode.ERROR, "该租赁记录不属于当前用户", {})

            if query.returned:
                return response(ResponseCode.ERROR, "该租赁记录已归还", {})

            data = {
                'power_bank': query.power_bank.id,
                'number': query.number,
                'user': query.user.id,
                "returned": True,
            }
            serializer = PowerBankRentalSerializer(instance=query, data=data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data = serializer.to_representation(serializer.instance)
                return response(ResponseCode.SUCCESS, "归还成功", data)
            except ValidationError as e:
                return validation_exception(e)
        elif type_ == 'fee':
            rental_query = PowerBankRentalInfo.objects.filter(id=rental).first()

            if rental_query is None:
                return response(ResponseCode.ERROR, "租赁记录不存在", {})

            if rental_query.user.id != uid:
                return response(ResponseCode.ERROR, "该支付记录不属于当前用户", {})

            fee_query = PowerBankFeeInfo.objects.filter(rental=rental).first()
            if fee_query is None:
                return response(ResponseCode.ERROR, "费用记录不存在", {})

            if fee_query.paid:
                return response(ResponseCode.ERROR, "该费用记录已支付", {})

            data = {
                'rental': rental,
                'fee': fee_query.fee,
                'paid': True,
            }
            serializer = PowerBankFeeSerializer(instance=fee_query, data=data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data = serializer.to_representation(serializer.instance)
                return response(ResponseCode.SUCCESS, "支付成功", data)
            except ValidationError as e:
                return validation_exception(e)
        else:
            return response(ResponseCode.ERROR, "类型错误", {})


    def delete_info(self, request, version, kwargs):
        raise UnknownActionError("不支持此操作")


