#!/bin/sh

module purge
module load GCC/6.2.0
module=MPICH
version=3.2
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

mpic++ -v
if [ $? != 0 ]; then
	echo "Unable to run mpic++ -v"
	exit 1
fi

