#!/bin/sh
module purge
module load GCC/5.4.0-2.27
module load OpenMPI/2.0.0
mpicc -o mpi_mm.c.exe /hpc/grid/scratch/workspace/BuildTest/source/ebapps/OpenMPI/code/mpi_mm.c -O2
mpirun -np 4 ./mpi_mm.c.exe

