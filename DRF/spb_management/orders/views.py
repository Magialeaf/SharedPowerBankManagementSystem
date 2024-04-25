from django.shortcuts import render

from spb_management.base_class.CRUDInterface import UnknownActionError, CRUDInterface
# Create your views here.
"""
订单的创建、查询、支付、取消、完成等全生命周期管理。
订单费用计算、优惠活动处理、退款退货等操作。
"""


""" —————————————————————————————— """
""" |    PowerBankRentalInfo     | """
""" —————————————————————————————— """


class PowerBankRentalView(CRUDInterface):
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
""" |    PowerBankReturnInfo     | """
""" —————————————————————————————— """


class PowerBankReturnView(CRUDInterface):
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
""" |      PowerBankFeeInfo      | """
""" —————————————————————————————— """


class PowerBankFeeView(CRUDInterface):
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


