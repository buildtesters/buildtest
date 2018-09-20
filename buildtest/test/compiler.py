############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""
This function calculates the compiler wrapper when generating source test

:author: Shahzeb Siddiqui (Pfizer)
"""

import os

def get_compiler(configmap,appname,tcname):
        """
         This function gets the appropriate compiler tag and compiler type based on the
         application/toolchain + file extension. Compiler/Wrappers can be
         gcc,icc,mpicc,nvcc,javac,python,R,perl,etc...
         """

        # if app is GCC, GCCcore, -> compiler = gcc
        # if app toolchain is GCC, GCCcore, dummy -> compiler = gcc
        # if app is intel -> compiler = icc/mpiicc -> need tag: mpi=enabled
        # if app is python, tc=X -> compiler = python
        # if app is OpenMPI,MPICH,MVAPICH, tc=X -> compiler = mpicc
        # if app is CUDA, tc=X -> compiler = nvcc
        # if app is X, tc=gcccuda, compiler = gcc/nvcc need tag: cuda=enabled

        # if cuda enabled in YAML
        cuda = ""
        # if mpi is enabled in YAML
        mpi = ""
        if "cuda" in configmap:
                cuda=configmap["cuda"]
        if "mpi" in configmap:
                mpi=configmap["mpi"]

        # get extension for source file
        ext = os.path.splitext(configmap["source"])[1]
        compiler=""

        # compiler_type valid may be "gnu, intel, mpi, intel-mpi, R, java, python"
        compiler_type=""

        # condition to calculate compiler_type based on toolchain
        if tcname in ["GCC","GCCcore","gcccuda","dummy","gompi", "foss","goolfc"]:
                compiler_type="gnu"
        if tcname in ["intel", "iccifort","iccifortcuda","impi","iimpi","iimpic"]:
                compiler_type="intel"

        # if application is intel then compiler_type will be intel
        if appname in ["intel"]:
                compiler_type="intel"

        # if application is GCC then compiler type is gnu
        if appname in ["GCC", "GCCcore"]:
                compiler_type = "gnu"

        if appname in ["Java"]:
                compiler = "javac"
                compiler_type = "java"
                return compiler,compiler_type
        if appname in ["CUDA"]:
                compiler = "nvcc"
                compiler_type = "cuda"
                return compiler,compiler_type

        # MPI apps built with any toolchain (intel, gcc, pgi) will default to gnu. This is because all of these apps provide
        # mpicc, mpifort, mpic++. While intel mpi provides mpiicc, mpiifort, mpiic++
        if appname in ["MPICH","OpenMPI","MVAPICH"]:
                compiler_type="gnu"


        # determine compiler based on compiler_type and its file extension

        # perl extension
        if ext == ".py":
                compiler_type = "python"
                compiler = "python "
                return compiler,compiler_type
        if ext == ".pl":
                compiler_type = "perl"
                compiler = "perl"
                return compiler,compiler_type
        if ext == ".R":
                compiler_type = "R"
                compiler = "Rscript "
                return compiler,compiler_type
        # C extension
        if ext == ".c":
                if compiler_type == "gnu":
                        # set compiler to nvcc when cuda is enabled
                        if cuda == "enabled":
                                compiler="nvcc"
                        # set compiler to mpicc when mpi is enabled
                        elif mpi == "enabled":
                                compiler="mpicc"
                        else:
                                compiler="gcc"
                elif compiler_type == "intel":
                        # mpi test in intel test needs a check for mpi=enabled field to determine which wrapper to use
                        if mpi=="enabled":
                                compiler="mpiicc"
                        else:
                                compiler="icc"
        # C++ extension
        elif ext == ".cpp":
                if compiler_type == "gnu":
                        # set compiler to nvcc when cuda is enabled
                        if cuda == "enabled":
                                compiler="nvcc"
                        # set compiler to mpicc when mpi is enabled
                        elif mpi == "enabled":
                                compiler="mpic++"
                        else:
                                compiler="g++"
                elif compiler_type == "intel":
                        if mpi=="enabled":
                                compiler="mpiic++"
                        else:
                                compiler="icpc"
        # Fortran extension
        elif ext == ".f90" or ext == ".f" or ext == ".f77":
                if compiler_type == "gnu":
                        # set compiler to nvcc when cuda is enabled
                        if cuda == "enabled":
                                compiler="nvcc"
                        # set compiler to mpicc when mpi is enabled
                        elif mpi == "enabled":
                                compiler="mpifort"
                        else:
                                compiler="gfortran"
                elif compiler_type == "intel":
                        if mpi=="enabled":
                                compiler="mpiifort"
                        else:
                                compiler="ifort"

        return compiler,compiler_type
