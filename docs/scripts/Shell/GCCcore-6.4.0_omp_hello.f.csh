#!/bin/csh
module purge 
module load GCCcore/6.4.0
setenv OMP_NUM_THREADS 2
gfortran -o omp_hello.f.exe /home/siddis14/github/buildtest-configs/buildtest/source/gcccore/code/omp_hello.f -O2 -fopenmp
./omp_hello.f.exe