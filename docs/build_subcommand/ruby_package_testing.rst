Building Tests for Ruby packages (``buildtest build --ruby-package <RUBY-PACKAGE>``)
=======================================================================================

buildtest comes with option to build test for ruby packages to verify ruby packages
are working as expected. The ruby tests are coming from the repository
https://github.com/HPC-buildtest/Ruby-buildtest-config

In buildtest this repository is defined by variable ``BUILDTEST_RUBY_REPO`` that
can be tweaked by environment variable or configuration file (``config.yaml``)

buildtest supports tab completion for option ``--ruby-package`` which will show
a list of ruby packages available for testing.

To illustrate the tab completion feature see command below

::

    [siddis14@prometheus buildtest-framework]$ buildtest build --ruby-package
    addressable  bigdecimal

To build ruby package test you must specify a ``ruby`` module. buildtest will
generate the binarytest along with any test from ruby package specified by
option ``--ruby-package``.

The command ``buildtest build -s Ruby/2.5.0-intel-2018a --ruby-package addressable``
will build Ruby test along with any tests for Ruby package ``addressable``

.. program-output:: cat scripts/ruby_packagetest_addressable.txt

This option is compatible with ``--shell`` ``-enable-job`` and ``--job-template``
if you want to build tests with different shell or create job scripts
