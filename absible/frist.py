#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import inenvtory

import ansible.runner

aa = ansible.runner.Runner(
        module_name='shell',  # 调用shell模块，这个代码是为了示例执行shell命令
        module_args='hostname',  # shell命令
        host_list='inenvtory.py',  # host文件路径，我这调用的是dynamic inventory脚本，
        pattern='AA',  # host组名，需要执行shell命令的ip组，AA是在上面aa.py中定义的
)  # 其它没写的参数，都为是系统默认的
bb = aa.run()
print bb

