#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@author: Edward.Liu
@contact: lonnyliu@126.com
@software: PyCharm
@file: mongodb_monitor.py
@time: 16/6/29
"""
import pymongo
import sys
import subprocess


def mongodb_status(c1, c2, ):
    conn = pymongo.MongoClient('172.31.1.205', 27017)
    db_name = conn.ceshi
    status = db_name.command("serverStatus")
    return status[c1][c2]


print mongodb_status(sys.argv[1], sys.argv[2])


def get_tomcat_pid():
    # 自定义获取程序 pid 与启动命令
    path = "/software/Mongodb/data/master/config/master.conf"
    p = subprocess.Popen(['ps', '-Ao', 'pid,command'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if path in line:
            pid = int(line.split(None, 1)[0])
            if pid is not None:
                return 1
    return 0


print get_tomcat_pid()
