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

Building Test
~~~~~~~~~~~~~~

.. command-output:: buildtest help build

Buildspec Interface
~~~~~~~~~~~~~~~~~~~

.. command-output:: buildtest help buildspec

Query Report
~~~~~~~~~~~~~

.. command-output:: buildtest help report

Inspect Tests
~~~~~~~~~~~~~~

.. command-output:: buildtest help inspect

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

Timeline
---------

.. csv-table::
    :header: "Date", "Version", "Description"
    :widths: 20, 20, 80

    **Dec 17th 2021**, "`v0.12.0 <https://github.com/buildtesters/buildtest/releases/tag/v0.12.0>`_", "Make use of `rich <https://rich.readthedocs.io/en/stable/index.html>`_ library for printing output for various buildtest commands. Add  new commands such ``buildtest debugreport`` and ``buildtest config edit``. We removed few commands including ``buildtest config summary``, ``buildtest inspect id``."
    **Sep 9th 2021**, "`v0.11.0 <https://github.com/buildtesters/buildtest/releases/tag/v0.11.0>`_", "Re-implement core implementation of running and polling jobs using asynchronous job submission. In addition we added several new commands including: **buildtest cd**, **buildtest path** and **buildtest path** and we enable alias for sub-commands."
    **Aug 16th 2021**, "`v0.10.2 <https://github.com/buildtesters/buildtest/releases/tag/v0.10.2>`_", "Add support for multi executor support in buildspec via ``executors`` property. Add new commands ``buildtest report summary`` for summary of report file. The ``buildtest buildspec show`` command shows content of buildspec file given a test name. The ``buildtest edit`` command can be used to edit buildspec and validate with JSON schema upon closing file. In this release, we added ``buildtest inspect buildspec`` command to view records based on buildspec file."
    **Jul 30th 2021**, "`v0.10.1 <https://github.com/buildtesters/buildtest/releases/tag/v0.10.1>`_", "Add new commands ``buildtest buildspec summary``, ``buildtest buildspec invalid`` to show summary of buildspec cache and invalid buildspecs. Add ``buildtest build --filter`` to filter buildspecs during build. Add ``--terse`` option for several commands including **buildtest history list**, **buildtest report**, **buildtest buildspec find**. Add new command ``buildtest inspect query`` for querying test records. Added support for ``metrics`` property for defining arbitrary metrics in buildspec based on environment variable, variables or regular expression on stdout/stderr"
    **Jul 13th 2021**, "`v0.10.0 <https://github.com/buildtesters/buildtest/releases/tag/v0.10.0>`_", "In this release we added `spack <https://spack.readthedocs.io/>`__ support in buildtest by creating a new schema to write buildspecs that will generate spack commands. For more details see :ref:`spack schema <spack_schema>`. We added bash completion for buildtest commands which is enabled when installing buildtest. We added a new command ``buildtest buildspec validate``  that can be used for validating buildspecs  with JSON Schema."
    **Jun 11th 2021**, "`v0.9.6 <https://github.com/buildtesters/buildtest/releases/tag/v0.9.6>`_", "Added buildtest CDASH integration using ``buildtest cdash`` to upload test results. In this release we added ``buildtest history`` command to retrieve build history and query logfiles. Add global option ``-c`` in buildtest to specify alternate configuration file."
    **Mar 31th 2021**, "`v0.9.5 <https://github.com/buildtesters/buildtest/releases/tag/v0.9.5>`_", "Add support for PBS scheduler and reimplement ``buildtest inspect`` command"
    **Mar 14th 2021**, "`v0.9.4 <https://github.com/buildtesters/buildtest/releases/tag/v0.9.4>`_", "Introduced major change in buildtest configuration file (``settings.schema.json``) to define multiple HPC systems in configuration file. This lead to change in how ``executors`` are referenced in buildspec file."
    **Feb 22nd 2021**, "`v0.9.3 <https://github.com/buildtesters/buildtest/releases/tag/v0.9.3>`_", "Change Copyright details for project to include `LBNL <https://www.lbl.gov/>`_. We added `dependabot <https://dependabot.com/>`_ for managing dependencies, added OLCF facility pipelines for running regression test."
    **Jan 12th 2021**, "`v0.9.2 <https://github.com/buildtesters/buildtest/releases/tag/v0.9.2>`_", "Contains major refactor to ``compiler-v1.0-schema.json`` for writing compiler test using regular expression to search for compilers that are defined in configuration file."
    **Nov 24st 2020**, "`v0.9.1 <https://github.com/buildtesters/buildtest/releases/tag/v0.9.1>`_", "Added support for `Cobalt Scheduler <https://trac.mcs.anl.gov/projects/cobalt>`_."
    **Sep 3rd 2020**, "`v0.8.0 <https://github.com/buildtesters/buildtest/releases/tag/v0.8.0>`_", "Introduced `JSON Schema <https://json-schema.org/>`_ for validating buildspec. Add support for Slurm and LSF scheduler for job submission. Add support for building buildspecs by file, directory and tagname and command line interface to schema."
    **Sep 11th 2018**, "`v0.4.0 <https://github.com/buildtesters/buildtest/releases/tag/v0.4.0>`_", "buildtest was ported from Python 2 to 3."
    **Aug 20th 2017**, "`v0.1.5 <https://github.com/buildtesters/buildtest/releases/tag/v0.1.5>`_", "buildtest was converted from bash to Python and project was moved into github https://github.com/HPC-buildtest/buildtest."
    **Feb 18th 2017**, "N/A", "Start of project"


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
