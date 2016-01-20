#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/12/15'
#   motto:  'Good memory as bad written'

import os
import sys
import time


#删除文件-----------------------------------------------------------------
def remove(path):
    """
    Remove the file or directory
    """
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except OSError:
            print "Unable to remove folder: %s" % path
    else:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            print "Unable to remove file: %s" % path


# 遍历输入的文件夹,查询出number_of_days天前的文件,进行删除---------------------
def cleanup(number_of_days, path):
    """
    Removes files from the passed in path that are older than or equal
    to the number_of_days
    """
    time_in_secs = time.time() - (number_of_days * 24 * 60 * 60)
    """
    计算出当前时间与number_of_days天前的毫秒差
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)

            if stat.st_mtime <= time_in_secs:
                remove(full_path)

        if not os.listdir(root):
            remove(root)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    #sys.argv[1]天数 sys.argv[2]要遍历的目录
    days, path = int(sys.argv[1]), sys.argv[2]
    cleanup(days, path)
