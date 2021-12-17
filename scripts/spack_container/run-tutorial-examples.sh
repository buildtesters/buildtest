#!/bin/bash
# This script can be run as follows: docker run -v $BUILDTEST_ROOT:/home/spack/buildtest ghcr.io/buildtesters/buildtest_spack:latest bash /home/spack/buildtest/scripts/spack_container/run-tutorial-examples.sh
source /etc/profile
source /home/spack/buildtest/scripts/spack_container/setup.sh
python /home/spack/buildtest/scripts/spack_container/doc-examples.py