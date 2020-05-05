.. _Getting Started:

Getting Started with buildtest
==============================

Interacting with the client
---------------------------

After you install buildtest, you should find the client on your path::


      $ which buildtest
      ~/.local/bin/buildtest

If you don't see buildtest go back and review section :ref:`Setup`.

 - The test directory is where tests will be written, which defaults to ``$HOME/.buildtest/testdir``.
 - You can store tests (that can be referenced with relative paths) under ``$HOME/.buildtest/site``.


Cloning Tutorials
-----------------

To get started, let's clone the `tutorials <https://github.com/buildtesters/tutorials>`_ repository provided by buildtest
using ``buildtest get`` command::

    $ buildtest get https://github.com/buildtesters/tutorials.git
    Cloning into '/u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials'...
    remote: Enumerating objects: 91, done.
    remote: Counting objects: 100% (91/91), done.
    remote: Compressing objects: 100% (64/64), done.
    remote: Total 91 (delta 23), reused 85 (delta 19), pack-reused 0
    Unpacking objects: 100% (91/91), done.

This is equivalent to doing this::

    $ mkdir -p $HOME/.buildtest/site/github.com/buildtesters
    $ git clone https://github.com/buildtesters/tutorials.git $HOME/.buildtest/site/github.com/buildtesters/tutorials

For more details see :ref:`buildtest_get`

Build Usage
------------

The ``buildtest build`` command is used for building and running tests. Buildtest will read one or more Buildspecs (YAML)
file that adheres to one of the buildtest schemas. For a complete list of build options, run ``buildtest build --help``

.. program-output:: cat docgen/buildtest_build_--help.txt

Building a Test
----------------

To build a test, we use the ``-b`` option to select the Buildspec to build let's run the following

.. program-output:: cat docgen/gettingstarted-example1.txt

Buildtest will discover the Buildspecs specified by ``-b`` option, later you will see you can provide more than one
Buildspec on the command line. Buildtest will display the Buildspec Name, a Test name, Status of the test, and
full path to Buildspec file. Finally, buildtest will summarize the test results with list of pass and failed tests.

In the command above we specified an absolute path to a Buildspec, alternately we can specify a relative path from ``site``
directory to build the test. For example, the above command could be achieved by running::

    buildtest build -b github.com/buildtesters/tutorials/system/systemd.yml

Buildtest, will resolve the Buildspec path relative to your working directory, so if you don't like to specify a long path.
you can ``cd`` into a particular location and build from there. For instance, you can go to the root of **tutorials** repo
and build your Buildspec as follows::

    cd $HOME/.buildtest/site/github.com/buildtesters/tutorials
    buildtest build -b system/systemd.yml

Buildtest supports building multiple Buildspecs, just specify the ``-b`` option for every Buildspec you want to build. For
example let's build the following::

    $ buildtest build -b system/disk_usage.yml -b system/selinux.yml

            Discovered Buildspecs

    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/disk_usage.yml
    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/selinux.yml



    Buildspec Name                 SubTest                        Status                         Buildspec Path
    ________________________________________________________________________________________________________________________
    disk_usage                     root_disk_usage                PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/disk_usage.yml
    selinux                        selinux_disable                PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/selinux.yml


    ============================================================
                            Test summary
    ============================================================
    Executed 2 tests
    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%


buildtest can automatically detect Buildspecs based on filepath and directory so if you know location to where
Buildspecs are located you can specify a directory. For instance, we can build all Buildspecs in a directory ``system``
as follows::

    $ buildtest build -b system/

            Discovered Buildspecs

    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/ulimits.yml
    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/disk_usage.yml
    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/systemd.yml
    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/selinux.yml



    Buildspec Name                 SubTest                        Status                         Buildspec Path
    ________________________________________________________________________________________________________________________
    ulimits                        ulimit_filelock                PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/ulimits.yml
    ulimits                        ulimit_cputime                 PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/ulimits.yml
    ulimits                        ulimit_stacksize               FAILED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/ulimits.yml
    disk_usage                     root_disk_usage                PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/disk_usage.yml
    systemd                        systemd_default_target         PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/systemd.yml
    selinux                        selinux_disable                PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/selinux.yml


    ============================================================
                            Test summary
    ============================================================
    Executed 6 tests
    Passed Tests: 5/6 Percentage: 83.333%
    Failed Tests: 1/6 Percentage: 16.667%

Buildtest will recursively find all ``.yml`` files when you specify a directory and process each Buildspec iteratively. You
may mix file and directory with ``-b`` option to control what Buildspecs to build.

Buildtest provides ``-x`` option to exclude Buildspecs which can be useful when you want to build in a directory and exclude
a few Buildspecs. For example we can exclude the failed test ``ulimits.yml`` as follows::


    $ buildtest build -b system/ -x system/ulimits.yml

                Discovered Buildspecs

    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/disk_usage.yml
    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/systemd.yml
    /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/selinux.yml



    Buildspec Name                 SubTest                        Status                         Buildspec Path
    ________________________________________________________________________________________________________________________
    disk_usage                     root_disk_usage                PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/disk_usage.yml
    systemd                        systemd_default_target         PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/systemd.yml
    selinux                        selinux_disable                PASSED                         /u/users/ssi29/.buildtest/site/github.com/buildtesters/tutorials/system/selinux.yml


    ============================================================
                            Test summary
    ============================================================
    Executed 3 tests
    Passed Tests: 3/3 Percentage: 100.000%
    Failed Tests: 0/3 Percentage: 0.000%

buildtest will discover all Buildspecs defined by ``-b`` option followed by excluding tests that were discovered by option
``-x``. You can specify ``-x`` multiple times as you like to exclude a file or directory.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows::

    $ buildtest build -b system/ -x system/
    There are no Buildspec files to process.

Buildtest will stop immediately if there are no Buildspecs to process, this is true if you were to specify files instead of
directory.




