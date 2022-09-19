.. _summary_of_buildtest:

Summary of buildtest
======================


.. contents::
   :backlinks: none

Background
------------

HPC System and Software Stack are tightly integrated with underlying architecture
which makes them highly sensitive to changes in system
such as OS, kernel, driver, or vendor updates. We need a testing
framework to automate acceptance testing of an HPC system so that HPC Support Teams
can increase **confidence** of their HPC system throughout the system lifecycle.

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
compilation and execution. Tools like `configure`, `cmake` and `autoconf` are
insufficient for testing because HPC software stack consist of applications
packaged in many formats and some are make-incompatible.

We wanted a framework that hides the complexity for compiling source code and
provide an easy markup language to define test configuration to create the test.
This leads to buildtest, which is a testing framework that generates test-scripts
using YAML that is validated with JSON Schemas. YAML was picked given its ease-of-use
and it lowers the barrier for writing tests.

Inception of buildtest
---------------------------

buildtest was founded by `Shahzeb Siddiqui <https://github.com/shahzebsiddiqui>`_
in 2017 when he was at `Pfizer <https://www.pfizer.com/>`_ tasked for testing
software stack for a data center migration.

Shahzeb was tasked with testing the software ecosystem by focusing on the most
important application due to time constraints. During this period, several dozen
test scripts were developed in shell-script that targeted core HPC tools such as
compilers, **MPI**, **R**, **Python**, etc. A single master script was used to
run all the tests which led to `buildtest`.

Preview of buildtest
----------------------

You can run ``buildtest help`` followed by name of command and it will provide an overview of the buildtest.

.. dropdown:: ``buildtest help build``

    .. command-output:: buildtest help build

.. dropdown:: ``buildtest help buildspec``

    .. command-output:: buildtest help buildspec

.. dropdown:: ``buildtest help report``

    .. command-output:: buildtest help report

.. dropdown:: ``buildtest help inspect``

    .. command-output:: buildtest help inspect

.. dropdown:: ``buildtest help config``

    .. command-output:: buildtest help config

Target Audience & Use Case
---------------------------

buildtest target audience is `HPC Staff` that wants to perform acceptance &
regression testing of their HPC system.

buildtest is not

  - replacement for `make`, `cmake`, `autoconf`, `ctest`
  - a software build framework (`easybuild <https://docs.easybuild.io/en/latest/>`_, `spack <https://spack.readthedocs.io/en/latest/>`__, `nix <https://nixos.org/>`_ , `guix <https://guix.gnu.org/>`_)
  - a replacement for benchmark tools or test suite from upstream package
  - a replacement for writing tests, you will need to write your tests defined by buildtest schemas, however you can copy/paste & adapt tests from other sites that are applicable to you.

Typical use-case:

  - Run your test suite during system maintenance
  - Perform daily tests for testing various system components. These tests should be short
  - Run weekly/biweekly test on medium/large workload including micro-benchmark
  - Run tests for newly installed software package typically requested by user.

If you are interested trying out buildtest check out :ref:`getting_started` and
`Join Slack Channel <https://hpcbuildtest.herokuapp.com/>`_.

Related Projects and community efforts
---------------------------------------

+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+
| Project                                                                              | Description                                                                                                                                                                                                                                                                                                         | State    |
+======================================================================================+=====================================================================================================================================================================================================================================================================================================================+==========+
| `ReFrame <https://reframe-hpc.readthedocs.io/en/stable/>`_                           | is a high level regression framework for writing regression test for HPC systems. Tests are written in Python class andit has support for cray programming environment, job scheduler, module integration, parameter tests, test dependency,and sanity check. The project is led by `CSCS <https://www.cscs.ch/>`_. | Active   |
+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+
| `Pavilion2 <https://github.com/hpc/pavilion2>`_                                      | is a framework for running and analyzing tests targeting HPC systems. Tests are written in YAML and majority of pavilion commands are implemented through python plugins using yapsy. Pavilion2 is developed by `LANL <https://www.lanl.gov/>`_.                                                                    | Active   |
+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+
| `Automatic Testing of Installed Software (ATIS) <https://github.com/besserox/ATIS>`_ | This project was presented by Xavier Besseron in `FOSDEM14 <https://archive.fosdem.org/2014/schedule/event/hpc_devroom_automatic_testing/>`_ that targets MPI testing using ctest and cdash. This project is no longer in development.                                                                              | Obsolete |
+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+
| `hpcswtest <https://github.com/idaholab/hpcswtest>`_                                 | is a HPC Software Stack Testing Framework developed by `Idaho National Lab <http://www.inl.gov>`_. The framework is built using C++11 and JSON file to define test configuration.                                                                                                                                   | Obsolete |
+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+
| `PVCS <https://github.com/cea-hpc/PCVS>`_                                            | is a validation engine to run large tests for HPC systems, the framework is written in Perl and recipe known as **Test Expression (TE)** are written in YAML. This project is developed by `CEA <http://www-hpc.cea.fr/index-en.htm>`_.                                                                             | Obsolete |
+--------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------+

The `System Test Working Group <https://github.com/olcf/hpc-system-test-wg>`_ hosted
a BOF `HPC System Testing: Procedures, Acceptance, Regression Testing, and Automation <https://sc19.supercomputing.org/presentation/?id=bof195&sess=sess324>`_
in SuperComputing '19. This working group is aimed at discussing acceptance and regression
testing procedure and lessons learned from other HPC centers.
