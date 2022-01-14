#!/bin/bash
. /etc/profile
export PATH=/home/spack/.local/bin:$PATH
. /home/spack/buildtest/scripts/spack_container/setup.sh
pip3 install -r $BUILDTEST_ROOT/docs/requirements.txt &> /dev/null
python $BUILDTEST_ROOT/buildtest/tools/unittests.py