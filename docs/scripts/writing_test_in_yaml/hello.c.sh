#!/bin/sh
module purge
module load GCC/5.4.0-2.27
gcc -o hello.c.exe /hpc/grid/scratch/workspace/BuildTest/BuildTest/source/GCC/code/hello.c -O2
./hello.c.exe

