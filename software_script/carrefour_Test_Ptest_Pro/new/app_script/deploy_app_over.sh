#!/usr/bin/env bash

#For Deploy Tomcat_app

parameter=$1

handel(){
	echo -e "\033[31mWaitting For Tomcat_APP Start................\033[0m"
	echo "76132fbbe6" |sudo -S /software/script/carrefour_app.py -d ${parameter} >/dev/null 2>&1
}
handel_status(){
	/software/script/carrefour_app.py -d status
}
deploy_laster(){
		/software/script/service_check.py
	
}
case ${parameter} in
    deploy)
        handel;
        deploy_laster;
        ;;
    status)
        handel_status;
        ;;
   *)
      echo "`basename ${0}`:usage: deploy|status"
      exit 1 # Command to come out of the program with status 1
      ;;
esac