Sanity Check
=============

Sanity Check for System Packages
---------------------------------

buildtest can perform sanity check for all binaries defined by a system
package. This may be useful when running test periodically to monitor system
changes.

To build test for system package you will want to use
``buildtest build --package <package>`` and specify the name of the
installed system package.

For instance, lets build the tests for ``coreutils`` package by running ``buildtest build --package coreutils``:

.. program-output:: cat scripts/coreutils-binary-test.txt


Sanity Check for Modules
------------------------

buildtest can conduct sanity check for all active modules by running ``-b``,
``--binary`` option or setting ``BUILDTEST_BINARY=True`` in your
configuration file.

For instance let's assume the following modules are active modules in your
shell

::

    $ ml

    Currently Loaded Modules:
      1) eb/2018   2) GCCcore/6.4.0   3) binutils/2.28-GCCcore-6.4.0   4) GCC/6.4.0-2.28


buildtest will seek out all binary executables in each module file and run
``which`` command against the binary and load the appropriate modules

Shown below is an example.

::

    $ buildtest build -b
    Detecting Software:eb/2018
    No $PATH set in your module  eb/2018   so no possible binaries can be found
    There are no binaries for package: eb/2018
    Detecting Software:GCCcore/6.4.0
    Generating  19  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/GCCcore/6.4.0
    Detecting Software:binutils/2.28-GCCcore-6.4.0
    Generating  18  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/binutils/2.28-GCCcore-6.4.0
    Detecting Software:GCC/6.4.0-2.28
    No $PATH set in your module  GCC/6.4.0-2.28   so no possible binaries can be found
    There are no binaries for package: GCC/6.4.0-2.28


modules that dont have ``PATH`` set or no binary executables are found in
the directory, then buildtest will not generate any test.

Shown below is an example test script for gcc binary

::

    #!/bin/sh


    module load GCCcore/6.4.0
    which gcc



Shell Types
--------------

Currently buildtest supports ``sh``, ``bash``, ``csh`` shell for creating
test scripts. buildtest defaults to ``sh`` but this can be tweaked

To create tests for different shell types try ``buildtest build --shell <shell>``
or set the variable ``BUILDTEST_SHELL`` in your configuration file or via
environment variable

Let's build test with ``csh``

.. program-output:: cat scripts/build-shell-csh.txt

buildtest will add the appropriate shell extension for the test script to
avoid name conflicts.

Another way to build for different shell is to set ``BUILDTEST_SHELL`` as we
see in example below

.. program-output:: cat scripts/build-shell-bash.txt