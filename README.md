## Application Testing
---
### Description
The BuildTest repository is a automatic framework for generating tests for software applications designed to work in a HPC environment.  This framework heavily relies on application to be built with [Lmod](https://github.com/TACC/Lmod) and [EasyBuild](https://github.com/hpcugent/easybuild-easyconfigs) 

---
### Setup
Specify your path for **BTMODROOT** (Module Tree Root) path in **setup.sh**.  This is used by **buildtest** to find all your modules in order to verify your test are generated based on your module environment. 

If you are using a Hierarchical Module Naming Scheme for your Module Trees, you would have the following directories. Please specify the parent directory as your BTMODROOT assuming this is where all your modules reside. 
```
Compiler
Core
MPI
```

For instance, my BTMODROOT on my system is set to /nfs/grid/software/testing/RHEL7/easybuild/modules/ 
```
hpcswadm@hpcv18$ls -l /nfs/grid/software/testing/RHEL7/easybuild/modules/
total 8
drwxr-xr-x 5 hpcswadm hpcswadm 4096 Mar 13 14:26 all
drwxr-xr-x 3 hpcswadm hpcswadm 4096 Mar 13 14:34 Tools

```
 
Once this is setup, you can check if your modules are picked up with **buildtest**



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
    
    	./testgen.sh -s netCDF -v 4.4.1 -b intel/2017.01  -m "<module>/<version> <module>/version ..."

```




Each test case will reside in a directory **$software/$version/$toolchain**. If no toolchain is specified the path will be be

**software/version/dummy/dummy**

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
 2. **singlesourcedirectory** -- A directory containing source files used for building test from source. Each test is mapped to a single source file. The test uses src/$software/template.sh script to generate the test. If your test fits in this method, then place the test in this directory.
 3. **env.sh** -- Initializes environment variables used for compiling code. For instance environment variables like CC, CXX, FC, F77, F90 are set accordingly if needed.
 

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


