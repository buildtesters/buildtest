#!/bin/bash


cd /clust/app/hpcswbuild/hpcswadm/jenkins/buildtest/Andover/ListSoftwareVersions/buildtest-framework
git fetch origin devel
git pull -r origin devel

ml Anaconda3
source activate buildtest
export CONDA_ENVS_PATH=/clust/app/hpcswbuild/hpcswadm/.conda/
source activate buildtest
export PATH=$PWD:$PATH


# eb-2018 prod stack
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/SandyBridge/redhat/7.3/modules/all
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/Haswell/redhat/7.3/modules/all:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/commons/modules/all:$BUILDTEST_MODULE_ROOT
# eb-2017 stack
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL7/easybuild/modules/all:$BUILDTEST_MODULE_ROOT
# medsci stack
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL7/medsci/modules/all:$BUILDTEST_MODULE_ROOT
# legacy RHEL6 stack
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL6/chemistry/:$BUILDTEST_MODULE_ROOT
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL6/general/:$BUILDTEST_MODULE_ROOT
# non-easybuild stack
export BUILDTEST_MODULE_ROOT=/nfs/grid/software/RHEL7/non-easybuild/modules/all:$BUILDTEST_MODULE_ROOT

export BUILDTEST_CONFIGS_REPO=/clust/app/hpcswbuild/hpcswadm/buildtest-configs
export BUILDTEST_R_REPO=/clust/app/hpcswbuild/hpcswadm/R-buildtest-config
export BUILDTEST_PERL_REPO=/clust/app/hpcswbuild/hpcswadm/Perl-buildtest-config
export BUILDTEST_PYTHON_REPO=/clust/app/hpcswbuild/hpcswadm/Python-buildtest-config
export BUILDTEST_RUBY_REPO=/clust/app/hpcswbuild/hpcswadm/Ruby-buildtest-config

_buildtest list -svr
