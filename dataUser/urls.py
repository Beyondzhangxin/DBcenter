# coding=utf-8
from django.conf.urls import url

from dataUser import views

urlpatterns = [
    url('ownedFiles', views.ownedFiles),
    url('sharedFiles', views.sharedFiles),
    url('addShareUser', views.addShareUser),
    url('cancelShareUser', views.cancelShareUser),
    url('changeFileStatus', views.changeFileStatus),


]