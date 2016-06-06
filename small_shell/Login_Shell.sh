#!/usr/bin/env bash

Network_Device=`ifconfig -a | grep -i --color hwaddr | awk '{print $1}'`

Host_Address=`ifconfig ${Network_Device} | grep "inet addr" | head -n 1 | awk '{print $2}' | awk -F : '{print $2}'`
Name=`hostname`
export PS1="\[\033[01;31m\]\u\[\033[00m\]@\[\033[01;32m\]${Host_Address}\[\033[00m\][\[\033[01;33m\]${Name}\[\033[00m\]]:\[\033[01;34m\]\w\[\033[00m\]\n$ "
echo ${Network_Device},${Host_Address}