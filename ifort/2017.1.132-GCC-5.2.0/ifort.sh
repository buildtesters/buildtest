#!/bin/sh

module purge
module=ifort
version=2017.1.132-GCC-5.2.0
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

ifort -v
if [ $? != 0 ]; then
	echo "Unable to run ifort -v"
	exit 1
fi

