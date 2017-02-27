#!/bin/sh

module purge
module load GCC/5.2.0
module=MPICH
version=3.2
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

mpicc -v
if [ $? != 0 ]; then
	echo "Unable to run mpicc -v"
	exit 1
fi

