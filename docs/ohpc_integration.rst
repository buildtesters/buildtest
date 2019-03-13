.. _OHPC_Integration:

OpenHPC Integration
======================

buildtest can test the OpenHPC software collection. In-order for buildtest to test
OpenHPC you must set the variable in your configuration file

::

    BUILDTEST_OHPC=True

You may set this as environment variables


::

        # bash/sh shell
        export BUILDTEST_OHPC=True

        #csh/tcsh shell
        setenv BUILDTEST_OHPC True

You may specify the option ``--ohpc`` at the command line which will enable OpenHPC
integration.

You would want to configure your configuration file to specify BUILDTEST_MODULE_ROOT to
the root of the software stack.

Shown below is an example found in buildtest configuration (``$HOME/.buildtest/settings.yaml``) that
tests the gnu7 and openmpi3 stack.

::


    BUILDTEST_MODULE_ROOT:
        - /opt/ohpc/pub/modulefiles
        - /opt/ohpc/pub/moduledeps/gnu7
        - /opt/ohpc/pub/moduledeps/gnu7-openmpi3

The YAML configuration for OHPC Software Stack can be found at https://github.com/HPC-buildtest/buildtest-configs/tree/master/buildtest/ohpc

Building tests for OpenHPC software
-------------------------------------


To build a test specify the ``--ohpc`` or enable BUILDTEST_OHPC at configuration file or
via environment variable

Shown below is an example build of gnu7/7.3.0 with buildtest.

::

    (buildtest) buildtest-framework[devel] $ buildtest build -s gnu7/7.3.0 --ohpc
    Detecting Software:  gnu7/7.3.0
    --------------------------------------------
    [STAGE 1]: Building Binary Tests
    --------------------------------------------
    Detecting Test Type: Software
    Processing Binary YAML configuration:  /lustre/workspace/home/siddis14/buildtest-configs/buildtest/ohpc/gnu7/7.3.0/command.yaml
    Generating  10  binary tests
    Binary Tests are written in  /tmp/buildtest-tests/ebapp/gnu7/7.3.0/
    Writing Log file:  /tmp/buildtest/gnu7/7.3.0/buildtest_11_34_25_10_2018.log

To run the test you dont need to anything special just run as follows

::

    buildtest run -s gnu7/7.3.0


OpenHPC will use a Hierarchical Module Naming Scheme which will require some modules (i.e compiler, mpi) to be
loaded first in order to load the appropriate module.

For instance hdf5/1.10.2 will require loading ``gnu7`` and ``openmpi3`` module before we load
hdf5. This can be achieved using option ``--prepend-modules`` as follows

::

    (buildtest) buildtest-framework[devel] $ buildtest build -s hdf5/1.10.2 --prepend-modules gnu7/7.3.0 --prepend-modules openmpi3/3.1.0
    Detecting Software:  hdf5/1.10.2
    --------------------------------------------
    [STAGE 1]: Building Binary Tests
    --------------------------------------------
    Detecting Test Type: Software
    Processing Binary YAML configuration:  /lustre/workspace/home/siddis14/buildtest-configs/buildtest/ohpc/hdf5/1.10.2/command.yaml
    Generating  22  binary tests
    Binary Tests are written in  /tmp/buildtest-tests/ebapp/hdf5/1.10.2/
    Writing Log file:  /tmp/buildtest/hdf5/1.10.2/buildtest_11_44_25_10_2018.log


This will result in the test scripts to have the following modules loaded before loading hdf5.

::

    #!/bin/sh
    module purge
    module load gnu7/7.3.0
    module load openmpi3/3.1.0
    module load hdf5/1.10.2
    which gif2h5

Build YAML configuration for OpenHPC software
----------------------------------------------

To build yaml configuration for OpenHPC software you can use the option ``buildtest yaml --ohpc``.

buildtest will write the yaml configuration at ``$BUILDTEST_CONFIGS_REPO/buildtest/ohpc/${software}/${version}/command.yaml``

::

    (buildtest) buildtest-framework[devel] $ buildtest yaml -s gnu7/7.3.0 --ohpc
    Please check YAML file  /lustre/workspace/home/siddis14/buildtest-configs/buildtest/ohpc/gnu7/7.3.0/command.yaml  and fix test accordingly

How buildtest checks for OpenHPC Configuration
------------------------------------------------

buildtest will check if your system has ``ohpc-release`` package installed in your system
which is required to install OpenHPC components. buildtest will not assume anything after
this so if you have not installed the software collection from OpenHPC then
buildtest will not work. Furthermore, buildtest assumes your shell environment is
configured so that the appropriate module trees are available for testing.

To demonstrate this, the following command is run on a system not configured with OpenHPC attempting
to build ncurses package.

::

    (buildtest-0.6.3) [siddis14@adwnode1 buildtest-framework]$ buildtest build --ohpc -s ncurses/6.0-GCCcore-6.4.0
    This system is not configured with OpenHPC. Package ohpc-release is not installed.

You will expect the same result if you were trying to create yaml files for particular software
that does not have OpenHPC configured.

For instance the following will fail

::

    (buildtest-0.6.3) [siddis14@adwnode1 buildtest-framework]$ buildtest yaml --ohpc -s ncurses/6.0-GCCcore-6.4.0
    This system is not configured with OpenHPC. Package ohpc-release is not installed.
