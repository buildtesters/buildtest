#!/bin/csh
# MIT License

# Copyright (c) 2021, The Regents of the University of California,
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

# if BUILDTEST_ROOT not defined in current shell set, figure out directory path for 
# sourced script (setup.csh) and set BUILDTEST_ROOT
if (! $?BUILDTEST_ROOT) then
    # figure out a command to list open files (Linux)
    if (-d /proc/$$/fd) then
        set _open_fd = "ls -l /proc/$$/fd"
    # for Mac
    else
        which lsof > /dev/null
        if ($? == 0) then
            set _open_fd = "lsof -p $$"
        endif
    endif


    # filter list of open files
    if ( $?_open_fd ) then
        set _source_file = `$_open_fd | sed -e 's/^[^/]*//' | grep "/setup.csh"`
    endif

    # setup.csh is located in $BUILDTEST_ROOT 
    if ( $?_source_file ) then
        setenv BUILDTEST_ROOT `dirname "$_source_file"`
    endif

    if (! $?BUILDTEST_ROOT) then
        echo "Cannot set $BUILDTEST_ROOT based on path to setup.csh."
        echo "Try setting BUILDTEST_ROOT to root of buildtest repo and try again."
        exit 1
    endif
endif


# error printing tables from tabulate when utf8 encoding not set. See https://github.com/buildtesters/buildtest/issues/665
setenv LANG en_US.utf8

set pip=pip

if ( ! -x `command -v $pip` ) then 
  echo "cannot find program $pip, please install $pip"
  exit 1
endif

echo "Installing buildtest dependencies"
pip install -r ${BUILDTEST_ROOT}/requirements.txt > /dev/null
set bin=${BUILDTEST_ROOT}/bin
set path=($path $bin)

# add PYTHONPATH for buildtest to persist in shell environment
if (! $?PYTHONPATH ) then
	setenv PYTHONPATH $BUILDTEST_ROOT
else
        setenv PYTHONPATH ${PYTHONPATH}:$BUILDTEST_ROOT
endif

echo "BUILDTEST_ROOT: $BUILDTEST_ROOT"
set buildtest_path=`which buildtest`
echo "buildtest command: ${buildtest_path}"
