#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


# Import libary~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import subprocess
import time
import sys
import signal
import os
import argparse
import httplib
import socket
import fcntl
import struct


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Tomcat(object):
    def __init__(self):
        self.tomcat_exe = "tomcat_" + "solr"
        self.Tomcat_Home = "/software/%s" % self.tomcat_exe
        self.Tomcat_Log_Home = "/software/%s/logs" % self.tomcat_exe
        self.counnt = 10
        # deploy options
        self.timeStr = time.strftime("%Y-%m-%d-%H:%M")
        # deploy options --->end

    # Get HostName IPaddress
    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    # Get Tomcat_PID~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_tomcat_pid(self):
        p = subprocess.Popen(['ps', '-Ao', 'pid,command'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'java' in line:
                if self.tomcat_exe in line:
                    pid = int(line.split(None, 1)[0])
                    return pid

    # Start Tomcat Process~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start_tomcat(self):
        os.environ["JAVA_HOME"] = "/software/jdk1.7.0_51"
        os.environ["JRE_HOME"] = "/software/jdk1.7.0_51/jre"
        if self.get_tomcat_pid() is not None:
            print "#" * 40
            print "\033[32m %s Is Started \033[0m" % self.tomcat_exe
            print "#" * 40
        else:
            # Start Tomcat
            command_start_tomcat = "%s/bin/startup.sh" % self.Tomcat_Home
            p = subprocess.Popen(command_start_tomcat, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            print stdout, stderr

    # Stop Tomcat process~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def stop_tomcat(self):
        wait_sleep = 0
        if self.get_tomcat_pid() is None:
            print "#" * 40
            print "\033[32m %s is Not Running\033[0m" % self.tomcat_exe + "~" * 20
            print "#" * 40
        else:
            command_stop_tomcat = "%s/bin/shutdown.sh" % self.Tomcat_Home
            p = subprocess.Popen(command_stop_tomcat, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            while (self.get_tomcat_pid() is not None):
                print "waiting for processes to exit\n"
                wait_sleep += 1
                time.sleep(1)
                if wait_sleep == self.counnt:
                    os.kill(self.get_tomcat_pid(), signal.SIGKILL)
                    print "\033[32m Stop Tomcat is sucessful \033[0m"
                    break

    # View TomcatLogs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def tomcat_log(self):
        command_tomcat_log = "tail -f %s/catalina.out " % self.Tomcat_Log_Home
        p = subprocess.Popen(command_tomcat_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        returncode = p.poll()
        try:
            while returncode is None:
                line = p.stdout.readline()
                returncode = p.poll()
                line = line.strip()
                print line
            print returncode
        except KeyboardInterrupt:
            print 'ctrl+d or z'

    def get_status_code(self, host, path="/"):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path)
            return conn.getresponse().status

        except StandardError:
            return None

    def check_arg(self, args=None):
        parser = argparse.ArgumentParser(
            description="EG: '%(prog)s'  -d start|stop|restart|status|log")
        # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        parser.add_argument('-d', '--handle', default='log',
                            help='Input One of the {start|stop|status|restart|log}')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

        if len(sys.argv) <= 2:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)


if __name__ == '__main__':
    print "\033[31mSolr Ipadress Is:%s\033[0m" % socket.gethostbyname(socket.gethostname())
    args = Tomcat().check_arg(sys.argv[1:])
    Handle = Tomcat()
    try:
        if args.handle == 'log':
            Handle.tomcat_log()
        elif args.handle == 'start':
            Handle.start_tomcat()
        elif args.handle == 'stop':
            Handle.stop_tomcat()
        elif args.handle == 'restart':
            Handle.stop_tomcat()
            time.sleep(5)
            Handle.start_tomcat()
        elif args.handle == 'status':
            if Handle.get_tomcat_pid() is not None:
                ipaddress_port = Handle.get_ip_address('eth1') + ":80"
                front_return_code = Handle.get_status_code(host=ipaddress_port, path='/solr')
                print "#" * 40
                print "\033[32m %s Is Running is PID:\033[0m" % Handle.tomcat_exe + "\033[31m %s \033[0m" % Handle.get_tomcat_pid()
                if front_return_code == 200:
                    print "\033[32m %s Process Is Exist Service Is available Return Code:\033[0m" % Handle.tomcat_exe + "\033[31m%s\033[0m" % front_return_code + "\033[32mCheck URL:http://%s/solr\033[0m" % ipaddress_port
                else:
                    print "\033[32mProcess Is Exist Service Is Not available\033[0m"
                print "#" * 40
            else:
                print "#" * 40
                print "\033[32m %s Not Running Or Not Exist \033[0m" % Handle.tomcat_exe
                print "#" * 40
        else:
            print "\033[31mYou Input parameter Is Not Exist\033[0m"
    except TypeError:
        args.print_help()
