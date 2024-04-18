from django.core.cache import caches

# 缓存时间：秒 * 分 * 时 * 天
SAVE_TIME = 60 * 60 * 24 * 1
cache = caches["area"]


class AreaDataRedis:
    @staticmethod
    def set_area_data(area_data):
        key_id = int(area_data.get("id", ""))
        key_lat_lng = str(area_data.get("latitude", "")) + "_" + str(area_data.get("longitude", ""))
        if key_id and key_lat_lng:
            cache.set(key_id, area_data, SAVE_TIME)  # 存储新的缓存信息
            cache.set(key_lat_lng, area_data, SAVE_TIME)  # 存储新的缓存信息
            return True
        return False

    @staticmethod
    def get_area_data_by_id(id_):
        return cache.get(id_)

    @staticmethod
    def get_area_data_by_lat_lng(latitude, longitude):
        key_lat_lng = str(latitude) + "_" + str(longitude)
        return cache.get(key_lat_lng)

    @staticmethod
    def delete_area_data(area_data):
        key_id = int(area_data.get("id", ""))
        key_lat_lng = str(area_data.get("latitude", "")) + "_" + str(area_data.get("longitude", ""))
        if key_id and key_lat_lng:
            cache.delete(key_id, area_data, SAVE_TIME)  # 存储新的缓存信息
            cache.delete(key_lat_lng, area_data, SAVE_TIME)  # 存储新的缓存信息
            return True
        return False

    @staticmethod
    def set_area_data_count(count):
        cache.set("area_data_count", count, SAVE_TIME)
        return True

    @staticmethod
    def get_area_data_count():
        return cache.get("area_data_count")

    @staticmethod
    def delete_area_data_count():
        cache.delete("area_data_count")
        return True

