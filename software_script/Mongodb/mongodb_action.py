#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import subprocess
import argparse, sys, os
import signal, time


def check_arg(self, args=None):
    parser = argparse.ArgumentParser(
            description="Mongodb Start|stop|status"
                        "EG: '%(prog)s' -C (Cluster Name) -t start|stop|restart|status")
    # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    parser.add_argument('-C', '--Cluster', default='master',
                        help='Input One of the Cluster Node Name')
    parser.add_argument('-t', '--action', default='status', help='Input One of the Action')

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def get_mongodb_pid(cluster_node):
    p = subprocess.Popen(['ps', '-Ao', 'pid,command'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if "%s.conf" % cluster_node in line:
            pid = int(line.split(None, 1)[0])
            return pid


def get_mongodb_ip():
    get_ip_command = """ifconfig  | grep "inet addr" | awk '{print $2}' | sed -n '2p' | awk -F ':' '{print $2}'"""
    mongodb_ip = subprocess.Popen(get_ip_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = mongodb_ip.communicate()
    return stdout


def start_mongodb(cluster):
    if get_mongodb_pid(cluster) is None:
        mongodb_bin_home = "/software/mongodb_bin/bin"
        mongodb_config_path = "/software/Mongodb/data/%s/config/%s.conf" % (cluster, cluster)
        start_mongod_command = "%s/mongod" % mongodb_bin_home + " " + "-f" + " " + "%s" % mongodb_config_path
        p_mongodb = subprocess.Popen(start_mongod_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        mongod_stdout, mongodb_stderr = p_mongodb.communicate()
        if get_mongodb_pid(cluster) is None:
            print "\033[31mMongodb %s(%s) Start Failed!!!\033[0m" % (cluster, get_mongodb_ip())
        else:
            print "\033[32mMongodb %s(%s) Start SuccessFul!!!\033[0m" % (
                cluster, get_mongodb_ip()) + "\t" + "\033[31mPID IS:%s\033[0m" % get_mongodb_pid(
                    cluster)
    else:
        print "\033[31mMongodb %s(%s) is Started!!!\033[0m" % (cluster, get_mongodb_ip())


def stop_mongodb(cluster):
    mongodb_pid_path = "/software/Mongodb/%s.pid" % cluster
    if get_mongodb_pid(cluster) is not None:
        os.kill(get_mongodb_pid(cluster), signal.SIGKILL)
        os.remove(mongodb_pid_path)
        print "\033[32m Stop Mongodb %s(%s) is sucessful \033[0m" % (cluster, get_mongodb_ip())
    else:
        print "\033[31mMongodb %s(%s) Not Running!!!\033[0m" % (cluster, get_mongodb_ip())


if __name__ == '__main__':
    args = check_arg(sys.argv[1:])
    if args.action == 'status':
        if get_mongodb_pid(args.Cluster) is not None:
            print "\033[32mMongodb %s(%s) Is Running\033[0m" % (
                args.Cluster, get_mongodb_ip()) + "\t" + "\033[31mPID Is:%s\033[0m" % get_mongodb_pid(
                    args.Cluster)
        else:
            print "\033[31mMongodb %s(%s) Is Not Running\033[0m" % (args.Cluster, get_mongodb_ip())
    elif args.action == 'stop':
        stop_mongodb(args.Cluster)
    elif args.action == 'start':
        start_mongodb(args.Cluster)
    elif args.action == 'restart':
        stop_mongodb(args.Cluster)
        time.sleep(5)
        start_mongodb(args.Cluster)
    else:
        args.print_help()
