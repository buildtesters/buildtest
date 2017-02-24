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

ompi_info
if [ $? != 0 ]; then
	echo "Unable to run ompi_info"
	exit 1
fi

