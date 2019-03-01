import base64
import json
import os
import uuid

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods
from clickhouse_driver import Client

from utils.testmat import readFile

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
                    doDataInsert(tableName,name,user,dataType,(val.T).tolist())
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
        try:
            tableName = 'cloudpss.cloudpss' + ''.join(str(uuid.uuid1()).split('-'))
            doDataInsert(tableName, fileName, user, dataType, data)
            response['msg'] = 'success'
            response['error_num'] = 0
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})

def doDataInsert(tableName,fileName,user,dataType,data):
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
    createFileIndex(fileName, tableName, user, dataType)


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



@require_http_methods(['GET'])
def delTable(request):
    response = {}
    tableName = request.GET.get('tableName')
    try:
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
    tableName=request.GET.get('targetName')
    start = int(request.GET.get('start'))
    pageSize = int(request.GET.get('length'))
    end = start+pageSize-1
    response={}
    try:
        res = client.execute("select * from " + tableName)
        response['data']=res[start:end]
        response['recordsFiltered'] = len(res)
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


def createFileIndex(sourceFileName, targetFileName, user, dataType):
    insert('cloudpss.index', '(sourceName,targetName,user,type)',
           [[sourceFileName, targetFileName, user, dataType]])


def insert(table, column, value):
    client.execute('INSERT INTO %s %s VALUES' % (table, column), value)


@require_http_methods(['GET'])
def test(request):
    return render(request, 'clickhouse/test.html')

@require_http_methods(['GET'])
def dataTable(request):
    return render(request, 'clickhouse/dataTable.html')

