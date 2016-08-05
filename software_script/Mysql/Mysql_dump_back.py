#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@author: Edward.Liu
@contact: lonnyliu@126.com
@software: PyCharm
@file: Mysql_dump_back.py
@time: 16/8/1
"""

import subprocess
import datetime
import os
import sys

# Mysql Connection Info
DB_Host = "10.171.1.1"
DB_User = "root"
DB_Password = "jlfmysql"
DB_Name = "cybershop"
# Mysql Bin Pach Info
Mysql_bin_home = "/software/carrefour_mysql/bin"
# Time
now = datetime.datetime.now().strftime('%Y-%b-%d_%H')
# Mysql Backup Path
Mysql_backup_path = "/software/mysql_every_backup"
backup_laste_files = "%s/%s_%s.sql.gz" % (Mysql_backup_path, DB_Name, now)
# backup server
backup_server = "10.171.35.16"
backup_path = "/software/mysql_bakcup_files"


def Mysql_Backup():
    backup_command = "%s/mysqldump -h %s -u%s -p%s %s | gzip -9 > %s" % (
        Mysql_bin_home, DB_Host, DB_User, DB_Password, DB_Name, backup_laste_files)
    backup_run = subprocess.Popen(backup_command, shell=True)
    backup_run.wait()

    if os.path.exists(backup_laste_files):
        print "\033[32mMsyql Backup Successful!!!\033[0m"
    else:
        sys.exit(1)


def Transfer_Backup_Files():
    transfer_files = "scp %s %s:%s" % (backup_laste_files, backup_server, backup_path)
    transfer_run = subprocess.Popen(transfer_files, shell=True)
    transfer_run.wait()
    remove_local_backup_files = "rm -rf %s" % backup_laste_files
    remove_run = subprocess.Popen(remove_local_backup_files, shell=True)
    remove_run.wait()


def main():
    Mysql_Backup()
    Transfer_Backup_Files()


if __name__ == '__main__':
    main()
