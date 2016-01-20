#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import urllib
import time, os
import tarfile
import subprocess


def download():
    global libevent_url, memcached_url, download_path
    libevent_url = "http://124.200.96.150:8081/serverpackages/Memcacehd/libevent-2.0.22-stable.tar.gz"
    memcached_url = "http://www.danga.com/memcached/dist/memcached-1.4.0.tar.gz"
    download_path = "/software/packages"
    if os.path.exists(download_path):
        print "\033[31mDownload Files" + "\n" + "%s\033[0m" % libevent_url.split('/')[5] + "\n" + "\033[31m%s\033[0m" % \
                                                                                                  memcached_url.split(
                                                                                                          '/')[
                                                                                                      5]
        os.chdir(download_path)
        urllib.urlretrieve(libevent_url, "libevent-2.0.22-stable.tar.gz")
        time.sleep(5)
        urllib.urlretrieve(memcached_url, "memcached-1.4.0.tar.gz")
        if os.path.exists("%s/%s" % (download_path, libevent_url.split('/')[5])) and os.path.exists(
                        "%s/%s" % (download_path, memcached_url.split('/')[5])):
            print "\033[32mDownLoad OK\033[0m" + "!" * 10
    else:
        os.makedirs(download_path)
        print "\033[31mDownload Files" + "\n" + "%s\033[0m" % libevent_url.split('/')[5] + "\n" + "\033[31m%s\033[0m" % \
                                                                                                  memcached_url.split(
                                                                                                          '/')[
                                                                                                      5]
        os.chdir(download_path)
        urllib.urlretrieve(libevent_url, "libevent-2.0.22-stable.tar.gz")
        time.sleep(5)
        urllib.urlretrieve(memcached_url, "memcached-1.4.0.tar.gz")
        if os.path.exists("%s/%s" % (download_path, libevent_url.split('/')[5])) and os.path.exists(
                        "%s/%s" % (download_path, memcached_url.split('/')[5])):
            print "\033[32mDownLoad OK\033[0m" + "!" * 10


def install(mem_path, lib_path):
    os.chdir(download_path)
    # 安装 Libevent
    print "\033[32mStart install Libevent\033[0m" + "*" * 20
    # 解压文件
    t_lib = tarfile.open(libevent_url.split('/')[5])
    t_lib.extractall(".")
    t_lib.close()
    # 解压文件结束
    # 安装 libevent
    os.chdir(libevent_url.split('/')[5].split('.tar.gz')[0])
    install_command = "./configure --prefix=%s && make && make install" % lib_path
    proc = subprocess.Popen(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    print "*" * 10 + "\033[31mExit Code: %s\033[0m" % proc.returncode + "*" * 10
    # 安装完毕
    # 安装 Memcached
    print "-" * 10 + "Memcached Install" + "-" * 10
    os.chdir(download_path)
    t_mem = tarfile.open(memcached_url.split('/')[5])
    t_mem.extractall(".")
    t_mem.close()
    os.chdir(memcached_url.split('/')[5].split('.tar.gz')[0])
    install_memcached = "./configure --prefix=%s --with-libevent=%s && make && make install" % (mem_path, lib_path)
    proc_m = subprocess.Popen(install_memcached, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc_m.communicate()
    print "*" * 10 + "\033[31mexit code:%s\033[0m" % proc_m.returncode + "*" * 10
    # 安装 Memcached 完毕


if __name__ == "__main__":
    download()
    memcached_path = raw_input("Please Input memcached Install Path Default(/software/memcached)!!!").strip()
    if len(memcached_path) == 0:
        memcached_path = "/software/memcached"
    libevent_path = raw_input("Please Input Libevent Install Path(/software/libevent)!!!").strip()
    if len(libevent_path) == 0:
        libevent_path = "/software/libevent"
    install(memcached_path, libevent_path)
