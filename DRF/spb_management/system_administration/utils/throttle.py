from spb_management.router.throttle_base import AuthThrottle, AnonThrottle


class CarouselChartGetThrottle(AnonThrottle):
    scope = "carousel_chart_get"
    THROTTLE_RATES = {"carousel_chart_get": "30/m"}


class CarouselChartPostThrottle(AuthThrottle):
    scope = "carousel_chart_post"
    THROTTLE_RATES = {"carousel_chart_post": "12/m"}


class CarouselChartImgThrottle(AuthThrottle):
    scope = "carousel_chart_img"
    THROTTLE_RATES = {"carousel_chart_img": "10/m"}