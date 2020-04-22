.. _summary_of_buildtest:

Summary of buildtest
======================


.. contents::
   :backlinks: none

Background
------------

HPC computing environment is a tightly coupled system that includes a cluster of nodes and accelerators interconnected
with a high-speed interconnect, a parallel filesystem, multiple storage tiers, a batch scheduler for users to submit
jobs to the cluster and a software stack for users to run their workflows. A **software stack is a collection of compilers, MPI, libraries, system utilities and scientific packages**
typically installed in a parallel file-system. A module tool like ``environment-modules`` or ``Lmod`` is generally used
for loading the software environment into the users’ shell environment.

Software are packaged in various forms that determine how they are installed. A few package formats are:
``binary``, ``Makefile``, ``CMake``, ``Autoconf``, ``github``, ``PyPi``, ``Conda``, ``RPM``, ``tarball``, ``rubygem``,
``MakeCp``, ``jar``, and many more. With many packaging formats, this creates a burden for HPC support team to learn how
to build software since each one has a unique build process. Software build tools like
`EasyBuild <https://easybuild.readthedocs.io/en/latest/>`_ and `Spack <https://spack.readthedocs.io/en/latest/>`_ can
build up to 1000+ software packages by supporting many packaging formats to address all sorts of software builds.
Easybuild and Spack provide end-end software build automation that helps HPC site to build a very large software stack
with many combinatorial software configurations. During the installation, some packages will provide a test harness that
can be executed via Easybuild or Spack which typically invokes a ``make test`` or ``ctest`` for packages that follow
ConfigureMake, Autoconf, or CMake install process.

Many HPC sites rely on their users for testing the software stack, and some sites may develop in-house test scripts to run
sanity check for popular scientific tools. Despite these efforts, there is little or no collaboration between HPC sites
on sharing tests because they are site-specific and often provide no documentation. For many sites, the HPC support team
don’t have the time for conducting software stack testing because:

1. lack of domain expertise and understaffed
2. no standard test-suite and framework to automate test build and execution.

Frankly, HPC support teams are so busy with important day-day operation and engineering projects that software testing
is either neglected or left to end-users. This demands for a concerted effort by HPC community to **build a strong open-source community**
around software stack testing.

There are two points that need to be addressed. First, we need a **framework to do automatic testing** of installed software
stack. Second, is to **build a test repository** for scientific software that is community driven and reusable amongst the
HPC community. An automated test framework is a harness for *automating* the test creation process, but it requires a
community contribution to accumulate this repository on per-package basis.

**buildtest** was designed to address both these points, it is a **framework** to perform automatic testing and it provides
a repository of test-configurations that can be shared by HPC community.


Motivation
-----------

There are many build automations tools for compiling source code into binary code, the most used tool is the **make**
utility found in most Linux systems. Build scripts like **configure**, **cmake** and **autoconf** can generate files
used by make for installing the software. Makefile is a file used by make program that shows how to compile and link a
program which is the basis for building a software package. One can invoke **make test** which will run the target named
**test** in Makefile that dictates how tests are compiled and run. Makefile is hard to interpret and requires in-depth
experience with shell-scripting and strong understanding of how package is built and tested. Note that package
maintainers must provide the source files, headers, and additional libraries to test the software and make test simply
the test compilation and execution. Tools like configure, cmake and autoconf are insufficient for testing because HPC
software stack consist of applications packaged in many formats and some are make-incompatible.

We wanted a framework that hides the complexity for compiling source code and provide an easy markup language to define
test configuration to create the test. This leads to buildtest, a framework that automates test creation by using test
configuration written in YAML syntax. YAML was picked given its simplicity and it lowers the barrier for new
to start sharing test configuration in order to build a comprehensive test suite that will work with buildtest

Inception of buildtest
---------------------------

buildtest was founded by *Shahzeb Siddiqui* in 2017 when he was at Pfizer tasked for testing software stack during a
data center migration.

Shahzeb was tasked with testing the software ecosystem by focusing on the most important application due to
time constraints. During this period, several dozen test scripts were developed in shell-script that targeted core
HPC tools such as compilers, **MPI**, **R**, **Python**, etc. A single master script was used to run all the tests which
led to buildtest. Originally buildtest was implemented in bash and due to several language limitations, it was ported
to Python. In September 2018, buildtest was ported from Python 2 to Python 3. The project was started on Feb 24th, 2017
and source code and documentation can be found on GitHub.


Description
-----------

**buildtest** is a python framework for automating software stack testing by utilizing test configurations (YAML) to
generate test scripts. The framework is tightly integrated with Lmod module system to allow the framework to load modules
properly when building test. buildtest was designed on the premise of reusable and easy to read test configuration that
can be shared by the HPC community sites. buildtest aims to abstract test complexity so the user can
focus on writing test with minimal knowledge of the system.

buildtest is available on Github at https://github.com/buildtesters/buildtest

