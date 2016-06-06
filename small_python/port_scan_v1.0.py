#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

import socket
import argparse
import sys


def check_port(ip, port):
    # 扫描IP 端口
    Local_ipaddr = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # s.connect((ip, int(port)))
    result = s.connect_ex((ip, port))
    if result == 0:
        print u'Ip:%s' % Local_ipaddr + '---->' + u'IP:%s' % ip + u'端口:' + '%d ' % port + u'\033[32m开放\033[0m'
    else:
        print u'Ip:%s' % Local_ipaddr + '---->' + u'IP:%s' % ip + u'端口:' + '%d ' % port + u'\033[31m未开放\033[0m'
    s.close()
    # 扫描结束


def check_arg(self, args=None):
    parser = argparse.ArgumentParser(description='Script to learn basic argparse')
    parser.add_argument('-H', '--host', help='Input Host group', default='cache')

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


if __name__ == '__main__':
    # 获取到去除脚本本身的所有参数
    args = check_arg(sys.argv[1:])
    if args.host == 'cache':
        print u'Web To Cache'
        for i in range(8, 11):
            ip_addr = '10.171.35.%s' % i
            print u'开始扫描IP:%s' % ip_addr
            for port in range(11210, 11220):
                check_port(ip_addr, port)
    elif args.host == 'DB':
        print u'Web To DB'
        for i in range(1, 3):
            ip_addr = '10.171.1.%s' % i
            print u'开始扫描IP:%s' % ip_addr
            check_port(ip_addr, 3306)
    elif args.host == 'mongodb':
        print u'Web To Mongodb'
        for i in range(8, 11):
            ip_addr = '10.171.35.%s' % i
            print u'开始扫描IP:%s' % ip_addr
            check_port(ip_addr, 27017)
    elif args.host == 'solr':
        print u'Web To Solr'
        for i in range(8, 11):
            ip_addr = '10.171.35.%s' % i
            print u'开始扫描IP:%s' % ip_addr
            check_port(ip_addr, 8080)
    elif args.host == 'nfs':
        print u'web TO Nfs'
        for i in range(14, 16):
            ip_addr = '10.171.35.%s' % i
            print u'开始扫描IP:%s' % ip_addr
            check_port(ip_addr, 111)
