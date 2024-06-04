.. _building_test:

Building Test  (``buildtest build``)
======================================

This reference guide will get you familiar with buildtest command line interface. Once
you complete this section, you can proceed to :ref:`writing buildspecs <buildspec_tutorial>`
section where we will cover how to write buildspecs.

When you clone buildtest, you also get a set of buildspecs that you can run on your
system. The ``buildtest build`` command is used for building and running tests.
Buildtest will read one or more buildspecs file that adheres to one of the
buildtest schemas. For a complete list of build options please run ``buildtest build --help``.

.. note::
   ``buildtest bd`` is an alias for ``buildtest build`` command.

Build Usage
------------

.. dropdown:: ``buildtest build --help``

    .. command-output:: buildtest build --help
       :shell:

Building a Test (``buildtest build --buildspec``)
---------------------------------------------------

To build a test, we use the ``--buildspec`` or short option ``-b`` to specify the
path to buildspec file. Let's see some examples, first we specify a full path to buildspec file.
In this example, buildtest will :ref:`discover buildspecs <discover_buildspecs>` followed by
parsing the test with appropriate schema and generate a shell script that is run
by buildtest. You can learn more about :ref:`build and test process <build_and_test_process>`.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml``

    .. command-output:: buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml
        :shell:

.. Note::
    buildtest will only read buildspecs with ``.yml`` extension, if you specify a
    ``.yaml`` it will be ignored by buildtest.

The ``--buildspec`` option can be used to specify a file or directory path. If you want
to build multiple buildspecs in a directory you can specify the directory path
and buildtest will recursively search for all ``.yml`` files. In the next example,
we build all tests in directory **general_tests/configuration**.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/general_tests/configuration/``

    .. command-output:: buildtest build -b $BUILDTEST_ROOT/general_tests/configuration/
       :shell:

Building Multiple Buildspecs
------------------------------

You can append ``-b`` option to build multiple buildspecs in the same
command. Buildtest will discover buildspecs for every argument (``-b``) and accumulate
a list of buildspecs to run. In this example, we instruct buildtest to build
a buildspec file and all buildspecs in a directory path.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/general_tests/configuration/ -b $BUILDTEST_ROOT/tutorials/vars.yml``

    .. command-output:: buildtest build -b $BUILDTEST_ROOT/general_tests/configuration/ -b $BUILDTEST_ROOT/tutorials/vars.yml
       :shell:

.. _exclude_buildspecs:

Excluding Buildspecs (``buildtest build --exclude``)
------------------------------------------------------

So far we learned how to build buildspecs by file and directory path using the ``-b``
option. Next, we will discuss how one may exclude buildspecs which behaves similar to
``-b`` option. You can exclude buildspecs via ``--exclude`` or short option ``-x``
which can be useful when you want to exclude certain files or sub directory.

For example we can build all buildspecs in ``tutorials`` but exclude file ``tutorials/vars.yml``
by running::

    $ buildtest build -b tutorials -x tutorials/vars.yml

buildtest will discover all buildspecs and then exclude any buildspecs specified
by ``-x`` option. You can specify ``-x`` multiple times just like ``-b`` option.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows

.. dropdown:: ``buildtest bd -b tutorials/ -x tutorials/``
   :color: warning

    .. command-output:: buildtest bd -b tutorials/ -x tutorials/
        :returncode: 1

Buildtest will stop immediately if there are no Buildspecs to process, this is
true if you were to specify files instead of directory.

In this example, we build all buildspecs in a directory but exclude a file. Buildtest
will report the excluded buildspecs in the output and ``-x`` option can be appended multiple times.
The ``-x`` can be a file or a directory and behaves similar to ``-b`` option.

.. dropdown:: ``buildtest bd -b general_tests/configuration/ -x general_tests/configuration/ulimits.yml``

    .. command-output:: buildtest bd -b general_tests/configuration/ -x general_tests/configuration/ulimits.yml

.. _build_by_tags:

Building By Tags (``buildtest build --tags``)
-----------------------------------------------

