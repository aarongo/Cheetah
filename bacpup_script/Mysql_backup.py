#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Mysql Database Backup Python Script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import time
import subprocess
import paramiko


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 备份数据库的公用方法
class DB_Back(object):
    def __init__(self):
        self.DB_User = 'root'
        self.DB_Passwd = "comall2014"
        self.DB_Name = "cybershop_b2b2c_dev"
        self.DB_Backup_path = "/software/DB_Backup"
        self.DB_Home = "/software/mysql/bin"
        self.DATETIME = time.strftime("%Y-%m-%d~%H")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start_backup(self):
        print "\033[32mWaitting Backuping Databases %s\033[0m" % self.DB_Name
        backup_exec = "%s/mysqldump -u" % self.DB_Home + self.DB_User + " " + "-p" + self.DB_Passwd + " " + self.DB_Name + " > " + self.DB_Backup_path + "/" + self.DATETIME + "~" + self.DB_Name + ".sql"
        subprocess.call(backup_exec, shell=True)
        Generate_Fiels_Path = self.DB_Backup_path + "/" + self.DATETIME + "~" + self.DB_Name + ".sql"
        if os.path.exists(Generate_Fiels_Path):
            print "\033[32mDatabases %s Backup SuccessFull!!!!\033[0m" % self.DB_Name
        else:
            print "\033[31mDatabases %s Backup Failed!!!\033[0m" % self.DB_Name

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def backup(self):

        if os.path.exists(self.DB_Backup_path):
            self.start_backup()
        else:
            os.makedirs(self.DB_Backup_path)
            self.start_backup()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    mysql_back = DB_Back()
    mysql_back.backup()
