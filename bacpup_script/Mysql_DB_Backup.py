#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


"""
Python Backup Mysql Database

1.Start Local Backup Mysql Database
2.Handle Local Backup Mysql Database(tar)
3.Send Mysql Backup Mysql Database Files To Remote Server
4.Other Mysql Backup way Remote Server Run mysqldump -uuser -ppassword -h Mysql_Host DATABASES  > Bckup_PATH/***.sql
5.-H Specify a remote mysql server (此选项可以实现在远端备份 mysql 服务器)
"""

import paramiko
import time
import subprocess
import os
import tarfile
import sys
import argparse
import shutil


class Backup_DB(object):
    ### Start Backup Localhost Databases
    def local_DB(self, DB_NAME, DB_BACK_PATH, DB_BACKUP_FILES):
        DB_USER = 'root'
        DB_PASSWD = 'comall2014'
        DB_DUMP_BIN_HOME = '/usr/bin/mysqldump'
        DB_Back_Command = '%s -u%s -p%s %s > %s/%s' % (
            DB_DUMP_BIN_HOME, DB_USER, DB_PASSWD, DB_NAME, DB_BACK_PATH, DB_BACKUP_FILES)
        if not os.path.exists(DB_BACK_PATH):
            os.mkdir(DB_BACK_PATH)
            print "\033[31mStarting Mysql Backup..........\033[0m"
            Dump = subprocess.Popen(DB_Back_Command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            Dump.wait()
            if Dump.returncode != 0:
                print "\033[31mMysql Backup Is OK!!!\033[0m"

    ### DB_Files Handle Backup --->start
    def DB_File_Handle(self, DB_BACKUP_FILES, DB_BACK_PATH, tarfile_name):
        print "\033[31mPackaging Backup Files.........\033[0m"
        os.chdir(DB_BACK_PATH)
        tar = tarfile.open(tarfile_name, "w:gz")
        tar.add(DB_BACKUP_FILES)
        tar.close()
        if os.path.exists(tarfile_name):
            print "\033[32mPackaging Is SuccessFul!!!\033[0m"
        else:
            print "\033[32mPackaging Is Failed!!!\033[0m"
            ### DB_Files Handle  -->End


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mongodb Backup Rewrite')
    parser.add_argument('-H', '--Host', help="Send backupfiles Host IP(发送备份文件到远程服务器地址)", required='True')
    parser.add_argument('-u', '--user', help='Remote Host User', default='root')
    parser.add_argument('-S', '--database', help="Designation Mysql Database", required='True')
    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    ### Set Up Public_par
    DB_NAME = args.database
    DB_BACK_PATH = '/software/DB_Back'
    DATETIME = time.strftime("%Y-%m-%d~%H")
    DB_back_files = '%s-%s.sql' % (DB_NAME, DATETIME)
    DB_Back_tar = '%s-%s.tar.gz' % (DATETIME, DB_NAME)
    #### Send Backup Files To Remote Host par
    Remote_Host = args.Host
    Remote_User = args.user
    Remote_password = 'RPBqoTbJyuhaHVRrc#RX23ox='

    LocalBackupFiles = "%s/%s" % (DB_BACK_PATH, DB_Back_tar)
    Remote_Backup_Path = "/home/general/depository/Mysql_Backup/%s" % DB_Back_tar
    ### Set Remote --->End


    ### Set Up Public_par --->End

    Mysql = Backup_DB()
    Mysql.local_DB(DB_NAME=args.database, DB_BACK_PATH=DB_BACK_PATH,
                   DB_BACKUP_FILES=DB_back_files)
    Mysql.DB_File_Handle(DB_BACKUP_FILES=DB_back_files, DB_BACK_PATH=DB_BACK_PATH, tarfile_name=DB_Back_tar)
    Remote = SSHConnection(args.Host, args.user, Remote_password)
    Remote.put(local_path=LocalBackupFiles, remote_path=Remote_Backup_Path)
    Remote.close()
    ### Delete Mysql BackupFiles
    shutil.rmtree(DB_BACK_PATH)
    ### Delete Mysql BackupFiles --->End
