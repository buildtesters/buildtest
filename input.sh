#!/bin/sh
./buildtest -s GCC -v 5.4.0-2.27 
./buildtest -s GCC -v 6.2.0-2.27 
./buildtest -s intel -v 2017.01
./buildtest -s CMake -v 3.7.1 -b GCCcore/.5.4.0
./buildtest -s Java -v 1.8.0_92
./buildtest -s git -v 2.10.2 -b GCCcore/.5.4.0
./buildtest -s Python -v 2.7.12 -b foss/.2016.03
./buildtest -s hwloc -v 1.11.3 -b GCC/5.4.0-2.27
./buildtest -s numactl -v 2.0.11 -b GCC/5.4.0-2.27
./buildtest -s CUDA -v 8.0.44 -b GCC/5.4.0-2.27
./buildtest -s OpenMPI -v 2.0.0 -b GCC/5.4.0-2.27
./buildtest -s OpenMPI -v 2.0.1 -b GCC/6.2.0-2.27
./buildtest -s Bowtie2 -v 2.2.9 -b GCCcore/.5.4.0


