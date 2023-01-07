Quick Start Guide
==================

Building Test
--------------

The ``buildtest build`` command is used for running a test. There are several ways to run the test,
the most common way to run arbitrary test is to specify file path::

    buildtest build -b <file>

To specify multiple files you can append ``-b`` option::

    buildtest build -b <file1> -b <file2>

To run all tests within a directory, specify path to directory, let's assume we want
to run all tests in **examples** directory you can do the following::

    buildtest build -b examples

buildtest can exclude buildspecs via ``-x`` option which can operate on file or directory similar to ``-b``. This can be useful
if you want to run tests in a directory but exclude one file. For example you can do the following to exclude test ``examples/hello.yml``::

  buildtest build -b examples -x examples/hello.yml

Inspecting a test
--------------------

Upon execution of test you can inspect test results for a given test, where **name** is the name of test::

    buildtest inspect query <name>

To see content of output and error file for a given test, you can run::

    buildtest inspect query -o -e <name>

You can inspect multiple tests simultaneously since test names are positional arguments,
let's assume we have two test names **jobA** and **jobB**, we can do the following::

    buildtest inspect query jobA jobB

Every test has a unique identifier, if you want to select a specific test run you specify the test identifier such as following::

  buildtest inspect query always_fail/c0e886c6-8a1f-4063-846f-d16bc4733b04

Note buildtest has tab completion so test IDs will be auto-completed as you type.

You can use regular expression with ``buildtest inspect query`` command which can be useful to select multiple
tests. You must specify test names in quotes in order for buildtest to process regular expression::

  buildtest inspect query "always_fail/(c0|8e)"

To see a list of available tests you can run::

  buildtest inspect query list

You can retrieve path attributes for a given test via ``buildtest path`` command which expects a test name. To
retrieve path for a test you can run::

  buildtest path hello_world

Note you can only specify one test name. You can retrieve path to output or error file by running::

  buildtest path -o hello_world
  buildtest path -e hello_world

Querying Test Report
----------------------

buildtest will keep track of all tests in a report file, to see all tests you can run::

    buildtest report

To see all pass or failed tests you can run::

   buildtest report --pass
   buildtest report --fail

If you want to filter tests by returncode you can use ``--filter`` field which expects a key=value pair. You can see
all available filter fields via ``buildtest report --helpfilter``. To filter by returncode 1 you can do::

  buildtest report --filter returncode=1

Developing a test
------------------

When you are creating a test known as **buildspec** you will want to make sure buildspec is valid, this can
be done by running **buildtest buildspec validate**. The command works similar to ``buildtest build`` where one
can specify file or directory. To validate multiple buildspecs you can do the following::

  buildtest buildspec validate -b <file1> -b <file2>
  buildtest buildspec validate -b <dir1> -b <file1>

buildtest can load all buildspecs in the cache so you can query cache to find all buildspecs, query all tags,
search for test maintainers and much more. To see all available buildspecs in the cache you can run::

  buildtest buildspec find

If you want to see a summary you can run::

  buildtest buildspec summary

To see all invalid buildspecs in your cache you can run::

  buildtest buildspec find invalid

The ``buildtest buildspec edit-test`` and ``buildtest buildspec edit-file`` are builtin commands to open
buildspeec in editor similar to how one would open in your preferred editor. The one benefit of using these commands,
is buildtest will validate the test after closing file. The difference between the two commands is one operates on test
names while the later operates on file names. Shown below is an example::

    buildtest buildspec edit-test hello_world
    buildtest buildspec edit-file examples/foo.yml

You can view content of buildspec via ``buildtest buildspec show`` where argument is name of test. You can
specify multiple test name to see content of all tests such as shown below::

    buildtest buildspec show hello_world foo_bar

The ``buildtest buildspec show-fail`` command will show content of all buildspecs that failed tests during execution which
are all tests reported by ``buildtest report --fail``. Note this is not to be confused with all invalid buildspecs.