#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


"""
    1.远程下载文件到部署机
    2.分发下载后的文件到其他节点,并发形式
    3.分别执行远端脚本,A.stop B.deploy C.status
"""

import argparse, sys, os
import urllib
import paramiko
import subprocess


class Download_War(object):
    def report(self, blocknum, blockSize, totalSize):
        '''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = int(blocknum * blockSize * 100 / totalSize)
        sys.stdout.write("\r%d%%" % percent + ' complete')
        sys.stdout.flush()

    def download(self):
        try:
            stable_url = "http://124.200.96.150:8081/"
            global war_url
            war_url = stable_url + raw_input("\033[32mPlease Input Download Files Names:\033[0m").strip()
            url_code = urllib.urlopen(war_url)
            if url_code.code == 200:
                download_file_name = '/software/%s' % war_url.split('/')[3]
                sys.stdout.write('\rDownloading ' + download_file_name + '...\n')
                urllib.urlretrieve(war_url, download_file_name, reporthook=self.report)
                '''
                urllib.urlretrieve(url[, filename[, reporthook[, data]]])
                参数说明：
                url：外部或者本地url
                filename：指定了保存到本地的路径（如果未指定该参数，urllib会生成一个临时文件来保存数据）；
                reporthook：是一个回调函数，当连接上服务器、以及相应的数据块传输完毕的时候会触发该回调。我们可以利用这个回调函数来显示当前的下载进度。
                data：指post到服务器的数据。该方法返回一个包含两个元素的元组(filename, headers)，filename表示保存到本地的路径，header表示服务器的响应头。
                '''
                sys.stdout.write("\rDownload complete, saved as %s" % (download_file_name) + '\n\n')
                sys.stdout.flush()
            else:
                print "URL IS Not Exists"
                sys.exit()
        except KeyboardInterrupt, err:
            print "control +c"

    def check_arg(self, args=None):
        parser = argparse.ArgumentParser(
                description="Carrefour_Front Start|stop|status|deploy"
                            "EG: '%(prog)s' -t start|stop|restart|status|deploy")
        # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        parser.add_argument('-H', '--host', default='ALL', help='Input Host ipaddress or ALL')
        parser.add_argument('-t', '--action', default='status',
                            choices=['start', 'stop', 'status', 'restart', 'deploy'],
                            help='Input One of the Action start|stop|status|restart|deploy')

        if len(sys.argv) <= 2:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)


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

    # ----------------------------------------------------------------------

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


class Run_Script(object):
    def now_run(self, host, action):
        remote_script_command = "/software/script/carrefour_front.py -d %s" % action
        remote_script_run = "ssh %s %s" % (host, remote_script_command)
        p_run = subprocess.Popen(remote_script_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p_run_stdout, p_run_stderr = p_run.communicate()
        print p_run_stdout


if __name__ == '__main__':
    args = Download_War().check_arg(sys.argv[1:])
    if args.host == 'ALL':
        if args.action == 'deploy':
            # 执行下载到指定位置
            Download_War().download()

            # 分发文件
            for i in range(1, 25):
                ipaddress = '10.171.112.%s' % i
                server_user = 'cdczhangg'
                server_password = '76132fbbe6'
                # 文件路径
                local_path = '/software/%s' % war_url.split('/')[3]
                dst = '/software/%s' % war_url.split('/')[3]
                # 发送文件
                ssh = SSHConnection(ipaddress, server_user, server_password)
                ssh.put(local_path, dst)
                ssh.close()
                Run_Script().now_run(ipaddress, args.action)
        else:
            for i in range(1, 25):
                ipaddress = '10.171.112.%s' % i
                Run_Script().now_run(ipaddress, args.action)
    else:
        ipaddress = args.host
        if args.action != 'deploy':
            Run_Script().now_run(ipaddress, args.action)
        else:
            server_user = 'cdczhangg'
            server_password = '76132fbbe6'
            # 文件路径
            local_path = '/software/%s' % war_url.split('/')[3]
            dst = '/software/%s' % war_url.split('/')[3]
            ssh = SSHConnection(ipaddress, server_user, server_password)
            ssh.put(local_path, dst)
            ssh.close()
            Run_Script().now_run(ipaddress, args.action)
