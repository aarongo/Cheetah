#!/bin/bash
#对比当前时间与月底的时间是否相等,来清除上一个月的数据
#YM 年月
#cal $ym|xargs|awk '{print $NF}' 月底时间

YM=`date +%m" "%Y`
last_M=`cal $ym|xargs|awk '{print $NF}'`
Now=`date +%d`
if [ ${Now} = ${last_M} ]; then
	/bin/find /software/mysqldata  -type f -mtime +${last_M} -exec rm -rf {} \;
else
	echo ${YM} ${last_M} ${Now}
fi