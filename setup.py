############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#    This file is part of buildtest.
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
@author: Shahzeb Siddiqui (Pfizer)
"""

from setuptools import setup, find_packages
from buildtest.tools.config import BUILDTEST_VERSION

setup(name='buildtest-framework',
      version=BUILDTEST_VERSION,
      author='Shahzeb Siddiqui',
      author_email='shahzebmsiddiqui@gmail.com',
      description='HPC Application Testing Framework',
      long_description=open('README.rst').read(),
      url="https://github.com/HPC-buildtest/buildtest-framework",
      license='GPLv2',
      classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.6",
            "Topic :: Software Development :: Build Tools",
            "Topic :: Software Development :: Testing",
       ],
       packages=find_packages(),
       include_package_data=True,
       scripts = [
        '_buildtest',
       ],
       install_requires = [
            "argcomplete",
            "PyYAML",
        "buildtest-configs=="+BUILDTEST_VERSION,
	    "Python-buildtest-config=="+BUILDTEST_VERSION,
	    "Perl-buildtest-config=="+BUILDTEST_VERSION,
	    "Ruby-buildtest-config=="+BUILDTEST_VERSION,
	    "R-buildtest-config=="+BUILDTEST_VERSION,
       ]
)
