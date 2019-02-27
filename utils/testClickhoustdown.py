#-*- coding:utf-8 -*-
from __future__ import division
from datetime import date, timedelta

from numpy.core.tests.test_mem_overlap import xrange
from sqlalchemy import func
from sqlalchemy import create_engine, Column, MetaData, literal,text

from clickhouse_sqlalchemy import types, engines
from clickhouse_sqlalchemy import Table
from clickhouse_sqlalchemy import make_session
from clickhouse_sqlalchemy import get_declarative_base
from clickhouse_driver import Client
import json
import traceback
from threading import Thread
from threading import RLock
import sys,os
CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST','192.168.0.133')
CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER','default')
CLICKHOUSE_DBNAME = os.getenv('CLICKHOUSE_DBNAME','cloudpss')
CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD','')
CLICKHOUSE_PORT = os.getenv('CLICKHOUSE_PORT',None)
tableName1='cloudpss_3_1_1541217990_result'
# tableName1='cloudpss_3_'
# tableName2='cloudpss_3_1_1540977466_result'
class ClickHouseImpl(object):
    def __init__(self):
        self.client = Client(host=CLICKHOUSE_HOST,port=CLICKHOUSE_PORT,database=CLICKHOUSE_DBNAME,user=CLICKHOUSE_USER,password=CLICKHOUSE_PASSWORD)

    def getLikeTables(self,name):
        return self.client.execute("show tables from cloudpss like '%"+name+"%' ")

    def selectexec(self,startid=-1,endid=-1,tableName=None):
        # mutex.acquire()
        """
            固定查询方法
        """
        # if getattr('resultTable',None)==None:
        #     self.resultTable=self.createResultTable()
        #     tableName=tableName or self.resultTable.name
        # if startid==-1:
        if endid==-1:
            data=self.client.execute("(select * from `"+tableName+"`)")
        else:
            data=self.client.execute("(select * from `"+tableName+"` where id > "+str(startid)+" and id < "+str(endid)+" order by `id` )  ")
        # else:
        #     endid= endid or startid +7
        #     data=self.client.execute("(select * from `"+tableName+"` where id > "+str(startid)+" and id < "+str(endid)+" order by `id` )  ")
        #     if(len(data)<1):
        #         data=self.client.execute("(select * from `"+tableName+"` where id > "+str(startid)+" order by `id` limit 50 ) ")
        # mutex.release()
        return data
    def selectData(self,channel=None,start=-1,end=-1,tableName=None):
        """
            获取数据方法2，所有的数据在同一张表内
            channel 要获取的通道
            startTime endTime 获取的时间区域 startTime默认为-1 即全部数据 endTime为空是默认获取大于startTime的数据，否则获取区间数据。
            datakey 获取数据的唯一值，默认为使用类的值
        """
        
        try:
            data=self.selectexec(start,end,tableName)
            if(len(data)<1):
                return -1
            result={}
            dataMap={}
            ids=[]
            # dataMap['id']=data[0]
            for val in data:
                channelnames=val[1]
                datas=list(val[2])
                # times=list(val[3])
                ids.append(val[0])
                for indx in xrange(len(channelnames)):
                    channel=channelnames[indx]
                    cdata=list(datas[indx])
                    # print cdata
                    # time=times[indx]
                    # cdata=[]
                    # cdata=zip(time,data)
                    channelList=[]
                    channelList=dataMap.get(channel,[])

                    channelList=channelList+cdata
                    dataMap[channel]=channelList
            result['data']=dataMap
            result['id']=ids
            return result
        except Exception as e:
            traceback.print_exc()
            data="data doesn't exist"
        return -1

    def dropTable(self,name):
        return self.client.execute("DROP TABLE IF EXISTS %s" % (name,))


def testfunc(tableName,filePath,start=-1,endtime=-1,num=-1):
    t=ClickHouseImpl()
    tables= t.getLikeTables(tableName1)
    # print tables
    times=0
    for table in tables:
        # print table
        # t.dropTable(table[0])
        
        data=t.selectData(tableName=table[0],start=start,end=endtime)
        sp = os.path.join(filePath,str(table[0])+'.text')   
        jf = open(sp,'w+')
        s=file_iterator(data['data'])
        while s:
            try:
                # print s.next()
                jf.write(s.next())
            except StopIteration as e:
                print(e)
                break
                pass
            
        jf.close()
        times+=1
        if num>-1 and times>num:
            break
        
        # break
    #     # json.dump( data, jf,indent=2,ensure_ascii=False)
    #     # jf.close()
    # data=t.selectData(tableName=tableName,start=start)
    # if data!=-1:
    #     start=data['id'][len(data['id'])-1]
    #     print start
    #     testfunc(tableName,start)
    #     del t


def file_iterator(channel,chunk_size=512):
    yield 'startTime='+str(0)+' endTime='+str(3)
    for key,val in channel.items():
        yield ' '+key+'='+str(10000)+','+str(len(val))
    yield '\n'
    for key in channel:
        data=channel[key]
        for indx in range(len(data)):
            yield str(data[indx])+'\n'
filePath='C:\\Users\\dps-dm\\Desktop\\ProjectTempTest\\clickhouseText\\result'
if len(sys.argv)>1:
    filePath=sys.argv[1]
isExists=os.path.exists(filePath)
print(isExists)
if not isExists:
    os.makedirs(filePath)
startTime=-1
if len(sys.argv)>2:
    startTime=int(sys.argv[2])
endtime=-1
if len(sys.argv)>3:
    endtime=int(sys.argv[3])
num=-1
if len(sys.argv)>4:
    num=int(sys.argv[4])
testfunc(tableName1,filePath,startTime,endtime,num)


# t1=ClickHouseImpl()
# t1.addx(2)
# t1.printx()
# t2=ClickHouseImpl()
# # t1.addx(2)
# t2.printx()
