import os

from django.core.files.storage import default_storage
from rest_framework import serializers
from spb_management.settings import MEDIA_URL
from spb_management.utils.my_crypto import HashFunc


class ImgAPI:
    MEDIA_ADDR = "http://127.0.0.1:8000"
    RELATIVE_MEDIA_URL = MEDIA_URL.removeprefix("/")
    __images = "images"

    __avatar_path = "/user_avatars/"
    __merchant_img_path = "/merchant_img/"
    __carousel_chart_path = "/carousel_chart/"
    __power_bank_img_path = "/power_bank_img/"

    user_avatar_path = RELATIVE_MEDIA_URL + __images + __avatar_path
    merchant_img_path = RELATIVE_MEDIA_URL + __images + __merchant_img_path
    carousel_chart_path = RELATIVE_MEDIA_URL + __images + __carousel_chart_path
    power_bank_img_path = RELATIVE_MEDIA_URL + __images + __power_bank_img_path

    default_avatar_path = MEDIA_ADDR + MEDIA_URL + __images + __avatar_path + "default.png"

    @staticmethod
    def get_avatar(name):
        return ImgAPI.get_url(ImgAPI.user_avatar_path, name)

    @staticmethod
    def get_merchant_img(name):
        return ImgAPI.get_url(ImgAPI.merchant_img_path, name)

    @staticmethod
    def get_carousel_chart(name):
        return ImgAPI.get_url(ImgAPI.carousel_chart_path, name)

    @staticmethod
    def get_power_bank_img(name):
        return ImgAPI.get_url(ImgAPI.power_bank_img_path, name)

    @staticmethod
    def get_url(base_url, name):
        return ImgAPI.MEDIA_ADDR + "/" + base_url + str(name)

    @staticmethod
    def check_img(base_url, name):
        url = os.path.join(base_url, name)[6:]
        if not default_storage.exists(url):
            raise serializers.ValidationError("图片不存在于服务器中")


class UploadImage:
    IMG_ERROR = 0
    IMG_NEW = 1
    IMG_EXIST = 2

    @staticmethod
    def validate_image(file):
        """
        验证上传文件的格式和大小是否符合要求。
        """
        # 检查文件格式
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        filename, extension = os.path.splitext(file.name)
        if extension.lower() not in allowed_extensions:
            return False, '上传的图片只能是 JPG, JPEG, PNG, GIF 或 BMP 格式！'

        # 检查文件大小
        max_size = 2 * 1024 * 1024  # 2 MB
        if file.size > max_size:
            return False, '上传的图片大小不能超过 2MB！'

        return True, None  # 文件验证通过，返回True和空字符串（或其他默认值）


    # todo: 要改
    @staticmethod
    def upload_image(request, base_url):
        # 获取上传的文件
        file = request.FILES.get('file')

        if not file:
            return UploadImage.IMG_ERROR, '缺少文件参数'

        res = UploadImage.validate_image(file)
        if not res[0]:
            return UploadImage.IMG_ERROR, res[1]

        # 读取文件内容并计算哈希值
        file_content = file.read()
        hashed_filename = HashFunc.md5(file_content) + os.path.splitext(file.name)[1]

        url = os.path.join(base_url, hashed_filename)[6:]

        # 检查哈希值对应的文件是否已存在
        if default_storage.exists(url):
            # 文件已存在，返回哈希值
            return UploadImage.IMG_EXIST, hashed_filename

        # 保存文件到指定位置，使用哈希值作为文件名
        saved_filename = default_storage.save(url, file)
        if not saved_filename:
            return UploadImage.IMG_ERROR, "保存文件失败"

        # 返回成功响应，包含带有哈希值的文件URL
        return UploadImage.IMG_NEW, hashed_filename

