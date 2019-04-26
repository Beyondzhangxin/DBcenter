import urllib
# from django.utils.module_loading import import_by_path
# if django.get_version() >= "1.7":
#     from django.utils.module_loading import import_string
# else:
#     from django.utils.module_loading import import_by_path as import_string
from django.utils.module_loading import import_string as import_by_path
from .models import SSOUser
from . import REMOTE_AUTH_TOKEN_URL, SSO_USER_STORAGE
from .apiclient import client
from django.contrib.auth.backends import ModelBackend

from django.conf import settings
import logging
logging.basicConfig()
logger = logging.getLogger("API_CLIENT")
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)


class SSOAuthBackend:
    def __init__(self):
        SSO_USER_STORAGE_CLZ = import_by_path(SSO_USER_STORAGE)
        self.storageengine = SSO_USER_STORAGE_CLZ()

    def authenticate(self, request, request_token=None, auth_token=None):
        logger.debug("SSOAuthBackend")
        code, user_info = client.send_request(
            REMOTE_AUTH_TOKEN_URL + "?" + urllib.parse.urlencode({"request_token": request_token, "auth_token": auth_token}))
        user = user_info["user"]
        u = SSOUser(**user)
        self.storageengine.save(user["id"], u)
        return u

    def get_user(self, user_id):
        return self.storageengine.find(user_id)

