#!/bin/bash

yum install -y which git wget make
# https://tecadmin.net/install-python-3-7-on-centos/ python 3 installation
yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel
cd /tmp
wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz
tar xzf Python-3.7.11.tgz
cd Python-3.7.11
./configure --enable-optimizations
make altinstall

wget https://bootstrap.pypa.io/get-pip.py
python3.7 get-pip.py
ln -s /usr/local/bin/python3.7 /usr/local/bin/python3

/opt/pbs/bin/qmgr -c "create node pbs"
/opt/pbs/bin/qmgr -c "set node pbs queue=workq"
/opt/pbs/bin/qmgr -c "set server job_history_enable=True"