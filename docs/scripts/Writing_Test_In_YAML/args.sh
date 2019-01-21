#!/bin/sh
module purge
module load foss/.2016.03
module load Python/2.7.12
python  /hpc/hpcswadm/buildtest/buildtest-configs/ebapps/Python/code/arg.py hello world