buildtest can perform builds by tags by using ``--tags`` or short option (``-t``).
In order to use this feature, buildtest must load buildspecs in :ref:`cache <find_buildspecs>` which can be run
via ``buildtest buildspec find``. If you are unsure of the available tags you can
run ``buildtest buildspec find --tags`` or let buildtest tab-complete the available tags. For more details
see :ref:`buildspec_tags`.


Let's assume you want to build by tag name ``network``, buildtest
will attempt to find all tests that contain ``tags: ['network']`` in the buildspec
which is loaded in the buildcache cache. If a test matches the tag name, the test
will be picked up during the discover process.

.. dropdown:: ``buildtest build -t network``

    .. command-output:: buildtest build -t network

You can build by multiple tags by specifying ``--tags`` multiple times. In next
example we build all tests with tag name ``pass`` and ``python``.

.. dropdown:: ``buildtest build -t python -t pass``

    .. command-output:: buildtest build -t python -t pass

When multiple tags are specified, we search each tag independently and if it's
found in the buildspec cache we retrieve the buildspec file and add file to queue.
This queue is a list of buildspecs that buildtest will process (i.e ``parse``, ``build``, ``run``).
You can :ref:`query tags <buildspec_tags>` from buildspecs cache to see all available
tags by running ``buildtest buildspec find --tags``.

.. Note:: The ``--tags`` is used for discovering buildspec file and not filtering tests
   by tag.

You can specify multiple tag names as a comma separated list. In the
example below we build all tests with tag names ``pass``, ``fail`` and ``network``.

.. dropdown:: ``buildtest build -t pass,fail -t network``

    .. command-output:: buildtest build -t pass,fail -t network

You can combine ``--tags`` with ``--buildspec`` to discover buildspecs in a single command.
buildtest will query tags and buildspecs independently and combine all discovered
buildspecs together.

.. dropdown:: ``buildtest build --tags pass --buildspec tutorials/python-hello.yml``

    .. command-output:: buildtest build --tags pass --buildspec tutorials/python-hello.yml

As you may see, there are several ways to build buildspecs with buildtest. Tags is
great way to build a whole collection of tests if you don't know path to all the files. You can
specify multiple tags per buildspecs to classify how test can be run.

Exclude by tags (``buildtest build --exclude-tags``)
------------------------------------------------------

You can exclude tests by tagname using ``--exclude-tags`` option or
short option (``-xt``). Any tests that contains the ``tags`` field
is searched with list of excluded tags. If there is a match, the test
is skipped. If the test **does not** contain ``tags`` key, the test will be
included to run.

Let's take an example buildspec file which contains 4 tests.

.. literalinclude:: ../tutorials/test_status/pass_returncode.yml
    :language: yaml
    :emphasize-lines: 7,15,24,33

We will demonstrate this feature, by excluding tests with tag name ``pass``. Take note all tests
are run except for those that include ``pass``.

.. dropdown:: buildtest build -b tutorials/test_status/pass_returncode.yml -xt pass

    .. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml -xt pass

We can specify tags as a comma separated list to specify multiple
tags so one can do ``-xt tag1,tag2`` which is equivalent to ``-xt tag1 -xt tag2``.
You may even mix the two formats together where you can exclude tags: **tag1**, **tag2**, **tag3**
by running ``-xt tag1 -xt tag2,tag3``.

In this example below, we will exclude both  ``pass`` and ``fail`` tags which results in error message
where no test are eligible to run after exclusion has been applied.

.. dropdown:: buildtest build -b tutorials/test_status/pass_returncode.yml -xt pass,fail

    .. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml -xt pass,fail
        :returncode: 1

Building by Test Names (``buildtest build --name``)
-----------------------------------------------------

You can discover buildspecs by test names using the ``--name`` option or short option ``-n``. This feature can be used if
you want to run a particular test and not worrying about the buildspec file that is belongs to. Note we have tab
completion builtin to this feature to show list of tests that are found in the buildspec cache. Shown below
is an example output of the tab completion listing all available tests

