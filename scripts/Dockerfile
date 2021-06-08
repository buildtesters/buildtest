FROM pbspro/pbspro
ENV PBS_START_MOM="1"
RUN yum install -y which python3 \
 && /opt/pbs/bin/qmgr -c "create node pbs" \
 && /opt/pbs/bin/qmgr -c "set node pbs queue=workq" \
 && /opt/pbs/bin/qmgr -c "set server job_history_enable=True"
