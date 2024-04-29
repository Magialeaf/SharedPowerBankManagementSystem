from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError

from merchants.models import MerchantInfo
from merchants.utils.serializer import MerchantSerializer
from merchants.utils.throttle import MerchantThrottle
from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.base_class.UploadImgAPI import UploadImgAPI
from spb_management.router import Internet
from spb_management.router.image_operation import UploadImage, ImgAPI
from spb_management.router.permission import MoreAndMaintainerPermission, NotAnonPermission
from spb_management.router.response_data import ResponseCode, response
from spb_management.utils.my_exception import validation_exception

# Create your views here.
"""
商户注册与认证流程。
商户信息管理，包括基本信息、联系方式、所属区域等。
商户下的充电宝设备管理和财务结算功能。
"""


class MerchantView(GetAndPostAPIView):
    permission_classes = [MoreAndMaintainerPermission, ]
    throttle_classes = [MerchantThrottle, ]

    def get(self, request, version, **kwargs):
        action = request.GET.get("action")
        if action == "get":
            return self.get_merchant(kwargs.get("pk", None))
        elif action == "getList":
            page = kwargs.get("pk", 1)
            conditions, data = Internet.get_internet_data(request)
            return self.get_merchant_list(page, conditions)
        elif action == "getIdList":
            area_id = kwargs.get("pk", 0)
            return self.get_merchant_id_list(area_id)
        return response(ResponseCode.ERROR, "请求参数错误", {})

    def post(self, request, version, **kwargs):
        action = request.POST.get("action")
        if action == "create":
            return self.create_merchant(request)
        elif action == "update":
            id_ = kwargs.get("pk", None)
            condition, data = Internet.get_internet_data(request)
            return self.update_merchant(id_, data)
        elif action == "delete":
            id_ = kwargs.get("pk", None)
            return self.delete_merchant(id_)

        return response(ResponseCode.ERROR, "请求参数错误", {})

    def get_merchant(self, id_):
        if id_ is None:
            return response(ResponseCode.ERROR, "请求参数错误", {})

        # cache_data = AreaDataRedis.get_area_data_by_id(id_)
        # if cache_data:
        #     return response(ResponseCode.SUCCESS, "获取区域成功", cache_data)

        query = MerchantInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "商户不存在", {})

        serialized_data = MerchantSerializer(query).data
        # AreaDataRedis.set_area_data(serialized_data)
        return response(ResponseCode.SUCCESS, "获取商户成功", serialized_data)

    def get_merchant_list(self, page, conditions):
        page = page if page > 0 else 1
        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if conditions:
            keyword = conditions.get("keyword", None)
            keycode = conditions.get("keyAreaId", None)
            base_query = Q()
            if keyword:
                match_fields = ['shop_name', 'address', 'liaison']
                for field in match_fields:
                    base_query |= Q(**{f'{field}__icontains': keyword})
            if keycode:
                base_query &= Q(area=keycode)
            area_values = MerchantInfo.objects.filter(base_query).values()[start_index:start_index + items_per_page]
            total = MerchantInfo.objects.filter(base_query).count()
        else:
            area_values = MerchantInfo.objects.values()[start_index:start_index + items_per_page]
            total = MerchantInfo.objects.count()
        res = MerchantSerializer(area_values, many=True)
        extra = {
            "total": total,
            "pageSize": items_per_page,
        }
        return response(ResponseCode.SUCCESS, "获取区域列表成功", res.data, extra=extra)

    def get_merchant_id_list(self, area_id):
        if area_id == 0:
            return response(ResponseCode.ERROR, "请求参数错误", {})

        query = MerchantInfo.objects.filter(area=area_id).values("id", 'shop_name')
        data = [{"id": i["id"], "name": i["shop_name"]} for i in query]
        return response(ResponseCode.SUCCESS, "获取区域列表成功", data)
    
    def create_merchant(self, request):
        conditions, data = Internet.get_internet_data(request)
        ser = MerchantSerializer(data=data)

        try:
            ser.is_valid(raise_exception=True)
            create_data = ser.save()
            return response(ResponseCode.SUCCESS, "添加商户成功", create_data)
        except ValidationError as e:
            return validation_exception(e)
    
    def update_merchant(self, id_, data):
        try:
            area_instance = MerchantInfo.objects.filter(id=id_).first()
        except MerchantInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "商户不存在", {})

        ser = MerchantSerializer(area_instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            return response(ResponseCode.SUCCESS, "更新商户成功", res)
        except ValidationError as e:
            return validation_exception(e)
    
    def delete_merchant(self, id_):
        query = MerchantInfo.objects.filter(id=id_).values().first()
        if query:
            MerchantInfo.objects.filter(id=id_).delete()
            # AreaDataRedis.delete_area_data(query)
            return response(ResponseCode.SUCCESS, "删除商户成功", {})
        else:
            return response(ResponseCode.ERROR, "商户不存在", {})


class MerchantImgThrottle(UploadImgAPI):
    throttle_classes = [MerchantThrottle, ]

    def __init__(self):
        super().__init__(ImgAPI.merchant_img_path)
