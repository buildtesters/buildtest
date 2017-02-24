#!/bin/sh

module purge
module load GCC/6.2.0
module=OpenMPI
version=2.0.1
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi
SOURCE=hello.cpp
EXEC=hello.cpp.exe
mpic++ -o $EXEC $SOURCE 
if [ $? != 0 ]; then
	echo "Unable to build program $SOURCE "
	exit 1
fi

mpirun -np 2 ./$EXEC
if [ $? != 0 ]; then
	echo "Unable to run $EXEC"
	exit 1
fi

rm ./$EXEC
