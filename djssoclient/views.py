import json
import urllib
# import urlparse
# from urllib.parse import urlparse
import urllib.parse as urlparse

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .apiclient import client
from . import REMOTE_REQUEST_TOKEN_URL, REMOTE_SSO_LOGIN_URL,REMOTE_AUTH_BACKEND_URL
from . import PRIVATE_PEM,PUBLIC_PEM
from .authbackend import SSOAuthBackend


from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64


def encrypt(message):
    public_key = PUBLIC_PEM
    public_rsakey = RSA.importKey(public_key)  # 导入读取到的公钥
    public_cipher = Cipher_pkcs1_v1_5.new(public_rsakey)  # 生成对象
    cipher_text = base64.b64encode(public_cipher.encrypt(message.encode(encoding="utf-8"))) 
    return cipher_text
def decrypt(message):
    try:
        private_key = PRIVATE_PEM
        private_rsakey = RSA.importKey(private_key)  # 导入读取到的私钥
        private_cipher = Cipher_pkcs1_v1_5.new(private_rsakey)  # 生成对象
        text = private_cipher.decrypt(base64.b64decode(message), "ERROR")  # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
        return text
    except Exception as e:
        print (e)

# from django.conf import settings
import logging
logging.basicConfig()
logger = logging.getLogger("VIEWS")
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
 
def viewAuth(request):
    request_token = request.GET.get("request_token")
    auth_token = request.GET.get("auth_token")
    redirect_to = request.GET.get("redirect", settings.LOGIN_REDIRECT_URL)
    
    user = authenticate(request_token=request_token, auth_token=auth_token)
    if user is not None:
        auth_login(request, user)  # create session, write cookies
    else:
        raise PermissionDenied
    return HttpResponseRedirect(redirect_to)
    # return JsonResponse({
    #     'user':user.username
    # })


def viewLogin(request):
    _, token_info = client.send_request(REMOTE_REQUEST_TOKEN_URL)
    request_token = token_info["request_token"]

    restserver = settings.SSO_API_AUTH_SETTING["url"]
    url_parts = list(urlparse.urlparse(restserver))
    query = {"api_key": settings.SSO_API_AUTH_SETTING["apikey"],
             "request_token": request_token,
             "next": request.build_absolute_uri(
                 reverse("ssoauth") + "?redirect=%s" % request.GET.get("next", settings.LOGIN_REDIRECT_URL))}
    url_parts[2] = REMOTE_SSO_LOGIN_URL
    url_parts[4] = urllib.parse.urlencode(query)
    ssoLoginURL = urlparse.urlunparse(url_parts)
    print (ssoLoginURL)
    return HttpResponseRedirect(ssoLoginURL)

@csrf_exempt
@require_http_methods(['POST'])
def viewAuthBackEnd(request):
    email =json.loads(request.body)['email']
    password =  json.loads(request.body)['password']
    # encrypt_email = encrypt(email)
    # decrypt_email = decrypt(encrypt_email)
    # print (encrypt_email)
    # print (decrypt_email)
    _, login_info = client.send_request(REMOTE_AUTH_BACKEND_URL+ "?" + urllib.parse.urlencode({"email": encrypt(email), "password": encrypt(password)}))
    if login_info.get('status') is False:
        return JsonResponse({
            'info':login_info.get('info'),
            'status':login_info.get('status')
        })
    print (login_info)
    request_token = login_info.get("request_token")
    auth_token = login_info.get("auth_token")
    user = authenticate(request_token=request_token, auth_token=auth_token)
    if user is not None:
        auth_login(request, user)  # create session, write cookies
    else:
        raise PermissionDenied
    return JsonResponse({
        'user':user.username,
        'email':user.email,
        'status':login_info.get('status')
    })
    # _, token_info = client.send_request(REMOTE_AUTH_BACKEND_URL)
    
