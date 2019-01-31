buildtest Architecture
=======================


.. contents::
   :backlinks: none


This section will explain how the buildtest framework is designed in regards
to

* Software and Toolchain Check in buildtest
* How buildtest deals with Flat Naming Scheme and Hierarchical Module Naming Scheme and module format
* How buildtest determines a software is from easybuild
* Test Directory Structure (``$BUILDTEST_TESTDIR``)
* Source Directory Structure (``BUILDTEST_CONFIGS_REPO``)


Software and Toolchain Check
----------------------------

buildtest takes argument to build tests for software that can take argument from
``--software``. The argument to --software is auto-populated based on the
software modules found in module tree ``$BUILDTEST_MODULE_ROOT``.

Similarly, ``--toolchain`` is auto-populated based on union of software modules
present in ``$BUILDTEST_MODULE_ROOT`` and the toolchain list. Every
toolchain must be a software found in module tree ``$BUILDTEST_MODULE_ROOT``.

Several buildtest options are supplied as **choice** attribute in
``argparse.arg_argument``. For more details on implementation see ``buildtest.tools.menu``


Module File Format and Module Naming Scheme
-------------------------------------------

Modulefiles are used in test script to load the software environment to test
the software's functionality. Typically the HPC software stack is installed in
a cluster filesystem in a non-standard Linux path so modules
are used to load the environment properly.

Names of modulefiles depend on module naming scheme used at your site. In easybuild
this is controlled by ``eb --module-naming-scheme``. The default naming scheme is
**Easybuild Module Naming Scheme (EasyBuildMNS)** which is a flat naming scheme.
This naming scheme is simple because it presents the software stack in
one directory and names of module file tend to be long because they take the
format of ``<app>/<version>-<toolchain>``.

For instance loading ``OpenMPI-2.0.0`` built with ``GCC-5.4.0-2.27`` will be

.. code::

   module load OpenMPI/2.0.0-GCC-5.4.0-2.27

Similarly, easybuild supports **Hierarchical Module Naming Scheme (HMNS)** that
categorize software module stack in different trees that are loaded dynamically
based on your current module list.

With HMNS, the the module format will be different. You will  be loading the
toolchain module (``GCC``) followed by the application module (``OpenMPI``).

.. code::

   module load GCC/5.4.0-2.27
   module load OpenMPI/2.0.0

Modules in EasyBuildMNS will be unique so you will just  use ``buildtest build -s``
and toolchain option ``--toolchain`` will be ignored. If you have a HMNS module tree defined
in BUILDTEST_MODULE_ROOT then you will need to use both options ``buildtest build -s <app> -t <toolchain>``

Easybuild automatically generates modules for all software installed by easybuild
and each module is written in a way to load all dependent modules necessary,
therefore users don't need to worry about loading every dependent module in their
environment.

How buildtest gets the software module stack
--------------------------------------------

As mentioned previously, buildtest makes use of environment variable
``$BUILDTEST_MODULE_ROOT`` (i.e root of module tree) to find all the software
modules. Easybuild supports Tcl and Lua modules so buildtest attempts to find
all files that are actual module files.

buildtest ignores ``.version`` or ``.default`` files and accepts all other files
in the module tree. This information is processed further by stripping full
path to extract the module name depending if you specified BUILDTEST_MODULE_NAMING_SCHEME
as Flat Naming Scheme (FNS) or Hierarchical Module Naming Scheme (HMNS). This
can be specified in the buildtest command line ``buildtest build --module-naming-scheme`` or
environment variable ``$BUILDTEST_MODULE_NAMING_SCHEME`` or in ``settings.yml``

The software module stack is used to populate the choice entries for ``--software``
and ``--toolchain``.

buildtest takes a union of a list of predefined toolchains from ``eb --list-toolchains``
that is defined in module ``buildtest.tools.easybuild.list_toolchain`` and
list of software module stack. For details on implementation check out
``buildtest.tools.software.get_software_stack``
and ``buildtest.tools.software.get_toolchain_stack``

Determine if software is installed with easybuild
---------------------------------------------------------

