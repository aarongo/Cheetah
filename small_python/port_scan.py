#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

import socket
import time
import thread

def socket_port(ip, port):
    '''
        多线程扫描端口开通情况
    '''
    try:
        if port >= 65535:
            print u'端口扫描结束'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            lock.acquire()
            print ip, u':', port, u'端口开放'
            lock.release()
        s.close()
    except:
        print u'端口扫描异常'


def ip_scan(ip):
    try:
        print u'开始扫描 %s' % ip
        start_time = time.time()
        # 定义需要扫描端口的范围
        for i in range(3305, 3307):
            thread.start_new_thread(socket_port, (ip, int(i)))
        print u'扫描端口完成，总共用时 ：%.2f' % (time.time() - start_time)
        # raw_input("Press Enter to Exit")
    except:
        print u'扫描ip出错'


if __name__ == '__main__':
    for ip in range(1, 3):
        url = '10.171.1.%s' % ip
        lock = thread.allocate_lock()
        ip_scan(url)
