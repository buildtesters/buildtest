.. _building_test:

Building Test via buildtest
==============================

This guide will get you familiar with buildtest command line interface. Once
you complete this section, you can proceed to :ref:`writing buildspecs <writing_buildspecs>`
section where we will cover how to write buildspecs.

Once you install buildtest, you should find the `buildtest` command in your **$PATH**.
You can check the path to buildtest command by running::

      $ which buildtest

If you don't see buildtest go back and :ref:`install buildtest <Setup>`.


When you clone buildtest, you also get a set of buildspecs that you can run on your
system. The ``buildtest build`` command is used for building and running tests.
Buildtest will read one or more buildspecs file that adheres to one of the
buildtest schemas. For a complete list of build options, run ``buildtest build --help``

Build Usage
------------

.. program-output:: cat docgen/buildtest_build_--help.txt


Building a Test
----------------

To build a test, we use the ``--buildspec`` or short option ``-b`` to specify the
path to buildspec file. Let's see some examples, first we specify a full path to buildspec file.
In this example, buildtest will :ref:`discover buildspecs <discover_buildspecs>` followed by
parsing the test with appropriate schema and generate a shell script that is run
by buildtest. You can learn more about :ref:`build and test process <build_and_test_process>`.

.. program-output:: cat docgen/getting_started/building/buildspec_abspath.txt

.. Note::
    buildtest will only read buildspecs with ``.yml`` extension, if you specify a
    ``.yaml`` it will be ignored by buildtest.

The ``--buildspec`` option can be used to specify a file or directory path. If you want
to build multiple buildspecs in a directory you can specify the directory path
and buildtest will recursively search for all ``.yml`` files. In the next example,
we build all tests in directory **general_tests/configuration**.

.. program-output:: cat docgen/getting_started/building/buildspec_directory.txt

Building Multiple Buildspecs
------------------------------

You can append ``-b`` option to build multiple buildspecs in the same
command. Buildtest will discover buildspecs for every argument (``-b``) and accumulate
a list of buildspecs to run. In this example, we instruct buildtest to build
a buildspec file and all buildspecs in a directory path.

.. program-output:: cat docgen/getting_started/building/multi_buildspecs.txt

.. _exclude_buildspecs:

Excluding Buildspecs
---------------------

So far we learned how to build buildspecs by file and directory path using the ``-b``
option. Next, we will discuss how one may exclude buildspecs which behaves similar to
``-b`` option. You can exclude buildspecs via ``--exclude`` or short option ``-x``
which can be useful when you want to exclude certain files or sub directory.

For example we can build all buildspecs in ``tutorials`` but exclude file ``tutorials/vars.yml``
by running::

    $ buildtest build -b tutorials -x tutorials/vars.yml

buildtest will discover all buildspecs and then exclude any buildspecs specified
by ``-x`` option. You can specify ``-x`` multiple times just like ``-b`` option.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows::

    $ buildtest build -b tutorials/ -x tutorials/
    There are no Buildspec files to process.

Buildtest will stop immediately if there are no Buildspecs to process, this is
true if you were to specify files instead of directory.

In this example, we build all buildspecs in a directory but exclude two files. Buildtest
will report the excluded buildspecs in the output.

.. program-output:: cat docgen/getting_started/building/exclude_buildspecs.txt

.. _build_by_tags:

Building By Tags
-----------------

buildtest can perform builds by tags by using ``--tags`` or short option (``-t``).
In order to use this feature, buildtest must load buildspecs in :ref:`cache <find_buildspecs>` which can be run
via ``buildtest buildspec find``.

To build all tutorials tests you can perform ``buildtest build --tags tutorials``.
In buildspec file, there is a field ``tags: [tutorials]`` to classify tests.
buildtest will read the cache file ``var/buildspec-cache.json`` and see which
buildspecs have a matching tag. You should run ``buildtest buildspec find``
atleast once, in order to detect cache file.

.. program-output::  cat docgen/getting_started/building/tags.txt

