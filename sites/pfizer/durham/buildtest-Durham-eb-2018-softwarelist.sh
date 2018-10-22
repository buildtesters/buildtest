#!/bin/bash


cd /lustre/workspace/home/hpcswbuild/hpcswadm/jenkins/buildtest/Durham/eb-2018/softwarelist/buildtest-framework
git fetch origin devel
git pull -r origin devel
ml Anaconda3
export CONDA_ENVS_PATH=/lustre/workspace/home/hpcswadm/.conda
source activate buildtest

export PATH=$PWD:$PATH

export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all
_buildtest list -svr


export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/Haswell/redhat/7.3/modules/all
_buildtest list -svr


export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all
_buildtest list -svr

export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/SkyLake/redhat/7.3/modules/all
_buildtest list -svr

export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/commons/modules/all
_buildtest list -svr

export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/IvyBridge/redhat/7.3/all
_buildtest list -svr

export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/Haswell/redhat/7.3/all
_buildtest list -svr

export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/Broadwell/redhat/7.3/all
_buildtest list -svr

export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/SkyLake/redhat/7.3/all
_buildtest list -svr


export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/commons/all
_buildtest list -svr
