from django.db.models import Q
from django.shortcuts import render
from rest_framework.exceptions import ValidationError

from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.router import Internet
from spb_management.router.image_operation import ImgAPI, UploadImage
from spb_management.router.permission import MoreAndAdminPermission
from spb_management.router.response_data import response, ResponseCode
from spb_management.utils.my_exception import validation_exception
from system_administration.models import CarouselChartInfo
from system_administration.utils.serializer import CarouselChartSerializer, CarouselChartImgSerializer
from system_administration.utils.throttle import CarouselChartGetThrottle, CarouselChartPostThrottle, \
    CarouselChartImgThrottle

# Create your views here.
"""
系统设置管理，如全局配置项、公告发布等。
日志管理和审计追踪，记录关键操作和异常事件。
数据备份与恢复、系统性能监控等功能。
"""


""" —————————————————————————————— """
""" |          轮播图             | """
""" —————————————————————————————— """


class CarouselChartView(GetAndPostAPIView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.throttle_classes = [CarouselChartGetThrottle, ]
        else:
            self.permission_classes = [MoreAndAdminPermission, ]
            self.throttle_classes = [CarouselChartPostThrottle, ]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, version, **kwargs):
        action = request.GET.get('action', '')
        if action == "get":
            id_ = kwargs.get("pk", -1)
            return self.get_carousel_chart(id_)
        elif action == "showList":
            num = kwargs.get("pk", 5)
            return self.show_carousel_chart(num)
        elif action == "getList":
            page = kwargs.get("pk", 1)
            conditions, data = Internet.get_internet_data(request)
            return self.get_carousel_chart_list(page, conditions)

    def post(self, request, version, **kwargs):
        action = request.POST.get('action', '')

        if action == 'create':
            return self.create_carousel_chart(request)
        elif action == 'update':
            id_ = kwargs.get('pk', None)
            return self.update_carousel_chart(id_, request)
        elif action == 'delete':
            id_ = kwargs.get('pk', None)
            return self.delete_carousel_chart(id_)

        return response(ResponseCode.ERROR, '参数错误', {})

    def get_carousel_chart(self, id_):
        query = CarouselChartInfo.objects.filter(id=id_).first()
        if query:
            ser = CarouselChartSerializer(query)
            return response(ResponseCode.SUCCESS, '获取轮播图成功', ser.data)
        else:
            return response(ResponseCode.ERROR, '轮播图不存在', {})

    def show_carousel_chart(self, num):
        query = CarouselChartInfo.objects.filter(active=True).values("id", "img")[:num]
        ser = CarouselChartImgSerializer(query, many=True)
        data = ser.to_representation(query)
        return response(ResponseCode.SUCCESS, '获取轮播图成功', data)

    def get_carousel_chart_list(self, page, conditions):
        page = page if page > 0 else 1
        items_per_page = 10
        start_index = (page - 1) * items_per_page

        if conditions:
            keyword = conditions.get("keyword", None)
            base_query = Q()
            if keyword:
                match_fields = ['title']
                for field in match_fields:
                    base_query |= Q(**{f'{field}__icontains': keyword})
            area_values = CarouselChartInfo.objects.filter(base_query).values()[start_index:start_index + items_per_page]
            total = CarouselChartInfo.objects.filter(base_query).count()
        else:
            area_values = CarouselChartInfo.objects.values()[start_index:start_index + items_per_page]
            total = CarouselChartInfo.objects.count()
        res = CarouselChartSerializer(area_values, many=True)
        extra = {
            "total": total,
            "pageSize": items_per_page,
        }
        return response(ResponseCode.SUCCESS, "获取轮播图成功", res.data, extra=extra)

    def create_carousel_chart(self, request):
        conditions, data = Internet.get_internet_data(request)
        ser = CarouselChartSerializer(data=data)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "创建轮播图成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def update_carousel_chart(self, id_, request):
        conditions, data = Internet.get_internet_data(request)
        query = CarouselChartInfo.objects.filter(id=id_).first()
        if not query:
            return response(ResponseCode.ERROR, "轮播图不存在", {})

        if 'img' not in data:
            data['img'] = query.img.name

        ser = CarouselChartSerializer(instance=query, data=data)
        try:
            ser.is_valid(raise_exception=True)
            res = ser.save()
            data = ser.to_representation(res)
            return response(ResponseCode.SUCCESS, "更新轮播图成功", data)
        except ValidationError as e:
            return validation_exception(e)

    def delete_carousel_chart(self, id_):
        query = CarouselChartInfo.objects.filter(id=id_)
        if query:
            CarouselChartInfo.objects.filter(id=id_).delete()
            return response(ResponseCode.SUCCESS, "删除轮播图成功", {})
        else:
            return response(ResponseCode.ERROR, "轮播图不存在", {})


""" —————————————————————————————— """
""" |        轮播图               | """
""" —————————————————————————————— """


class CarouselChartImgView(GetAndPostAPIView):
    permission_classes = [MoreAndAdminPermission, ]
    throttle_classes = [CarouselChartImgThrottle, ]

    def post(self, request, version, **kwargs):
        res = UploadImage.upload_image(request, ImgAPI.carousel_chart_path)
        if res[0] == UploadImage.IMG_ERROR:
            return response(ResponseCode.ERROR, res[1], {})
        elif res[0] == UploadImage.IMG_NEW:
            return response(ResponseCode.SUCCESS, "上传成功", {"img": res[1]})
        elif res[0] == UploadImage.IMG_EXIST:
            return response(ResponseCode.SUCCESS, "图片已存在", {"img": res[1]})