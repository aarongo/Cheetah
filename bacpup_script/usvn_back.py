#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/11/16'
#   motto:  'Good memory as bad written'

import datetime
import os
import tarfile
import subprocess


# usvn 备份--------------------------------------------------------------
class Usvn_Backend(object):
    # ------------------------------------------------------------------
    def __init__(self):
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H')
        self.Root_Directory = "/software"
        self.back_directory = "usvn"
        self.Remote_Send_Dir = "/install/backup/usvnback"

    # 打包文件------------------------------------------------------------
    def Package(self):
        global tarfile_name
        print "\033[32mWaitIng Packaging..........\033[0m"
        os.chdir(self.Root_Directory)
        tarfile_name = "%s-%s.tar.gz" % (self.back_directory, self.date_time)
        tar = tarfile.open(tarfile_name, "w:gz")
        tar.add(self.back_directory)
        tar.close()
        if os.path.exists(tarfile_name):
            print "\033[32m..........Packaging Is SuccessFul!!!\033[32m"
        else:
            print "\033[32m..........Packaging Is Failed!!!\033[0m"


# 执行远程命令传送文件---------------------------------------------------------
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

        self.session = self.transport.open_channel(kind='session')

    # ----------------------------------------------------------------------
    def _openSFTPConnection(self):
        """
        Opens an SFTP connection if not already open
        """
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True

    # ----------------------------------------------------------------------
    #下载文件时需要指定两端文件名
    def get(self, remote_path, local_path=None):
        """
        Copies a file from the remote host to the local host.
        """
        self._openSFTPConnection()
        self.sftp.get(remote_path, local_path)

    # ----------------------------------------------------------------------
    #传送文件是需要两端都要指定文件名称
    def put(self, local_path, remote_path=None):
        """
        Copies a file from the local host to the remote host
        """
        self._openSFTPConnection()
        self.sftp.put(local_path, remote_path)

    # ----------------------------------------------------------------------
    def run(self, command, nbytes=4096):
        # Run Command out|err
        stdout_data = []
        stderr_data = []
        self.session.exec_command(command)
        while True:
            if self.session.recv_ready():
                stdout_data.append(self.session.recv(nbytes))
            if self.session.recv_stderr_ready():
                stderr_data.append(self.session.recv_stderr(nbytes))
            if self.session.exit_status_ready():
                break
        print "\033[31m*********************\033[0m"
        print '\033[32mExit status is: \033[0m', self.session.recv_exit_status()
        print "\033[31m*********************\033[0m"
        print ''.join(stdout_data)
        print ''.join(stderr_data)

    def close(self):
        """
        Close SFTP connection and ssh connection
        """
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
        self.transport.close()
        self.session.close()


if __name__ == '__main__':
    subprocess.call('clear', shell=True)
    try:
        try:
            import paramiko
        except ImportError:
            print "\033[32mInstalling Paramiko.........\033[0m"
            install_paramiko = "pip install paramiko"
            subprocess.call(install_paramiko, shell=True)
        # Run Usvn Unpack--------------------------------------------------------------
        unpack = Usvn_Backend()
        unpack.Package()
        # Put UsvnBack Files To Remote Server
        Send_Files = SSHConnection("172.31.1.160", "root", "comall2014")
        #Set local_path Names,remote_path Names
        local_path_files = "%s/%s" % (unpack.Root_Directory, tarfile_name)
        remote_path_files = "%s/%s" % (unpack.Remote_Send_Dir, tarfile_name)
        Send_Files.put(local_path_files, remote_path_files)
        #remove tarfiles
        os.chdir(unpack.Root_Directory)
        os.remove(tarfile_name)
        #remove end!!!!
        Send_Files.close()
    except KeyboardInterrupt:
        print "Contorl+C+Z"
