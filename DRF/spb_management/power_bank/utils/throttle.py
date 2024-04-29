from spb_management.router.throttle_base import AuthThrottle


class PowerBankImgThrottle(AuthThrottle):
    scope = "power_bank_img"
    THROTTLE_RATES = {scope: "10/m"}


class PowerBankThrottle(AuthThrottle):
    scope = "power_bank"
    THROTTLE_RATES = {scope: "30/m"}


class PowerBankMaintenanceThrottle(AuthThrottle):
    scope = "power_bank"
    THROTTLE_RATES = {scope: "30/m"}