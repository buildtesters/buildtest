from setuptools import setup, find_packages

import os
import sys

sys.path.insert(0, os.path.abspath("src"))

from buildtest.tools.config import BUILDTEST_VERSION

setup(
    name="buildtest-framework",
    version=BUILDTEST_VERSION,
    author="Shahzeb Siddiqui",
    author_email="shahzebmsiddiqui@gmail.com",
    description="HPC Application Testing Framework",
    long_description=open("README.rst").read(),
    url="https://github.com/HPC-buildtest/buildtest-framework",
    license="GPLv2",
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
    scripts=["buildtest",],
    install_requires=[
        "argcomplete",
        "PyYAML",
        "buildtest-configs==" + BUILDTEST_VERSION,
        "Python-buildtest-config==" + BUILDTEST_VERSION,
        "Perl-buildtest-config==" + BUILDTEST_VERSION,
        "Ruby-buildtest-config==" + BUILDTEST_VERSION,
        "R-buildtest-config==" + BUILDTEST_VERSION,
    ],
)
