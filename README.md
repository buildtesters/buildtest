## Application Testing
---
### Description
The Application Testing repository consist of test cases designed to test the software packages after installation. Each test is designed to check a specific functionality of the application. In most cases, the return code is checked to see if the command was executed successfully. 

---
### Setup
In order to write your test cases, please use the testgen script to generate your template test case. Afterward make any changes necessary appropriate for the test case.

The testgen.sh script is designed to test binaries, for instance if you want to write a test case to test a specific binary this can be done very quickly. The script testgen.sh will use the template file generic.txt in order to write the test case. Templates files can be found in the directory **template** 

Please refer to **help** command in order to learn how to use the testgen.sh. Simply type **testgen.sh --help**

Each test case will reside in a directory $software/$version/$toolchain where software and version are specified in the testgen.sh script. The software and version must match the name of the module you are trying to test because it will use this for loading the appropriate module and put that in the test case. Software built with a Toolchain must be specified when writing the test in order to create the test properly. Toolchain will automatically be added in the script as part of module load.

The command used to generate the  test case will be recorded in a file $software>/$version/$toolchain/input.txt. 

### Code repository

The testgen script can be used for building from source code. In order to reuse code for different application, we have placed the source code in **src** directory which can be used by testgen to generate scripts. See **testgen --help** for more information on how to build from source

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


> ctest .
hpcswadm@hpcv18$ctest .
Test project /hpc/hpcswadm/backup/applicationtesting/build
      Start  1: GCC-5.2.0-dummy-dummy-gcc
 1/71 Test  #1: GCC-5.2.0-dummy-dummy-gcc .....................................   Passed    0.27 sec
      Start  2: GCC-5.2.0-dummy-dummy-gfortran
 2/71 Test  #2: GCC-5.2.0-dummy-dummy-gfortran ................................   Passed    0.17 sec
      Start  3: GCC-5.2.0-dummy-dummy-g++
 3/71 Test  #3: GCC-5.2.0-dummy-dummy-g++ .....................................   Passed    0.17 sec
      Start  4: GCC-5.2.0-dummy-dummy-hello_c
 4/71 Test  #4: GCC-5.2.0-dummy-dummy-hello_c .................................   Passed    0.20 sec
      Start  5: GCC-5.2.0-dummy-dummy-hello_fortran
 5/71 Test  #5: GCC-5.2.0-dummy-dummy-hello_fortran ...........................   Passed    0.20 sec
      Start  6: GCC-5.2.0-dummy-dummy-hello_cpp
 6/71 Test  #6: GCC-5.2.0-dummy-dummy-hello_cpp ...............................   Passed    0.35 sec
      Start  7: GCC-6.2.0-dummy-dummy-gcc

```


