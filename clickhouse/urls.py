# coding=utf-8
from django.conf.urls import url

from clickhouse import views, electri_views, saoping_views

urlpatterns = [
    url('dataImport', views.dataImport),
    url('doDataImport', views.doDataImport),
    url('getFileList', views.searchFileByType),
    url('getTypeList', views.getTypelistByUser),
    url('getTable', views.getTableContentByName),
    url('getCol', views.getCol),
    url('getIndex', views.getDataIndex),
    url('deleteTable', views.delTable),
    url('dataTable', views.dataTable),
    url('userSpace', views.getUserSpaceInfo),
    url('test', views.test),
    url('electri_tr/channelIdCount',electri_views.channelIdCount),
    url('electri_tr/channels',electri_views.channels),
    url('electri_tr/idChannelData',electri_views.idChannelData),
    url('electri_tr/alltables',electri_views.alltables),
    url('electri_tr/tables',electri_views.tables),
    url('electri_tr/multables',electri_views.multables),
    url('electri_tr/taskIdChannels',electri_views.channels_from_taskId),
    url('electri_tr/delTable',electri_views.delTable),
    url('electri_tr/channelData',electri_views.channelData),
    url('electri_tr/space',electri_views.space),
    url('electri_tr/downloadMat',electri_views.downloadMat),
    url('electri_tr/tasks',saoping_views.tasks),
    url('saoping/multiTasks',saoping_views.mulTasks),
    url('saoping/getData',saoping_views.Phase_magnitude),


]
