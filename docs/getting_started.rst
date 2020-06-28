.. _Getting Started:

Getting Started with buildtest
==============================

Interacting with the client
---------------------------

After you install buildtest, you should find the client on your path::


      $ which buildtest
      ~/.local/bin/buildtest

If you don't see buildtest go back and review section :ref:`Setup`.

Cloning Tutorials
-----------------

To get started, let's clone the `tutorials <https://github.com/buildtesters/tutorials>`_ repository provided by buildtest
using ``buildtest repo add`` command::

    $ buildtest repo add git@github.com:buildtesters/tutorials.git
    Cloning into '/private/tmp/github.com/buildtesters/tutorials'...
    remote: Enumerating objects: 124, done.
    remote: Counting objects: 100% (124/124), done.
    remote: Compressing objects: 100% (88/88), done.
    remote: Total 124 (delta 40), reused 110 (delta 28), pack-reused 0
    Receiving objects: 100% (124/124), 22.95 KiB | 979.00 KiB/s, done.
    Resolving deltas: 100% (40/40), done.

For more details see :ref:`buildtest_repo`

Buildspecs
------------

buildtest is able to find and validate all buildspecs in your repos. The
command ``buildtest buildspec`` comes with the following options.

.. program-output:: cat docgen/buildtest_buildspec_--help.txt

To find all buildspecs run ``buildtest buildspec find`` which will discover
all buildspecs in all repos. buildtest will recursively traverse all repos
and seek out all `.yml` extensions so make sure your buildspecs conform to
the file extension.


.. program-output:: cat docgen/getting_started/buildspec-find.txt

buildtest will find all buildspecs and validate each file with the appropriate
schema type. buildspecs that pass validation will be displayed on screen.
buildtest will report all invalid buildspecs in a text file for you to review.

If you want to view or edit a buildspec you can type the name of test. Since we
can have more than one test in a buildspec, opening any of the `name` entry
that map to same file will result in same operation.

For example, we can view ``systemd_default_target`` as follows

.. program-output:: cat docgen/getting_started/buildspec-view.txt

To edit a buildspec you can run ``buildtest buildspec edit <name>`` which
will open file in editor. Once you make change, buildtest will validate the
buildspec upon closure, if there is an issue buildtest will report an error
during validation and you will be prompted to fix issue until it is resolved.

For example we can see an output message after editing file, user will be prompted
to press a key which will open the file in editor::

    $ buildtest buildspec edit systemd_default_target
    version 1.1 is not known for type {'1.0': 'script-v1.0.schema.json', 'latest': 'script-v1.0.schema.json'}. Try using latest.
    Press any key to continue

Build Usage
------------

The ``buildtest build`` command is used for building and running tests. Buildtest will read one or more Buildspecs (YAML)
file that adheres to one of the buildtest schemas. For a complete list of build options, run ``buildtest build --help``

.. program-output:: cat docgen/buildtest_build_--help.txt

Building a Test
----------------

To build a test, we use the ``-b`` to specify the the path to Buildspec file.
buildtest will discover the buildspecs specified by ``-b`` option, later you will
see you can provide more than one buildspec on the command line.

You can specify a full path to buildspec as follows

.. program-output:: cat docgen/getting_started/buildspec-abspath.txt

Alternately, you can specify a relative path from your current directory. The same
test can be built if you change into directory and run as follows::

    cd /tmp/github.com/buildtesters/tutorials
    buildtest build -b system/systemd.yml

Here is an example build with relative path

.. program-output:: cat docgen/getting_started/buildspec-relpath.txt

buildtest will add the cloned repository in buildspec search path which is a colon
separated list of paths to search. For example shown below we are at $HOME and we
are able the test ``examples/systemd.yml`` even if it's not in relative path but
it is a path found in the buildspec search path

.. code-block:: console

    (buildtest) siddiq90@DOE-7086392 ~ % pwd
    /Users/siddiq90
    (buildtest) siddiq90@DOE-7086392 ~ % ls examples/systemd.yml
    ls: examples/systemd.yml: No such file or directory
    (buildtest) siddiq90@DOE-7086392 ~ % buildtest build -b examples/systemd.yml
    Paths:
    __________
    Prefix: /private/tmp
    Buildspec Search Path: ['/private/tmp/github.com/buildtesters/tutorials', '/Users/siddiq90/.buildtest/site']
    Test Directory: /private/tmp/tests

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /private/tmp/github.com/buildtesters/tutorials/examples/systemd.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    systemd_default_target    script-v1.0.schema.json   /private/tmp/tests/systemd/systemd_default_target.sh /private/tmp/github.com/buildtesters/tutorials/examples/systemd.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    systemd_default_target local.bash           FAIL                 1                    /private/tmp/github.com/buildtesters/tutorials/examples/systemd.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 0/1 Percentage: 0.000%
    Failed Tests: 1/1 Percentage: 100.000%

