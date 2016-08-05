#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@author: Edward.Liu
@contact: lonnyliu@126.com
@software: PyCharm
@file: memcached_monitor.py
@time: 16/7/14
"""

import subprocess


def get_tomcat_pid():
    # 自定义获取程序 pid 与启动命令
    path = "memcached"
    p = subprocess.Popen(['netstat', ' -ntupl'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    print out
get_tomcat_pid()