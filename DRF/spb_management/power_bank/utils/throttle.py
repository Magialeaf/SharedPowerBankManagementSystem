from spb_management.router.throttle_base import AuthThrottle


class PowerBankImgThrottle(AuthThrottle):
    scope = "power_bank_img"
    THROTTLE_RATES = {scope: "10/m"}