Building Multiple Buildspecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Buildtest supports building multiple Buildspecs, just specify the ``-b`` option
for every Buildspec you want to build. For example let's build the following

.. program-output:: cat docgen/getting_started/multi-buildspecs.txt

buildtest can automatically detect Buildspecs based on filepath and directory so
if you know location to where Buildspecs are located you can specify a directory.
For instance, we can build all Buildspecs in a directory ``examples/openacc`` as follows

.. program-output:: cat docgen/getting_started/buildspec-directory.txt

Buildtest will recursively find all ``.yml`` files when you specify a directory
and process each Buildspec iteratively. You may mix file and directory with
``-b`` option to control what Buildspecs to build.

Excluding Buildspecs
~~~~~~~~~~~~~~~~~~~~~

Buildtest provides ``-x`` option to exclude Buildspecs which can be useful when
you want to build in a directory and exclude a few files or an entire directory.
For example we can do the following to exclude ``examples/systemd.yml`` but build
all buildspecs in ``examples`` directory::

    $ buildtest build -b examples -x examples/systemd.yml

buildtest will discover all Buildspecs and then exclude any buildspecs specified
by ``-x`` option. You can specify ``-x`` multiple times just like ``-b`` option.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows::

    $ buildtest build -b examples/ -x examples/
    There are no Buildspec files to process.

Buildtest will stop immediately if there are no Buildspecs to process, this is
true if you were to specify files instead of directory.

Invalid Buildspecs
~~~~~~~~~~~~~~~~~~~~

buildtest will skip any buildspecs that fail to validate, in that case
the test script will not be generated. Here is an example where only one buildspec
was successfully built and run while the other failed to pass validation

.. program-output:: cat docgen/getting_started/invalid-buildspec.txt

buildtest may skip tests from running if buildspec specifies an invalid
executor name since buildtest needs to know this in order to delegate test
to Executor class responsible for running the test. Here is an example
where test failed to run since we provided invalid executor.

.. program-output:: cat docgen/getting_started/invalid-executor.txt

Buildtest Report
-----------------

The ``buildtest report`` command will show result of all tests in a tabular
form. Shown below is an example::

    $ buildtest report
    name                 state                returncode           starttime            endtime              runtime              buildid              buildspec
    systemd_default_target FAIL                 1                    2020/06/15 23:35:13  2020/06/15 23:35:13  000.01 systemd_default_target_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/systemd.yml
    ulimit_filelock      FAIL                 1                    2020/06/15 23:35:13  2020/06/15 23:35:13  000.01 ulimit_filelock_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/ulimits.yml
    ulimit_cputime       PASS                 0                    2020/06/15 23:35:13  2020/06/15 23:35:13  000.01 ulimit_cputime_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/ulimits.yml
    ulimit_stacksize     FAIL                 1                    2020/06/15 23:35:13  2020/06/15 23:35:13  000.01 ulimit_stacksize_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/ulimits.yml
    selinux_disable      FAIL                 1                    2020/06/15 23:35:13  2020/06/15 23:35:13  000.01 selinux_disable_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/selinux.yml
    hello_f              FAIL                 127                  2020/06/15 23:35:13  2020/06/15 23:35:13  000.01 hello_f_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/serial/compiler_schema_hello.yml
    hello_c              PASS                 0                    2020/06/15 23:35:13  2020/06/15 23:35:14  000.12 hello_c_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/serial/compiler_schema_hello.yml
    hello_cplusplus      PASS                 0                    2020/06/15 23:35:14  2020/06/15 23:35:14  000.34 hello_cplusplus_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/serial/compiler_schema_hello.yml
    passing_args         PASS                 0                    2020/06/15 23:35:14  2020/06/15 23:35:14  000.11 passing_args_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/serial/compiler_schema_hello.yml
    vecadd_gnu           PASS                 0                    2020/06/15 23:35:14  2020/06/15 23:35:14  000.12 vecadd_gnu_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/openacc/vecadd.yml
    root_disk_usage      PASS                 0                    2020/06/15 23:35:14  2020/06/15 23:35:14  000.01 root_disk_usage_2020-06-15-23-35 /private/tmp/github.com/buildtesters/tutorials/examples/disk_usage.yml

buildtest will store result metadata of each test in a file ``var/report.json`` which
is found in root of buildtest. This file is updated upon every ``buildtest build`` command.

Logfile
-------

Currently, buildtest will write the log file for any ``buildtest build`` command
in ``buildtest.log`` of the current directory. The logfile will be overwritten
if you run repeative commands from same directory. A permanent log file location
will be implemented (TBD).
