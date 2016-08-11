#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

import socket
import httplib

tomcat_exe = "tomcat_app"


def get_status_code(host, path="/"):
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status

    except StandardError:
        return None


def service_check():
    while True:
        ipaddress_port = socket.gethostbyname(socket.gethostname()) + ":80"
        app_return_code = get_status_code(host=ipaddress_port, path='/mobile/api/user/login')
        if app_return_code == 200:
            print "\033[32m %s Process Is Exist Service Is available Return Code:\033[0m" % tomcat_exe + "\033[31m%s\033[0m" % app_return_code + "\033[32mCheck URL:http://%s/mobile/api/user/login\033[0m" % ipaddress_port
            break


service_check()