.. code-block:: console

      buildtest build --name _bin_bash_shell
    _bin_bash_shell                   current_user_queue                lsf_version                       runtime_test_pass                 status_regex_stderr_pass
    _bin_sh_shell                     dead_nodes                        metric_file_regex                 sh_shell                          status_regex_stdout_fail
    add_numbers                       display_hosts_format              metric_file_regex_invalid_file    shell_options                     status_regex_stdout_pass
    always_fail                       display_lsf_hosts                 metric_regex_example              show_accounts                     status_returncode_by_executors
    always_pass                       executors_sbatch_declaration      multiple_executors                show_all_jobs                     stream_test
    assert_contains_fail              executors_vars_env_declaration    node_down_fail_list_reason        show_host_groups                  string_tag
    assert_eq_example                 exit1_fail                        nodes_state_allocated             show_jobs                         summary_example
    assert_eq_invalid_metric          exit1_pass                        nodes_state_completing            show_lsf_configuration            symlink_test
    assert_eq_mismatch                fail_test                         nodes_state_down                  show_lsf_models                   systemd_default_target
    assert_gt_example                 file_and_dir_checks               nodes_state_idle                  show_lsf_queues                   tcsh_env_declaration
    assert_le_example                 file_count_by_expression          nodes_state_reboot                show_lsf_queues_current_user      test1
    assert_lt_example                 file_count_by_extension           pass_and_fail_test                show_lsf_queues_formatted         test2


Let's try building an example test by name ``hello_world``. Take note in output, buildtest will show a breakdown of buildspecs
discovered by the test name.

.. dropdown:: ``buildtest build --name hello_world``

    .. command-output:: buildtest build --name hello_world

You can specify multiple test names just specify the option multiple times. In example below we will demonstrate this example

.. dropdown:: ``buildtest build --name add_numbers --name summary_example``

    .. command-output:: buildtest build --name add_numbers --name summary_example

Please note, buildtest will discover buildspecs given the test name (``--name``) option and then run all tests defined in the buildspec file.
A buildspec file may include several tests and by default all of them are run. This option is
**not meant to filter buildspecs by the selected test**, but only a means for discovering buildspecs by test name.

.. _build_by_executor:

Building by Executors (``buildtest build --executor``)
-------------------------------------------------------

Every buildspec is associated to an executor which is responsible for running the test.
You can instruct buildtest to run all tests by given executor via ``--executor`` option or short option ``-e``.
For instance, if you want to build all test associated to executor ``generic.local.csh`` you can run::

  $ buildtest build --executor generic.local.csh

buildtest will query buildspec cache for the executor name and retrieve a list of
buildspecs with matching executor name. To see a list of available executors in
buildspec cache see :ref:`querying buildspec executor <buildspec_executor>`.

.. Note:: By default all tests are run in buildspec file.  The ``buildtest build --executor`` option discovers
   buildspecs if one of the test matches the executor name. The ``--executor`` option
   is **not filtering tests but only discovering buildspecs**.

In this example we run all tests that are associated to ``generic.local.csh`` executor.

.. dropdown:: ``buildtest build --executor generic.local.csh``

    .. command-output:: buildtest build --executor generic.local.csh

.. Note:: The ``--executor`` option can be appended to discover tests by multiple executors.

.. _filter_buildspecs_with_buildtest_build:

Filtering Buildspecs (``buildtest build --filter``)
-----------------------------------------------------

buildtest has support for filtering buildspecs based on certain attributes defined in buildspec file. Upon :ref:`discover_buildspecs`, buildtest
will filter out tests or entire buildspec files. The ``buildtest build --filter`` option can be used to filter tests where the format is ``key1=val1;key2=val2,val3``.
The semicolon is used to specify multiple filter fields and the comma is used to specify multiple values for a given field.

To see all available filter fields you can run ``buildtest build --helpfilter`` and buildtest will
report the fields followed by description.

.. dropdown:: ``buildtest build --helpfilter``

    .. command-output:: buildtest build --helpfilter

