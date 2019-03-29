#!/bin/bash
module purge
module load GCC
gcc -O3 src/hello.c -o hello
./hello
rm ./hello
