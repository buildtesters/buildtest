#!/bin/bash
# get platform
platform=$(python -c "import platform; print(platform.system())")

#echo "${BASH_SOURCE[0]}"
#echo "platform:" $platform

#if [ "$platform" == "Darwin" ]; then
#  realpath=$(grealpath ${BASH_SOURCE[0]})
#  echo realpath
#  buildtest_root="$(dirname "$(grealpath ${BASH_SOURCE[0]})")"
#fi

buildtest_root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd)"
echo "buildtest root is ${buildtest_root}"

echo "Installing buildtest dependencies"
pip install -r ${buildtest_root}/requirements.txt &> /dev/null

bin=${buildtest_root}/bin
export PATH=${bin}:$PATH
# add PYTHONPATH for buildtest to persist in shell environment
export PYTHONPATH=${buildtest_root}:$PYTHONPATH

buildtest_path=$(which buildtest)
echo "Adding ${bin} to PATH variable"
echo "buildtest command: ${buildtest_path}"
