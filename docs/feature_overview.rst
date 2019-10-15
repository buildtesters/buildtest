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

.. program-output:: cat scripts/buildtest-list-software.txt

Similarly we can retrieve full name of module file and absolute path to
module file using ``buildtest list --module`` or short option ``buildtest list -m``

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

