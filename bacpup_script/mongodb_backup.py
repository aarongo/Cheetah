#!/usr/bin/python
# _*_coding:utf-8_*_
"""           15-9-18
          author = 'yulong'
    Good memory than rotten written
"""
import datetime
import subprocess
import os
import pexpect


class Mysql_Backup(object):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H")
    delete_day_ago = 5
    mongodb_host = "localhost"  # mongodb主机地址
    mongodb_port = 27017  # mongodb 端口
    mongodb_name = "ceshi"
    mongodbdump_bin_home = "/install/mongodb/bin/mongodump"  # mongodbdump 目录
    local_backup_dir = "/software/mongodb_back"  # 本地备份路径
    remote_user = 'user'  # 远程主机用户
    remote_password = 'password'  # 远程用户密码
    remote_host = 'x.x.x.x'  # 远程主机ip
    remote_backup_dir = "/install/backup/mongodb_backup"  # 远程备份目录
    command = " %s -h %s:%s -d %s -o %s > /dev/null" % (
        mongodbdump_bin_home, mongodb_host, mongodb_port, mongodb_name, local_backup_dir)

    def backup(self):
        ret = -1
        print "\033[32m***********String Mongodb Backing************"
        db_back = subprocess.Popen(self.command, shell=True)
        db_back.wait()
        path = self.local_backup_dir
        if len(os.listdir(path)) == 0:
            print "\033[31m ***************Mongodb Backup Is Failed***************\033[0m"
        else:
            print "\033[32m ***************Mongodb Backup Is Successful***************\033[0m"
            ret = 0
        return ret

    def package(self):
        print "\033[32m##########Mongodb Packaging##########\033[0m"
        command = "cd %s && tar czvf %s-%s.tar.gz %s && rm -rf %s" % (
            self.local_backup_dir, self.now, self.mongodb_name,
            self.mongodb_name, self.mongodb_name)

        subprocess.call(command, shell=True)
        print "\033[32m#####################################\033[0m"

    def send_mongodb_files(self):
        #############################
        # 传送文件到远程,遍历目录下的所有文件赋值给files 之后传送fiels
        for files in os.listdir(self.local_backup_dir):
            scp_command = "scp %s/%s %s@%s:%s" % (
                self.local_backup_dir, files, self.remote_user, self.remote_host, self.remote_backup_dir)
        print "\033[32m**********Running Scp To Remote Server....................\033[0m"
        command_output, exitstatus = pexpect.run(scp_command, events={'(?i)password': 'password\n'}, withexitstatus=1)
        print "\033[32m***************Mongodb BackUp Result***************\033[0m", command_output
        # 判断远程文件是否传送成功
        remote_command = """ssh %s@%s "ls %s/%s" """ % (
            self.remote_user, self.remote_host, self.remote_backup_dir, files)
        '''使用pexpect.run 发送密码的方式 执行远程命令进行判断备份文件是否存在 command_output(命令输出）exitstatus(命令执行状态）
            当命令成功时返回的状态码为0,当Linux exitcode 不是0的时候 exitstatus返回不等于0,即可判断远程文件是否传送成功
        '''
        command_output, exitstatus = pexpect.run(remote_command,
                                                 events={'(?i)password': 'password\n'}, withexitstatus=1)
        if exitstatus == 0:
            command_rm = "rm -rf %s/*" % self.local_backup_dir
            print "\033[32m**********Delete LocalHost Files**********\033[0m"
            subprocess.call(command_rm, shell=True)
            print "\033[32m************************************************\033[0m"
        else:
            print "\033[31m******************Send Files Failed********************\033[0m"

    def days_delete_agos(self):
        # 执行远程命令删除备份机上的5天前的备份(保留5天的备份）此处comall2014需要更改
        command = """ssh %s@%s "cd %s && find . -mtime +%s -exec rm -Rf -- {} \;" """ % (
            self.remote_user, self.remote_host,
            self.remote_backup_dir, self.delete_day_ago)
        command_output, exitstatus = pexpect.run(command,
                                                 events={'(?i)password': 'password\n'}, withexitstatus=1)
        if exitstatus != 0:
            print "\033[32m***************Delete 5 days BackFiles Failed**************\033[0m"
        else:
            print "\033[31m**************Delete 5 Days BackFiles Sucessful OR Don't Exist 5 Days BackFiles*************\033[0m"


if __name__ == "__main__":
    run_start = Mysql_Backup()
    run_start.days_delete_agos()
    if run_start.backup() == 0:
        run_start.package()
        run_start.send_mongodb_files()
