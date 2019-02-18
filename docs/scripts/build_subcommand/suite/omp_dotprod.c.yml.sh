#!/bin/sh
module purge 
module load GCC
export OMP_NUM_THREADS=2 
cd /tmp/buildtest/tests/suite/openmp/dotprod
gcc -o omp_dotprod.c.exe /home/siddis14/github/buildtest-configs/buildtest/suite/openmp/dotprod/src/omp_dotprod.c -fopenmp 
./omp_dotprod.c.exe
rm ./omp_dotprod.c.exe
