#!/bin/bash

ml Anaconda3
conda create -y -n buildtest-check argcomplete PyYAML 
source activate buildtest-check
# building python wheel for buildtest-framework
cd ~/github/buildtest-framework
rm dist/*
python setup.py sdist


# building python wheel for R-buildtest-config
cd ~/github/R-buildtest-config/
rm dist/*
python setup.py sdist


# building python wheel for Python-buildtest-config
cd ~/github/Python-buildtest-config/
rm dist/*
python setup.py sdist


# building python wheel for Ruby-buildtest-config
cd ~/github/Ruby-buildtest-config/
rm dist/*
python setup.py sdist


# building python wheel for Perl-buildtest-config
cd ~/github/Perl-buildtest-config/
rm dist/*
python setup.py sdist

pip install dist/* ~/github/R-buildtest-config/dist/* ~/github/Python-buildtest-config/dist/* ~/github/Perl-buildtest-config/dist/* ~/github/Ruby-buildtest-config/dist/*

cd $HOME
which _buildtest

sh ~/github/buildtest-framework/success_test.sh
rm -rf ~/.conda/envs/buildtest-check

conda create -y -n 
