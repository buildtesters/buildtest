Building Tests for Perl packages (``buildtest --perl-package <PERL-PACKAGE>``)
===============================================================================

buildtest comes with option to build test for perl packages to verify perl packages
are working as expected. The Perl tests are coming from the repository
https://github.com/HPC-buildtest/Perl-buildtest-config

In buildtest this repository is defined by variable ``BUILDTEST_PERL_REPO`` that
can be tweaked by environment variable or configuration file (``config.yaml``)

buildtest supports tab completion for option ``--perl-package`` which will show
a list of perl packages available for testing.

To illustrate the tab completion feature see command below

.. code::

    siddis14@prometheus buildtest-framework]$ buildtest build --perl-package
    Algorithm  AnyData    AppConfig  Authen


To build perl package test you must specify a ``Perl`` module. buildtest will
generate the binarytest along with any test from perl package specified by
option ``--perl-package``.

The command ``buildtest build -s Perl/5.26.0-GCCcore-6.4.0 --perl-package AnyData``
will build Perl test along with Perl package ``AnyData``

.. program-output:: cat scripts/perl_packagetest_AnyData.txt

Perl Package Check Validation
-------------------------------

buildtest will check if perl package exists for particular perl module specified
in ``--software`` to ensure tests are not created that are bound to fail due to
missing package.

To illustrate see the following example where we try building test for perl package
``Algorithm``.

``buildtest build -s Perl/5.26.0-GCCcore-6.4.0 --perl-package Algorithm``

.. program-output:: cat scripts/perl_packagetest_Algorithm.txt


This option is compatible with ``--shell`` and ``--job-template`` if you want to build
tests with different shell or create job scripts
