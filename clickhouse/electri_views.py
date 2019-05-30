# coding=utf-8
"""
电磁暂态部分的请求
"""
import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from clickhouse.electri_tr import *

@require_http_methods(['POST'])
def downloadMat(request):
    param = json.loads(request.body)
    tableName=param.get('tableName')
    channels=param.get('channels')
    saveToMat(tableName,channels)
    with open('output.mat','rb') as file_obj:
        blob=file_obj.read()
    return HttpResponse(blob, content_type='application / octet - stream')

def space(request):
    response={}
    try:
        data=countSpace()
        response['data']=data
        response['error_num'] = 0
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def channelData(request):
    response={}
    tableName=request.GET.get('tableName')
    channels=json.loads(request.GET.get('channels'))
    try:
        data =selectchannelexec(tableName=tableName,channels=channels)
        response['data'] = data
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def delTable(request):
    response = {}
    tableName = request.GET.get('tableName')
    try:
        deleteTable(tableName)
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def tables(request):
    searchParam=request.GET.get('searchParam')
    response = {}
    try:
        tables = getTables(searchParam)
        response['data'] = tables
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def channelIdCount(request):
    tableName = request.GET.get('tableName')
    channel = request.GET.get('channel')
    response = {}
    try:
        count = getChannelIdCount(tableName, channel)
        response['count'] = count
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def channels(request):
    tableName = request.GET.get('tableName')
    response = {}
    try:
        channels = getChannels(tableName)
        response['channels'] = list(channels)
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def idChannelData(request):
    tableName = request.GET.get('tableName')
    id = request.GET.get('id')
    channel = request.GET.get('channel')
    response = {}
    try:
        result = selectIdChannelexec(id,tableName,channel)
        response['data'] = list(result[0])
        response['time'] = list(result[1])
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
