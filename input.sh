#!/bin/sh

# This file serves the purpose for building test in batch for multiple apps. Edit this file as needed
python buildtest.py -s GCC/5.4.0-2.27 
python buildtest.py -s GCC/6.2.0-2.27 
python buildtest.py -s intel/2017.01
python buildtest.py -s CMake/3.7.1 -t GCCcore/.5.4.0
python buildtest.py -s Java/1.8.0_92
python buildtest.py -s git/2.10.2 -t GCCcore/.5.4.0
python buildtest.py -s Python/2.7.12 -t foss/.2016.03
python buildtest.py -s hwloc/1.11.3 -t GCC/5.4.0-2.27
python buildtest.py -s hwloc/1.11.3 -t GCC/6.2.0-2.27
python buildtest.py -s numactl/2.0.11 -t GCC/5.4.0-2.27
python buildtest.py -s numactl/2.0.11 -t GCC/6.2.0-2.27
python buildtest.py -s CUDA/8.0.44 -t GCC/5.4.0-2.27
python buildtest.py -s OpenMPI/2.0.0 -t GCC/5.4.0-2.27
python buildtest.py -s OpenMPI/2.0.1 -t GCC/6.2.0-2.27
python buildtest.py -s OpenMPI/2.0.2 -t iccifort/.2017.1.132-GCC-5.4.0-2.27
python buildtest.py -s Bowtie2/2.2.9 -t GCCcore/.5.4.0
python buildtest.py -s Bowtie/1.1.2 -t GCCcore/.5.4.0
python buildtest.py -s binutils/.2.27 
python buildtest.py -s Anaconda2/4.2.0 -t GCC/5.4.0-2.27
python buildtest.py -s netCDF/4.4.1 -t intel/2017.01
python buildtest.py -s  HMMER/3.1b2 -t GCCcore/.5.4.0
python buildtest.py -s FastQC/0.11.5-Java-1.8.0_92 -t GCCcore/.5.4.0
python buildtest.py -s seqtk/1.2 -t GCCcore/.5.4.0
python buildtest.py -s PCRE/8.38 -t GCC/5.4.0-2.27
python buildtest.py --system all

