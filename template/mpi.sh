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
EXEC=$(basename SOURCE).exe
COMPILER=
$COMPILER -o $EXEC $SOURCE 
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
