#!/bin/bash


cd /clust/app/hpcswbuild/hpcswadm/jenkins/buildtest/Andover/eb-2018/diff-trees/buildtest-framework
git fetch origin devel
git pull -r origin devel

ml Anaconda3
export CONDA_ENVS_PATH=/clust/app/hpcswbuild/hpcswadm/.conda
source activate buildtest
export PATH=$PWD:$PATH

export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all:/clust/app/easybuild/2018/Haswell/redhat/7.3/modules/all:/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all:/clust/app/easybuild/2018/SandyBridge/redhat/7.3/modules/all
export BUILDTEST_LOGDIR=$PWD/logs
export BUILDTEST_TESTDIR=$PWD/tests
export BUILDTEST_CONFIGS_REPO=/clust/app/hpcswbuild/hpcswadm/buildtest-configs
export BUILDTEST_R_REPO=/clust/app/hpcswbuild/hpcswadm/R-buildtest-config
export BUILDTEST_PERL_REPO=/clust/app/hpcswbuild/hpcswadm/Perl-buildtest-config
export BUILDTEST_PYTHON_REPO=/clust/app/hpcswbuild/hpcswadm/Python-buildtest-config
export BUILDTEST_RUBY_REPO=/clust/app/hpcswbuild/hpcswadm/Ruby-buildtest-config
export BUILDTEST_TCL_REPO=/clust/app/hpcswbuild/hpcswadm/Tcl-buildtest-config

rm -rf $BUILDTEST_LOGDIR


_buildtest --diff-trees /clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all,/clust/app/easybuild/2018/Haswell/redhat/7.3/modules/all
_buildtest --diff-trees /clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all,/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all
_buildtest --diff-trees /clust/app/easybuild/2018/IvyBridge/redhat/7.3/modules/all,/clust/app/easybuild/2018/SandyBridge/redhat/7.3/modules/all
_buildtest --diff-trees /clust/app/easybuild/2018/Haswell/redhat/7.3/modules/all,/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all
_buildtest --diff-trees /clust/app/easybuild/2018/Haswell/redhat/7.3/modules/all,/clust/app/easybuild/2018/SandyBridge/redhat/7.3/modules/all




