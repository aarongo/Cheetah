##***Process Script***
###***脚本名称***
>	Memcached
>>	action_memcached.py

>	carrefour_test
>>	carrefour_front.py
>>	carrefour_web.py
>>	carrefour_test_deploy.sh

##脚本介绍
###***action_memcached.py***
        脚本执行:python <path>/action_memcached.py -P `port`(port=Number or port='all') -t `start|stop|status`<br>
        脚本介绍:脚本有一个隐藏参数 -u `user` (指定 Memcached 启动时的用户默认是`root` 可以自己指定)<br>
        执行例子 python <path>/action_memcached.py -P 123456 -t start (启动单个端口)<br>
                python <path>/action_memcached.py -P all -t start (启动多个端口默认为[11211-11215])<br>
                python <path>/action_memcached.py -P 123456 -t status (查看单个端口状态)<br>
                python <path>/action_memcached.py -P all -t start (查看所有已启动的端口)<br>
                
###***carrefour_front.py***
```
	python <Path>/carrefour_front.py -d {start|stop|restart|status|log}
	cd <path>	./carrefour_front.py -d {start|stop|restart|status|log}
```
###***carrefur_web.py***
```
	python <Path>/carrefour_web.py -d {start|stop|restart|status|log}
	cd <path> ./carrefour_web.py -d {start|stop|restart|status|log}
```
###***carrefour_test_deploy.sh***
```
bash <Path>/carrefour_test_deploy.sh deploy SVN(版本号)
```