#!/usr/bin/env bash
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


# check carrefour access url

echo -e "\033[32m开始测试URL可访问性\033[0m"
for line in $(cat url_list.txt)
    do
        code=`curl -I -m 10 -o /dev/null -s -w %{http_code} ${line}`
        printf "URL=${line}---->状态码为:${code}\n"
    done
