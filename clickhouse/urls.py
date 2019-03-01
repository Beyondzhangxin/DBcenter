# coding=utf-8
from django.conf.urls import url

from clickhouse import views

urlpatterns = [
    url('dataImport', views.dataImport),
    url('doDataImport', views.doDataImport),
    url('getFileList', views.searchFileByType),
    url('getTypeList', views.getTypelistByUser),
    url('getTable', views.getTableContentByName),
    url('getIndex', views.getDataIndex),
    url('deleteTable', views.delTable),
    url('dataTable', views.dataTable),
    url('test', views.test),
]
