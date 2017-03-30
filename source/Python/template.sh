#!/bin/sh

module purge
module=
version=
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi
SOURCE=
COMPILER=python
$COMPILER $SOURCE 
if [ $? != 0 ]; then
	echo "Unable to run program $SOURCE "
	exit 1
fi
