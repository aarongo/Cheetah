#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
import paramiko
import argparse
import sys


class SSHConnection(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, host, username, password, port=22):
        """Initialize and setup connection"""
        self.sftp = None
        self.sftp_open = False

        # open SSH Transport stream
        self.transport = paramiko.Transport((host, port))

        self.transport.connect(username=username, password=password)

    # ----------------------------------------------------------------------
    def _openSFTPConnection(self):
        """
        Opens an SFTP connection if not already open
        """
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True

    def put(self, local_path, remote_path=None):
        """
        Copies a file from the local host to the remote host
        """
        self._openSFTPConnection()
        self.sftp.put(local_path, remote_path)

    # ----------------------------------------------------------------------
    def close(self):
        """
        Close SFTP connection and ssh connection
        """
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
        self.transport.close()


class Run_Cmd(object):
    def Run(self, hostname, username, password, command, port=22, nbytes=4096):
        client = paramiko.Transport((hostname, port))
        client.connect(username=username, password=password)

        stdout_data = []
        stderr_data = []
        session = client.open_channel(kind='session')
        session.exec_command(command)
        while True:
            if session.recv_ready():
                stdout_data.append(session.recv(nbytes))
            if session.recv_stderr_ready():
                stderr_data.append(session.recv_stderr(nbytes))
            if session.exit_status_ready():
                break

        print 'exit status: ', session.recv_exit_status()
        print ''.join(stdout_data)
        print ''.join(stderr_data)

        session.close()
        client.close()


if __name__ == "__main__":
    username = "cdczhangg"
    pw = "76132fbbe6"
    parser = argparse.ArgumentParser(
            description="eg: '%(prog)s' -h ipaddress -d {front|web}")
    # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    parser.add_argument('-t', '--Handle', action='store', nargs='?', dest='handle', choices=('app', 'weixin'),
                        help='Input One of the {app|weixin}')  # nargs='?' 有一个货没有参数都可以
    parser.add_argument('-d', '--Handle1', action='store', nargs='+', dest='handle1',
                        choices=('log', 'start', 'stop', 'status', 'restart', 'deploy'),
                        help='operating Tomcat log|start|stop|status|restart')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    app_addr_list = ['10.151.254.3', '10.151.254.11']
    weixin_addr_list = ['10.151.254.14', '10.151.254.15']
    if len(sys.argv) <= 3:
        parser.print_help()
    else:
        try:
            remote_script = Run_Cmd()
            if args.handle == 'weixin':
                if args.handle1[0] == 'deploy':
                    source_files = '/software/mobile_war/cybershop-mobile-0.0.1-SNAPSHOT.war'
                    dest_files = '/software/cybershop-mobile-0.0.1-SNAPSHOT.war'
                    command = "/software/script/carrefour_wechat.py -c mobile -d deploy"
                    for ip in weixin_addr_list:
                        print "\033[32mDeploy Weixin Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        send_files = SSHConnection(ip, username, pw)
                        send_files.put(source_files, dest_files)
                        send_files.close()
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'status':
                    command = "/software/script/carrefour_wechat.py -c mobile -d status"
                    for ip in weixin_addr_list:
                        print "\033[32mWeixin Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'start':
                    command = "/software/script/carrefour_wechat.py -c mobile -d start"
                    for ip in weixin_addr_list:
                        print "\033[32mWeixin Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'stop':
                    command = "/software/script/carrefour_wechat.py -c mobile -d stop"
                    for ip in weixin_addr_list:
                        print "\033[32mWeixin Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'restart':
                    command = "/software/script/carrefour_wechat.py -c mobile -d restart"
                    for ip in weixin_addr_list:
                        print "\033[32mWeixin Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
            if args.handle == 'app':
                if args.handle1[0] == 'deploy':
                    source_files = '/software/mobile_war/cybershop-mobile-0.0.1-SNAPSHOT.war'
                    dest_files = '/software/cybershop-mobile-0.0.1-SNAPSHOT.war'
                    command = "/software/script/carrefour_app.py -c mobile -d deploy"
                    for ip in app_addr_list:
                        send_files = SSHConnection(ip, username, pw)
                        send_files.put(source_files, dest_files)
                        send_files.close()
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'status':
                    command = "/software/script/carrefour_app.py -c mobile -d status"
                    for ip in app_addr_list:
                        print "\033[32mAPP Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'start':
                    command = "/software/script/carrefour_app.py -c mobile -d start"
                    for ip in app_addr_list:
                        print "\033[32mAPP Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'stop':
                    command = "/software/script/carrefour_app.py -c mobile -d stop"
                    for ip in app_addr_list:
                        print "\033[32mAPP Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
                if args.handle1[0] == 'restart':
                    command = "/software/script/carrefour_app.py -c mobile -d restart"
                    for ip in app_addr_list:
                        print "\033[32mAPP Ipaddress:\033[0m" + "\033[31m%s\033[0m" % ip
                        remote_script.Run(hostname=ip, username=username, password=pw, command=command)
        except TypeError:
            parser.print_help()
