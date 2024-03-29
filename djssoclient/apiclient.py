import urllib
# import urllib2
import urllib.request as urllib2
import json
# import urlparse
import urllib.parse as urlparse
# from urllib.parse import urljoin
import time
import logging
import hmac
import hashlib
import base64
import abc

from urllib.request import HTTPError
from django.conf import settings

logging.basicConfig()
logger = logging.getLogger("API_CLIENT")
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)


class AbsAPIClient(object):  # provide overwrite later
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send_request(self, url, data=None, datafunc=json.loads):
        return


class APIClientHTTPError(Exception):
    def __init__(self, reason, code, *args, **kwargs):
        super(APIClientHTTPError, self).__init__(reason, code, *args, **kwargs)
        self.code = code
        self.message = reason


class APIClient(AbsAPIClient):
    def __init__(self, apikey, seckey, url):
        self.opener = urllib2.build_opener()
        self._baseurl = url
        self._ak = str(apikey)
        self._sk = str(seckey)

    def _sign_msg(self, msg):
        dig = hmac.new(bytes(self._sk,'latin-1'), bytes(msg,'latin-1'), digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def _sign_url(self, _url):
        url = ("/" + _url) if not _url.startswith("/") else _url
        url_parts = urlparse.urlparse(url)
        qs = urlparse.parse_qs(url_parts.query)
        qs["timestamp"] = time.time()  # UNIX time
        qs["apikey"] = self._ak
        new_qs = urllib.parse.urlencode(qs, True)
        tmpurl = urlparse.urlunparse(list(url_parts[0:4]) + [new_qs] + list(url_parts[5:]))
        final_url = tmpurl + "&signature=" + self._sign_msg(tmpurl)  # sign url
        return final_url

    def send_request(self, url, data=None, datafunc=json.loads):
        logger.debug("send to: %s" % urlparse.urljoin(self._baseurl, self._sign_url(url)))
        try:
            t_request = urllib.request.Request(urlparse.urljoin(self._baseurl, self._sign_url(url)))
            self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            # resp = self.opener.open(t_request, data)
            resp = urllib.request.urlopen(t_request, data)
            return resp.code, datafunc(resp.read()) if datafunc else resp.read()
        except HTTPError as e:
            raise APIClientHTTPError(e.code, e.fp.read() if (e.fp and e.code == 403) else e.msg)

client = APIClient(**settings.SSO_API_AUTH_SETTING)
