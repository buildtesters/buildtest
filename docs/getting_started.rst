.. _Getting Started:

Getting Started with buildtest
==============================

Interacting with the client
---------------------------

After you install buildtest, you should find the client on your path::


      $ which buildtest
      ~/.local/bin/buildtest


At this point you've also already configured build test, and are either working
on a cluster with Lmod or have it installed. As a reminder:

 - The test directory is where tests will be written, which defaults to ``$HOME/.buildtest/testdir``.
 - You can store tests (that can be referenced with relative paths) under ``$HOME/.buildtest/site``.


Cloning Tutorials
-----------------

To get started, let's clone a repository with tutorial tests. Since this is a group of tests,
we can put it in our tests directory by using the "get" command::

    $ buildtest get https://github.com/HPC-buildtest/tutorials.git
    Cloning into '/home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials'...

Which would be equivalent to doing this::

    $ mkdir -p $HOME/.buildtest/site/github.com/HPC-buildtest
    $ git clone https://github.com/HPC-buildtest/tutorials.git $HOME/.buildtest/site/github.com/HPC-buildtest/tutorials

You can also clone a specific branch::

    $ buildtest get -b add/hello-world-test https://github.com/HPC-buildtest/tutorials.git

And in either case, if the folder already exists, you'll be told::

    $ buildtest get https://github.com/HPC-buildtest/tutorials.git
    /home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials already exists. Remove and try again.

The tests are organized by their namespace, meaning that you'll find GitHub repos organized under
github.com, then the organization or username, and then the repository name.


Create a Test Configuration
---------------------------

We can refer to a config as a relative path to the test config root at ``$HOME/.buildtest/site`` or
we can provide a relative path to a config file anywhere on our system. Let's start
with the latter, and change directory to interact with our test configurations::

    $ cd /home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials


Let's take a look at the simplest of examples - a "Hello buildtest" example! This is
located in ``hello-world``::

    $ cd hello-world

Let's take a quick look at the structure of the folder here::


    $ tree
    .
    ├── hello.sh.yml
    └── src
        └── hello.sh

    1 directory, 2 files


The yaml (extension ``yml`` above) files in the root of the folder are test configurations.
This means that we write here the commands, environment, and other variables that are needed
for the test. Notice that the naming is in the format of ``[name][language].yml``. We know off
the bat that this is intended to test a bash script. Let's take a look at the file::


    testtype: singlesource
    scheduler: local
    description: Hello World buildtest Example
    maintainer:
    - vsoch

    program:
      source: hello.sh
    

You'll see that most of the file is metadata. The testtype ``singlesource`` is exactly
what it sounds like - we are going to run a single script, the program ``hello.sh``.
There are no surprises here::


    $ cat src/hello.sh 
    #!/bin/bash

    printf "Hello buildtest\n"


On a high level, the scripts you will run to test and other source files will
be located in the ``src`` folder of a test root, directly under one or more
configurations that reference them.


Run the Test Configuration
---------------------------

Let's run our test! We could be doing this from a relative path to the test configuration
file, **or** as a relative path from the root of our testdir at ``$HOME/.buildtest/site``
For example, either of the two would work in the case of this test::

    $ buildtest build -c github.com/HPC-buildtest/tutorials/hello-world/hello.sh.yml
    $ buildtest build -c hello.sh.yml


**Note** This test is currently expected to work when the recipe types are updated.

Run a Compiler Configuration
----------------------------

The example above is relatively simple because we don't actually build anything.
However, buildtest is strongest in it's ability to model compilers and settings.
For this next example, let's run a configuration intended to test a fortran compiler.
Since we don't have it on the path, let's load "ifort" with a module::

    $ module load ifort


Now let's take at the recipe in the tutorials folder under ``compilers/hello.f.yml ``::


	testtype: singlesource
	description: Hello World Fortran example using Intel compiler
	scheduler: local

	program:
	  source: hello.f90
	  compiler: intel
	  fflags: -O2

	maintainer:
	- shahzeb siddiqui shahzebmsiddiqui@gmail.com


