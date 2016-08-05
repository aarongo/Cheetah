#!/usr/bin/env bash
# Author: Edward.Liu
# Author-Email: lonnyliu@126.com


#Set Global Parameters
proxy_user=ecommerce_china
proxy_password=xK8-4=gF
download_url=http://182.50.117.44:8081/
source_war_path=/software
source_war_files="cybershop-front-0.0.1-SNAPSHOT.war"
handle="$1"
#定义 web 服务器 IP 数组
web_address_list=(10.171.112.1 10.171.112.2 10.171.112.3 10.171.112.4 10.171.112.5 10.171.112.6
                    10.171.112.7 10.171.112.8 10.171.112.9 10.171.112.10 10.171.112.11 10.171.112.12
                    10.171.112.13 10.171.112.14 10.171.112.15 10.171.112.16 10.171.112.17 10.171.112.18
                    10.171.112.19 10.171.112.20 10.171.112.21 10.171.112.22 10.171.112.23 10.171.112.24)
#set GLobal Parameters End

download_war(){
    #判断 war 是否存在
    cd ${source_war_path}
    if [ -f "${source_war_files}" ]; then
        rm -rf ${source_war_path}/${source_war_files}
        echo -en "\033[32mEnter You DownLoad Files > \033[0m"
        read Files_Name
        echo You Will Download Files:: ${Files_Name}
        sleep 3
        wget --proxy-user=${proxy_user} --proxy-passwd=${proxy_password} ${download_url}${Files_Name} -P ${source_war_path}
    else
        echo -en "\033[32mEnter You DownLoad Files > \033[0m"
        read Files_Name
        echo You Will Download Files:: ${Files_Name}
        sleep 3
        wget --proxy-user=${proxy_user} --proxy-passwd=${proxy_password} ${download_url}${Files_Name} -P ${source_war_path}
    fi

}
handle_files(){
    
    #截取输入的文件后续目录可用
    if [ ! ${Files_Name} ]; then
        echo "\033[31m Files_Name variable Is Null"
    else
        #处理下载后的文件
        printf "\e[32mHanlde Files ${Files_Name}..........\n\e[0m"
        after_tar=${Files_Name%%.*}
        tar xzvf ${source_war_path}/${Files_Name} -C ${source_war_path}
        mv ${source_war_path}/${after_tar}/${source_war_files} ${source_war_path}/
        rm -rf ${source_war_path}/${after_tar} && rm -rf ${source_war_path}/${Files_Name}
        printf "\e[32mHandle Files End.......\n\e[0m"
    fi
    
    #文件处理完毕
}
remote_handle(){
    #获取数组的值和下角标,下角标+1 做为 节点名称,根据下角标获取 IP 地址 做并发处理& 等待 do 里边的都完成后执行后边的 command
    for address in "${!web_address_list[@]}";
    do
    {
        printf "copying ${Files_Name} To %s\t%s\n" "web$[address+1]" "${web_address_list[${address}]}.........."
        scp ${source_war_path}/${source_war_files} ${web_address_list[${address}]}:${source_war_path}
        printf "\e[31mCopy Files Overed!!!\n\e[0m"
        printf "\e[31mHandle Remote %s\t%s\n\e[0m" "web$[address+1]"
        ssh -tt ${web_address_list[${address}]} "/software/script/carrefour_front.py -d ${handle}"
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
            ssh -tt ${web_address_list[${address}]} "/software/script/carrefour_front.py -d ${handle}"
    }&
    wait
    done
}
case ${handle} in
    deploy)
        download_war;
        handle_files;
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
