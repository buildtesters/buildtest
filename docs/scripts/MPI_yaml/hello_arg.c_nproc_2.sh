#!/bin/sh
module purge
module load GCC/5.4.0-2.27
module load OpenMPI/2.0.0
mpicc -o hello_arg.c.exe /hpc/grid/hpcws/hpcengineers/siddis14/buildtest-framework/buildtest-configs/mpi/code/hello_arg.c
mpirun -np 2 ./hello_arg.c.exe hi how are you
