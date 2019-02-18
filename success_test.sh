#!/bin/bash
buildtest --help
buildtest -V
buildtest list -ls
buildtest list -svr
buildtest list -ec
buildtest find -fc all
buildtest find -ft all 
buildtest show -c
buildtest show -k singlesource
#buildtest --scantest
buildtest --clean-logs
buildtest build -p gcc
buildtest --logdir /tmp build -p gcc 
buildtest build -S compilers
buildtest run -S compilers
buildtest build -S openmp
buildtest run -S openmp
buildtest build -S cuda
buildtest run -S cuda
buildtest build -S cuda -s CUDA/7.5.18
buildtest run -S cuda
#buildtest build -s GCCcore/6.4.0 --shell csh
#buildtest build -s GCCcore/6.4.0 --enable-job

#buildtest build -s Python/2.7.14-intel-2018a --python-package dateutil
#buildtest build -s R/3.4.3-intel-2018a-X11-20171023 --r-package abc
#buildtest build -s Ruby/2.5.0-intel-2018a --ruby-package addressable
#buildtest build -s Perl/5.26.0-GCCcore-6.4.0 --perl-package AnyData
