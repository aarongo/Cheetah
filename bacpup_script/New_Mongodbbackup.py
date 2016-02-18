#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


"""
    mongodbbackup script Rewrite

    1.首先在 Mongodb服务器进行 mongodb 的数据备份
    2.将备份文件进行打包
    3.将 tar 包文件传送到远端服务器
    4.脚本以选项的方式进行
        例如: ./mongodbbackup.py -H <ipaddress>
"""


import paramiko
import argparse
import sys
import subprocess
import os
import datetime
import tarfile
import shutil


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


class MongodbBackup(object):
    # ----------------------------------------------------------------------------
    def local_backup(self, tarfile_name, Now, mongodb_DB_Name):
        ### Set Mongodb Info---------
        mongodb_Host = 'localhost'
        mongodb_Port = 27017
        mongodb_Bin_Home = '/install/mongodb/bin/mongodump'
        mongodb_Back_Dir = '/software/mongodb_back'
        mongodb_Backup_Command = "%s -h %s:%s -d %s -o %s > /dev/null" % (
            mongodb_Bin_Home, mongodb_Host, mongodb_Port, mongodb_DB_Name, mongodb_Back_Dir)
        ### Set Mongodb Info ---->End

        ### Start Backup Mongodb
        if os.path.exists(mongodb_Back_Dir):
            print "\033[32m***********String Mongodb Backing************\033[0m"
            mongodb_Backup_Start = subprocess.Popen(mongodb_Backup_Command, shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
            mongodb_Backup_Start.wait()
            if mongodb_Backup_Start.returncode == 0:
                print "\033[32m*****Mongodb Backup OK!!!*****\033[0m"
            else:
                print "\033[31m*****Mongodb Backup Failed!!!!!*****\033[0m"
        else:
            os.mkdir(mongodb_Back_Dir)
            print "\033[32m***********String Mongodb Backing************\033[0m"
            mongodb_Backup_Start = subprocess.Popen(mongodb_Backup_Command, shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
            mongodb_Backup_Start.wait()
            if mongodb_Backup_Start.returncode == 0:
                print "\033[32m*****Mongodb Backup OK!!!*****\033[0m"
            else:
                print "\033[31m*****Mongodb Backup Failed!!!!!*****\033[0m"
        ### Backup Mongodb --->End

        ### Start Package Mongodb Files
        os.chdir(mongodb_Back_Dir)
        tar = tarfile.open(tarfile_name, "w:gz")
        tar.add(mongodb_DB_Name)
        tar.close()
        if os.path.exists(tarfile_name):
            print "\033[32m..........Packaging Is SuccessFul!!!\033[0m"
        else:
            print "\033[32m..........Packaging Is Failed!!!\033[0m"
            ### Package Mongodb -->End


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mongodb Backup Rewrite')
    parser.add_argument('-H', '--Host', help="Send backupfiles Host IP", required='True')
    parser.add_argument('-u', '--user', help='Remote Host User', default='root')
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
    ### Set Use Info
    mongodb_DB_Name = 'ceshi'
    Now = datetime.datetime.now().strftime('%Y-%m-%d-%H')
    backup_file_name = "Mongodb-%s-%s.tar.gz" % (mongodb_DB_Name, Now)
    password = "RPBqoTbJyuhaHVRrc#RX23ox="

    LocalBackupFiles = "/software/mongodb_back/%s" % backup_file_name
    Remote_Backup_Path = "/home/general/depository/mongodbbackup_files/%s" % backup_file_name
    ### Set Use -->End
    M_Backup = MongodbBackup()
    M_Backup.local_backup(backup_file_name, Now, mongodb_DB_Name)
    args = parser.parse_args()
    print "\033[31mSend Backup Files To Remote Server\033[0m"
    ssh = SSHConnection(args.Host, args.user, password)
    ssh.put(local_path=LocalBackupFiles, remote_path=Remote_Backup_Path)
    ssh.close()
    ### Empty LocalBackup directory
    shutil.rmtree('/software/mongodb_back')
    ### Empty LocalBackup -->End
