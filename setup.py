from setuptools import setup, find_packages

import os
import sys

from buildtest import BUILDTEST_VERSION

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
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["PyYAML>=5.2", "distro==1.4.0", "jsonschema==3.0.2",],
    entry_points={"console_scripts": ["buildtest=buildtest.main:main"]},
)
