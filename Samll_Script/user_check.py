#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com



import subprocess


def user_check():
    user = "cdczhangg"
    check_command = """echo "76132fbbe6" |sudo -S /usr/bin/tail -n 3 /etc/sudoers"""
    hostname_command = "hostname"

    for i in range(1, 17):
        ip_address = "10.171.35.%s" % i
        remote_name = "ssh %s@%s %s" % (user, ip_address, check_command)
        p = subprocess.Popen(remote_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        remote_name = "ssh %s@%s %s" % (user, ip_address, hostname_command)
        p_name = subprocess.Popen(remote_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        name_stdout, name_stderr = p_name.communicate()
        if "%c4CHappl" in stdout:
            print "Ip addresss is :%s" % ip_address + "\n" + "主机名为:%s" % name_stdout + "\n" + "用户或者组存在于配置为中" + "\n" + "%s" % stdout + "用户拥有 sudo 权限"


user_check()
