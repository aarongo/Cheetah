#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com



import json


def ip_list():
    aa = {
        "AA": {
            "hosts": ['192.168.0.41']
        }
    }
    return json.dumps(aa)


ip_list()
