## Application Testing
---
### Description
The BuildTest repository is an **Automatic Test Generation Framework** for writing test cases suited to work well in a HPC environment.  This framework heavily relies that your application is built with  [EasyBuild](https://github.com/hpcugent/easybuild-easyconfigs)  and your system has  [Lmod](https://github.com/TACC/Lmod) or [Environment Modules](http://modules.sourceforge.net/) for managing modules

---
### Setup
Specify your path for **BUILDTEST_MODROOT** (Module Tree Root) path in **setup.sh**.  This is used by **buildtest** to find all your modules in order to verify your test are generated based on your module environment. 

If you are using a **"Hierarchical Module Naming Scheme"** for your Module Naming Scheme, you would have the following directories.  
```
Compiler
Core
MPI
```
Specify the directory where you see these directories as your path for **BUILDTEST_MODROOT** assuming this is where all your modules reside.

For instance, my **BUILDTEST_MODROOT** on my system is set to **/nfs/grid/software/testing/RHEL7/easybuild/modules/all** 
```
[hpcswadm@amrndhl1157 BuildTest]$ ls -l /nfs/grid/software/testing/RHEL7/easybuild/modules/all/
total 12
drwxr-xr-x  6 hpcswadm hpcswadm 4096 Mar 21 10:56 Compiler
drwxr-xr-x 14 hpcswadm hpcswadm 4096 Mar 21 10:41 Core
drwxr-xr-x  3 hpcswadm hpcswadm 4096 Mar 21 00:54 MPI
```
 
Once this is setup, you can check if your modules are picked up by running **buildtest -l**

Easyconfig setup with BuildTest
----------------

BuildTest utilizes the easyconfig files as part of the verification process to ensure test are created based on the module files and the toolchain used by Easybuild. The buildtest does a 2-step verification to make sure the test are created for the correct software package.

**Module File Verification:** buildtest makes use of **$BUILDTEST_MODROOT** to find all the modules and stores the values in an array. Whenever an argument is passed for **--software** and **--version** it is checked with the module array to make sure it exist. If there is no module found with the following name, the program will halt because the test relies upon loading the module before running the test

**Easyconfig Toolchain verification:** Each software version is built with a particular toolchain in EasyBuild. In order to make sure we are building for the correct test in the event of multiple packages being installed with different toolchain we need a way to classify which package to use. 

For instance if **flex/2.6.0** is installed with **GCCcore/5.4.0**, **GCCcore/6.2.0**, **dummy** toolchain then we have three instances of this package in different module trees. We can perform this test by searching all the easyconfig files with the name flex-2.6.0 and search for the tag **toolchain = { name='toolchain-name', version='toolchain-version' }**

Module File Check is not sufficient for checking modules in the event when there is a match for a software package but there is a toolchain mismatch. For instance if Python 2.7.12 is built with foss toolchain only and the user request to build Python 2.7.12 with intel, the module file verification will pass but it wouldn't pass the Toolchain verification stage. 

In order for this to work properly, clone your easyconfig repository that you used to install your software packages on the cluster in the top level directory. 

Next specify the path for **$BUILDTEST_EASYCONFIGDIR** to the path where your easyconfig files reside. 

**Note: Keep this repository up to date as you build new software packages**

Usage
-----

```
Usage: buildtest 
   -s --software 	  application name. This must match the module name

   -v --version		  application version. This must match the module version

   -m --modules		  adding extra modules prior to loading application. Use 
			  this to resolve dependencies, if it is not captured in 
			  module file

   -l --list		  List current modules in the system based on variable BTMODROOT. 
			  Check setup.sh to see the path for BTMODROOT

   -b --buildtoolchain	  The toolchain used to build the package. This refers to the EasyBuild toolchain
			  used for building the package. Check your easyconfig to see what toolchain you used. 
	
			  If a package is built with dummy toolchain don't specify this paramter. 
		          Test directory format: <software>/<version>/<toolchain>/<test>.sh
			
			  Toolchain module must be present in order for test to be created.

   -h --help   		  displays basic help

Example:
    1. 	Run test for software GCC version 5.4.0-2.27
       	
    	./buildtest -s GCC -v 5.4.0-2.27

    2. Run test for Python version 2.7.12 built with foss .2016.03  toolchain.
    	./buildtest -s Python -v 2.7.12 -b foss/.2016.03

    3.	Modules should be passed in quotation if adding multiple modules to path
    
    	./buildtest -s netCDF -v 4.4.1 -b intel/2017.01  -m "<module>/<version> <module>/version ..."

```




Each test case will reside in a directory **$software/$version/$toolchain**. If no toolchain is specified the path will be **software/version/dummy/dummy**

All tests are recorded in the directory **testing**.

 - Testing Structure Layout
	 - **testing/CMakeLists.txt**  - List of entries for each software 
	 - **testing/$software/CMakeLists.txt** - List of version entries for each software
	 - **testing/$software/$version/CMakeLists.txt** - List of toolchain entries for each version of the software
	 - **testing/$software/$version/$toolchain-name/CMakeLists.txt** - Entry for each toolchain version
	 - **testing/$software/$version/$toolchain-name/$toolchain-version/CMakeLists.txt** - Entry for each test to run 


Whenever you build the test, you must specify the software and version and this must match the name of the module you are trying to test, otherwise there is no way of knowing what is being tested.  Each test will attempt to load the application module along with the toolchain if specified prior to anything.


### Code repository
The code repository is a collection of code examples for each application. 
Each application will have a directory **src/$software** will have the following
 1. **command.txt** - This file keeps a record of what binary comands to test. Each binary command can have a paramter used to test the particular command. 
	 ```
	 hpcswadm@hpcv18$cat GCC/command.txt 
	c++ --version
	cpp --version
	g++ --version
	gcc --version
	gcc-ar --version
	gcc-nm --version
	gcc-ranlib --version
	gcov --version
	gcov-tool --version
	gfortran --version
	 ```
 2. **generic** -- A directory containing source files used to work with template/generic.sh. Each test is mapped to a single source file. If your test fits in this method, then place the test in this directory.
 3. **mpi** -- A directory containing MPI source files used to work with template/mpi.sh. 
 3. **custom** -- A directory that needs a custom template in order to generate test. The template file is in **src/$software/custom/template.sh**. Each test has 1-1 mapping to a source file. A **setup.sh** file can be specified in this directory if needed, otherwise it will use **src/setup.sh** 

setup.sh file is used to set CC, CXX, FC, F77, F90 are set accordingly if needed.
 

### Testing

In order to test your scripts, make sure you have cmake version 2.8 or higher. The test will be executed using the ctest utility provided by cmake package. 


```
> cmake --version
cmake version 2.8.11

> mkdir build
> cd build 

> cmake ..
-- The C compiler identification is GNU 4.8.5
-- The CXX compiler identification is GNU 4.8.5
-- Check for working C compiler: /bin/cc
-- Check for working C compiler: /bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working CXX compiler: /bin/c++
-- Check for working CXX compiler: /bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Configuring done
-- Generating done
-- Build files have been written to: /hpc/hpcswadm/backup/applicationtesting/build

hpcswadm@hpcv18$ctest -I 1,10
Test project /hpc/hpcswadm/applicationtesting/build
      Start  1: GCC-5.4.0-2.27-dummy-dummy-c++
 1/10 Test  #1: GCC-5.4.0-2.27-dummy-dummy-c++ ..........   Passed    0.23 sec
      Start  2: GCC-5.4.0-2.27-dummy-dummy-cpp
 2/10 Test  #2: GCC-5.4.0-2.27-dummy-dummy-cpp ..........   Passed    0.23 sec
      Start  3: GCC-5.4.0-2.27-dummy-dummy-g++
 3/10 Test  #3: GCC-5.4.0-2.27-dummy-dummy-g++ ..........   Passed    0.24 sec
      Start  4: GCC-5.4.0-2.27-dummy-dummy-gcc
 4/10 Test  #4: GCC-5.4.0-2.27-dummy-dummy-gcc ..........   Passed    0.24 sec
      Start  5: GCC-5.4.0-2.27-dummy-dummy-gcc-ar
 5/10 Test  #5: GCC-5.4.0-2.27-dummy-dummy-gcc-ar .......   Passed    0.24 sec
      Start  6: GCC-5.4.0-2.27-dummy-dummy-gcc-nm
 6/10 Test  #6: GCC-5.4.0-2.27-dummy-dummy-gcc-nm .......   Passed    0.24 sec
      Start  7: GCC-5.4.0-2.27-dummy-dummy-gcc-ranlib
 7/10 Test  #7: GCC-5.4.0-2.27-dummy-dummy-gcc-ranlib ...   Passed    0.23 sec
      Start  8: GCC-5.4.0-2.27-dummy-dummy-gcov
 8/10 Test  #8: GCC-5.4.0-2.27-dummy-dummy-gcov .........   Passed    0.23 sec
      Start  9: GCC-5.4.0-2.27-dummy-dummy-gcov-tool
 9/10 Test  #9: GCC-5.4.0-2.27-dummy-dummy-gcov-tool ....   Passed    0.23 sec
      Start 10: GCC-5.4.0-2.27-dummy-dummy-gfortran
10/10 Test #10: GCC-5.4.0-2.27-dummy-dummy-gfortran .....   Passed    0.24 sec


```
