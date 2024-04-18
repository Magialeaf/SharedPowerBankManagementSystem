from spb_management.router.throttle_base import AuthThrottle


class AreaThrottle(AuthThrottle):
    scope = "area"
    THROTTLE_RATES = {"area": "50/m"}