#!/bin/sh

function usage () {
   cat <<EOF
Usage: testgen [-s] [-v] [-e] 
   -s   application name. This must match the module name
   -v   application version. This must match the module version
   -e   executable to test of the particular application
   -h   displays basic help
EOF
}

software=""
version=""
executable=""
depmodules=""
while getopts ":s:v:e:m:h" opt; do
  case $opt in
    s)
      echo "-s was triggered, Parameter: $OPTARG" >&2
      software=$OPTARG
      ;;
    v)
      echo "-v was triggered, Parameter: $OPTARG" >&2
      version=$OPTARG
      ;;
    e)
      echo "-e was triggered, Parameter: $OPTARG" >&2
      executable=$OPTARG
      ;;
    m) 
	echo "-m was triggered, Parameter: $OPTARG" >&2
        depmodules=$OPTARG
	;;
    h)
      usage
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ "$software" == "" ] || [ "$version" == "" ] || [ "$executable" == "" ]; then
	echo "need to specify option -s -v -e in your command"
fi
#echo $1 $2 $3
echo "software="$software
echo "version="$version
echo "executable="$executable
echo "depmodules="$depmodules

array=(${depmodules// / })
for i in "${array[@]}"
do
	echo $i
done

if [ ! -d $software/$version ]; then
	mkdir -p $software/$version
fi

# if test case doesn't exist then create the test script and add command to testall.sh
if [ ! -f "$software/$version/${executable}.sh" ]; then
	echo "sh $executable.sh " >> $software/$version/testall.sh	

	# copy template file to its proper directory
	cp template.txt $software/$version/$executable.sh

	# applying changes to module, version and executable in file
	sed -i 's/EXECUTABLE/'$executable'/g' $software/$version/$executable.sh
	sed -i 's/$1/'$software'/g' $software/$version/$executable.sh
	sed -i 's/$2/'$version'/g' $software/$version/$executable.sh

	# adding depended modules to file at line 4, this is aright after module purge
	for i in "${array[@]}"
	do
        	sed -i '4i module load '${i} $software/$version/$executable.sh
	done

else
	echo "file found"
fi

cp template.txt $software/$version/$executable.sh
sed -i 's/EXECUTABLE/'$executable'/g' $software/$version/$executable.sh
sed -i 's/$1/'$software'/g' $software/$version/$executable.sh
sed -i 's/$2/'$version'/g' $software/$version/$executable.sh

# adding depended modules to file at line 4, this is aright after module purge
for i in "${array[@]}"
do
        sed -i '4i module load '${i} $software/$version/$executable.sh
done


