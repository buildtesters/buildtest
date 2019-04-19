#!/bin/sh
module purge
module load eb/2018 
export OMP_NUM_THREADS=2
cd /home/siddis14/buildtest/suite/openmp/dotprod
gcc -o omp_dotprod.c.exe /home/siddis14/buildtest-framework/toolkit/buildtest/suite/openmp/dotprod/src/omp_dotprod.c -fopenmp 
./omp_dotprod.c.exe 
rm ./omp_dotprod.c.exe 
