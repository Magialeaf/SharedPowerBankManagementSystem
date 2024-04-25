from spb_management.base_class.GetAndPostAPIView import GetAndPostAPIView
from spb_management.router.image_operation import UploadImage, ImgAPI
from spb_management.router.permission import MoreAndAdminPermission
from spb_management.router.response_data import response, ResponseCode


class UploadImgAPI(GetAndPostAPIView):
    permission_classes = [MoreAndAdminPermission, ]

    def __init__(self, url: ImgAPI, success_msg="上传成功", exist_msg="图片已经存在"):
        super().__init__()
        self.img_url = url
        self.success_msg = success_msg
        self.exist_msg = exist_msg

    def post(self, request, version, **kwargs):
        res = UploadImage.upload_image(request, self.img_url)
        if res[0] == UploadImage.IMG_ERROR:
            return response(ResponseCode.ERROR, res[1], {})
        elif res[0] == UploadImage.IMG_NEW:
            return response(ResponseCode.SUCCESS, self.success_msg, {"img": res[1]})
        elif res[0] == UploadImage.IMG_EXIST:
            return response(ResponseCode.SUCCESS, self.exist_msg, {"img": res[1]})
