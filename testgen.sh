#!/bin/sh

function usage () {
   cat <<EOF
Usage: testgen [-c] [-s] [-v] [-e] [-m]
   -c --compiler	  Set the compiler name for building a test from source file.
			  This will set the tag COMPILER if found in the template

   -s --software 	  application name. This must match the module name

   -v --version		  application version. This must match the module version

   -e --executable	  executable to test of the particular application
   
   -p --parameter	  pass parameters to executable command to test

   -m --modules		  adding extra modules prior to loading application. Use 
			  this to resolve dependencies, if it is not captured in 
			  module file

   -b --buildtoolchain	  The toolchain used to build the package, this is useful for 
			  identifying a test case by its build configuration when same 
			  version of software is built with different compilers, mpi, 
			  math libraries.
		
			  If a package is not built with any toolchain
		          don't use the flag and the script will generate the test case in a 
		          directory <software>/<version>/<toolchain>/<test>.sh

			  Default value is none.

			  Toolchain must be a valid module file since this must be loaded prior
			  to loading a module

   -t --template	  The template file used for creating the test script
			  generic: used for running executable [default]
			  mpi:	used for building mpi source code and running with mpirun
   
   -f --file		  Specify the source file used for building the executable. This file 
		          will be used for setting the tag SOURCE in the template file

   -n --name		  This parameter will set the name of the test script. By default this
			  would be the executable that is run, but for application that require
			  compilation from source (i.e using -f to import a source code in testing
			  directory) this would require a unique name for the test. Make sure the 
			  name of the test is unique, otherwise the test would not be generated

   -h --help   		  displays basic help

Example:
    1. 	This will create a test case for application GCC version 5.2.0 
       	and test the gcc command

    	./testgen.sh -s GCC -v 5.2.0 -e gcc

    2. This will create a test case for netCDF 4.4.1 and load the HDF5 module first
    	./testgen.sh -s netCDF -v 4.4.1  -e ncgen  -m "HDF5/1.8.16"

    	Modules should be passed in quotation if adding multiple modules to path
    
    	./testgen.sh -s netCDF -v 4.4.1  -e ncgen  -m "<module>/<version> <module>/version ..."

    3. 	Passing a parameter to an executable
	./testgen.sh -s OpenMPI -v 2.0.0 -e mpicc -p -v

    4. 	Generate a test script with toolchain
    	./testgen.sh -s OpenMPI -v 2.0.0 -b GCC-5.2.0 -e mpicc

    5.  An MPI test that specifies the source file, compiler wrapper,  
	mpi template and names the test script. This will copy the file 
	specified by -f into the proper directory, the compiler flag -c is 
	used for building the source file. The template option -t selects the 
	mpi template file which is a skeleton test script. 

	./testgen.sh -s OpenMPI -v 2.0.0 -c mpicc -f src/MPI/hello.c -b GCC/5.2.0 -t mpi -n hello_c
EOF
}

software=""
version=""
executable=""
depmodules=""
parameter=""
template=""
toolchain="none"
testname=""
compiler=""

#OPTS=`getopt -o svemptfh: --long verbose,dry-run,help,stack-size: -n 'parse-options' -- "$@"`

#echo $OPTS
#exit 1
# convert long argument names to short 
for arg in "$@"; do
  shift
  case "$arg" in
    "--software") set -- "$@" "-s" ;;
    "--version") set -- "$@" "-v" ;;
    "--executable") set -- "$@" "-e" ;;
    "--parameter") set -- "$@" "-p" ;;
    "--modules") set -- "$@" "-m" ;;
    "--buildtoolchain") set -- "$@" "-b" ;;
    "--template") set -- "$@" "-t" ;;
    "--name") set -- "$@" "-n" ;;
    "--compiler") set -- "$@" "-c" ;;
    "--file") set -- "$@" "-f" ;; 
    "--help") set -- "$@" "-h" ;;
    *)        set -- "$@" "$arg"
  esac
done

#OPT=`getopt -o s:v:e:m:p:t:f:h --long software:,version:,executable:,modules:,parameter:,template:,file:,help: -- "$@"`
#eval set -- "$OPT"

