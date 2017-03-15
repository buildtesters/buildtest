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
DIR=$(dirname $SOURCE)
EXEC=$(basename $SOURCE | cut -f1 -d.)
COMPILER=javac
$COMPILER $SOURCE 
if [ $? != 0 ]; then
	echo "Unable to build program $SOURCE "
	exit 1
fi
cd $DIR
java $EXEC
if [ $? != 0 ]; then
	echo "Unable to run $EXEC"
	exit 1
fi

rm ./${EXEC}.class
