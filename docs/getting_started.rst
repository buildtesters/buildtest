.. _Getting Started:

Getting Started with buildtest
==============================

Interacting with the client
---------------------------

After you install buildtest, you should find the client on your path::


      $ which buildtest
      ~/.local/bin/buildtest

If you don't see buildtest go back and review section :ref:`Setup`.

Buildspecs
------------

Finding Buildspecs
~~~~~~~~~~~~~~~~~~~~

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

buildtest will cache the results in **var/buildspec.cache** so subsequent
runs to ``buildtest buildspec find`` will be much faster since we read from cache.

Viewing Buildspecs
~~~~~~~~~~~~~~~~~~~~
If you want to view or edit a buildspec you can type the name of test. Since we
can have more than one test in a buildspec, opening any of the `name` entry
that map to same file will result in same operation.

For example, we can view ``systemd_default_target`` as follows

.. program-output:: cat docgen/getting_started/buildspec-view.txt

Editing Buildspecs
~~~~~~~~~~~~~~~~~~~~

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

.. _discover_buildspecs:

Discover Buildspecs
--------------------

The buildspec search resolution is described as follows:

- If file doesn't exist, check for file in :ref:`buildspec_roots` and break after first match

- If buildspec path is a directory, traverse directory recursively to find all ``.yml`` extensions

- If buildspec path is a file, check if file extension is not ``.yml``,  exit immediately

Shown below is a diagram on how buildtest discovers buildspecs. The user
inputs a buildspec via ``--buildspec`` or tags (``--tags``) :ref:`build_by_tags`
which will discover the buildspecs. User can :ref:`exclude_buildspecs`
using ``--exclude`` option which is processed after discovering buildspecs. The
excluded buildspecs are removed from list if found and final list of buildspecs
is processed.

.. image:: _static/DiscoverBuildspecs.jpg

Building a Test
----------------

To build a test, we use the ``--buildspec`` or short option ``-b`` to specify the
path to Buildspec file.


Let's see some examples, first we specify a full path to buildspec file

.. program-output:: cat docgen/getting_started/buildspec-abspath.txt

buildtest won't accept ``.yaml`` file extension for file, this can be demonstrated as
follows::

    $ buildtest build -b tests/examples/buildspecs/os.yaml
    Paths:
    __________
    Prefix: /private/tmp
    Buildspec Search Path: ['/Users/siddiq90/.buildtest/site']
    Test Directory: /private/tmp/tests
    tests/examples/buildspecs/os.yaml does not end in file extension .yml


In next example, our current directory is at $HOME and we are able to build
``examples/systemd.yml`` even if it's not in relative path but it is a path found
in the buildspec search path.

.. code-block:: console

    $ pwd
    /Users/siddiq90
    $ ls examples/systemd.yml
    ls: examples/systemd.yml: No such file or directory

.. program-output:: cat docgen/getting_started/buildspec-relpath.txt


buildtest can perform a directory build for instance let's build
for directory ``tests/examples/buildspecs`` where buildtest will recursively
search for all ``.yml`` files

.. program-output:: cat docgen/getting_started/buildspec-directory.txt

In next section, you will see, we can build multiple buildspecs and interchange
file and directory with ``-b`` option.


Building Multiple Buildspecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Buildtest supports building multiple buildspecs, just specify the ``-b`` option
for every Buildspec you want to build. In this example, we specify a file and
directory path. The search resolution is performed for every argument (``-b``)
independently, and accumulated into list.

.. program-output:: cat docgen/getting_started/multi-buildspecs.txt

.. _exclude_buildspecs:

Excluding Buildspecs
~~~~~~~~~~~~~~~~~~~~~

Buildtest provides ``--exclude`` option or short option ``-x`` to exclude
buildspecs which can be useful when you want to build all buildspecs in a directory
but exclude a few buildspecs or exclude a sub-directory.

For example we can build all buildspecs in ``examples`` but exclude file ``examples/systemd.yml``
by running::

    $ buildtest build -b examples -x examples/systemd.yml

buildtest will discover all Buildspecs and then exclude any buildspecs specified
by ``-x`` option. You can specify ``-x`` multiple times just like ``-b`` option.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows::

    $ buildtest build -b examples/ -x examples/
    There are no Buildspec files to process.

Buildtest will stop immediately if there are no Buildspecs to process, this is
true if you were to specify files instead of directory.

.. _build_by_tags:

Building By Tags
~~~~~~~~~~~~~~~~~

