import os
from django.conf import settings
from .version import __version__, VERSION


def _load_setting(n, default):
    return getattr(settings, n) if hasattr(settings, n) else default

remote_sso_url_prefix = _load_setting("SSO_REMOTE_URL_PREFIX", "/sso/")
REMOTE_REQUEST_TOKEN_URL = os.path.join(remote_sso_url_prefix, "reqeusttoken/")
REMOTE_AUTH_TOKEN_URL = os.path.join(remote_sso_url_prefix, "authtoken/")
REMOTE_SSO_LOGIN_URL = os.path.join(remote_sso_url_prefix, "login/")
REMOTE_AUTH_BACKEND_URL = os.path.join(remote_sso_url_prefix, "login_backend/")


# user storage
SSO_USER_STORAGE = _load_setting("SSO_USER_STORAGE", "djssoclient.userstorage.SSOUserDBStorage")
SSO_SETTING_CACHE = _load_setting("SSO_SETTING_CACHE", "default")

#RSA KEYS
PRIVATE_PEM = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQClSUcpD4z0xO7q6udFudJixO0BhCY7Nn2m1xdtss5Nv4x+tTkZ
0kI3LIRuAXtnKqPCbeIhCfDUtgAlnEj2n2sUXYYBQmLJcYTMTxMjhMosZVvN9L1Q
rzPACZUkDJm7fMlNO4WVoN994bQ5YjlOIQUwJCx6Gm9xbtqPtCzpJAseRQIDAQAB
AoGAARRVbqM3XHHczZPzJrVr9lEq6xOd3E0izPAiqwi76C4UEM/GK7D/1bRouP8x
ex8AKsjk7SpPdFQr9BLtNw8bd+fhCctL2btl0P9l+my4ktb893wEfx/moECqiAw5
j7bu0lU9McpXUrnSZzJ7g+/SlsvPsvePvz8YETOhVP3yQpECQQC5tLGdeoP9woEt
VTwoZh9Up7k0Srj/qNhmJldVzSkQI5ditXVmwfVDvh/K4k4ILYDMDCwlpefS6996
zyotMqdHAkEA49nhY1NR3UzSx3BAqYz8lGhvFDKB6k7//K74hfx1ayFdSYtSv249
w5EBIuBR1rvNAuU43aGT31Vj2CZYhHOsEwJBAKYT1OxTDwu4ETJrkbtHaSmaPeVo
Ff5+D9l63IwdSGXojpB2W6IkP6XvuBsHPGXP2+mf0TNyJdrZmykHcF6veC0CQQCk
EkjSlTTl/mPpaVOmw/c9htY13QjgCHMdKYGcOebzddsPElxLrL6dDNWcn5tO3X0L
ELSaI7evonV7OGGVPxYxAkAWmYeW2f7SPQsG/f34YiL62FVXaJBIeAvoVN5CZkfu
BIK9DnNmDskqb9XxEPzyZVtBvXfdj97osQbG/oXSBDvH
-----END RSA PRIVATE KEY-----'''
PUBLIC_PEM = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClSUcpD4z0xO7q6udFudJixO0B
hCY7Nn2m1xdtss5Nv4x+tTkZ0kI3LIRuAXtnKqPCbeIhCfDUtgAlnEj2n2sUXYYB
QmLJcYTMTxMjhMosZVvN9L1QrzPACZUkDJm7fMlNO4WVoN994bQ5YjlOIQUwJCx6
Gm9xbtqPtCzpJAseRQIDAQAB
-----END PUBLIC KEY-----'''