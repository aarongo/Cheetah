#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import subprocess


def check_own():
    user = 'cdczhangg'
    group = 'c4CHappl'
    command = "ls -l / | grep software | awk '{print $4}'"
    for ip in range(1, 17):
        ip_address = '10.171.35.%s' % ip

        remote_check = "ssh %s@%s" % (user, ip_address) + " " + "%s" % command
        p_check = subprocess.Popen(remote_check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (p_check_stdout, p_check_stderr) = p_check.communicate()
        if p_check_stdout.strip('\n') == group:
            print "%s" % ip_address + "权限更改正确"


check_own()
