#!/bin/bash
# This script is used to setup buildtest inside container. One should typically bind mount BUILDTEST_ROOT on host operating
# system inside container as follows:
# docker run -it -v  $BUILDTEST_ROOT:/home/spack/buildtest ghcr.io/buildtesters/buildtest_spack:latest

module load python

# setup python environment
python -m venv $HOME/pyenv/buildtest
source $HOME/pyenv/buildtest/bin/activate

cd $HOME/buildtest
# installing buildtest
source setup.sh

export BUILDTEST_CONFIGFILE=$BUILDTEST_ROOT/buildtest/settings/spack_container.yml
