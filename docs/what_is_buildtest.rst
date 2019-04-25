.. _summary_of_buildtest:

Summary of buildtest
======================


.. contents::
   :backlinks: none

What are we trying to solve?
-----------------------------

When you ask your HPC facilities the following question

*What type of testing are you doing against your software stack?*

The most common response you get are the following

- **NONE**
-  **I dont care, my users do the testing**.

Those that do any form of testing will write test scripts in-house with hard-coded
file paths, module names, and site-specific configuration that cannot be **reusable**
or shared between other HPC sites. Some may take one extra step and automate all test
via CI tools (Jenkins, Travis, ctest) and may even use dashboard like CDASH for visualizing
test results.

The mission of this project (*buildtest*) is to provide a mechanism to automate test
creation of test scripts and the ability to *share* test scripts in a high level configuration
format (YAML) that is easily interpreted


Motivation
-----------

A typical HPC facility supports hundreds of applications that is supported by the HPC team.
Building these software is a challenge and then figuring out how this software stack behaves
due to system changes (OS release, kernel path, glibc, etc...) is even more difficult.

Application Testing is difficult! Commercial and open-source application typically provide
test scripts such as **make test** or **ctest** that can test the software after building
(**make**) step. Unfortunately, these methods perform tests prior to installation (``make install``)
so the ability to test software in production is not possible. One could try to change the
the vendor test script to the install path but this requires significant change into
a complex makefile. Some software don't have any test scripts and you are on your own.

Writing test scripts manually can be tedious, also there is no sharing of tests
and most likely they are not compatible to work with other HPC sites because of different
software stack and hard-coded paths specific to the site. Easybuild_ and Spack_
are great tools for automating the installation of  the entire software stack for an HPC system,
buildtest is meant to complement these tools to test the software that is currently installed
in your system.


.. _EasyBuild: https://easybuild.readthedocs.io/en/latest/
.. _Spack: https://spack.readthedocs.io/en/latest/index.html

How was buildtest started?
---------------------------

Our institution was going to move our HPC cluster to another Data Center (DC),
and my task was to conduct software testing before and after the DC move. This
project started out by writing individual test scripts to test specific
features of a software. Most of the software testing was geared for ``compilers``,
``mpi``, ``R``, ``Python``, etc... Each test script could be run adhoc or via
master script that would run everything. Originally buildtest was implemented in bash and
then ported over to Python due to language limitation of bash.

Description
-----------

**buildtest** is a framework to automate testing for software stack in HPC
sites. buildtest aims to abstract test complexity so the user can
focus on writing test with minimal knowledge of the system. buildtest provides
a rich set of YAML keys with `key`, `value` pairs to define test options that
buildtest will parse and create a shell-script.

buildtest supports job submission to batch scheduler currently
``LSF`` and ``SLURM``. buildtest assumes your software is installed  and your
facility has module environment Lmod_ so you can
load the software environment.


.. _Lmod: https://github.com/TACC/Lmod

buildtest features
-------------------------------
0
 - Provide a rich YAML API to write test configuration that is **reusable** and **site agnostic**
 - Verify modulefiles can be loaded and conduct ``module load`` testing.
 - Sanity check for binaries for application and system packages
 - List software packages provided by ``MODULEPATH``
 - Support for logging
 - Search for YAML and test scripts
 - Summary of run output
 - Support for multiple shells (csh, bash, sh)
 - Generate job scripts (SLURM, LSF) for each test and automate job submission
 - Support for benchmark


buildtest is available on Github at https://github.com/HPC-buildtest/buildtest-framework
