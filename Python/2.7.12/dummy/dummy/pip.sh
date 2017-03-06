#!/bin/sh

module purge
module=Python
version=2.7.12
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

pip list
if [ $? != 0 ]; then
	echo "Unable to run pip list"
	exit 1
fi

