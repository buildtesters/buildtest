#!/bin/bash
. /home/spack/spack/share/spack/setup-env.sh
. "$(spack location -i lmod)/lmod/lmod/init/bash"
spack module tcl refresh --delete-tree -y
module use /home/spack/modules/linux-ubuntu22.04-x86_64_v3

