#!/usr/bin/env bash
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

yum -y update
yum groupinstall "Development tools"
echo "76132fbbe6" |sudo -S yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc gcc-c++
tar xzf /software/packages_source/Python-2.7.10.tgz
cd /software/Python-2.7.10
echo "76132fbbe6" |sudo -S ./configure --prefix=/usr/local
echo "76132fbbe6" |sudo -S make
echo "76132fbbe6" |sudo -S make altinstall

echo "76132fbbe6" |sudo -S mv /usr/bin/python /usr/bin/python2.6.6
echo "76132fbbe6" |sudo -S ln -s /usr/local/bin/python2.7 /usr/bin/python