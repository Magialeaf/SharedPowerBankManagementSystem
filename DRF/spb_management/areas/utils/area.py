from areas.models import AreaInfo


def get_area_code(area_id):
    if area_id:
        area_query = AreaInfo.objects.filter(id=area_id).first()
        if area_query:
            return area_query.code

    return None