And here is how to run the build, and see the output on the screen::

    $ buildtest build -c compilers/hello.f.yml
    $ buildtest build -c hello.f.yml
    ________________________________________________________________________________
                             build time: 03/01/2020 10:24:04
                                command: buildtest build -c compilers/hello.f.yml
                test configuration root: /home/users/vsochat/.buildtest/site
                     configuration file: hello.f.yml
                              buildpath: /home/users/vsochat/.buildtest/testdir/build_7
                                logpath: /home/users/vsochat/.buildtest/testdir/build_7/log/buildtest_10_24_01_03_2020.log
    ________________________________________________________________________________



    STAGE                                    VALUE
    ________________________________________________________________________________
    [LOAD CONFIG]                            PASSED
    [SCHEMA CHECK]                           PASSED
    [PROGRAM LANGUAGE]                       fortran
    [COMPILER NAME]                          intel
    [WRITING TEST]                           PASSED
    [NUMBER OF TEST]                         1
    Running All Tests from Test Directory: /home/users/vsochat/.buildtest/testdir/build_7
    ==============================================================
                         Test summary
    Executed 1 tests

We can see the input paths and metadata for the build, along with the various steps (and if they
were successful) at the bottom. Note that the outputs for our build are in a "build_7" folder
under our buildest home testdir, we'll be looking at that next.


Inspect Results
---------------

Aside from the terminal print above, we might want to look at results, especially if the
build is not successful. buildtest by default creates a new build_x directory under
the buildtest home testdir (defaults to ``$HOME/.buildtest/testdir``) that contains
a script generated to run the build, a folder for logs, and a folder for run output.::


    $ tree /home/users/vsochat/.buildtest/testdir/build_7/
    ├── hello.f.yml.0x741db6a9.sh
    ├── log
    │   ├── buildtest_10_23_01_03_2020.log
    │   └── buildtest_13_49_29_02_2020.log
    └── run
        └── buildtest_10_23_01_03_2020.run

    2 directories, 4 files


If we look in the shell script at the top level, we see exactly what was run.::


	#!/bin/bash
	TESTDIR=/home/users/vsochat/.buildtest/testdir/build_6
	SRCDIR=/home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials/compilers/src
	SRCFILE=$SRCDIR/hello.f90
	FC=ifort
	FFLAGS="-O2"
	EXECUTABLE=hello.f.yml.0x741db6a9.exec

	cd $TESTDIR
	$FC $FFLAGS -o $EXECUTABLE $SRCFILE
	$EXECUTABLE
	rm ./$EXECUTABLE


