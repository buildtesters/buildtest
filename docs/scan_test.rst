What can you test with buildtest? Use ``buildtest --scantest``
=================================================================

The option ``--scantest`` was provided to give users insight on what tests can be
conducted for software and system packages based on what is installed in your system.

buildtest will search repository ``BUILDTEST_CONFIGS_REPO`` and see if there are
any **yaml** files for software stack based on value provided by $BUILDTEST_MODULE_ROOT

buildtest will also check for system packages installed in your system and check
the repository BUILDTEST_CONFIGS_REPO for any system package yaml configuration.

Shown below is an output of ``--scantest`` which will give you idea what you can
test.

.. code::

    [siddis14@prometheus buildtest-framework]$ _buildtest --scantest


    Software Packages that can be tested with buildtest
    ---------------------------------------------------
    binutils
    bzip2
    cairo
    gettext
    git
    hwloc
    icc
    intel
    ncurses
    numactl


    System Packages that can be tested with buildtest
    ---------------------------------------------------
    CentrifyDC-openssh
    acl
    atop
    binutils
    bzip2
    chrony
    coreutils
    curl
    diffstat
    file
    firefox
    gcc
    gcc-c++
    gcc-gfortran
    git
    htop
    hwloc
    iptables
    ltrace
    ncurses
    numactl
    openssh-clients
    perl
    pinfo
    powertop
    procps-ng
    python
    rpm
    ruby
    sed
    singularity-runtime
    strace
    systemd
    tcsh
    time
    util-linux
    wget
    which
    xz
    yum
    zip
