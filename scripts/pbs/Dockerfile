FROM pbspro/pbspro:18.1
ENV PBS_START_MOM=1
RUN yum install -y which git wget make gcc gfortran csh tcsh && \
   # https://tecadmin.net/install-python-3-7-on-centos/ python 3 installation
   yum install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel && \
   wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz && \
   tar xzf Python-3.7.11.tgz && \
   cd Python-3.7.11 && \
   ./configure --enable-optimizations && \
   make altinstall && \
   /opt/pbs/bin/qmgr -c "create node pbs" && \
   /opt/pbs/bin/qmgr -c "set node pbs queue=workq" && \
   /opt/pbs/bin/qmgr -c "set server job_history_enable=True"

LABEL org.opencontainers.image.authors="shahzebmsiddiqui@gmail.com"
