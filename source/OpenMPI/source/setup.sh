#!/bin/sh
# use mpifort rather than mpif77 and mpif90 since it will be deprecated
export CC=mpicc
export CXX=mpicxx
export FC=mpifort
export F77=mpifort
export F90=mpifort
