from spb_management.router.throttle_base import AnonThrottle, AuthThrottle


class EnterThrottle(AnonThrottle):
    scope = "enter"
    THROTTLE_RATES = {scope: "5/10m"}


class UserThrottle(AnonThrottle):
    scope = "user"
    THROTTLE_RATES = {scope: "30/m"}


class AccountThrottle(AnonThrottle):
    scope = "account"
    THROTTLE_RATES = {scope: "10/m"}


class OneThrottle(AnonThrottle):
    scope = "one"
    THROTTLE_RATES = {scope: "10/m"}


class UserAvatarThrottle(AuthThrottle):
    scope = "user_avatar"
    THROTTLE_RATES = {scope: "10/m"}
