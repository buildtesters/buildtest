#!/bin/bash

ml Anaconda3
conda create -y -n buildtest-check argcomplete PyYAML 
source activate buildtest-check
cd ~/github/buildtest-framework
rm dist/*
python setup.py sdist
pip install dist/*

cd $HOME
which _buildtest

sh ~/github/buildtest-framework/success_test.sh
rm -rf ~/.conda/envs/buildtest-check
