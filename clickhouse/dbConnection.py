import datetime
import time
import uuid
from os.path import dirname, join as pjoin

from clickhouse_driver import Client
import numpy as np

# client = Client(host='192.168.0.133')

# list =DataTableIndex.objects.all()


# res=client.execute('select sum(fileSize) from cloudpss.index where user =%(user)s group by user ',{'user': '55'})
# client = Client(host='localhost')
# client.execute('alter table cloudpss.index add column fileSize UInt32 ')
# res=client.execute('select * from cloudpss.index where user =%(user)s', {'user': '52'})
# client.execute('create database if not exists cloudpss')
# client.execute('CREATE TABLE IF NOT EXISTS ' + 'cloudpss.c02261224' +
#                    ' (sourceName String, date Date default now(), targetName String,user String,type String)ENGINE = MergeTree(date,(targetName),8192)')

# try:
#     client.execute(
#         'CREATE TABLE IF NOT EXISTS cloudpss.c777 ' + '(index String,date Date default now(),value1 String,orderNum UInt32)' + 'ENGINE = MergeTree(date,(orderNum),8192)')
#     # res=client.execute('DROP TABLE IF EXISTS c02261224')
# except Exception as e:
#     print("error")
# insert("cloudpss.c777","(index,value,orderNum)",[['1 ','70' ,0],['2', '70', 1]])
# result=insert('cloudpss.index','(sourceName,targetName)',[['aa',time.strftime("%Y-%m-%d %X",time.localtime())],['bb',time.strftime("%Y-%m-%d %X",time.localtime())]])
# result = client.execute('show tables')
# result =client.execute('select * from cloudpss.index where sourceName = %s' % ('中啊文'))
# result = client.execute('select targetName from ' + 'cloudpss.index' + ' where sourceNaame = %(tn)s',
#                         {'tn': '负荷_供水压力.xlsx'})
# res=client.execute('select toFloat32OrZero(value2)  from cloudpss.cloudpssa2a31b0243db11e983be309c23643a08')
# temp =np.array(res).T.tolist()
# print(temp)

# result =client.execute("select targetName from %(db)s where sourceName = %(tn)s", {'db':'cloudpss.index','tn':'aa'})
# print(result)
# '负荷_供水压力.xlsx'
#
# user='Jason'
# dtype='default'
# res=client.execute("show databases ")
# path=os.path.dirname(__file__)
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = curPath[:curPath.find("DBcenter\\")+len("DBcenter\\")]  # 获取myProject，也就是项目的根路径
# dataPath = os.path.abspath(rootPath + 'data\\train.csv') # 获取tran.csv文件的路径
#
#
# tem=np.array([[8.00000e-04,1.60000e-03 ,2.40000e-03 ,3.49984e+01 ,3.49992e+01,
#   3.50000e+01]])
# for i in tem.T:
#     print(i)
#     print(np.concatenate((tem,[2]),axis=1))
# print(tem.T)
# x=np.array([[1,2,3,4]]).T
# print(x)
# t=np.array([[]])
# for i in x:
#     i=np.concatenate([list(i),[5]])
#     print(type(x))
# print(x)
# print(tem.shape)
# x = np.array([1, 2, 3, 4, 5])
# Y = np.array([[1,2,3],[4,5,6]])
# print()
# print('Original x = ', x)
# x = np.append(x, 6) # 秩为1的ndarray，直接append
# print()
# print('x = ', x)
# x = np.append(x, [7,8]) # 秩为1的ndarray，也可通过列表一次添加多个
# print()
# print('x = ', x)
# print()
# print('Original Y = \n', Y)
# v = np.append(Y, [[7,8,9]], axis=0) # 秩为2的ndarray，添加一行
# q = np.append(Y,[[9],[10]], axis=1) # 秩为2的ndarray，添加一列; 当然也可添加两列 q = np.append(Y,[[9,99],[10,100]], axis=1)
# print()
# print('v = \n', v)
# print()
# print('q = \n', q)
#
# Y = np.array([['1',2,3],['4',5,6]]).tolist()
# for k,v in enumerate(Y):
#     print(k)
#     print(v)
# print(Y)
# x=np.repeat([[1]],Y.shape[0],axis=0).tolist()
# print(x)
#
# tt=np.append(Y,x,axis=1)
# print(tt)
# x =np.arange(10)
# y=x.reshape(10,1)
# a=[[1,2,3],[1,2,3]]
# for i in range(0):
#     print(i)
# print(len(a[0]))
# print(dirname(sio.__file__))
from clickhouse.electri_tr import *

client = Client(host='192.168.0.133', database='cloudpss')


def selectexec(startid=-1, endid=None, tableName=None):
    """
        固定查询方法
    """
    if startid == -1:
        data = client.execute("(select * from `" + tableName + "` limit 6)")
    else:
        endid = endid or startid + 7
        data = client.execute("(select * from `" + tableName + "` where id > " + str(startid) + " and id < " + str(
            endid) + " order by `id` )  ")
        if (len(data) < 1):
            data = client.execute(
                "(select * from `" + tableName + "` where id > " + str(startid) + " order by `id` limit 50 ) ")
    return data


def selectchannelexec(startid=-1, endid=None, tableName=None, channels=[]):
    """
        固定查询方法
    """

    endid = endid or startid + 3
    sqlstr = "select id ,nl, da,tm from (select id, names,datas,times from `" + tableName + "` " + " order by id) array join names as nl,datas as da,times as tm"
    cond = " where nl = '" + channels[0] + "'"
    """多个通道同时查询"""
    # cond=" where nl like '%"+channels.pop()+"%'"
    channels.pop(0)
    for val in channels:
        cond = cond + " or nl = '" + val + "'"

    sqlstr = sqlstr + cond

    data = client.execute(sqlstr)
    # if startid==-1:
    #     data=self.client.execute(sqlstr)
    # else:
    #     endid= endid or startid +7
    #     data=self.client.execute("(select * from `"+tableName+"` where id > "+str(startid)+" and id < "+str(endid)+" order by `id` )  ")
    #     if(len(data)<1):
    #         data=self.client.execute("(select * from `"+tableName+"` where id > "+str(startid)+" order by `id` limit 50 ) ")
    return data



data1 = list(client.execute('select datas,times from cloudpss_3_18_1551867901_result_193673134 where id =1'))
# data1=getChannels('cloudpss_52_9_1554692007_result')
print(data1)
