Feature Overview
====================

Listing Unique Software and Software Versions
----------------------------------------------

buildtest can report unique software and software versions found in your module
system based on ``spider`` utility provided by Lmod. buildtest leverage this
feature which can be useful for HPC facilities to see a count of all
software packages and see what versions are installed for each package along
with the filepath to module file.

buildtest collects this information via ``BUILDTEST_MODULEPATH`` which is
equivalent to ``MODULEPATH`` but can be tweaked by buildtest to add & remove
directory at will.

Shown below is unique software list using ``buildtest list --list-software``

.. program-output:: cat scripts/buildtest-list-software.txt

Similarly we can search software version and filepath to module file using
``buildtest list --software-version-relation`` or short option ``buildtest list -svr``

.. program-output:: cat scripts/buildtest-list-software-modules.txt

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

.. program-output:: cat scripts/build-single-configuration.txt

buildtest can insert modules into test, just load the modules before you build
the test and it will insert them into your test script.

.. program-output:: cat scripts/build-single-configuration-module.txt

System Package Test
-------------------

buildtest can generate tests for system packages using the option
``buildtest build --package <package>``. Currently, system package test only
perform sanity check against binaries found in the system. The framework will automatically generate
binary test by checking the system default paths i.e ``/usr/bin``, ``/usr/local/bin``, ``/usr/sbin``.

For instance to build test for the system package ``coreutils`` you can do the
following

.. program-output:: cat scripts/coreutils-binary-test.txt

Running The Test
-----------------

You can run the in several ways. The easiest way to run the test is via buildtest
using ``buildtest run -S <suite>``

Here is the output of the following test

.. program-output:: cat scripts/run-openmp-suite.txt




TAB Completion
-----------------------

buildtest use the ``argcomplete`` python module to autocomplete buildtest
argument.
Just press TAB key on the keyboard to fill in the arguments.

For instance if you just type ``buildtest`` followed by TAB you should see the
following.

::

    $ buildtest
    benchmark     --clean-logs  -h            list          module        --scantest    --show-keys   -V            yaml
    build         find          --help        --logdir      run           --show        --submitjob   --version


.. Note:: You will need to press the TAB key few times before it shows all the
   arguments


Log files
---------

All buildtest logs will be written in ``BUILDTEST_LOGDIR``.

buildtest will store log files for ``buildtest build -s <app_name>/<app_ver>`` in
``BUILDTEST_LOGDIR/<app_name>/<app_ver>``. If toolchain option is specified for
instance ``buildtest build -s <app_name>/<app_ver> -t <tc_name>/<tc_ver>`` then
buildtest will store the logs in ``BUILDTEST_LOGDIR/<app_name>/<app_ver>/<tc_name>/<tc_ver>``.

Similarly logs for system tests like ``buildtest --package <package>`` will be stored in ``BUILDTEST_LOGDIR/system/<package>``

You may override BUILDTEST_LOGDIR option at command line via ``buildtest --logdir``
and you may even store individual buildtest runs in separate directories such as
the following

.. code::

   buildtest build -s OpenMPI/3.0.0-GCC-6.4.0-2.28 --logdir=/tmp
