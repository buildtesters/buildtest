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

from distutils.core import setup


setup(name='buildtest-framework',
      version='0.2.0',
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
            "Programming Language :: Python :: 2.6",
            "Topic :: Software Development :: Build Tools",
            "Topic :: Software Development :: Testing",
       ],
      zip_safe=False)
