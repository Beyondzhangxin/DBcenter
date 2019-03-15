import base64
import datetime
import json
import os
import uuid

import numpy as np
import pymysql
from django.core import serializers
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods
from clickhouse_driver import Client

from DBcenter.settings import DATABASES
from clickhouse.models import DataTableIndex
from utils.testmat import readFile

# database configuration
database_ip = DATABASES['default']['HOST']
database_port = DATABASES['default']['PORT']
database_name = DATABASES['default']['NAME']
user = DATABASES['default']['USER']
pwd = DATABASES['default']['PASSWORD']


client = Client('192.168.0.147')
# client = Client('localhost')
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("DBcenter\\")+len("DBcenter\\")]

@require_http_methods(['GET'])
def dataImport(request):
    userId = request.GET.get("userId")
    context = {'userId': userId}
    return render(request, 'clickhouse/dataImport.html', context)


@require_http_methods(['POST'])
def doDataImport(request):
    # dt=request.body.get('data')
    response = {}

    try:
        param=json.loads(request.body)
    except Exception as e:
        param=request.POST
    user = str(param.get('userId'))
    used_space_size=calculate_used_space(user)
    allowed_space_size=get_user_allowed_spaceSize(user)


    fileName = param.get('fileName')
    dataType = param.get('dataType')

    # load .mat file
    if request.POST.get('data') is None:
        data = param['data']
        data=base64.b64decode(data)
        filePath=os.path.abspath(rootPath + 'temp\\mat111'+'.mat')
        try:
            file =open(filePath,'wb')
            file.write(data)
            file.flush()
            mat_data=readFile(filePath)
            for key, val in mat_data.items():
                # process the data in mat file
                if type(val)==np.ndarray and val.ndim<=2:
                    if val.shape[0]>val.shape[1]:
                        val=val.T
                    val=val.astype(np.str)
                    tableName = 'cloudpss.cloudpss' + ''.join(str(uuid.uuid1()).split('-'))
                    name=fileName+'_'+key
                    fileSize=val.size*8
                    if (used_space_size + fileSize > allowed_space_size):
                        response['msg'] = '个人存储空间已满！'
                        response['error_num'] = 2
                        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
                    doDataInsert(tableName,name,user,dataType,(val.T).tolist(),fileSize)
                if type(val) == np.ndarray and val.ndim > 2:
                    raise NameError("数据维度有误！")
            response['msg'] = 'success'
            response['error_num'] = 0
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
        finally:
            file.close()

    else:
        # load .xsl file
        data=json.loads(param.get('data'))
        fileSize = float(param.get('size'))
        if (used_space_size + fileSize > allowed_space_size):
            response['msg'] = '个人存储空间已满！'
            response['error_num'] = 2
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
        try:
            tableName = 'cloudpss.cloudpss' + ''.join(str(uuid.uuid1()).split('-'))
            doDataInsert(tableName, fileName, user, dataType, data,fileSize)
            response['msg'] = 'success'
            response['error_num'] = 0
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def doDataInsert(tableName,fileName,user,dataType,data,fileSize):
    column = len(data[0])
    for index, value in enumerate(data):
        value.append(index)
    create_column = ' (index String,'
    insert_column = '(index,'
    for i in range(column - 1):
        create_column += 'value' + str(i + 1) + ' String,'
        insert_column += 'value' + str(i + 1) + ','
    create_column += 'date Date default now(),orderNum UInt32)'
    insert_column += 'orderNum)'
    client.execute('CREATE TABLE IF NOT EXISTS ' + tableName +
                   create_column + 'ENGINE = MergeTree(date,(orderNum),8192)')
    insert(tableName, insert_column, data)
    createFileIndex(fileName, tableName, user, dataType,fileSize)


