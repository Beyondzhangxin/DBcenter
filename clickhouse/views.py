import json
import uuid

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods
from clickhouse_driver import Client

# client = Client('192.168.0.147')
client = Client('localhost')


@require_http_methods(['GET'])
def dataImport(request):
    userId = request.GET.get("userId")
    context = {'userId': userId}
    return render(request, 'clickhouse/dataImport.html', context)


@require_http_methods(['POST'])
def doDataImport(request):
    data = json.loads(request.POST.get('data'))
    response = {}
    user = request.POST.get('userId')
    fileName = request.POST.get('fileName')
    dataType = request.POST.get('dataType')
    tableName = 'cloudpss.cloudpss' + ''.join(str(uuid.uuid1()).split('-'))
    dataLen = len(data[0])
    orderNum = 1
    # [value,value,orderNum,key]
    for item in data:
        item.extend([orderNum])
        orderNum += 1
    create_column = ' (index String,'
    insert_column = '(index,'
    for i in range(dataLen - 1):
        create_column += 'value' + str(i + 1) + ' String,'
        insert_column += 'value' + str(i + 1) + ','
    create_column += 'date Date default now(),orderNum UInt32)'
    insert_column += 'orderNum)'
    try:
        client.execute('CREATE TABLE IF NOT EXISTS ' + tableName +
                       create_column + 'ENGINE = MergeTree(date,(orderNum),8192)')
        insert(tableName, insert_column, data)
        createFileIndex(fileName, tableName, user, dataType)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


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