And then if we look in the logs directory, we see verbose output for the entire build:: 

	2020-03-01 10:23:39,580 [build.py:58 - func_build_subcmd() ] - [INFO] Creating Directory: /home/users/vsochat/.buildtest/testdir/build_6
	2020-03-01 10:23:39,581 [build.py:59 - func_build_subcmd() ] - [DEBUG] Current build ID: 6
	2020-03-01 10:23:39,586 [singlesource.py:410 - __init__() ] - [DEBUG] Source Directory: /home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials/compilers/src
	2020-03-01 10:23:39,586 [singlesource.py:411 - __init__() ] - [DEBUG] Source File: hello.f90
	2020-03-01 10:23:39,725 [singlesource.py:705 - build_test_content() ] - [DEBUG] testpath:/home/users/vsochat/.buildtest/testdir/build_6/hello.f.yml.0x741db6a9.sh
	2020-03-01 10:23:39,725 [singlesource.py:705 - build_test_content() ] - [DEBUG] shell:['#!/bin/bash']
	2020-03-01 10:23:39,725 [singlesource.py:705 - build_test_content() ] - [DEBUG] module:None
	2020-03-01 10:23:39,726 [singlesource.py:705 - build_test_content() ] - [DEBUG] metavars:['TESTDIR=/home/users/vsochat/.buildtest/testdir/build_6', 'SRCDIR=/home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials/compilers/src', 'SRCFILE=$SRCDIR/hello.f90', 'FC=ifort', 'FFLAGS="-O2"', 'EXECUTABLE=hello.f.yml.0x741db6a9.exec']
	2020-03-01 10:23:39,726 [singlesource.py:705 - build_test_content() ] - [DEBUG] envs:[]
	2020-03-01 10:23:39,726 [singlesource.py:705 - build_test_content() ] - [DEBUG] build:['cd $TESTDIR', '$FC $FFLAGS -o $EXECUTABLE $SRCFILE']
	2020-03-01 10:23:39,726 [singlesource.py:705 - build_test_content() ] - [DEBUG] run:['$EXECUTABLE', 'rm ./$EXECUTABLE']
	2020-03-01 10:23:39,727 [writer.py:16 - write_test() ] - [INFO] Opening Test File for Writing: /home/users/vsochat/.buildtest/testdir/build_6/hello.f.yml.0x741db6a9.sh
	2020-03-01 10:23:39,733 [build.py:115 - func_build_subcmd() ] - [INFO] Reading Build Log File: /home/users/vsochat/.buildtest/var/build.json
	2020-03-01 10:23:39,734 [build.py:121 - func_build_subcmd() ] - [DEBUG] Adding latest build to dictionary
	2020-03-01 10:23:39,734 [build.py:122 - func_build_subcmd() ] - [DEBUG] {'TESTS': ['/home/users/vsochat/.buildtest/testdir/build_6/hello.f.yml.0x741db6a9.sh'], 'TESTDIR': '/home/users/vsochat/.buildtest/testdir/build_6', 'TESTCOUNT': 1, 'CMD': 'buildtest build -c hello.f.yml', 'BUILD_TIME': '03/01/2020 10:23:39', 'LOGFILE': '/home/users/vsochat/.buildtest/testdir/build_6/log/buildtest_10_23_01_03_2020.log'}
	2020-03-01 10:23:39,734 [build.py:123 - func_build_subcmd() ] - [INFO] Updating Build Log File: /home/users/vsochat/.buildtest/var/build.json
	2020-03-01 10:23:39,742 [file.py:119 - create_dir() ] - [DEBUG] Creating Directory: /home/users/vsochat/.buildtest/testdir/build_6/run


And finally,  the output file for the run is located in ``run``. 
This file can be very important, especially in the case of failed builds. 
For example, let's say that forgot to load the module "ifort." We would
have seen this output file instead, along with a failed build message::

	Test Name:/home/users/vsochat/.buildtest/testdir/build_6/hello.f.yml.0x741db6a9.sh
	Return Code: 1
	---------- START OF TEST OUTPUT ---------------- 
	/home/users/vsochat/.buildtest/testdir/build_6/hello.f.yml.0x741db6a9.sh: line 10: ifort: command not found
	/home/users/vsochat/.buildtest/testdir/build_6/hello.f.yml.0x741db6a9.sh: line 11: hello.f.yml.0x741db6a9.exec: command not found
	rm: cannot remove ‘./hello.f.yml.0x741db6a9.exec’: No such file or directory
	------------ END OF TEST OUTPUT ---------------- 

Next Steps
----------

We've just shown you how to target a specific configuration file. In fact, you
can use ``buildtest build`` to discover more than one configuration file,
either under a specific directory outside of your buildtest test config directory
or within it. For example, the following command will find either a ``hello.sh.yml``
that is located in your present working directory, or the first file named ``hello.sh.yml``
in your testing root at ``$HOME/.buildtest/site``::

	buildtest build -c hello.sh.yml

The following will target a specific file path under your test config root::


	buildtest build -c github.com/HPC-buildtest/tutorials/hello-world/hello.sh.ym


If you provide a directory name as a relative path, buildtest will discover all test configurations under it::


	buildtest build -c hello-world


And if you provide a relative path under the test config root, that directory will be targeted instead::


	buildtest build -c github.com/HPC-buildtest/tutorials/hello-world/


And of course you can provide a direct path to a single file, as we showed in the examples above.
