#!/bin/bash

cd ~/github/buildtest-framework
rm dist/*
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*


# building python wheel for R-buildtest-config
cd ~/github/R-buildtest-config/
rm dist/*
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*


# building python wheel for Python-buildtest-config
cd ~/github/Python-buildtest-config/
rm dist/*
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*


# building python wheel for Ruby-buildtest-config
cd ~/github/Ruby-buildtest-config/
rm dist/*
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*



# building python wheel for Perl-buildtest-config
cd ~/github/Perl-buildtest-config/
rm dist/*
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

cd ~/github/buildtest-configs
rm dist/*
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

exit 
pip install -i https://test.pypi.org buildtest-framework
