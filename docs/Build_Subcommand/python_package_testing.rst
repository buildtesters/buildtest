Building Tests for Python  Packages (``_buildtest build --python-package <PYTHON-PACKAGE>``)
=================================================================================================

buildtest comes with option to build test for python packages to test python packages
are working as expected. The Python tests are coming from the repository
https://github.com/HPC-buildtest/Python-buildtest-config

In buildtest this repository is defined by variable ``BUILDTEST_PYTHON_REPO`` that
can be tweaked by environment variable or configuration file (``config.yaml``)

buildtest supports tab completion for option ``--python-package`` which will show
a list of python packages available for testing.

To illustrate the tab completion feature see command below

.. code::

    [siddis14@prometheus buildtest-framework]$ _buildtest build --python-package
    anaconda-client  Babel            bitarray         cdecimal         cryptography     deap             mpi4py           nose             paramiko         pytz
    astriod          backports_abc    blist            chest            Cython           funcsigs         netaddr          numpy            paycheck         scipy
    astropy          beautifulsoup4   Bottleneck       colorama         dateutil         mock             netifaces        os               pyparsing        setuptools


To build python package test you must specify a ``Python`` module. buildtest will
generate the binarytest along with any test from python package specified by
option ``--python-package``.

.. program-output:: cat scripts/python_packagetest_dateutil.txt


Python Package Check Validation
-------------------------------

buildtest will check if python package exists for particular Python module specified
in ``--software`` to ensure tests are not created that are bound to fail due to
missing package.

To illustrate see the following example where we try building test for python package
``Bottleneck``

.. program-output:: cat scripts/python_packagetest_Bottleneck.txt


This option is compatible with ``--shell``, ``--enable-job`` and ``--job-template`` if you want to build
tests with different shell or create job scripts
