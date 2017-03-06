#!/bin/sh

module purge
module load GCC/5.2.0
module=CUDA
version=8.0.44
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi
SOURCE=saxpy.cu
EXEC=$SOURCE.exe
COMPILER=nvcc
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
