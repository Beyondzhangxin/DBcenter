import datetime
import time
import uuid

from clickhouse_driver import Client

from clickhouse.views import insert

client = Client(host='192.168.0.147')
# client = Client(host='localhost')

# client.execute('create database if not exists cloudpss')
# client.execute('CREATE TABLE IF NOT EXISTS ' + 'cloudpss.index' +
#                    ' (sourceName String, date Date default now(), targetName String,user String,type String)ENGINE = MergeTree(date,(targetName),8192)')
# try:
#     res=client.execute('DROP TABLE IF EXISTS cloudpss0722793614b711e98ccd30b49eb09678')
# except Exception as e:
#     print("error")
# insert("cloudpss.table_5","(index,value)",[['1', '3.6'], ['2', '3.6'], ['3', '3.6'], ['4', '3.6'], ['5', '3.6'], ['6', '3.6'], ['7', '3.6'], ['8', '3.6'], ['9', '3.6'], ['10', '3.6'], ['11', '3.6'], ['12', '3.6'], ['13', '3.6'], ['14', '3.6'], ['15', '3.6'], ['16', '3.6'], ['17', '3.6'], ['18', '3.6'], ['19', '3.6'], ['20', '3.6'], ['21', '3.6'], ['22', '3.6']])

# result=insert('cloudpss.index','(sourceName,targetName)',[['aa',time.strftime("%Y-%m-%d %X",time.localtime())],['bb',time.strftime("%Y-%m-%d %X",time.localtime())]])
# result = client.execute('show tables')
# result =client.execute('select * from cloudpss.index where sourceName = %s' % ('中啊文'))
# result = client.execute('select targetName from ' + 'cloudpss.index' + ' where sourceNaame = %(tn)s',
#                         {'tn': '负荷_供水压力.xlsx'})

# result =client.execute("select targetName from %(db)s where sourceName = %(tn)s", {'db':'cloudpss.index','tn':'aa'})
# print(result)
# '负荷_供水压力.xlsx'
#
# user='Jason'
# dtype='default'
res=client.execute("show databases ")
print(res)