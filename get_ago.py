#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


URL = 'http://esb.hnair.net:8888/webservice/Projects_HnaESBService_initial_ESBService?wsdl'
import sys
import urllib
import urllib2
import time


def sendsms(mobile, content):
    content = '[%s] %s' % (time.strftime('%Y%m%d %H:%M:%S'), content)
    data = {'mobile': mobile, 'content': content}
    body = urllib.urlencode(data)
    request = urllib2.Request(URL, body)
    urldata = urllib2.urlopen(request)
    # print urldata.read()


if __name__ == '__main__':
    sendsms(sys.argv[1], sys.argv[2])