In this example, we will discover all buildspecs based on tagname ``pass`` and then filter each **test** by tagname **pass** specified by ``--filter tags=pass``.

.. dropdown:: ``buildtest build -t pass --filter tags=pass``

    .. command-output:: buildtest build -t pass --filter tags=pass


buildtest can run filter tests by :ref:`maintainers <maintainers>`, this can be useful if you want to run tests that you are maintainer. The ``maintainers`` field is
set per buildspec and not each test. You can filter maintiners via ``--filter maintainers=<MAINTAINER_NAME>``. If the ``maintainers`` field is not specified
the buildspec will be filtered out if ``--filter maintainers`` is specified. In this next example, we will build all tests for maintainer
``@shahzebsiddiqui``.

.. dropdown:: ``buildtest build -b tutorials --filter maintainers=@shahzebsiddiqui``

    .. command-output:: buildtest build -b tutorials --filter maintainers=@shahzebsiddiqui

Please see :ref:`buildspec_maintainers` on list of maintainers and breakdown of buildspecs by maintainers.

We can also filter tests by ``type`` field in the buildspec which corresponds to the schema type. In this next example, we filter all tests by script schema type by
passing option ``--filter type=script``.

.. dropdown:: ``buildtest build -b tutorials --filter type=script --dry-run``

    .. command-output:: buildtest build -b tutorials --filter type=script --dry-run

Filter By Executor Type
-------------------------

In a HPC environment, you may want to run test locally on a login node or perhaps you only want to run batch jobs given a list of buildspecs specified on command line.
This can be done in buildtest via option **buildtest build --executor-type** which takes one of two values **local** or **batch**. If you want to filter all tests
by local executor you can do ``buildtest build --executor-type local``. buildtest will filter test based on the ``executor`` property defined in the buildspec. Let's assume
we want to run all test by ``python`` tag on local executor you can do the following:

.. dropdown:: ``buildtest build -t python --executor-type local``

    .. command-output:: buildtest build -t python --executor-type local

Now let's say we want to rerun same command but now only run test that are batch, we can specify ``--executor-type batch`` and buildtest will filter tests
by executor and find all batch executors. In this case we see that all tests were filtered out and we have no test run.

.. dropdown:: ``buildtest build -t python --executor-type batch``
    :color: warning

    .. command-output:: buildtest build -t python --executor-type batch
        :returncode: 1

This option can be particularly useful if want to run a lot of tests and you are not sure which ones will run locally or batch. Let's say you have all
your buildspecs in a directory name **tests** and you want to run all test that will use local executor and you don't want to run the batch jobs then you
can do the following:

.. code-block::

    buildtest build -b tests --executor-type local

.. _build_stage:

Configure Build Stages
-----------------------

We can control behavior of ``buildtest build`` command to stop at certain phase
using ``--validate`` and ``--dry-run`` options.

Buildtest will validate all the buildspecs in the parse stage, so you can
instruct buildtest to stop at parse stage via ``--validate``. This can be useful
when debugging buildspecs that are invalid. In this example below, we instruct
buildtest to stop after parse stage.

.. dropdown:: ``buildtest build -b tutorials/vars.yml --validate``

    .. command-output:: buildtest build -b tutorials/vars.yml --validate

.. _invalid_buildspecs:

Invalid Buildspecs
--------------------

buildtest will skip any buildspecs that fail to validate, in that case
the test script will not be generated. Here is an example where we have an invalid
buildspec.

.. dropdown:: ``buildtest build -b tutorials/invalid_buildspec_section.yml``
   :color: warning

    .. command-output:: buildtest build -b tutorials/invalid_buildspec_section.yml
        :returncode: 1

buildtest may skip tests from running if buildspec specifies an invalid
executor name since buildtest needs to know this in order to delegate test
to Executor class responsible for running the test. Here is an example
where test failed to run since we provided invalid executor.

.. dropdown:: ``buildtest build -b tutorials/invalid_executor.yml``
   :color: warning

    .. command-output:: buildtest build -b tutorials/invalid_executor.yml
        :returncode: 1

