from django.core.cache import caches

# 缓存时间：秒 * 分 * 时 * 天
SAVE_TIME = 60 * 60 * 24 * 1
cache = caches["merchant"]


class MerchantDataRedis:
    pass