while getopts ":b:c:e:f:hm:n:p:s:t:v:" opt; do
#while true;
  case $opt in
    b)
        toolchain=$OPTARG
        ;;
    c)
	compiler=$OPTARG
	;;
    e)
        executable=$OPTARG
        ;;
    f)
        filename=$OPTARG
        ;;
    h)
        usage
        exit 0
        ;;
    m)
        depmodules=$OPTARG
        ;;
    n)
        testname=$OPTARG
        ;;
    p)
        parameter=$OPTARG
        echo "parameter was invoked with $OPTARG"
        ;;

    s)
      	software=$OPTARG
	;;
    t)
        echo "template flag invoked"
        template=$OPTARG
        ;;
    v)
      	version=$OPTARG
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

echo "software="$software
echo "version="$version
echo "executable="$executable
echo "depmodules="$depmodules
echo "param="${parameter[@]}
echo "toolchain="$toolchain
echo "filename="$filename
echo "template="$template

if [ "$software" == "" ] || [ "$version" == "" ] ; then
	echo "need to specify option -s -v in your command"
	exit 1
fi

if [ "$template" == "" ]; then
	template="template/generic.txt"
elif [ "$template" == "mpi" ]; then
	template="template/mpi-build.txt"
else
	echo "invalid template, please select a valid template"
	echo "exiting program..."
	exit 1
fi
# if filename is specified then --test-name must be specified
if [ "$filename" != "" ] && [ "$testname" == "" ]; then
	echo "option --test-name must be specified when using --file"
	echo "exiting program..."
	exit 1
fi

# check if file exists
if [ ! -f $filename ]; then
	echo "can't find file $filename"
	echo "exiting program..."
        exit 1
fi
# default value of testname is the value of the executable specified by -e
if [ "$testname" == "" ]; then
	testname=$executable
fi

# split string by space and put in array. Since multiple modules can be 
# passed we need to process each module separately
array=(${depmodules// / })
for i in "${array[@]}"
do
	echo $i
done
 
if [ ! -d $software/$version/$toolchain ]; then
	mkdir -p $software/$version/$toolchain
fi
currentcommand="$0 $@"
echo $currentcommand
# if test case doesn't exist then create the test script and add command to testall.sh

if [ ! -f "$software/$version/$toolchain/${testname}.sh" ]; then
	echo "sh $testname.sh " >> $software/$version/$toolchain/testall.sh	

	# copy template file to its proper directory
	cp $template $software/$version/$toolchain/$testname.sh
	
	# if --file is specified then condition below must be true, we must copy file in propery directory
	if [ "$filename" != "" ]; then
		cp $filename $software/$version/$toolchain/
	fi

	# if filename variable is set, lets fix the SOURCE tag with the filename
	if [ "$filename" != "" ]; then
		file_strip_dir=`basename $filename`
		sed -i 's/SOURCE=/SOURCE='$file_strip_dir'/g' $software/$version/$toolchain/$testname.sh
	fi
	
	 # if compiler variable is set, lets fix the COMPILER tag 
        if [ "$compiler" != "" ]; then
                sed -i 's/COMPILER=/COMPILER='$compiler'/g' $software/$version/$toolchain/$testname.sh
        fi


	
	# applying changes to module, version and executable in file
	sed -i 's/EXECUTABLE/'$executable' '$parameter'/g' $software/$version/$toolchain/$testname.sh
	sed -i 's/module=/module='$software'/g' $software/$version/$toolchain/$testname.sh
	sed -i 's/version=/version='$version'/g' $software/$version/$toolchain/$testname.sh


	if [ "$toolchain" != "none" ]; then
		sed -i '4i module load '$toolchain $software/$version/$toolchain/$testname.sh
	fi
	# adding depended modules to file at line 4, this is aright after module purge
	for i in "${array[@]}"
	do
        	sed -i '4i module load '${i} $software/$version/$toolchain/$testname.sh
	done
	
	echo "Creating Test $software/$version/$toolchain/$testname.sh"
	echo "Writing Test command to $software/$version/$toolchain/testall.sh"

else
	echo "Test already exists. Check file $software/$version/$toolchain/$testname.sh"
	echo "Exiting Program."
	exit 1;
fi

if [ ! -f "$software/$version/$toolchain/input.txt" ]; then
	echo $currentcommand > $software/$version/$toolchain/input.txt
else
	echo $currentcommand >> $software/$version/$toolchain/input.txt
	#grep "$command" $software/$version/input.txt
fi
