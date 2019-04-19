#!/bin/sh
module purge
module load eb/2018 
cd /home/siddis14/buildtest/suite/compilers/helloworld
g++ -O3 -o hello.cpp.exe /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/src/hello.cpp 
./hello.cpp.exe 
rm ./hello.cpp.exe 
