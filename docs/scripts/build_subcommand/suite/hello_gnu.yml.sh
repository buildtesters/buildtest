#!/bin/sh
module purge 
module load GCC
cd /tmp/buildtest/tests/suite/compilers/helloworld
g++ -O3 -o hello.cpp.exe /home/siddis14/github/buildtest-configs/buildtest/suite/compilers/helloworld/src/hello.cpp 
./hello.cpp.exe
rm ./hello.cpp.exe
