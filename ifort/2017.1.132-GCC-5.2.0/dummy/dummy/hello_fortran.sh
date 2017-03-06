#!/bin/sh

module purge
module=ifort
version=2017.1.132-GCC-5.2.0
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi
SOURCE=hello.f90
EXEC=$SOURCE.exe
COMPILER=ifort
$COMPILER -o $EXEC $SOURCE 
if [ $? != 0 ]; then
	echo "Unable to build program $SOURCE "
	exit 1
fi

./$EXEC
if [ $? != 0 ]; then
	echo "Unable to run $EXEC"
	exit 1
fi

rm ./$EXEC
