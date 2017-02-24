#!/bin/sh

module purge
module load iccifort/2017.1.132-GCC-5.2.0
module=impi
version=2017.1.132
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

mpiicpc -v
if [ $? != 0 ]; then
	echo "Unable to run mpiicpc -v"
	exit 1
fi

