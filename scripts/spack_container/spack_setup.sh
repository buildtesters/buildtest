#!/bin/bash
export SPACK_ROOT=/home/spack/spack
export PATH="${SPACK_ROOT}/bin:${PATH}"

. "${SPACK_ROOT}/share/spack/setup-env.sh"
. "$(spack location -i lmod)/lmod/lmod/init/bash"
module use /home/spack/modules/linux-ubuntu22.04-x86_64_v3
