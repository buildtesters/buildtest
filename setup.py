from setuptools import setup, find_packages

import os
import sys

from buildtest import BUILDTEST_VERSION

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
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.6",
            "Topic :: Software Development :: Build Tools",
            "Topic :: Software Development :: Testing",
       ],
       packages=find_packages(),
       include_package_data=True,
       install_requires = [
            "argcomplete==1.9.5", 
            "PyYAML>=5.1",
            "distro==1.4.0",
            "termcolor==1.1.0",
       ],
       entry_points = {'console_scripts': ['buildtest=buildtest.main:main']}
)
