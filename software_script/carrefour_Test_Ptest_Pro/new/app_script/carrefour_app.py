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
import contextlib
import zipfile
import httplib
import socket


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Tomcat(object):
    def __init__(self):
        self.tomcat_exe = "tomcat_" + "app"
        self.Tomcat_Home = "/software/%s" % self.tomcat_exe
        self.Tomcat_Log_Home = "/software/%s/logs" % self.tomcat_exe
        self.counnt = 10
        # deploy options
        self.timeStr = time.strftime("%Y-%m-%d-%H:%M")
        self.source_files = "/software/cybershop-mobile-0.0.1-SNAPSHOT.war"
        self.dest_dir = "/software/upload_project/%s-%s" % (
            self.timeStr, self.source_files.split('/')[2].split('.war')[0])
        self.dest_deploy_dir = "/software/deploy_app/%s" % self.source_files.split('/')[2].split('.war')[0]
        self.images_Home = "/software/picture_upload"
        self.static_assets = "%s/assets" % self.dest_dir
        self.static_images_lins = "%s/assets/upload" % self.dest_dir
        # deploy options --->end

    # Get Tomcat_PID~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_tomcat_pid(self):
        # 自定义获取程序 pid 与启动命令
        p = subprocess.Popen(['ps', '-Ao', 'pid,command'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'java' in line:
                if self.tomcat_exe in line:
                    pid = int(line.split(None, 1)[0])
                    return pid
                    # 获取 END

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

    # Unzip Project_name~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def unzip(self):
        ret = 0
        try:
            with contextlib.closing(zipfile.ZipFile(self.source_files)) as zf:
                if not os.path.exists(self.dest_dir):
                    print "\033[32mPath %s Is Not Exists Creating\033[0m" % self.dest_dir
                    os.makedirs(self.dest_dir)
                    zf.extractall(self.dest_dir)
                    ret = 2

        except IOError:
            print "\033[31m%s Is Not Exists Please send Files\033[0m" % self.source_files
        return ret

    # Create Soft Links
    def soft_link(self):
        if os.path.islink(self.dest_deploy_dir):
            os.unlink(self.dest_deploy_dir)
            print "\033[32mCreating Static Files/Images Link\033[0m "
            if os.path.exists(self.static_assets):
                os.symlink(self.images_Home, self.static_images_lins)
            else:
                os.makedirs(self.static_assets)
                os.symlink(self.images_Home, self.static_images_lins)
            os.symlink(self.dest_dir, self.dest_deploy_dir)
        else:
            print "\033[32mCreating Static Files/Images Link\033[0m "
            if os.path.exists(self.static_assets):
                os.symlink(self.images_Home, self.static_images_lins)
            else:
                os.makedirs(self.static_assets)
                os.symlink(self.images_Home, self.static_images_lins)
            os.symlink(self.dest_dir, self.dest_deploy_dir)

    def get_status_code(self, host, path="/"):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path)
            return conn.getresponse().status

        except StandardError:
            return None

    def get_ago(self):
        os.chdir("/software/")
        if os.path.islink(self.dest_deploy_dir):
            real_path = os.readlink(self.dest_deploy_dir)
            f = open('Last_time.txt', 'w')
            f.write(real_path)
            f.close()

    def rollback(self):
        try:
            os.chdir("/software/")
            reover = open('Last_time.txt', 'r')
            old_path = reover.readline()
            reover.close()
            # 删除已经存在的项目链接,还原上一次部署
            if os.path.islink(self.dest_deploy_dir):
                os.unlink(self.dest_deploy_dir)
                os.symlink(old_path, self.dest_deploy_dir)
            else:
                print "\033[31mPlease Deploy Prodect\033[0m"
                # 删除软连接---> end 回退---> end
        except IOError:
            pass

    def check_arg(self, args=None):
        parser = argparse.ArgumentParser(
                description="~~~~~~~~~~~~~~~ 此脚本部署 carrefour-app-pro(生成环境部署)"
                            "EG: '%(prog)s'  -d start|stop|restart|status|log|deploy")
        # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        parser.add_argument('-d', '--handle', default='log',
                            help='Input One of the {start|stop|status|restart|log|deploy}')  # nargs='?' 有一个货没有参数都可以
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

        if len(sys.argv) <= 2:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)


if __name__ == '__main__':
    print "Web Ipadress Is:%s" % socket.gethostbyname(socket.gethostname())
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
        elif args.handle == 'deploy':
            Handle.get_ago()
            Handle.stop_tomcat()
            if Handle.unzip() != 0:
                Handle.soft_link()
            Handle.start_tomcat()
            print "\033[31mWaiting app Started SuccessFul!!!.......\033[0m"
            
        elif args.handle == 'status':
            if Handle.get_tomcat_pid() is not None:
                ipaddress_port = socket.gethostbyname(socket.gethostname()) + ":80"
                app_return_code = Handle.get_status_code(host=ipaddress_port, path='/mobile/api/user/login')
                print "#" * 40
                print "\033[32m %s Is Running is PID:\033[0m" % Handle.tomcat_exe + "\033[31m %s \033[0m" % Handle.get_tomcat_pid()
                if app_return_code == 200:
                    print "\033[32m %s Process Is Exist Service Is available Return Code:\033[0m" % Handle.tomcat_exe + "\033[31m%s\033[0m" % app_return_code + "\033[32mCheck URL:http://%s/mobile/api/user/login\033[0m" % ipaddress_port
                else:
                    print "\033[32mProcess Is Exist Service Is Not available\033[0m"
                print "#" * 40
            else:
                print "#" * 40
                print "\033[32m %s Not Running Or Not Exist \033[0m" % Handle.tomcat_exe
                print "#" * 40
        elif args.handle == 'rollback':
            print "\033[31mRollback last deployment\033[0m" + "....."
            Handle.stop_tomcat()
            Handle.rollback()
            Handle.start_tomcat()
            print "\033[32mWaiting Process Start\033[0m"
            while True:
                ipaddress_port = socket.gethostbyname(socket.gethostname()) + ":80"
                app_return_code = Handle.get_status_code(host=ipaddress_port, path='/mobile/api/user/login')
                if app_return_code == 200:
                    print "\033[32m %s Process Is Exist Service Is available Return Code:\033[0m" % Handle.tomcat_exe + "\033[31m%s\033[0m" % app_return_code + "\033[32mRollback Last Deployment SuccessFul\033[0m"
                    break
        else:
            print "\033[31mYou Input parameter Is Not Exist\033[0m"
    except TypeError:
        args.print_help()
