How to use buildtest
====================


.. contents::
   :backlinks: none


If you have not completed setup your environment please :ref:`checkout the  setup. <Setup>`


Usage
-----

Let's start with the basics.

If you are unsure about buildtest see the help section (``buildtest --help``) for more details.

.. program-output:: cat scripts/how_to_use_buildtest/buildtest-help.txt

Building the Test
-----------------

Whenever you want to build a test, check your module environment (``module av``) to find out what software package
exist on your system. Let's build test for ``GCCcore/6.4.0`` module using buildtest by running
``_buildtest build -s GCCcore/6.4.0``

.. program-output:: cat scripts/how_to_use_buildtest/example-GCCcore-6.4.0.txt


Running The Test
-----------------

You can run the in several ways. The easiest way to run the test is via buildtest
using ``_buildtest run -a GCCcore/6.4.0``

.. program-output:: cat scripts/how_to_use_buildtest/run-GCCcore-6.4.0.txt


TAB Argument Completion
-----------------------

buildtest use the argcomplete python module to autocomplete buildtest argument.
Just press TAB key on the keyboard to fill in the arguments.

For instance if you just type ``buildtest`` followed by TAB you should see the
following.

::

    (buildtest-0.5.0) [siddis14@adwnode1 buildtest-framework]$ buildtest
    build               -fc                 -ft                 list                run                 --show-keys         --version
    --clean-logs        --findconfig        -h                  --logdir            --scantest          --submitjob         yaml
    --diff-trees        --findtest          --help              --module-load-test  --show              -V


.. Note:: You will need to press the TAB key few times before it shows all the
   args

TAB completion works for choice parameters on options: ``--shell``, ``--software``,
``--toolchain``, ``--package``, ``--python-package``, ``--perl-package``, ``--r-package``,
``--ruby-package``, ``--testname``,

TAB complete on ``buildtest build --software``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


TAB complete on ``_buildtest build --software`` option will present all unique
software found in module tree defined by ``BUILDTEST_MODULE_ROOT``


::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ _buildtest build --software
    Display all 125 possibilities? (y or n)
    Autoconf/2.69-GCCcore-6.4.0                                 GROMACS/2016.5-intel-2018a                                  ncurses/6.0
    Automake/1.15.1-GCCcore-6.4.0                               GSL/2.4-GCCcore-6.4.0                                       ncurses/6.0-GCCcore-6.4.0
    Autotools/20170619-GCCcore-6.4.0                            Guile/1.8.8-GCCcore-6.4.0                                   netCDF/4.5.0-intel-2018a
    BamTools/2.5.1-intel-2018a                                  HDF5/1.10.1-intel-2018a                                     netCDF-Fortran/4.4.4-intel-2018a
    BEDTools/2.27.1-intel-2018a                                 help2man/1.47.4                                             nettle/3.3-GCCcore-6.4.0
    binutils/2.28                                               help2man/1.47.4-GCCcore-6.4.0                               NLopt/2.4.2-intel-2018a
   --More--

TAB complete on ``buildtest build --toolchain``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TAB completion on ``buildtest build --toolchain`` will present all
easybuild toolchains installed in the software stack

::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ buildtest build --toolchain
    foss/2018a                          GCCcore/6.4.0                       iccifort/2018.1.163-GCC-6.4.0-2.28  intel/2018a
    GCC/6.4.0-2.28                      gompi/2018a                         iimpi/2018a


TAB complete on ``buildtest build --package``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TAB completion on ``_buildtest build --package`` will display all the system package that have a yaml
file typically found in directory ``$BUILDTEST_CONFIGS_REPO/buildtest/system`` directory.

::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ buildtest build --package
    acl                  CentrifyDC-openssh   file                 git                  ncurses              powertop             sed                  util-linux           zip
    at                   chrony               firefox              htop                 numactl              procps-ng            singularity-runtime  wget
    atop                 coreutils            gcc                  hwloc                openssh-clients      python               strace               which
    binutils             curl                 gcc-c++              iptables             perl                 rpm                  systemd              xz
    bzip2                diffstat             gcc-gfortran         ltrace               pinfo                ruby                 time                 yum


TAB completion on ``_buildtest run --testname``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can run individual test via buildtest using ``--testname`` option and this supports
tab completion.

::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ buildtest run --testname /tmp/buildtest-tests/
    Display all 296 possibilities? (y or n)
    /tmp/buildtest-tests/ebapp/GCCcore/6.4.0/arglist.c.csh                                 /tmp/buildtest-tests/ebapp/Ruby/2.5.0-intel-2018a/tilt_--help.sh
    /tmp/buildtest-tests/ebapp/GCCcore/6.4.0/arglist.c.sh                                  /tmp/buildtest-tests/ebapp/Ruby/2.5.0-intel-2018a/which_htmldiff_--version.sh
    /tmp/buildtest-tests/ebapp/GCCcore/6.4.0/cpp_--version.sh                              /tmp/buildtest-tests/system/acl/_usr_bin_chacl_-l__.sh
    /tmp/buildtest-tests/ebapp/GCCcore/6.4.0/gcc-ar_-V.csh                                 /tmp/buildtest-tests/system/acl/_usr_bin_getfacl_-v.sh
    /tmp/buildtest-tests/ebapp/GCCcore/6.4.0/gcc-ar_-V.sh                                  /tmp/buildtest-tests/system/acl/_usr_bin_setfacl_-v.sh
    /tmp/buildtest-tests/ebapp/GCCcore/6.4.0/gcc-nm_-V.csh                                 /tmp/buildtest-tests/system/at/find__usr_bin_batch.sh
    /tmp/buildtest-tests/ebapp/GCCcore/6.4.0/gcc-nm_-V.sh                                  /tmp/buildtest-tests/system/at/find__usr_sbin_atd.sh

    --More--

TAB completion on ``buildtest run --software``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TAB completion works on ``buildtest run --software`` which return a list of software
you can run tests that were generated by ``_buildtest build -s <module>``

::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ buildtest run --software
    GCCcore/6.4.0                     Perl/5.26.0-GCCcore-6.4.0         Python/2.7.14-GCCcore-6.4.0-bare  R/3.4.3-intel-2018a-X11-20171023
    OpenMPI/3.0.0-GCC-6.4.0-2.28      Python/2.7.14-GCCcore-6.4.0       Python/2.7.14-intel-2018a         Ruby/2.5.0-intel-2018a



TAB completion on ``buildtest run --package``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TAB completion works on ``buildtest run --package`` which return a list of
system package you can run tests that were generated by ``buildtest build --package <package>``

::

    (buildtest) [siddis14@adwnode1 buildtest-framework]$ _buildtest run --package
    acl        at         atop       binutils   bzip2      chrony     coreutils  curl       gcc        wget


System Package Test
-------------------

buildtest can generate tests for system packages using the option
``buildtest build --package <package>``. Currently, system package test only
perform santiy check against binaries found in the system. The framework will automatically generate
binary test by checking the system default paths i.e ``/usr/bin``, ``/usr/local/bin``, ``/usr/sbin``.

For instance to build test for the system package ``gcc`` you can do the following

.. code::

   buildtest build --package gcc


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
