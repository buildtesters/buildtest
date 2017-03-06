#!/bin/sh

module purge
module load GCC/5.2.0
module=CUDA
version=8.0.44
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

nvcc --version
if [ $? != 0 ]; then
	echo "Unable to run nvcc --version"
	exit 1
fi

