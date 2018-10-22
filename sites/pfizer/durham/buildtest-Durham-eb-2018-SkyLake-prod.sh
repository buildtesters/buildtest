#!/bin/bash

cd /lustre/workspace/home/hpcswbuild/hpcswadm/jenkins/buildtest/Durham/eb-2018/SkyLake/prod/buildtest-framework
git fetch origin devel
git pull -r origin devel
ml Anaconda3
export CONDA_ENVS_PATH=/lustre/workspace/home/hpcswadm/.conda
source activate buildtest
export PATH=$PWD:$PATH

export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/SkyLake/redhat/7.3/modules/all
export BUILDTEST_LOGDIR=$PWD/logs
export BUILDTEST_TESTDIR=$PWD/tests
export BUILDTEST_MODULE_NAMING_SCHEME=FNS

rm -rf $BUILDTEST_LOGDIR

_buildtest build --all-software
_buildtest run --all-software




