#!/bin/bash

cd /lustre/workspace/home/hpcswbuild/hpcswadm/jenkins/buildtest/Durham/eb-2018/easyconfigs/buildtest-framework
git fetch origin devel
git pull -r origin devel
ml Anaconda3
export CONDA_ENVS_PATH=/lustre/workspace/home/hpcswadm/.conda
source activate buildtest

export PATH=$PWD:$PATH

export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/IvyBridge/redhat/7.3:/nfs/grid/software/easybuild/Haswell/redhat/7.3:/nfs/grid/software/easybuild/Broadwell/redhat/7.3:/nfs/grid/software/easybuild/SkyLake/redhat/7.3
export BUILDTEST_MODULE_BROOT=/clust/app/easybuild/2018/IvyBridge/redhat/7.3:/clust/app/easybuild/2018/Haswell/redhat/7.3:/clust/app/easybuild/2018/Broadwell/redhat/7.3:/clust/app/easybuild/2018/SkyLake/redhat/7.3:$BUILDTEST_EBROOT
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/commons:/clust/app/easybuild/2018/commons:$BUILDTEST_EBROOT
export BUILDTEST_LOGDIR=$PWD/logs
export BUILDTEST_TESTDIR=$PWD/tests

rm -rf $BUILDTEST_LOGDIR

_buildtest list --easyconfigs

