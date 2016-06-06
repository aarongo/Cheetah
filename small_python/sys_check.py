#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import subprocess


def check():
    user = 'cdczhangg'
    hostname_command = "hostname"
    command = "df -HT | grep '/software' | awk '{print $2}'"
    dir_owner = """/bin/ls -ll / | grep 'software' | /bin/awk '{print $3"\t"$4}'"""
    cpu_info = " cat /proc/cpuinfo |grep 'cores' | uniq  |awk '{print $4}'"
    mem_size = "cat /proc/meminfo | grep MemTotal | awk '{print $2}'"
    for ip in range(1, 17):
        ip_address = '10.171.35.%s' % ip

        # 主机名
        remote_name = "ssh %s@%s %s" % (user, ip_address, hostname_command)
        p_name = subprocess.Popen(remote_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        name_stdout, name_stderr = p_name.communicate()
        # 获取硬盘大小
        remote_disk_size = "ssh %s@%s %s" % (user, ip_address, command)
        p_size = subprocess.Popen(remote_disk_size, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        disk_size_stdout, disk_size_stderr = p_size.communicate()
        # # 获取分区权限

        remote_owner = """ssh %s@%s "%s" """ % (user, ip_address, dir_owner)
        p_owner = subprocess.Popen(remote_owner, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p_owner_stdout, p_owner_stderr = p_owner.communicate()

        # 获取 CPU 信息
        remote_cpu = "ssh %s@%s %s" % (user, ip_address, cpu_info)
        p_cpu = subprocess.Popen(remote_cpu, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p_cpu_stdout, p_cpu_stderr = p_cpu.communicate()
        # 获取内存大小
        remote_mem = "ssh %s@%s %s" % (user, ip_address, mem_size)
        p_mem = subprocess.Popen(remote_mem, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p_mem_stdout, p_mem_stderr = p_mem.communicate()
        print "主机名:%s" % name_stdout + "硬盘大小(/software):%s" % disk_size_stdout + "目录属性:%s" % p_owner_stdout + "CPU核数为:%s" % p_cpu_stdout + "内存大小:%s" % round(
                int(p_mem_stdout) / float(1024 * 1024)) + "GB"


check()
