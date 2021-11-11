#!/bin/bash
. ~/spack/share/spack/setup-env.sh
. $(spack location -i lmod)/lmod/lmod/init/bash
spack load --only package git
spack module tcl refresh --delete-tree -y