buildtest can perform builds by tags by using ``--tags`` option. To build all tutorials
tests you can perform ``buildtest build --tags tutorials``. In the buildspec
there is a field ``tags: [tutorials]`` to classify tests. buildtest will read the
cache file ``var/buildspec-cache.json`` and see which buildspecs have a matching
tag. You should run ``buildtest buildspec find`` atleast once, in order to detect
cache file.


::

    $ buildtest build --tags tutorials
    Paths:
    __________
    Prefix: None
    Buildspec Search Path: ['/Users/siddiq90/Documents/buildtest/tutorials']
    Test Directory: /Users/siddiq90/Documents/buildtest/var/tests

    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /Users/siddiq90/Documents/buildtest/tutorials/pass_returncode.yml
    /Users/siddiq90/Documents/buildtest/tutorials/python-shell.yml
    /Users/siddiq90/Documents/buildtest/tutorials/compilers/passing_args.yml
    /Users/siddiq90/Documents/buildtest/tutorials/environment.yml
    /Users/siddiq90/Documents/buildtest/tutorials/invalid_executor.yml
    /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml
    /Users/siddiq90/Documents/buildtest/tutorials/selinux.yml
    /Users/siddiq90/Documents/buildtest/tutorials/skip_tests.yml
    /Users/siddiq90/Documents/buildtest/tutorials/vars.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    [skip] test is skipped.
     Name                  | Schema File               | Test Path                                                                                     | Buildspec
    -----------------------+---------------------------+-----------------------------------------------------------------------------------------------+--------------------------------------------------------------------------
     exit1_fail            | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/pass_returncode/exit1_fail.sh          | /Users/siddiq90/Documents/buildtest/tutorials/pass_returncode.yml
     exit1_pass            | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/pass_returncode/exit1_pass.sh          | /Users/siddiq90/Documents/buildtest/tutorials/pass_returncode.yml
     returncode_mismatch   | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/pass_returncode/returncode_mismatch.sh | /Users/siddiq90/Documents/buildtest/tutorials/pass_returncode.yml
     circle_area           | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.python/python-shell/circle_area.py        | /Users/siddiq90/Documents/buildtest/tutorials/python-shell.yml
     executable_arguments  | compiler-v1.0.schema.json | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/passing_args/executable_arguments.sh | /Users/siddiq90/Documents/buildtest/tutorials/compilers/passing_args.yml
     environment_variables | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/environment/environment_variables.sh | /Users/siddiq90/Documents/buildtest/tutorials/environment.yml
     wrongexecutor         | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/badexecutor/invalid_executor/wrongexecutor.sh   | /Users/siddiq90/Documents/buildtest/tutorials/invalid_executor.yml
     _bin_sh_shell         | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/shell_examples/_bin_sh_shell.sh        | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml
     _bin_bash_shell       | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/shell_examples/_bin_bash_shell.sh    | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml
     bash_shell            | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/shell_examples/bash_shell.sh         | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml
     sh_shell              | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/shell_examples/sh_shell.sh             | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml
     shell_options         | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/shell_examples/shell_options.sh        | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml
     selinux_disable       | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/selinux/selinux_disable.sh           | /Users/siddiq90/Documents/buildtest/tutorials/selinux.yml
     unskipped             | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/skip_tests/unskipped.sh              | /Users/siddiq90/Documents/buildtest/tutorials/skip_tests.yml
     variables             | script-v1.0.schema.json   | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/vars/variables.sh                    | /Users/siddiq90/Documents/buildtest/tutorials/vars.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    [wrongexecutor]: Failed to Run Test
     name                  | executor     | status   |   returncode | testpath
    -----------------------+--------------+----------+--------------+-----------------------------------------------------------------------------------------------
     exit1_fail            | local.sh     | FAIL     |            1 | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/pass_returncode/exit1_fail.sh
     exit1_pass            | local.sh     | PASS     |            1 | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/pass_returncode/exit1_pass.sh
     returncode_mismatch   | local.sh     | FAIL     |            2 | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/pass_returncode/returncode_mismatch.sh
     circle_area           | local.python | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.python/python-shell/circle_area.py
     executable_arguments  | local.bash   | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/passing_args/executable_arguments.sh
     environment_variables | local.bash   | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/environment/environment_variables.sh
     _bin_sh_shell         | local.sh     | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/shell_examples/_bin_sh_shell.sh
     _bin_bash_shell       | local.bash   | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/shell_examples/_bin_bash_shell.sh
     bash_shell            | local.bash   | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/shell_examples/bash_shell.sh
     sh_shell              | local.sh     | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/shell_examples/sh_shell.sh
     shell_options         | local.sh     | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.sh/shell_examples/shell_options.sh
     selinux_disable       | local.bash   | FAIL     |            1 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/selinux/selinux_disable.sh
     unskipped             | local.bash   | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/skip_tests/unskipped.sh
     variables             | local.bash   | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/vars/variables.sh



    Error Messages from Stage: Run
    ________________________________________________________________________________
    [wrongexecutor]: executor badexecutor is not defined in /Users/siddiq90/.buildtest/config.yml



    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 14 tests
    Passed Tests: 11/14 Percentage: 78.571%
    Failed Tests: 3/14 Percentage: 21.429%

