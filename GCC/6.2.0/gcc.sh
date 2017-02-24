#!/bin/sh

module purge
module=GCC
version=6.2.0
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

gcc -v
if [ $? != 0 ]; then
	echo "Unable to run gcc"
	exit 1
fi

