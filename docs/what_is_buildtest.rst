.. _summary_of_buildtest:

Summary of buildtest
======================


.. contents::
   :backlinks: none

Background
------------

HPC computing environment is a tightly coupled system that includes a cluster of
nodes and accelerators interconnected with a high-speed interconnect, a parallel
filesystem, multiple storage tiers, a batch scheduler for users to submit
jobs to the cluster and a software stack for users to run their workflows. A
**software stack is a collection of compilers, MPI, libraries, system utilities and scientific packages**
typically installed in a parallel file-system. A module tool like
``environment-modules`` or ``Lmod`` is generally used for loading the software
environment into the users’ shell environment.

Software are packaged in various forms that determine how they are installed. A
few package formats are: ``binary``, ``Makefile``, ``CMake``, ``Autoconf``,
``github``, ``PyPi``, ``Conda``, ``RPM``, ``tarball``, ``rubygem``, ``MakeCp``,
``jar``, and many more. With many packaging formats, this creates a burden for
HPC support team to learn how to build software since each one has a unique
build process. Software build tools like `EasyBuild <https://easybuild.readthedocs.io/en/latest/>`_
and `Spack <https://spack.readthedocs.io/en/latest/>`_ can build up to 1000+
software packages by supporting many packaging formats to address all sorts of
software builds. Easybuild and Spack provide end-end software build automation
that helps HPC site to build a very large software stack with many combinatorial
software configurations. During the installation, some packages will provide a
test harness that can be executed via Easybuild or Spack which typically invokes
a ``make test`` or ``ctest`` for packages that follow ConfigureMake, Autoconf,
or CMake install process.

Many HPC sites rely on their users for testing the software stack, and some sites
may develop in-house test scripts to run sanity check for popular scientific
tools. Despite these efforts, there is little or no collaboration between HPC
sites on sharing tests because they are site-specific and often provide no
documentation. For many sites, the HPC support team don’t have the time for
conducting software stack testing because:

1. lack of domain expertise and understaffed
2. no standard test-suite and framework to automate test build and execution.

Frankly, HPC support teams are so busy with important day-day operation and
engineering projects that software testing is either neglected or left to
end-users. This demands for a concerted effort by HPC community to
**build a strong open-source community** around software stack testing.

There are two points that need to be addressed. First, we need a
**framework to do automatic testing** of installed software stack. Second, is to
**build a test repository** for scientific software that is community driven and
reusable amongst the HPC community. An automated test framework is a harness for
*automating* the test creation process, but it requires a community contribution
to accumulate this repository on per-package basis.

**buildtest** was designed to address both these points, it is a **framework** to
perform automatic testing and it provides a repository of test-configurations
that can be shared by HPC community.


Motivation
-----------

There are many build automations tools for compiling source code into binary code,
the most used tool is the **make** utility found in most Linux systems. Build
scripts like **configure**, **cmake** and **autoconf** can generate files
used by make for installing the software. Makefile is a file used by make
program that shows how to compile and link a program which is the basis for
building a software package. One can invoke **make test** which will run the
target named **test** in Makefile that dictates how tests are compiled and run.
Makefile is hard to interpret and requires in-depth experience with
shell-scripting and strong understanding of how package is built and tested.
Note that package maintainers must provide the source files, headers, and
additional libraries to test the software and make test simply the test
compilation and execution. Tools like configure, cmake and autoconf are
insufficient for testing because HPC software stack consist of applications
packaged in many formats and some are make-incompatible.

We wanted a framework that hides the complexity for compiling source code and
provide an easy markup language to define test configuration to create the test.
This leads to buildtest, a framework that automates test creation by using test
configuration written in YAML syntax. YAML was picked given its simplicity and
it lowers the barrier for new to start sharing test configuration in order to
build a comprehensive test suite that will work with buildtest.

Inception of buildtest
---------------------------

buildtest was founded by `Shahzeb Siddiqui <https://github.com/shahzebsiddiqui>`_
in 2017 when he was at `Pfizer <https://www.pfizer.com/>`_ tasked for testing
software stack for a data center migration.

Shahzeb was tasked with testing the software ecosystem by focusing on the most
important application due to time constraints. During this period, several dozen
test scripts were developed in shell-script that targeted core HPC tools such as
compilers, **MPI**, **R**, **Python**, etc. A single master script was used to
run all the tests which led to buildtest.

Target Audience & Use Case
---------------------------

buildtest target audience is the following:

  - `HPC Staff`:  that wants to perform acceptance & regression testing of their HPC system.
  - `Research Software Engineers`: that want to test software installed in HPC system

buildtest is not

  - replacement for `make`, `cmake`, `autoconf`, `ctest`
  - a software build framework (`easybuild`, `spack`, `nix`, `guix`)
  - a replacement for benchmark tools or test suite from upstream package
  - a replacement for writing tests, you will need to write your tests defined by buildtest schemas, however you can copy/paste & adapt tests from other sites that are applicable to you.

Typical use-case :

  1. Run your test suite during system maintenance

  2. Perform daily tests for testing various system components. These tests should be short

  3. Run weekly/biweekly test on medium/large workload including micro-benchmark


If you are interested in buildtest, please `Join Slack Channel <https://hpcbuildtest.herokuapp.com/>`_
and your feedback will help improve buildtest.

Timeline
---------

.. csv-table::
    :header: "Date", "Description"
    :widths: 30, 60

    **Feb 18th 2017**,"Start of project"
    **Aug 20th 2017**,"In `v0.1.5 <https://github.com/buildtesters/buildtest/releases/tag/v0.1.5>`_ buildtest was converted from bash to Python and project was moved into github https://github.com/HPC-buildtest/buildtest"
    **Sep 11th 2018**,"In `v0.4.0 <https://github.com/buildtesters/buildtest/releases/tag/v0.4.0>`_ buildtest was ported from Python 2 to 3"
    **Mar 3rd 2020**,"A spin-off project called `lmodule <https://lmodule.readthedocs.io/en/latest/>`_ was formed based on buildtest module features"


Related Projects and community efforts
---------------------------------------

- `ReFrame: <https://reframe-hpc.readthedocs.io/en/stable/>`_ ``Re`` gression ``FRAME`` work for Software Testing. ReFrame is developed by `CSCS <https://www.cscs.ch/>`_

- `Pavilion2: <https://github.com/hpc/pavilion2>`_ is a framework for running and analyzing tests targeting HPC systems. Pavilion2 is developed by `LANL <https://www.lanl.gov/>`_

- `Automatic Testing of Installed Software (ATIS) <https://github.com/besserox/ATIS>`_ - This project was presented by Xavier Besseron in `FOSDEM14 <https://archive.fosdem.org/2014/schedule/event/hpc_devroom_automatic_testing/>`_ however this project is no longer in development.

- `hpcswtest <https://github.com/idaholab/hpcswtest>`_ - is a HPC Software Stack testing framework by `Idaho National Lab <http://www.inl.gov>`_ however this project is no longer in development.


The `System Test Working Group <https://github.com/olcf/hpc-system-test-wg>`_ hosted
a BOF `HPC System Testing: Procedures, Acceptance, Regression Testing, and Automation <https://sc19.supercomputing.org/presentation/?id=bof195&sess=sess324>`_
in SuperComputing '19. This working group is aimed at discussing acceptance and regression
testing procedure and lessons learned from other HPC centers.