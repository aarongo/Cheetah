#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import psutil
import argparse
import sys
import subprocess

# 获取 Memcached 程序 pid~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def process_id():
    pid = {}  # 存放获取到的进程 ID 服务端口
    for proc in psutil.process_iter():  # 迭代正在运行的运行的进程,进行排序
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])  # 获取返回字符串的指定字段
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo.get('name') == 'memcached':  # 通过字典获取指定的名称的进程
                pid[pinfo.get('cmdline')[-1]] = pinfo.get('pid')  # 将端口号与相应的进程 ID 关联存放到 pid{}
    return pid


# 选择停止单个或者全部端口~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def select_stop(parameter):
    if bool(process_id()):  # 判断 pid 字典是否为空
        try:  # 判断输入的是否为数字
            int(parameter.port)
            if parameter.port in process_id().keys():
                print "\033[32m选择的端口为:%s" % parameter.port + "\n" + "\033[32m该端口的 PID:%s\033[0m" % process_id()[
                    parameter.port]
                print "\033[31mStoping Memcached %s\033[0m" % parameter.port
                process = psutil.Process(process_id()[parameter.port])  # 实例化该 PID 进程
                process.terminate()  # 停止该 pid 所指进程
                try:  # 判断停止是否成功
                    process_id()[parameter.port]
                except KeyError:
                    print "\033[32mStop Memcached %s Sucessful\033[0m" % parameter.port + "!" * 20
            else:
                print "\033[31m输入的端口不存在\033[0m" + "!" * 20
        except ValueError, err:
            if parameter.port == 'all':  # 当不输入数字是否于此相等
                print "\033[32mStop All Memcached Process\033[0m" + "!" * 20
                for key in process_id().keys():
                    process = psutil.Process(process_id()[key])  # 实例化该 PID 进程
                    process.terminate()
                    print "\033[32mStop Memcached %s Sucessful\033[0m" % key + "!" * 20  # 选择启动单个端口~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            else:
                print "\033[Please Input Number Port\033[0m" + "!" * 20
    else:
        print "\033[31mNo Process Started\033[0m"


# 选择启动单个或者多个端口~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def select_start(parameter):
    """
    启动方法简介:
     首先判断 -P 参数的类型
        try 是数字
            输入的参数存不存在已经启动的进程中
                if 不在已启动中,进行启动
        except 不是数字
            是否 等于 'all'    #全部启动11211-11215
                判断进程时候存在 如果存在 不进行启动 如果不存在 进行启动
    """
    # 获取参数
    port = parameter.port
    user = parameter.user
    memcached_home = "/software/memcached"  # 定义 Memcached_home目录
    try:
        int(port)
        if port in process_id().keys():
            print "\033[32mThis Port Is Started\033[0m"
        else:
            start_memcached = "%smemcached -c 512 -d -u %s -m 512 -p %s" % (memcached_home, user, port)
            code = subprocess.Popen(start_memcached, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, sherr = code.communicate()
            if code.returncode != 0:
                print "\033[31mStart Memcached Ok\033[0m" + "!" * 20
                print sherr
            else:
                print "\033[32mStart Memcached Ok Port:%s\033[0m" % port + "!" * 20
    except ValueError, err:
        if port == 'all':
            if bool(process_id()):
                print "\033[32mAll Port Is Started\033[0m"
            else:
                print "\033[32mStart Memcached All Port [11211-11215]\033[0m"
                port_list = ['11211', '11212', '11213', '11214', '11215']
                for i in port_list:
                    start_memcached = "%smemcached -c 512 -d -u %s -m 512 -p %s" % (memcached_home, user, i)
                    code = subprocess.Popen(start_memcached, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    out, err = code.communicate()
                    if code.returncode != 0:
                        print "\033[31mStart Memcached Failed\033[0m" + "!" * 20
                        print err
                    else:
                        print "\033[32mStart Memcached %s Ok\033[0m" % i + "!" * 20
        else:
            print "\033[31mPlease Input Number EG: -P 123456\033[0m" + "!" * 20


# 获取单个进程或者多个进程状态~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def select_status(parameter):
    if str(parameter.port) in process_id().keys():
        print "\033[32mMemcached的端口为:%s\033[0m" % str(
                parameter.port) + "\n" + "*" * 20 + "\n" + "\033[32mMemcached端口的 PID:%s\033[0m" % \
                                                           process_id()[str(parameter.port)]
    elif str(parameter.port) == 'all':
        for s in process_id().keys():
            print "-" * 40
            print "\033[32mMemcached的端口为:%s\033[0m" % s + "\t" + "\033[32mMemcached端口的 PID:%s\033[0m" % process_id()[s]
    else:
        print "\033[32mMemcached端口为%s 不存在\033[0m" % str(parameter.port)


def check_arg(self, args=None):
    parser = argparse.ArgumentParser(description='Script to learn basic argparse')
    parser.add_argument('-P', '--port', help="Memcached Port Or 'all' start[11211-11215]", required='True')
    parser.add_argument('-u', '--user', help='User Name', default='root')
    parser.add_argument('-t', '--action', help='Action start|stop|status', default='status')

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


if __name__ == '__main__':
    args = check_arg(sys.argv[1:])  # 获取到去除脚本本身的所有参数
    if args.action == 'status':
        select_status(args)
    elif args.action == 'start':
        select_start(args)
    elif args.action == 'stop':
        select_stop(args)
