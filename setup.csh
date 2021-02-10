#!/bin/csh
# MIT License

# buildtest Copyright (c) 2021, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory (subject to receipt of
# any required approvals from the U.S. Dept. of Energy), Shahzeb Siddiqui,
and Vanessa Sochat. All rights reserved.

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

set command=($_)
set sourced_file=`readlink -f $command[2]`
set buildtest_root=`dirname "$sourced_file"`

set pip=pip

if ( ! -x `command -v $pip` ) then 
  echo "cannot find program $pip, please install $pip"
  exit 1
endif

echo "Installing buildtest dependencies"
pip install -r ${buildtest_root}/requirements.txt > /dev/null
set bin=${buildtest_root}/bin
set path=($path $bin)

# add PYTHONPATH for buildtest to persist in shell environment
if (! $?PYTHONPATH ) then
	setenv PYTHONPATH $buildtest_root
else
        setenv PYTHONPATH ${PYTHONPATH}:$buildtest_root
endif

set buildtest_path=`which buildtest`
echo "buildtest command: ${buildtest_path}"
