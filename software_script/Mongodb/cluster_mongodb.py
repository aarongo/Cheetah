#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

import argparse, sys
import subprocess


def check_arg(self, args=None):
    parser = argparse.ArgumentParser(
            description="Mongodb Start|stop|status"
                        "EG: '%(prog)s' -C (Cluster Name) -t start|stop|restart|status")
    # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    parser.add_argument('-C', '--Cluster', default='master', choices=['master', 'slaver', 'arbiter'],
                        help='Input One of the master|slaver|arbiter')
    parser.add_argument('-t', '--action', default='status', choices=['start', 'stop', 'status', 'restart'],
                        help='Input One of the Action start|stop|status|restart')

    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args)


def mongodb_handle(cluster, action):
    mongodb_command = '/software/script/mongodb_action.py -C %s -t %s' % (cluster, action)
    remote_host = {
        'master': '10.171.35.8',
        'slaver': '10.171.35.9',
        'arbiter': '10.171.35.10',
    }
    if cluster in remote_host.keys():
        run_command = "ssh %s %s" % (remote_host.get(cluster), mongodb_command)
        p_mongodb = subprocess.Popen(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        mongod_stdout, mongodb_stderr = p_mongodb.communicate()
        print mongod_stdout
    else:
        print "Exist Not Host"


if __name__ == '__main__':
    args = check_arg(sys.argv[1:])
    mongodb_handle(args.Cluster, args.action)
