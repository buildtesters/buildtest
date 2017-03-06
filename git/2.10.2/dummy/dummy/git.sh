#!/bin/sh

module purge
module=git
version=2.10.2
module load $module/$version

if [ $? != 0 ]; then
	echo "unable to load module $module/$version"
	exit 1
fi

git clone https://github.com/pezmaster31/bamtools.git
if [ $? != 0 ]; then
	echo "Unable to run git "
	exit 1
fi

rm -rf bamtools

