#!/bin/csh
module purge 
module load GCCcore/6.4.0
setenv OMP_NUM_THREADS 2
gcc -o omp_mm.c.exe /home/siddis14/github/buildtest-configs/buildtest/source/gcccore/code/omp_mm.c -O2 -fopenmp
./omp_mm.c.exe