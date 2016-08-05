#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@author: Edward.Liu
@contact: lonnyliu@126.com
@software: PyCharm
@file: nginx_analysis.py
@time: 16/6/29
"""
from collections import Counter
import sys


def analysis_ip():
    # 统计访问IP  URL存放位置
    top_ip_list = []
    with open('nginx.log') as fp:
        for line in fp:
            dick_list = eval(line)
            top_ip_list.append(dick_list['remoteORlbIP'])
    myset_ip = set(top_ip_list)
    for item_ip in myset_ip:
        print top_ip_list.count(item_ip), item_ip


def analysis_uri():
    # 统计访问IP  URL存放位置
    top_url_list = []
    with open('nginx.log') as fp:
        for line in fp:
            dick_list = eval(line)
            top_url_list.append(dick_list['uri'])
    for key, value in Counter(top_url_list).items():
        print key, value


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'ip':
            analysis_ip()
        elif sys.argv[1] == 'url':
            analysis_uri()
        else:
            print u'Please Input Right Parameter!!! EG:%s ip' % sys.argv[0]
            sys.exit(1)
    except IndexError:
        print u'Please Input Parameter!!!'
