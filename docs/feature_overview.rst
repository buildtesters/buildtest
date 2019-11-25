Feature Overview
====================

Listing Software and Modules
-----------------------------

buildtest can report unique software and module versions found in your module
system based on ``spider`` utility provided by Lmod. This
feature can be useful for HPC facilities to see a count of all
software packages and see what versions are installed for each package along
with the filepath to module file.

buildtest collects this information via ``BUILDTEST_MODULEPATH`` which is
equivalent to ``MODULEPATH`` but can be tweaked by buildtest to add & remove
directory at will.

Shown below is unique software list using ``buildtest list --software``

.. program-output:: head -n 10 docgen/buildtest_list_--software.txt

Similarly we can retrieve full name of module file and absolute path to
module file using ``buildtest list --module`` or short option ``buildtest list -m``

.. program-output:: head -n 10 docgen/buildtest_list_--modules.txt

Module Testing
---------------

HPC sites may have hundreds if not thousand module files, it would be great to
test all of them. buildtest can conduct ``module load`` testing on module files
and report ``SUCCESS`` or ``FAIL`` upon module load by checking exit status.

.. program-output:: cat scripts/module-load.txt


Building Test
-----------------

To build a test, buildtest requires an input configuration file that can be
specified by option ``-c`` or long option ``--config``. This option is part of
``buildtest build``

Shown below is an example build

.. program-output:: cat docgen/tutorial.compilers.args.c.yml.txt


System Package Test
-------------------

buildtest can generate tests for system packages using the option
``buildtest build --package <package>``. Currently, system package test only
perform sanity check against binaries found in the system. The framework will automatically generate
binary test by checking the system default paths i.e ``/usr/bin``, ``/usr/local/bin``, ``/usr/sbin``.

For instance to build test for the system package ``coreutils`` you can do the
following

.. program-output:: cat docgen/coreutils.txt

Build Report
-------------

Every build from buildtest is tracked internally, this can be retrieved using ``buildtest status report`` which shows
a history of all builds.

.. program-output:: cat scripts/buildtest_build_report.txt

Each build ID can be used to retrieve log and  test-scripts and run the test independently. This can be done
via::

   buildtest build log <ID>
   buildtest build test <ID>
   buildtest build run <ID>

For example you can retrieve tests scripts generated from a build via ``buildtest build test``

.. program-output:: cat scripts/buildtest_build_test.txt

TAB Completion
-----------------------

buildtest use the ``argcomplete`` python module to autocomplete buildtest
argument. Just press TAB key on the keyboard to fill in the arguments. It is highly
recommended to use the :ref:`autocomplete` feature when using buildtest.

.. Note:: Please be patient! You may need to press the TAB key few times before it shows all the
   arguments

