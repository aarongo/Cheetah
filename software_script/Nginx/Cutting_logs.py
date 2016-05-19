#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

import shutil, os, subprocess
from datetime import datetime, timedelta


# 1.创建文件夹(按月)
# 2.切割日志
# 3.重新打开日志文件
# 4.删除一个月之前的文件


class Nginx_Log_Cutting(object):
    def __init__(self):
        self.save_path = "/software/nginx_logs"
        self.cut_path = "%s" % self.save_path + '/' + '%s' % datetime.today().strftime("%Y%m")
        self.soure_path = "/install/nginx/logs/172.31.0.253_access.log"
        self.dist_path = "%s" % self.cut_path + "/" + "%s" % (datetime.now() - timedelta(days=1)).strftime(
                "%Y-%m-%d") + "-" + "access.log"
        self.nginx_pid = "/install/nginx/logs/nginx.pid"
        self.again_nginx = "kill -s USR1 `cat %s`" % self.nginx_pid

    # ---------------1----------------
    def create_dir(self):
        if os.path.exists(self.save_path):
            os.chdir(self.save_path)
            if not os.path.exists(self.cut_path):
                os.makedirs(self.cut_path)

        else:
            os.makedirs(self.save_path)
            os.chdir(self.save_path)
            os.makedirs(self.cut_path)

    # ---------------2-----------------
    def cutting_log(self):
        shutil.move(self.soure_path, self.dist_path)

    # ----------------3------------------
    def again(self):
        subprocess.call(self.again_nginx, shell=True)

    def main(self):
        self.create_dir()
        self.cutting_log()
        self.again()


if __name__ == '__main__':
    cutting = Nginx_Log_Cutting()
    cutting.main()
