from spb_management.router.throttle_base import AuthThrottle


class PowerBankRentalThrottle(AuthThrottle):
    scope = "power_bank_rental"
    THROTTLE_RATES = {scope: "30/m"}


class PowerBankReturnThrottle(AuthThrottle):
    scope = "power_bank_return"
    THROTTLE_RATES = {scope: "30/m"}


class PowerBankFeeThrottle(AuthThrottle):
    scope = "power_bank_fee"
    THROTTLE_RATES = {scope: "30/m"}