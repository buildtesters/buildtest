############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-configs
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

from setuptools import setup,find_packages

VERSION='0.6.1'
setup(
      name='buildtest-configs',
      version=VERSION,
      description="""Test configuration for buildtest-framework""",
      long_description=open('README.rst').read(),
      url='https://github.com/HPC-buildtest/buildtest-configs',
      author='Shahzeb Siddiqui',
      author_email='shahzebmsiddiqui@gmail.com',
      license='GPLv2',
      classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
      ),
      platforms = "Linux",
      packages=find_packages(),
      include_package_data=True,
      install_requires = [ 'buildtest-framework=='+VERSION ],
      )