You can build by multiple tags by specifying ``--tags`` multiple times. In next
example we build all tests with tag name ``pass`` and ``python``.

.. program-output:: cat docgen/getting_started/building/multi_tags.txt

When multiple tags are specified, we search each tag independently and if it's
found in the buildspec cache we retrieve the buildspec file and add file to queue.
This queue is a list of buildspecs that buildtest will process (i.e ``parse``, ``build``, ``run``).
You can :ref:`query tags <buildspec_tags>` from buildspecs cache to see all available
tags by running ``buildtest buildspec find --tags``.

.. Note:: The ``--tags`` is used for discovering buildspec file and not filtering tests
   by tag. If you want to filter tests by tags use ``--filter-tags``.

The ``--filter-tags`` or short option ``-ft`` is used for filtering tests by
tag name. The ``--filter-tags`` is used in conjunction with other options like
``--buildspec``, ``--tags``, or ``--executor`` for discovering buildspecs.
Let's rerun the previous example and filter tests by ``pass``. Now we only see
tests built with tagname ``pass`` and all remaining tests were ignored.

.. program-output:: cat docgen/getting_started/building/combine_filter_tags_buildspec.txt

The ``--filter-tags`` option can be appended multiple times to filter tests by
multiple tags. If buildtest detects no tests were found when filtering tests by
tag name then buildtest will report a message. In example below we see no buildspecs
were found with tag name ``compile`` in the test.


.. program-output:: cat docgen/getting_started/building/filter_tags_nobuildspecs.txt

You can combine ``--tags`` with ``--buildspec`` to discover buildspecs in a single command.
buildtest will query tags and buildspecs independently and combine all discovered
buildspecs together.

.. program-output:: cat docgen/getting_started/building/combine_tags_buildspec.txt

As you may see, there are several ways to build buildspecs with buildtest. Tags is
great way to build a whole collection of tests if you don't know path to all the files. You can
specify multiple tags per buildspecs to classify how test can be run.

.. _build_by_executor:

Building by Executors
---------------------

Every buildspec is associated to an executor which is responsible for running the test.
You can instruct buildtest to run all tests by given executor via ``--executor`` option.
For instance, if you want to build all test associated to executor ``generic.local.python`` you can run::

  $ buildtest build --executor generic.local.python

buildtest will query buildspec cache for the executor name and retrieve a list of
buildspecs with matching executor name. To see a list of available executors in
buildspec cache see :ref:`querying buildspec executor <buildspec_executor>`.

.. Note:: By default all tests are run in buildspec file.  The ``buildtest build --executor`` option discovers
   buildspecs if one of the test matches the executor name. The ``--executor`` option
   is **not filtering on test level**  like ``--filter-tags`` option.

In this example we run all tests that are associated to ``generic.local.python`` executor. Notice how
buildtest filters tests by executor named **generic.local.sh**.

.. program-output:: cat docgen/getting_started/building/single_executor.txt

We can append arguments to ``--executor`` to search for multiple executors by
specifying ``--executor <name1> --executor <name2>``. In next example we search
all tests associated with ``generic.local.python`` and ``generic.local.csh`` executor.

.. Note:: If you specify multiple executors, buildtest will combine the executors
   into list, for example ``buildtest build --executor generic.local.python --executor generic.local.csh`` is converted
   into a list - ``[generic.local.python, generic.local.csh]``, and buildtest will
   discover buildspecs based on ``executor`` field in testname.

.. program-output:: cat docgen/getting_started/building/multi_executor.txt

.. _discover_buildspecs:

Discover Buildspecs
--------------------

Now, let's discuss how buildtest discovers buildspecs since there are several ways to build
buildspecs.

The buildspec search resolution is described as follows:

- If file or directory specified by ``-b`` option doesn't exist we exit immediately.

- If buildspec path is a directory, traverse directory recursively to find all ``.yml`` extensions

- If buildspec path is a file, check if file extension is not ``.yml``,  exit immediately

- If user specifies ``--tags`` or ``--executor`` we search in buildspec cache to discover buildspecs.

