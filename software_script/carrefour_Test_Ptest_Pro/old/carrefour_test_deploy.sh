#!/usr/bin/env bash

#定义 代码存放路径
SVN_EXPORT="/install/carrefour-test/test"
#定义 部署文件路径
DEPLOY_DIR="${SVN_EXPORT}/cybershop-front/target"
DEPLOY_DIR_WEB="${SVN_EXPORT}/cybershop-web/target"
#远程服务器地址
REMOTE_ADDR=172.31.1.101
#远程服务器地址- web
REMOTE_ADDR_WEB=172.31.1.100
#远程服务器路径
REMOTE_DIR="/software/"
#远程服务器脚本路径
REMOTE_SCRIPT="/software/script/carrefour_front.py"
REMOTE_SCRIPT_WEB="/software/script/carrefour_web.py"



echo -e "\033[32m######################################################\033[0m"
echo -e "\033[31m           脚本执行操作              \033[0m"
echo -e "\033[31m           front_test.sh front(前台) 20355(SVN 版本号)\033[0m"
echo -e "\033[32m######################################################\033[0m"



#定义 svn 更新方法
svn_update () {
    cd ${SVN_EXPORT}
    /usr/bin/svn update -r ${SVN_NUMBER}
}


#定义 项目编译方法
project_build () {
    cd ${SVN_EXPORT}
    /install/maven/bin/mvn clean install -Ptest -DskipTests
}


#定义文件传送方法
send_project () {
    /usr/bin/scp ${DEPLOY_DIR}/cybershop-front-0.0.1-SNAPSHOT.war ${REMOTE_ADDR}:${REMOTE_DIR}
    /usr/bin/scp ${DEPLOY_DIR_WEB}/cybershop-web-0.0.1-SNAPSHOT.war ${REMOTE_ADDR_WEB}:${REMOTE_DIR}
    if [ $? -eq 0 ]; then
        echo -e "\033[32mSend Project Files OK\033[0m"
    fi
}


#定义执行远程部署方法
service_deploy () {
    ssh ${REMOTE_ADDR} "${REMOTE_SCRIPT} -d deploy"
    ssh ${REMOTE_ADDR_WEB} "${REMOTE_SCRIPT_WEB} -d deploy"

}

main () {
#定一 svn 版本号
SVN_NUMBER=${2}
case ${1} in
    deploy)
        svn_update;
        project_build;
        send_project;
        service_deploy;
        ;;

    *)
        echo "Usage:$0(deploy)"
        exit 1
        ;;
esac
}
main ${1} ${2}