@require_http_methods(['GET'])
def searchFileByType(request):
    response = {}
    type = request.GET.get('dataType')
    user = request.GET.get('userId')
    try:
        if not type is None:
            res = client.execute(
                "select sourceName,date,targetName from cloudpss.index where user=%(user)s and type=%(dtype)s",
                {'user': user, 'dtype': type})
        else:
            res=client.execute(
                "select sourceName,date,targetName from cloudpss.index where user=%(user)s",
                {'user': user})
        response['data'] = res
        response['msg'] = 'success'
        response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def calculate_used_space(userId):
    try:
        db = pymysql.connect(database_ip, user, pwd, database_name)
        cursor = db.cursor()
        sql = "SELECT SUM(fileSize) from (SELECT * from data_table_index where user="+userId+" GROUP BY fileSize )a"
        cursor.execute(sql)
        rs = cursor.fetchone()
        db.close()
        if not rs[0] is None:
            return float(rs[0])

        else:
            return 0
    except Exception as e:
        return None



def get_user_allowed_spaceSize(userId):
    return 10485760


def getUserSpaceInfo(request):
    response = {}
    userId=request.GET.get('userId')
    used_space_size = calculate_used_space(userId)
    allowed_space_size = get_user_allowed_spaceSize(userId)
    left_space_size = allowed_space_size - used_space_size
    response['used_space_size'] = used_space_size
    response['allowed_space_size'] = allowed_space_size
    response['left_space_size'] = left_space_size
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET'])
def delTable(request):
    response = {}
    tem=request.GET.get('tablelist')
    tablelist = json.loads(request.GET.get('tablelist'))

    try:
        for tableName in tablelist:
            table_index=DataTableIndex.objects.get(targetname=tableName)
            table_index.delete()
            res = client.execute("drop table if exists "+tableName)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

@require_http_methods(['GET'])
def getTypelistByUser(request):
    response = {}
    user = request.GET.get('userId')
    try:
        res = client.execute("select type from cloudpss.index where user=%(user)s  group by type ", {'user': user})
        response['data'] = res
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

@require_http_methods(['GET'])
def getDataIndex(request):
    userId=request.GET.get('userId')
    response={}
    try:
        # res = client.execute('select * from cloudpss.index where user =%(user)s', {'user': userId})
        data=DataTableIndex.objects.all().values()
        res=[]
        for item in data:
            res.append(list(item.values()))
        response['data']=res
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        print(e)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


def getTableContentByName(request):
    tableName = request.GET.get('targetName')
    source = request.GET.get('source')
    response = {}
    try:
        if source == 'cloudSpace':
            start = request.GET.get('start')
            length = request.GET.get('length')
            response = {}
            start = int(start) + 1
            length = int(length)
            end = start + length - 1
            res = client.execute("select * from " + tableName + " where orderNum between %(start)d and %(end)d",
                                 {'start': start, 'end': end})
        else:
            page = int(request.GET.get('page'))
            pageSize = int(request.GET.get('pageSize'))
            start = page * pageSize + 1
            end = (page + 1) * pageSize
            res = client.execute("select * from " + tableName + " where orderNum between %(start)d and %(end)d",
                                 {'start': start, 'end': end})
        response['data'] = res
        res = client.execute("DESC TABLE " + tableName)
        columns = []
        for item in res:
            columns.append(item[0])
        response['columns'] = columns[0:len(res)]
        res = client.execute("select count() from " + tableName)
        response['recordsTotal'] = res[0][0]
        response['total'] = res[0][0]
        response['recordsFiltered'] = res[0][0]
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        print(e)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET'])
def showTableList(request):
    pass


@require_http_methods(['POST'])
def searchFromFileName(request):
    pass


def hasTable(database, tableName):
    result = client.execute('select targetName from ' + database + ' where sourceName = %(tn)s', {'tn': tableName})
    if len(result) > 0:
        return result[0][0]
    else:
        return False


def createFileIndex(sourceFileName, targetFileName, user, dataType,fileSize):

    t=DataTableIndex(sourcename=sourceFileName,date=datetime.datetime.now(),targetname=targetFileName,user=user,type=dataType,filesize=fileSize)
    t.save()

def insert(table, column, value):
    client.execute('INSERT INTO %s %s VALUES' % (table, column), value)


@require_http_methods(['GET'])
def test(request):
    return render(request, 'clickhouse/test.html')

@require_http_methods(['GET'])
def dataTable(request):
    return render(request, 'clickhouse/dataTable.html')

