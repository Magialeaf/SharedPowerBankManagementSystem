from django.shortcuts import render

from power_bank.utils.throttle import PowerBankImgThrottle
from spb_management.base_class.CRUDInterface import CRUDInterface, UnknownActionError
from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.base_class.UploadImgAPI import UploadImgAPI
from spb_management.router.image_operation import ImgAPI
from spb_management.router.response_data import response, ResponseCode

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
    def get_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的get_info")

    def get_list(self, request, version, kwargs):
        raise UnknownActionError("未实现的get_list")

    def create_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的create_info")

    def update_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的update_info")

    def delete_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的delete_info")


""" —————————————————————————————— """
""" |    PowerBankMaintenance    | """
""" —————————————————————————————— """


class PowerBankMaintenanceView(CRUDInterface):
    def get_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的get_info")

    def get_list(self, request, version, kwargs):
        raise UnknownActionError("未实现的get_list")

    def create_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的create_info")

    def update_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的update_info")

    def delete_info(self, request, version, kwargs):
        raise UnknownActionError("未实现的delete_info")


""" —————————————————————————————— """
""" |       PowerBankImg         | """
""" —————————————————————————————— """


class PowerBankImgView(UploadImgAPI):
    throttle_classes = [PowerBankImgThrottle, ]
    def __init__(self):
        super().__init__(ImgAPI.power_bank_img_path)