#!/usr/bin/env bash
# Author: Edward.Liu
# Author-Email: lonnyliu@126.com


#Set Global Parameters
proxy_user=ecommerce_china
proxy_password=xK8-4=gF
download_url=http://182.50.117.44:8081/
source_war_path=/software
source_war_files="cybershop-web-0.0.1-SNAPSHOT.war"
handle="$1"
#定义 web_Front 服务器 IP 数组
web_address_list=(10.171.112.1 10.171.112.2)
#set GLobal Parameters End


remote_handle(){
    #获取数组的值和下角标,下角标+1 做为 节点名称,根据下角标获取 IP 地址 做并发处理& 等待 do 里边的都完成后执行后边的 command
    for address in "${!web_address_list[@]}";
    do
    {
        printf "copying ${Files_Name} To %s\t%s\n" "web$[address+1]" "${web_address_list[${address}]}.........."
        scp ${source_war_path}/${source_war_files} ${web_address_list[${address}]}:${source_war_path}
        printf "\e[31mCopy Files Overed!!!\n\e[0m"
        printf "\e[31mHandle Remote %s\t%s\n\e[0m" "web$[address+1]"
        ssh  ${web_address_list[${address}]} "/software/script/carrefour_web.py -d ${handle}"
        if [ $? -ne 0 ]; then
            printf "\e[31mHandle ${handle} Is Failed\n\e[0m"
        else
            printf "\e[31mHandle ${handle} Is OK!!!\n\e[0m"
        fi
    }&
    wait
    done
}
tomcat_status(){
    for address in "${!web_address_list[@]}";
    do
    {
            ssh -tt ${web_address_list[${address}]} "/software/script/carrefour_web.py -d ${handle}"
    }&
    wait
    done
}
case ${handle} in
    deploy)
        remote_handle;
        ;;
    status)
        tomcat_status;
        ;;
   *)
      echo "`basename ${0}`:usage: deploy|status"
      exit 1 # Command to come out of the program with status 1
      ;;
esac

