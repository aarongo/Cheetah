Process Script
====
#脚本名称
- memcached.py <br>
        脚本执行 python <path>/action_memcached.py -P `port`(port=Number or port='all') -t `start|stop|status`
        脚本介绍 **脚本有一个隐藏参数 -u `user` (指定 Memcached 启动时的用户默认是`root` 可以自己指定)
        执行例子 python <path>/action_memcached.py -P 123456 -t start (启动单个端口)
                python <path>/action_memcached.py -P all -t start (启动多个端口默认为[11211-11215])
                                                or
                python <path>/action_memcached.py -P 123456 -t status (查看单个端口状态)
                python <path>/action_memcached.py -P all -t start (查看所有已启动的端口)
                
