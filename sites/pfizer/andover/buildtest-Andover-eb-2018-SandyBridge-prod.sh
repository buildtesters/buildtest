 #!/bin/bash

cd /clust/app/hpcswbuild/hpcswadm/jenkins/buildtest/Andover/eb-2018/SandyBridge/prod/buildtest-framework
git fetch origin devel
git pull -r origin devel
ml Anaconda3
source activate buildtest
export CONDA_ENVS_PATH=/clust/app/hpcswbuild/hpcswadm/.conda/
source activate buildtest
export PATH=$PWD:$PATH

export BUILDTEST_MODULE_ROOT=/clust/app/easybuild/2018/SandyBridge/redhat/7.3/modules/all
export BUILDTEST_LOGDIR=$PWD/logs
export BUILDTEST_TESTDIR=$PWD/tests
export BUILDTEST_MODULE_NAMING_SCHEME=FNS
export BUILDTEST_CONFIGS_REPO=/clust/app/hpcswbuild/hpcswadm/buildtest-configs
export BUILDTEST_R_REPO=/clust/app/hpcswbuild/hpcswadm/R-buildtest-config
export BUILDTEST_PERL_REPO=/clust/app/hpcswbuild/hpcswadm/Perl-buildtest-config
export BUILDTEST_PYTHON_REPO=/clust/app/hpcswbuild/hpcswadm/Python-buildtest-config
export BUILDTEST_RUBY_REPO=/clust/app/hpcswbuild/hpcswadm/Ruby-buildtest-config

 rm -rf $BUILDTEST_LOGDIR
 rm -rf $BUILDTEST_TESTDIR
 _buildtest build --all-software
 _buildtest run --all-software
