#coding:utf-8
"""
    需要安装的python依赖 
    1. pip install scipy （自动安装numpy，如果没安装自行安装 pip install numpy）
    2. pip install h5py

"""
import os
from os.path import dirname, join as pjoin
def readMatFile(file):
    """
        read Mat file
    """
    import scipy.io as sio
    data_dir = pjoin(dirname(sio.__file__), 'matlab', 'tests', 'data')
    mat = sio.loadmat(file)
    return mat

def readH5MatFile(file):
    """
        read H5 file
    """
    import h5py 
    f = h5py.File(file,'r')
    result={}
    for key in f.keys():
        result[key]=f[key].value.T
    return result
def readFile(file):
    """
        读取matlab文件
        matlab有两种数据形式，异常处理，然后第一种方式成为则使用第二种，如果两种都错误则报错
    """
    data=[]
    try:
        data=readMatFile(file)
    except Exception as e:
        data=readH5MatFile(file)
    return data




"""
    以下是测试代码
"""

"""
    {
        tabel1:[[],[],[]],
        tabel2:[[],[],[]],
        ....
    }
"""

