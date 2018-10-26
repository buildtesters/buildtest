#!/bin/bash

VERSION=0.6.2
cd ~/github/buildtest-framework
rm dist/*
python setup.py sdist
twine upload -r pypi dist/*


# building python wheel for R-buildtest-config
cd ~/github/R-buildtest-config/
rm dist/*
python setup.py sdist
twine upload -r pypi  dist/*


# building python wheel for Python-buildtest-config
cd ~/github/Python-buildtest-config/
rm dist/*
python setup.py sdist
twine upload -r pypi  dist/*


# building python wheel for Ruby-buildtest-config
cd ~/github/Ruby-buildtest-config/
rm dist/*
python setup.py sdist
twine upload  -r pypi dist/*



# building python wheel for Perl-buildtest-config
cd ~/github/Perl-buildtest-config/
rm dist/*
python setup.py sdist
twine upload -r pypi  dist/*

cd ~/github/buildtest-configs
rm dist/*
python setup.py sdist
twine upload -r pypi dist/*

exit 
ml Anaconda3
conda create -n buildtest-$VERSION python=3.6
source activate buildtest-$VERSION
pip install buildtest-framework

cd $HOME
which _buildtest