Validate Tests (``buildtest build --validate``)
------------------------------------------------

When you use the **buildtest build** command, you have the option to enter a validate mode by
adding the ``--validate`` option. In this mode, the command will validate given buildspecs 
and stop after the parse stage. It's particularly useful when you're creating or editing a
buildspec file and want to check its validity before entering the build stage.
For instance, in the following example, we demonstrate how to instruct buildtest to halt after
the parse stage.

.. dropdown:: ``buildtest build -b tutorials/vars.yml --validate``

    .. command-output:: buildtest build -b tutorials/vars.yml --validate

Dry Run (``buildtest build --dry-run``)
----------------------------------------

When you use the **buildtest build** command, you have the option to enter a dry run mode by
adding the ``--dry-run`` option. In this mode, the command will simulate the build process
but won't execute the tests. It's particularly useful when you're creating or editing a
buildspec file and want to see how the test script is generated without actually running the tests.
For instance, in the following example, we demonstrate how to instruct buildtest to halt after
the build stage.

.. dropdown:: ``buildtest build -b tutorials/vars.yml --dry-run``

    .. command-output:: buildtest build -b tutorials/vars.yml --dry-run

Rebuild Tests (``buildtest build --rebuild``)
----------------------------------------------

buildtest can rebuild tests using the ``--rebuild`` option which can be useful if
you want to test a particular test multiple times. The rebuild option works across
all discovered buildspecs and create a new test instance (unique id) and test directory
path. To demonstrate we will build ``tutorials/python-shell.yml`` three times using
``--rebuild=3``.

.. dropdown:: ``buildtest build -b tutorials/python-shell.yml --rebuild=3``

    .. command-output:: buildtest build -b tutorials/python-shell.yml --rebuild=3

The rebuild works with all options including: ``--buildspec``, ``--exclude``, ``--tags``
and ``--executor``. buildtest will perform rebuild for all discovered tests, for instance in
this next example we will discover all tests by tag name **fail** and each test is rebuild twice.

.. dropdown:: ``buildtest build -t fail --rebuild 2``

    .. command-output:: buildtest build -t fail --rebuild 2

The rebuild option expects a range between **1-50**, the ``--rebuild=1`` is equivalent
to running without ``--rebuild`` option. We set a max limit for rebuild option to
avoid system degredation due to high workload.

If you try to exceed this bound you will get an error such as

.. dropdown:: ``buildtest build -b tutorials/test_status/pass_returncode.yml --rebuild 51``
    :color: warning

    .. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml --rebuild 51
        :returncode: 1

Limit Number of Tests (``buildtest build --limit``)
-----------------------------------------------------

The `buildtest build` command can limit the number of tests that can run via ``--limit`` option. This
can be useful when running large number of tests and you have no idea
how many tests will run. The ``--limit <NUM>`` option expects a positive number which will
limit number of tests to the total limit. If there are less tests to run than the
value specified by ``--limit``, then buildtest will run all the test. When buildtest has more
tests to run than the value specified by ``--limit``, then buildtest will exclude some tests.

To demonstrate this feature, we will run the same command with and without **--limit** option.

In first example, we will run a test that will run 4 tests.

.. dropdown:: ``buildtest build -b tutorials/test_status/pass_returncode.yml``

    .. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml

Now let's run this same test with ``--limit=2`` and notice buildtest will run **2/4** tests

.. dropdown:: ``buildtest build -b tutorials/test_status/pass_returncode.yml --limit=2``

    .. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml --limit=2

If you specify 0 or negative number you will get an error as follows

.. dropdown:: ``buildtest build -b tutorials/test_status/pass_returncode.yml --limit=0``
    :color: warning

    .. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml --limit=0
        :returncode: 2

Rerun Last Command (``buildtest build --rerun``)
-------------------------------------------------

The ``buildtest build --rerun`` command can be used to rerun **last successful** ``buildtest build`` command, this can be useful if you want to repeat a certain
build without having to remember the command or going through your command history to find the command you ran. When using this option all other options passed
to buildtest will be ignored. In order to use **--rerun** option you must run ``buildtest build`` command such that buildtest can rerun your last successful
command.

