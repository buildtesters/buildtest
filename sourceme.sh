#!/bin/bash

ROOT=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
export PATH=$ROOT/bin:$PATH
export BUILDTEST_ROOT=$ROOT
cd $BUILDTEST_ROOT
eval "$(register-python-argcomplete buildtest)"
