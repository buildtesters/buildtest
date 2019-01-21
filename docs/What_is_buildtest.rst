.. _What_is_buildtest:

What is buildtest
=================


.. contents::
   :backlinks: none


Description
-----------

**buildtest** is an Automated Test Generating Framework for writing test cases
efficiently and quickly for scientific applications. buildtest will generate
test scripts for any app & version automatically and tests can be recreated as
many times. buildtest makes use of EasyBuild_ easyconfig files to determine
which module + toolchain to use. You will need module environment
EnvironmentModules_ or Lmod_ on your system to use this framework

.. _EasyBuild: https://easybuild.readthedocs.io/en/latest/
.. _EnvironmentModules: http://modules.sourceforge.net/
.. _Lmod: https://github.com/TACC/Lmod


Motivation
-----------

A typical HPC facility supports hundreds of applications that is supported by the HPC team.
Building these software is a challnege and then figuring out how this software stack behaves
due to system changes (OS release, kernel path, glibc, etc...).

Application Testing is difficult. Commercial and open-source application typically provide
test scripts such as **make test** or **ctest** that can test the software after building
(**make**) step. Unfortunately, these methods perform tests prior to installation so
the ability to test software in production is not possible. One could try to change the
the vendor test script to the install path but this requires significant change into
a complex makefile

Writing test scripts manually can be tedious, also there is no sharing of tests
and most likely they are not compatible to work with other HPC sites because of different
software stack and hardcoded paths specific to the site. Easybuild
takes a step at improving application build process by automating the entire
software workflow that can be built on any HPC site .

buildtest takes a similar approach as EasyBuild but focusing on application
testing.



Objectives
-----------

buildtest will focus on the following key elements

        1. Provide a test toolkit with  examples for verifying software stack
        2. Ability to share test toolkit with the HPC community
        3. Parameterize tests and jobs for OpenMP, MPI to observe relationship with varying process/thread configuration
        4. Generate tests to be run with job scheduler to verify apps work on all compute nodes
        5. Provide performance metrics for tests scripts
        6. Integrate benchmarks to buildtest for stress testing
        7. Generate report for each test used for post-processing


buildtest framework
-------------------

buildtest is a python script that can generate self-contained testscripts in
shellscript. The test scripts can be run independently but they are
designed to work in CMake_ CTest Framework.

buildtest can do the following:

 - Creates test for binary testing, scripting tests, and compilation tests
 - Verify modulefile can be loaded.
 - generate tests for system packages
 - List software packages provided by MODULEPATH
 - List available toolchains
 - List software packages by versions
 - Support for logging
 - Search for YAML and test scripts
 - build tests easily for scripting languages (R, Python, Perl, Ruby, Tcl)
 - Run tests through an interactive menu
 - Scan tests and report which ones can be built with buildtest
 - build test for different shells (csh, bash, sh)
 - Generate job submission scripts for each test
 - build YAML configuration from buildtest for system & easybuild package

.. _CMake: https://cmake.org/documentation/

Github
------

buildtest is available on Github at https://github.com/HPC-buildtest

The project is divided into several repos.

- https://github.com/HPC-buildtest/buildtest-framework - This repo is the framework used to drive buildtest
- https://github.com/HPC-buildtest/buildtest-configs - This repo consist of YAML configuration for Easybuild and system package
- https://github.com/HPC-buildtest/Python-buildtest-config - This repo contains all Python code for each python package used by buildtest  for generating tests for  Python packages
- https://github.com/HPC-buildtest/R-buildtest-config - This repo contains all R code for each R package used by buildtest  for generating tests for R packages
- https://github.com/HPC-buildtest/Perl-buildtest-config - This repo contains all Perl code for each Perl package used by buildtest  for generating tests for Perl packages
- https://github.com/HPC-buildtest/Ruby-buildtest-config - This repo contains all Ruby code for each Ruby package used by buildtest  for generating tests for Ruby packages
- https://github.com/HPC-buildtest/buildtest - This repo is used to host the documentation found at http://buildtestdocs.readthedocs.io/en/latest/