Let's start by building a simple test.

.. dropdown:: ``buildtest build -b tutorials/vars.yml``

    .. command-output:: buildtest build -b tutorials/vars.yml

Next let's rerun the same command via ``buildtest build --rerun`` and take note that it will rerun same command as before

.. dropdown:: ``buildtest build --rerun``

    .. command-output:: buildtest build --rerun

If you pass additional options with ``--rerun`` it will simply be ignored. In this case ``-t python --dry-run`` will not be read by buildtest instead we will
rerun same command.

.. dropdown:: ``buildtest build --rerun -t python --dry-run``

    .. command-output:: buildtest build --rerun -t python --dry-run

.. Note::
    The ``buildtest clean`` will erase all history of builds and if you run ``buildtest build --rerun`` will raise an exception

Specify Modules in command line
--------------------------------

If your system supports ``modules`` such as environment-modules or Lmod you can specify a list
of modules to load (``module load``) in the test via ``buildtest build --modules``. You can specify
a comma separated list of modules to load, for example if you want to load `gcc` and `python` module in
your test you can run ``buildtest build --modules gcc,python``. You may specify full name of module with
version for instance you want test to load `gcc/9.3.0` and `python/3.7` you can run ``buildtest build --modules gcc/9.3.0,python/3.7``.

If you want test to run ``module purge`` before running test you can specify ``buildtest build --module-purge`` option. If you specify
``--module-purge`` and ``--modules`` then ``module purge`` will be run prior to loading any modules.

Similarly, you can unload modules before running any test via ``buildtest build --unload-modules`` which is a list of modules to run
``module unload`` command and works similar to ``--modules`` option. Buildtest will unload modules before loading modules if both `--modules` and
`--unload-modules` are specified. If `--module-purge` is also specified then we run **module purge** first before loading/unloading any modules.


Use Alternate Configuration file
---------------------------------

If you want to use an alternate configuration file when building test you can use ``buildtest -c <config> build``.
buildtest will prefer configuration file on command line over the user configuration (``$HOME/.buildtest/config.yml``). For more
details see :ref:`which_configuration_file_buildtest_reads`.

Removing Stage Directory
------------------------

buildtest will write the tests in `stage` directory where test will be executed, typically buildtest will keep the
stage directory but if you want to remove the directory you can use ``buildtest build --remove-stagedir``.

Specify Project Account for batch jobs (``buildtest build --account``)
------------------------------------------------------------------------

For batch jobs you typically require one to specify a project account in order to charge jobs depending on your
scheduler you can use ``buildtest build --account`` option and specify an account name. The command line
argument ``--account`` will override configuration setting. For more details see :ref:`project_account`

.. _test_timeout:

Test Timeout (``buildtest build --timeout``)
--------------------------------------------

Buildtest can terminate test based on timeout value specified via ``--timeout`` option which can be used to terminate
long running test. The timeout is in seconds and value must be a positive integer which is applied to all
test that are run via ``buildtest build`` command. If test exceeds the timeout value, then process will be terminated.

To demonstrate this behavior, we will run the following test with a timeout of 1 sec which is expected to fail.
Take note of the test returncode of test.

.. dropdown:: ``buildtest build -b tutorials/sleep.yml --timeout 1``

    .. command-output:: buildtest build -b tutorials/sleep.yml --timeout 1

Now if we run this test with a higher timeout value we will see this test will pass, if no timeout is specified then test will
run until completion.

.. dropdown:: ``buildtest build -b tutorials/sleep.yml --timeout 10``

    .. command-output:: buildtest build -b tutorials/sleep.yml --timeout 10

.. _using_profiles:

Using Profiles (``buildtest build --profile``)
-----------------------------------------------

Buildtest has a concept of profiles, which allows one to run a set of ``buildtest build`` options without having to remember
all the options. This can be useful if you are running a set of tests repeatedly. In-order to use profiles you must first,
create a profile by using ``--save-profile``.

