#!/bin/sh

module purge
module=icc
version=2017.1.132-GCC-5.2.0
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

icpc -v
if [ $? != 0 ]; then
	echo "Unable to run icpc -v"
	exit 1
fi

