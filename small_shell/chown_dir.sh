#!/usr/bin/env bash
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com
user=cdczhangg
for ip in 10.151.254.{1..16}
do
ssh ${ip} """echo "76132fbbe6" |sudo -S chown -R cdczhangg.c4CHappl /software"""
done