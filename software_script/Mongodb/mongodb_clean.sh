#!/bin/bash

#clear up Logs For Mongodb

#Remove Days
days=7

#Logs  Path
logpath=/software/Mongodb/data/master/log

#get Mongodb PID Read Pid files Only 1
Mongodb_PID=`sed -n '1,1p' /software/Mongodb/master.pid`

#Cut Mongodb Logs
kill -SIGUSR1 ${Mongodb_PID}

#Remove Old Logs Files
find ${logpath}/ -mtime +${days} -delete