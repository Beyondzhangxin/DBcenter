# coding=utf-8
from django.conf.urls import  url

from .views import *

urlpatterns = [
    url(r'^auth/$', viewAuth, name="ssoauth"),
    url(r'^login/$', viewLogin, name="login_redirect"),
    url(r'^login_backend/$', viewAuthBackEnd, name="login_redirect_backend"),
]

