from spb_management.router.throttle_base import AuthThrottle


class MerchantThrottle(AuthThrottle):
    scope = "merchant"
    THROTTLE_RATES = {"merchant": "50/m"}


class MerchantImgThrottle(AuthThrottle):
    scope = "merchant"
    THROTTLE_RATES = {"merchant": "10/m"}