All easybuild software will have the variable ``local root`` in the modulefile that points
to the root of the software package. For instance ``Anaconda2-5.0.1`` module file has the following
value

.. code::

        local root = "/nfs/grid/software/easybuild/commons/software/Anaconda2/5.1.0"

We use this value to check if there is a directory ``easybuild`` which eb should generate
to store log file, patches, easyconfigs, etc... In buildtest we check if there is an
easyconfig file in the ``easybuild`` directory and if it exists then we assume the application
is an easybuild software otherwise it is not.

For more details on implementation see ``buildtest.tools.easybuild.is_easybuild_app``

If you plan to mix easybuild module trees with non-easybuild module trees by defining
them in ``BUILDTEST_MODULE_ROOT`` then extra care must be taken.

If you are building tests for an application not built with easybuild you may run
into the following issue

.. code::

   [siddis14@amrndhl1157 buildtest-framework]$ buildtest build -s ruby/2.2.4
   Application: ruby/2.2.4  is not built from Easybuild, cannot find easyconfig file in installation directory

By default easybuild will check if the software is an easybuild app and will exit
immediately. If you want to ignore the easybuild check you may use the option
``_buildtest build --ignore-easybuild`` to bypass this error. This also assumes you have
the module tree defined in ``MODULEPATH`` so ``module load ruby/2.2.4`` will work
for the tests. If there are multiple counts of same application version module
across module trees you will need to fix that in your environment or modify which
module trees are exposed in ``BUILDTEST_MODULE_ROOT``


Testing Directory Structure
-------------------------------

buildtest will write the tests in the directory specified by **BUILDTEST_TESTDIR**. This value
can be specified in ``settings.yaml``, or environment variable ``$BUILDTEST_TESTDIR`` or command line
``buildtest --testdir <path>``.



Recall that CTest is the Testing Framework that automatically generates Makefiles necessary
to build and run the test. CTest will utilize *CMakeLists.txt* that will invoke
CTest api to run the the test.

.. include:: architecture/cmakelist_layout.txt

Whenever you build the test, you must specify the software and version
and this must match the name of the module you are trying to test, otherwise
there is no way of knowing what is being tested.  Each test will attempt to
load the application module along with the toolchain if specified prior to
anything. Similarly, toolchain must be specified with the exception of dummy
toolchain. If toolchain is hidden module in your system, you must specify
your toolchain version accordingly

CMake Configuration
-------------------

CMakeLists.txt for $BUILDTEST_TESTDIR/ebapps/GCC/CMakeLists.txt would like
this for ``GCC-5.4.0-2.27`` and ``GCC-6.2.0-2.27`` test

.. program-output:: cat scripts/architecture/GCC/CMakeLists.txt

The CMakeLists.txt in your test directory will look something like this

.. program-output:: cat scripts/architecture/GCC/test/CMakeLists.txt

Source Code Layout
--------------------

The source directory **BUILDTEST_CONFIGS_REPO** contains all the source code that
will be used for generating the test. Here, you will find config scripts used
for generating scripts. buildtest processes these config scripts inorder to
generate the test.


+---------------------------------------------------------------------+--------------------------------------------------------------------------+
|                     File                                            |                                Description                               |
+---------------------------------------------------------------------+--------------------------------------------------------------------------+
| $BUILDTEST_CONFIGS_REPO/buildtest/ebapps/$software/command.yaml     |       A list of binary executables and parameters to test                |
+---------------------------------------------------------------------+--------------------------------------------------------------------------+
| $BUILDTEST_CONFIGS_REPO/buildtest/source/$software/config/          |       Contains the yaml config files used for building test from source  |
+---------------------------------------------------------------------+--------------------------------------------------------------------------+
| $BUILDTEST_CONFIGS_REPO/buildtest/source/$software/code/            |       Directory Containing the source code, which is referenced          |
|                                                                     |       by the testscript and yaml files                                   |
+---------------------------------------------------------------------+--------------------------------------------------------------------------+
| $BUILDTEST_CONFIGS_REPO/system/$package/command.yaml                |       A list of binary executables and parameters to for system packages |
+----------------------------------------------------+-------------------------------------------------------------------------------------------+