Shown below is a diagram on how buildtest discovers buildspecs. The user can build buildspecs
by ``--buildspec``, :ref:`--tags <build_by_tags>`, or :ref:`--executor <build_by_executor>`
which will discover the buildspecs. You can :ref:`exclude buildspecs <exclude_buildspecs>`
using ``--exclude`` option which is processed after discovering buildspecs. The
excluded buildspecs are removed from list if found and final list of buildspecs
is processed.

.. image:: ../_static/DiscoverBuildspecs.jpg
   :scale: 75 %


Control builds by Stages
-------------------------

We can control behavior of ``buildtest build`` command to stop at certain phase
using ``--stage`` option. The **--stage** option accepts ``parse`` or ``build``, which
will instruct buildtest to stop at parse or build phase of the pipeline.

Buildtest will validate all the buildspecs in the parse stage, so you can
instruct buildtest to stop at parse stage via ``--stage=parse``. This can be useful
when debugging buildspecs that are invalid. In this example below, we instruct
buildtest to stop after parse stage.

.. program-output:: cat docgen/getting_started/building/stage_parse.txt

Likewise, if you want to troubleshoot your test script without running them you can
use ``--stage=build`` which will stop after build phase. This can
be used when you are writing buildspec to troubleshoot how test is generated.
In this next example, we inform buildtest to stop after build stage.

.. program-output:: cat docgen/getting_started/building/stage_build.txt

.. _invalid_buildspecs:

Invalid Buildspecs
--------------------

buildtest will skip any buildspecs that fail to validate, in that case
the test script will not be generated. Here is an example where we have an invalid
buildspec.

.. program-output:: cat docgen/getting_started/building/invalid_buildspec.txt

buildtest may skip tests from running if buildspec specifies an invalid
executor name since buildtest needs to know this in order to delegate test
to Executor class responsible for running the test. Here is an example
where test failed to run since we provided invalid executor.

.. program-output:: cat docgen/getting_started/building/invalid_executor.txt

Rebuild Tests
--------------

buildtest can rebuild tests using the ``--rebuild`` option which can be useful if
you want to test a particular test multiple times. The rebuild option works across
all discovered buildspecs and create a new test instance (unique id) and test directory
path. To demonstrate we will build ``tutorials/python-shell.yml`` three times using
``--rebuild=3``.

.. program-output:: cat docgen/getting_started/building/rebuild.txt

The rebuild works with all options including: ``--buildspec``, ``--exclude``, ``--tags``
and ``--executors``.

In the next example we rebuild tests by discovering all tags that contain **fail**.

.. program-output:: cat docgen/getting_started/building/rebuild_tags.txt

The rebuild option expects a range between **1-50**, the ``--rebuild=1`` is equivalent
to running without ``--rebuild`` option. We set a max limit for rebuild option to
avoid system degredation due to high workload.

If you try to exceed this bound you will get an error such as::

    $ buildtest build -b tutorials/pass_returncode.yml --rebuild 51
    usage: buildtest [options] [COMMANDS] build [-h] [-b BUILDSPEC] [-x EXCLUDE] [--tags TAGS] [-e EXECUTOR]
                                                [-s {parse,build}] [-t TESTDIR] [--rebuild REBUILD] [--settings SETTINGS]
    buildtest [options] [COMMANDS] build: error: argument --rebuild: 51 must be a positive number between [1-50]


Use Alternate Configuration file
---------------------------------

If you want to use an alternate configuration file when building test you can use ``buildtest -c <config> build``.
buildtest will prefer configuration file on command line over the user configuration (``$HOME/.buildtest/config.yml``). For more
details see :ref:`which_configuration_file_buildtest_reads`.

Keeping Stage Directory
------------------------

buildtest will create setup the test environment in the `stage` directory where test will be executed. Once
test is complete, buildtest will remove the `stage` directory. If you
want to preserve the stage directory you can use ``buildtest build --keep-stage-dir``, this
is only useful if you want to run the test manually