.. _invalid_buildspecs:

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
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | name                  | state   |   returncode | starttime           | endtime   |    runtime | build_id                               | buildspec                                                                |
    +=======================+=========+==============+=====================+===========+============+========================================+==========================================================================+
    | _bin_sh_shell         | FAIL    |            2 | 2020/08/11 10:17:14 |           | 0.00391071 | _bin_sh_shell_2020-08-11-10-17         | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml         |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | _bin_bash_shell       | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0846076  | _bin_bash_shell_2020-08-11-10-17       | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml         |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | bash_shell            | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0846076  | bash_shell_2020-08-11-10-17            | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml         |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | sh_shell              | FAIL    |            2 | 2020/08/11 10:17:14 |           | 0.00391071 | sh_shell_2020-08-11-10-17              | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml         |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | shell_options         | FAIL    |            2 | 2020/08/11 10:17:14 |           | 0.00391071 | shell_options_2020-08-11-10-17         | /Users/siddiq90/Documents/buildtest/tutorials/shell_examples.yml         |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | exit1_fail            | FAIL    |            2 | 2020/08/11 10:17:14 |           | 0.00391071 | exit1_fail_2020-08-11-10-17            | /Users/siddiq90/Documents/buildtest/tutorials/pass_returncode.yml        |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | exit1_pass            | FAIL    |            2 | 2020/08/11 10:17:14 |           | 0.00391071 | exit1_pass_2020-08-11-10-17            | /Users/siddiq90/Documents/buildtest/tutorials/pass_returncode.yml        |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | returncode_mismatch   | FAIL    |            2 | 2020/08/11 10:17:14 |           | 0.00391071 | returncode_mismatch_2020-08-11-10-17   | /Users/siddiq90/Documents/buildtest/tutorials/pass_returncode.yml        |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | selinux_disable       | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0846076  | selinux_disable_2020-08-11-10-17       | /Users/siddiq90/Documents/buildtest/tutorials/selinux.yml                |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | variables             | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0846076  | variables_2020-08-11-10-17             | /Users/siddiq90/Documents/buildtest/tutorials/vars.yml                   |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | circle_area           | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0538504  | circle_area_2020-08-11-10-17           | /Users/siddiq90/Documents/buildtest/tutorials/python-shell.yml           |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | executable_arguments  | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0846076  | executable_arguments_2020-08-11-10-17  | /Users/siddiq90/Documents/buildtest/tutorials/compilers/passing_args.yml |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | unskipped             | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0846076  | unskipped_2020-08-11-10-17             | /Users/siddiq90/Documents/buildtest/tutorials/skip_tests.yml             |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+
    | environment_variables | PASS    |            0 | 2020/08/11 10:17:14 |           | 0.0846076  | environment_variables_2020-08-11-10-17 | /Users/siddiq90/Documents/buildtest/tutorials/environment.yml            |
    +-----------------------+---------+--------------+---------------------+-----------+------------+----------------------------------------+--------------------------------------------------------------------------+


buildtest will store result metadata of each test in a file ``var/report.json`` which
is found in root of buildtest. This file is updated upon every ``buildtest build`` command.

Debug Mode
------------

buildtest can stream logs to ``stdout`` stream for debugging. You can use ``buildtest -d <DEBUGLEVEL>``
or long option ``--debug`` with any buildtest commands. The DEBUGLEVEL are:
``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``,  ``CRITICAL`` which controls
log level to be displayed in console. buildtest is using
`logging.setLevel <https://docs.python.org/3/library/logging.html#logging.Logger.setLevel>`_
to control log level.

The same content is logged in **buildtest.log** with default log level of ``DEBUG``.
If you want to get all logs use ``-d DEBUG`` with your buildtest command::

    buildtest -d DEBUG <command>

Logfile
-------

Currently, buildtest will write the log file for any ``buildtest build`` command
in ``buildtest.log`` of the current directory. The logfile will be overwritten
if you run repeative commands from same directory. A permanent log file location
will be implemented (TBD).
