#!/usr/bin/env bash
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

solr_handle (){
    echo "76132fbbe6" |sudo -S /software/script/solr_action.py -d ${handle}
}
handle=${1}
case ${1} in
    start)
        solr_handle;
        ;;
    stop)
        solr_handle;
        ;;
    restart)
        solr_handle;
        ;;
    status)
        solr_handle;
        ;;
    log)
        solr_handle;
        ;;
    *)
        echo "Usage:$0(start|stop|restart|log|status)"
        exit 1
        ;;
esac