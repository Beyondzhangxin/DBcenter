# coding=utf-8
from clickhouse_driver import Client


def selectSFRASYSChannelexec(indx=0, tableName=None, channels=[]):
    """
        固定查询方法
    """
    client = Client(host='192.168.0.133', database='cloudpss')
    tableName = tableName
    channelstr = ""
    for val in channels:
        channelstr += "'" + val + ':' + str(indx) + "',"

    channelstr = channelstr[0:len(channelstr) - 1]
    sqlstr = '''
       SELECT
               da,
               tm,
               nm
           FROM
           (
               SELECT
                   datas,
                   times,
                   nm
               FROM %s
               ARRAY JOIN
                   datas AS datas,
                   times AS times,
                   names AS nm
               WHERE nm IN (%s)
               ORDER BY id DESC
           )
           ARRAY JOIN
               datas AS da,
               times AS tm
           ORDER BY tm DESC
           LIMIT %d
       ''' % (tableName, channelstr, len(channels))
    data = client.execute(sqlstr)
    return data