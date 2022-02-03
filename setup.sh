#!/bin/bash
# MIT License

# Copyright (c) 2021-2022, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory (subject to receipt of
# any required approvals from the U.S. Dept. of Energy), Shahzeb Siddiqui,
# and Vanessa Sochat. All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

buildtest_root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd)"
pip=pip3

if ! [ -x "$(command -v $pip)" ]; then 
  echo "cannot find program $pip. Please see the pip documentation: https://pip.pypa.io/en/stable/installation/ on how to install pip"
  exit 1
fi

python=python3

# Need 'set +e' so that process is not terminated especially when using in CI
set +e

$python -c "import buildtest.main" &> /dev/null
returncode=$?


# if we are unable to import buildtest.main then install buildtest dependencies
if [ $returncode -ne 0 ]; then
  #$pip install --target ${buildtest_root}/.packages -r ${buildtest_root}/requirements.txt &> /dev/null
  $pip install -r ${buildtest_root}/requirements.txt &> /dev/null
fi

export BUILDTEST_ROOT=$buildtest_root
export PATH=${buildtest_root}/bin:$PATH

# for ZSH shell need to run autoload see https://stackoverflow.com/questions/3249432/can-a-bash-tab-completion-script-be-used-in-zsh
#if [ -n "$ZSH_VERSION" ]; then
  # compinit -C will ignore insecure files. See https://zsh.sourceforge.io/Doc/Release/Completion-System.html##Use-of-compinit
#  autoload -U +X compinit && compinit -C
#  autoload -U +X bashcompinit && bashcompinit
#fi

# enable bash completion script
source $buildtest_root/bash_completion.sh

# allow buildtest source code to PYTHONPATH so python can import buildtest
if [ -z "$PYTHONPATH" ]; then
  export PYTHONPATH=${BUILDTEST_ROOT}
else
  export PYTHONPATH=${BUILDTEST_ROOT}:$PYTHONPATH
fi