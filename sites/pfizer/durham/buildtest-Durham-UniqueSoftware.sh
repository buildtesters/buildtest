#!/bin/bash -li

cd /lustre/workspace/home/hpcswbuild/hpcswadm/jenkins/buildtest/Durham/UniqueSoftware/buildtest-framework
git fetch origin devel
git pull -r origin devel
ml Anaconda3
export CONDA_ENVS_PATH=/lustre/workspace/home/hpcswadm/.conda
source activate buildtest
export PATH=$PWD:$PATH

# eb-2018-test
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/IvyBridge/redhat/7.3/all/
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/Haswell/redhat/7.3/all/:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/Broadwell/redhat/7.3/all/:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/SkyLake/redhat/7.3/all/:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/easybuild/2018/commons/all/:$BUILDTEST_MODULE_ROOT
# eb-2018-prod
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/Haswell/redhat/7.3/modules/all:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/SkyLake/redhat/7.3/modules/all:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/commons/modules/all:$BUILDTEST_MODULE_ROOT
# eb-2017
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL7/easybuild/modules/all:$BUILDTEST_MODULE_ROOT
# medsci
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL7/medsci/modules/all:$BUILDTEST_MODULE_ROOT
# legacy RHEL6
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL6/chemistry/:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL6/general/:$BUILDTEST_MODULE_ROOT
# non-easybuild
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL7/non-easybuild/modules/all:$BUILDTEST_MODULE_ROOT

_buildtest list -ls
