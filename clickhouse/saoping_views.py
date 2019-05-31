# coding=utf-8
import json

import pymysql
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import numpy as np
from clickhouse.saoping_tool import selectSFRASYSChannelexec

database_ip = '192.168.0.148'
user = 'root'
pwd = 'dps@106'
database_name = 'cloudpssnet'
port = 8308


def tasks(request):
    """
    :param request:
    :return:所有扫频任务ID
    """
    response = {}

    try:
        db = pymysql.connect(host=database_ip, user=user, password=pwd, database=database_name, port=port)
        cursor = db.cursor()
        sql = "SELECT task_id from tasksmanager_tasksmanager WHERE task_type='SFRASYS' "
        cursor.execute(sql)
        rs = cursor.fetchall()
        db.close()
        res = []
        for item in rs:
            res.append(item[0])
        response['data'] = res
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def mulTasks(request):
    """
    :return:任务下的所有场景
    """
    response = {}
    taskId = request.GET.get('taskId')
    try:
        db = pymysql.connect(host=database_ip, user=user, password=pwd, database=database_name, port=port)
        cursor = db.cursor()
        sql = 'SELECT message from tasksmanager_tasksmanager WHERE task_id=' + str(taskId)
        cursor.execute(sql)
        rs = cursor.fetchone()
        db.close()
        mulTasks = json.loads(rs[0])['multiTasks']
        param = json.loads(rs[0])['sfraList']['param']
        response['data'] = {}
        response['data']['multiTasks'] = mulTasks
        response['data']['param'] = param
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
@require_http_methods(['POST'])
def Phase_magnitude(request):
    """
    :param request:
    :return: 返回场景相位和幅值
    """
    param = json.loads(request.body)
    taskId = param.get('taskId')
    multiTasks = param.get('multiTasks')
    try:
        db = pymysql.connect(host=database_ip, user=user, password=pwd, database=database_name, port=port)
        cursor = db.cursor()
        sql = 'SELECT user_id,simu,message,eventList from tasksmanager_tasksmanager WHERE task_id=' + str(taskId)
        cursor.execute(sql)
        rs = cursor.fetchone()
        db.close()
        mulTasksAll = json.loads(rs[2])['multiTasks']
        param = json.loads(rs[2])['sfraList']['param']
        userId = rs[0]
        simu = rs[1]
        eventList = json.loads(rs[3])
        response = {}
        channel_name = list(eventList["defaultApp"]['output'].keys())[0]
        data ={'param':[],'phaze':[],'mag':[]}
        for item in multiTasks:
            table_name = 'cloudpss_' + str(userId) + '_' + str(simu) + '_' + taskId + '_result_' + str(item)
            indx = mulTasksAll.index(item)+1
            res = selectSFRASYSChannelexec(indx, table_name, [channel_name + ':Phase', channel_name + ':Magnitude'])
            if len(res)==0:
                continue
            data['param'].append(param[indx-1])
            data['phaze'].append(res[0][0])
            data['mag'].append(res[1][0])
        phase=np.array(data['phaze'])
        unwrapphase = np.unwrap(phase)
        data['phaze']=list(unwrapphase)
        response['data'] = data
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
