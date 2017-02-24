#!/bin/sh

module purge
module=openmpi
version=1.4.3+gcc-5.2.0
module load RHEL6-software
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi
SOURCE="hello.c"
EXEC="hello.c_exe"

mpicc -o $EXEC $SOURCE 
if [ $? != 0 ]; then
	echo "Unable to build $SOURCE"
	exit 1
fi

mpirun -np 2 ./$EXEC
if [ $? != 0 ]; then
	echo "Unable to run $EXEC"
	exit 1
fi

rm ./$EXEC

