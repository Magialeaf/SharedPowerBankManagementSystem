from django.db.models import Q
from rest_framework.exceptions import ValidationError

from areas.models import AreaInfo
from areas.utils.serializer import AreaSerializer, AreaNameSerializer
from areas.utils.throttle import AreaThrottle
from areas.utils.redis_operation import AreaDataRedis
from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.router import Internet
from spb_management.router.permission import MoreAndMaintainerPermission
from spb_management.router.response_data import response, ResponseCode
from spb_management.utils.my_exception import validation_exception

# Create your views here.
"""
区域划分与管理，包括行政区划、商圈、具体地点等。
与商户及充电宝设备进行关联，便于地理定位和运营分析。
"""


""" —————————————————————————————— """
""" |          Areas             | """
""" —————————————————————————————— """


class AreaView(GetAndPostAPIView):
    permission_classes = [MoreAndMaintainerPermission, ]
    throttle_classes = [AreaThrottle, ]

    def get(self, request, version, **kwargs):
        action = request.GET.get("action")
        if action == "get":
            return self.get_area(kwargs.get("pk", None))
        elif action == "getByLL":
            conditions, data = Internet.get_internet_data(request)
            lat = conditions.get("latitude", '')
            lng = conditions.get("longitude", '')
            return self.get_area_by_lat_lng(lat, lng)
        elif action == "getList":
            page = kwargs.get("pk", 1)
            conditions, data = Internet.get_internet_data(request)
            return self.get_area_list(page, conditions)
        elif action == "getNameList":
            conditions, data = Internet.get_internet_data(request)
            return self.get_area_name_list(conditions)
        return response(ResponseCode.ERROR, "请求参数错误", {})

    def post(self, request, version, **kwargs):
        action = request.POST.get("action")
        if action == "create":
            return self.create_area(request)
        elif action == "update":
            id_ = kwargs.get("pk", None)
            condition, data = Internet.get_internet_data(request)
            return self.update_area(id_, data)
        elif action == "delete":
            id_ = kwargs.get("pk", None)
            return self.delete_area(id_)

        return response(ResponseCode.ERROR, "请求参数错误", {})

    def get_area(self, id_):
        if id_ is None:
            return response(ResponseCode.ERROR, "请求参数错误", {})

        cache_data = AreaDataRedis.get_area_data_by_id(id_)
        if cache_data:
            return response(ResponseCode.SUCCESS, "获取区域成功", cache_data)

        query = AreaInfo.objects.filter(id=id_).first()
        if query is None:
            return response(ResponseCode.ERROR, "区域不存在", {})

        serialized_data = AreaSerializer(query).data
        AreaDataRedis.set_area_data(serialized_data)
        return response(ResponseCode.SUCCESS, "获取区域成功", serialized_data)

    def get_area_by_lat_lng(self, lat, lng):
        exists, cached_data = self.get_area_data_by_lat_lng(lat, lng)
        if exists:
            return response(ResponseCode.SUCCESS, "获取区域成功", cached_data)
        return response(ResponseCode.ERROR, "区域不存在", {})

    def get_area_data_by_lat_lng(self, lat, lng):
        cache_data = AreaDataRedis.get_area_data_by_lat_lng(lat, lng)
        if cache_data:
            return True, cache_data

        # 从数据库中获取AreaInfo对象
        area_info = AreaInfo.objects.filter(latitude=lat, longitude=lng).first()

        if area_info is None:
            return False, "区域不存在"

        serialized_data = AreaSerializer(area_info).data
        AreaDataRedis.set_area_data(serialized_data)
        return True, serialized_data

    def get_area_list(self, page, conditions):
        page = page if page > 0 else 1
        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if conditions:
            keyword = conditions.get("keyword", None)
            keycode = conditions.get("keycode", None)
            base_query = Q()
            if keyword:
                match_fields = ['name', 'description']
                for field in match_fields:
                    base_query |= Q(**{f'{field}__icontains': keyword})
            if keycode:
                base_query &= Q(code=keycode)
            area_values = AreaInfo.objects.filter(base_query).values()[start_index:start_index + items_per_page]
            total = AreaInfo.objects.filter(base_query).count()
        else:
            area_values = AreaInfo.objects.values()[start_index:start_index + items_per_page]
            total = AreaInfo.objects.count()
        res = AreaSerializer(area_values, many=True)
        extra = {
            "total": total,
            "pageSize": items_per_page,
        }

        return response(ResponseCode.SUCCESS, "获取区域列表成功", res.data, extra=extra)

    def get_area_name_list(self, conditions):
        if 'code' in conditions:
            code = conditions['code']
            area_instance = AreaInfo.objects.filter(code=code).values("id", "name")

            if area_instance.exists():
                res = AreaNameSerializer(area_instance, many=True)
                return response(ResponseCode.SUCCESS, "获取区域列表成功", res.data)
            else:
                return response(ResponseCode.ERROR, "该地段没有区域存在", {})
        else:
            return response(ResponseCode.ERROR, "请求参数错误", {})


    def create_area(self, request):
        conditions, data = Internet.get_internet_data(request)
        ser = AreaSerializer(data=data)

        try:
            if ser.is_valid(raise_exception=True):
                lat = ser.validated_data['latitude']
                lng = ser.validated_data['longitude']
                exists, cached_data = self.get_area_data_by_lat_lng(lat, lng)

                if not exists:
                    create_data = ser.save()
                    return response(ResponseCode.SUCCESS, "添加区域成功", create_data)
                else:
                    return response(ResponseCode.ERROR, "区域已存在", cached_data)  # 返回已存在的区域数据
        except ValidationError as e:
            return validation_exception(e)

        return response(ResponseCode.ERROR, "添加区域失败", {})

    def update_area(self, id_, data):
        try:
            area_instance = AreaInfo.objects.get(id=id_)
        except AreaInfo.DoesNotExist:
            return response(ResponseCode.ERROR, "区域不存在", {})

        ser = AreaSerializer(area_instance, data=data, partial=True)
        try:
            ser.is_valid(raise_exception=True)
            area_instance = ser.save()  # 使用序列化器的save方法更新实例并触发缓存操作
            return response(ResponseCode.SUCCESS, "更新区域成功", ser.validated_data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_area(self, id_):
        query = AreaInfo.objects.filter(id=id_).values('id', 'latitude', 'longitude').first()
        if query:
            AreaInfo.objects.filter(id=id_).delete()
            AreaDataRedis.delete_area_data(query)
            return response(ResponseCode.SUCCESS, "删除区域成功", {})
        else:
            return response(ResponseCode.ERROR, "区域不存在", {})