For example, let's create a profile called **python-tests** for all tests with tag ``python``

.. dropdown:: ``buildtest build -t python --save-profile=python-tests``

    .. command-output:: buildtest build -t python --save-profile=python-tests

Next, let's see our configuration file, you will notice a new section called ``profiles``
with a profile called **python-tests**

.. dropdown:: buildtest configuration with profile

    .. command-output:: buildtest config view


Next, let's build the tests via newly created profile and take note that it will run all tests with tag `python`

.. dropdown:: ``buildtest build --profile=python-tests``

    .. command-output:: buildtest build --profile=python-tests


You can also specify an alternate location to write configuration file via ``--write-config-file`` when saving profile configuration.
This can be useful if one wants to use a new configuration file without overwriting the current file for testing purposes.
To demonstrate this, we will save the profile to configuration file ``/tmp/my_config.yml``

.. dropdown:: ``buildtest build -t python --save-profile=python --write-config-file=/tmp/my_config.yml``

    .. command-output:: buildtest build -t python --save-profile=python --write-config-file=/tmp/my_config.yml

    We can view the profile configuration file by specifying the path to the configuration file.

    .. command-output:: buildtest --config /tmp/my_config.yml config view

Please note that when using ``-write-config-file``, the path must be a file path and file must not exist. If you specify
a directory path or file already exists you will get an error message.

.. _limit_max_jobs:

Limit Maximum Jobs that can run concurrently (``buildtest build --max-jobs``)
-----------------------------------------------------------------------------

Buildtest can cap a limit on number of tests that can run concurrently. This can be set in configuration file via :ref:`max_jobs <configuring_max_jobs>`
field or overridden on command line option via ``--max-jobs``. By default, buildtest will run all jobs concurrently, however with
``--max-jobs``, buildtest will limit number of concurrent jobs specified by ``--max-jobs``.

Let's limit the number of concurrent jobs to 2 tests, take note that buildtest will run 2 tests per iteration, and wait until test is completed and
then proceed to next test.

.. dropdown:: ``buildtest build -b tutorials/hello_world.yml --rebuild=5 --max-jobs=2``

    .. command-output:: buildtest build -b tutorials/hello_world.yml --rebuild=5 --max-jobs=2

Strict Mode
------------

Buildtest has an option to enable strict mode for test execution which can be enabled via ``--strict`` option. If this
is set, buildtest will instead ``set -eo pipefail`` in the generated test which will cause test to exit immediately if any
commands fail. To demonstrate this we have the following buildspec, which runs an **ls** command for an invalid path followed by
an **echo** command.

.. literalinclude:: ../tutorials/strict_example.yml
    :language: yaml
    :emphasize-lines: 8

If we were to run this test without strict mode, we see the test will pass.

.. dropdown:: ``buildtest build -b tutorials/strict_example.yml``

    .. command-output:: buildtest build -b tutorials/strict_example.yml

Now let's run the same test with strict mode enabled, we will see the test will fail with a different return code.

.. dropdown:: ``buildtest build -b tutorials/strict_example.yml --strict``

    .. command-output:: buildtest build -b tutorials/strict_example.yml --strict

    We can see the generated test using **buildtest inspect query -t** and we will see the test script has **set -eo pipefail** in
    the generated test.

    .. command-output:: buildtest inspect query -t linux_strict_test

Display Mode
-------------

Buildtest can display output of test content and stream outout and error file to console. This can be useful
if you want to see how the test is generated for debugging purposes.

In order to use this functionality, you can specify the ``--display`` option which takes either ``output`` or ``test``.
When ``output`` is specified, buildtest will display output and error files to console. When ``test``
is specified, buildtest will display the content of the test and build script. You can append the ``--display`` option
if you want to specify both options. Shown below we run a test and display both output and test.

.. dropdown:: ``buildtest build -b tutorials/vars.yml --display output --display test``

    .. command-output:: buildtest build -b tutorials/vars.yml --display output --display test
