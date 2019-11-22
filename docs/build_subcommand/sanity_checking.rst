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

.. program-output:: cat docgen/coreutils.txt


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
      1) GCCcore/8.3.0               5) libreadline/8.0-GCCcore-8.3.0   9) GMP/6.1.2-GCCcore-8.3.0
      2) bzip2/1.0.8-GCCcore-8.3.0   6) Tcl/8.6.9-GCCcore-8.3.0        10) libffi/3.2.1-GCCcore-8.3.0
      3) zlib/1.2.11-GCCcore-8.3.0   7) SQLite/3.29.0-GCCcore-8.3.0    11) Python/3.7.4-GCCcore-8.3.0
      4) ncurses/6.1-GCCcore-8.3.0   8) XZ/5.2.4-GCCcore-8.3.0         12) PyCharm/2017.2.3



buildtest will seek out all binary executables in each module file and run
``which`` command against the binary and load the appropriate modules

Shown below is an example.

.. program-output:: cat docgen/module-binary.txt


modules that dont have ``PATH`` set or no binary executables are found in
the directory, then buildtest will not generate any test.

Shown below is an example test script for gcc binary

::

    #!/bin/sh


    module load GCCcore/8.3.0
    which gcc
