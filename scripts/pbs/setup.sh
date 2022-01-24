#!/bin/bash

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p ~/miniconda
export PATH=~/miniconda/bin:$PATH
conda create -n buildtest -y
source activate buildtest
source $HOME/buildtest/setup.sh
export BUILDTEST_CONFIGFILE=$BUILDTEST_ROOT/tests/settings/pbs.yml
