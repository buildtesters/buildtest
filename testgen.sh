#!/bin/sh

function usage () {
   cat <<EOF
Usage: testgen [-s] [-v] [-e] [-m]
   -s --software 	  application name. This must match the module name

   -v --version		  application version. This must match the module version

   -e --executable	  executable to test of the particular application
   
   -p --parameter	  pass parameters to executable command to test

   -m --modules		  adding extra modules prior to loading application. Use 
			  this to resolve dependencies, if it is not captured in 
			  module file

   -h   		  displays basic help

Example:
    1. This will create a test case for application GCC version 5.2.0 
       and test the gcc command

    ./testgen.sh -s GCC -v 5.2.0 -e gcc

    2. This will create a test case for netCDF 4.4.1 and load the HDF5 module first
    ./testgen.sh -s netCDF -v 4.4.1  -e ncgen  -m "HDF5/1.8.16"

    Modules should be passed in quotation if adding multiple modules to path
    
    ./testgen.sh -s netCDF -v 4.4.1  -e ncgen  -m "<module>/<version> <module>/version ..."

EOF
}

# convert long argument names to short 
for arg in "$@"; do
  shift
  case "$arg" in
    "--software") set -- "$@" "-s" ;;
    "--version") set -- "$@" "-v" ;;
    "--executable") set -- "$@" "-e" ;;
    "--parameter") set -- "$@" "-p" ;;
    "--modules") set -- "$@" "-m" ;;
    "--help") set -- "$@" "-h" ;;
    *)        set -- "$@" "$arg"
  esac
done

software=""
version=""
executable=""
depmodules=""
parameter=""
while getopts ":s:v:e:m:p:h" opt; do
  case $opt in
    s)
      	software=$OPTARG
      	;;
    v)
      	version=$OPTARG
      	;;
    e)
      	executable=$OPTARG
      	;;
    m) 
        depmodules=$OPTARG
        ;;
    p)
	parameter=$OPTARG
	;;
    h)
      	usage
      	exit 0
      	;;
    \?)
      	echo "Invalid option: -$OPTARG" >&2
      	echo "Please run ./testgen.sh -h for a list of options"
      	exit 1
      	;;
    :)
      	echo "Option -$OPTARG requires an argument." >&2
      	exit 1
      	;;
  esac
done

if [ "$software" == "" ] || [ "$version" == "" ] || [ "$executable" == "" ]; then
	echo "need to specify option -s -v -e in your command"
	exit 1
fi
#echo $1 $2 $3
echo "software="$software
echo "version="$version
echo "executable="$executable
echo "depmodules="$depmodules
echo "param="$parameter

# split string by space and put in array. Since multiple modules can be 
# passed we need to process each module separately
array=(${depmodules// / })
for i in "${array[@]}"
do
	echo $i
done

if [ ! -d $software/$version ]; then
	mkdir -p $software/$version
fi
currentcommand="$0 $@"
echo $currentcommand
# if test case doesn't exist then create the test script and add command to testall.sh
if [ ! -f "$software/$version/${executable}.sh" ]; then
	echo "sh $executable.sh " >> $software/$version/testall.sh	

	# copy template file to its proper directory
	cp template.txt $software/$version/$executable.sh

	# applying changes to module, version and executable in file
	sed -i 's/EXECUTABLE/'$executable' '$parameter'/g' $software/$version/$executable.sh
	sed -i 's/$1/'$software'/g' $software/$version/$executable.sh
	sed -i 's/$2/'$version'/g' $software/$version/$executable.sh

	# adding depended modules to file at line 4, this is aright after module purge
	for i in "${array[@]}"
	do
        	sed -i '4i module load '${i} $software/$version/$executable.sh
	done
	
	echo "Creating Test $software/$version/$executable.sh"
	echo "Writing Test command to $software/$version/testall.sh"

else
	echo "Test already exists. Check file $software/$version/$executable.sh"
	echo "Exiting Program."
	exit 1;
fi

if [ ! -f "$software/$version/input.txt" ]; then
	echo $currentcommand > $software/$version/input.txt
else
	echo $currentcommand >> $software/$version/input.txt
	#grep "$command" $software/$version/input.txt
fi
