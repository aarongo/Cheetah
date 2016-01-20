#!/usr/bin/python
# _*_coding:utf-8_*_


"""           15-9-21
          author : 'yulong'
    Good memory than rotten written
"""

import subprocess
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d")
images_dir = "/install/dockerimages"
back_dir = "/install/backup/carrefour_tset_images_back/"
command = "cd %s && mkdir %s && cp -r %s/* %s%s" % (back_dir, now, images_dir, back_dir, now)
back = subprocess.Popen(command, shell=True)
back.wait()
if back.returncode == 0:
    print "备份完成"
else:
    print "备份失败"