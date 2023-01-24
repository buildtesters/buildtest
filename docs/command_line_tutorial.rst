Buildtest Command Line Tutorial
=================================

For this session, we assume you have :ref:`installed buildtest <installing_buildtest>` on your system.
You can check if ``buildtest`` command is available by running::

    $ buildtest --help

If you receive an error please go back and re-install buildtest.

If you are new to buildtest you can review the :ref:`quick start guide <quick_start>` to learn the basics
of buildtest.


Building Test
---------------

The ``buildtest build`` command is used for running a test on your system given a :ref:`buildspec <what_is_buildspec>`
file (YAML). The most common way to build a test is specifying a file path via ``buildtest build -b <path>``. To get started,
let's build our first test by running the following::

    buildtest build -b $BUILDTEST_ROOT/tutorials/hello_world.yml

If you ran this successfully, you should see the following output

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/hello_world.yml``

    .. command-output:: buildtest build -b $BUILDTEST_ROOT/tutorials/hello_world.yml
       :shell:

The ``-b`` option can be specified multiple times and it can be used with directory path. buildtest
will recursively search for all *.yml* extensions and attempt to build all tests.

Let's try running the following command, where we will build by file and directory.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/hello_world.yml -b $BUILDTEST_ROOT/general_tests/configuration``

    .. command-output:: buildtest build -b $BUILDTEST_ROOT/tutorials/hello_world.yml -b $BUILDTEST_ROOT/general_tests/configuration
       :shell:

The ``-x`` option can be used to exclude buildspecs which works similar to ``-b`` where it can be a file or directory path.
In the next example try running the following commands::

    buildtest build -b general_tests/configuration -x general_tests/configuration/ulimits.yml
    buildtest build -b general_tests/configuration -x general_tests/configuration

You will notice in the 2nd command when buildtest has no buildspecs to build it will terminate immediately.

Buildtest supports test timeout which can be used if you don't want to wait indefinitely for test to complete. You
can use ``--timeout`` option which will terminate test if it exceeds the timelimit. The timeout is in number of
seconds. Let's try running the following example and take note of how timeout affects the test status::

    buildtest build -b tutorials/sleep.yml
    buildtest build -b tutorials/sleep.yml --timeout=1
    buildtest build -b tutorials/sleep.yml --timeout=5

buildtest supports test discovery based on :ref:`tags <build_by_tags>`  via
``buildtest build --tags`` or short option ``-t``. Let's try running the following test, take note
of the output as buildtest will show discovered buildspecs based on tag names

.. dropdown:: ``buildtest build -t python``

    .. command-output:: buildtest build -t python
       :shell:

To learn more about how to run tests, please refer to :ref:`building_test` guide.

Querying Test Report
-----------------------

buildtest will keep track of all tests in a report file (JSON) that can be used to display content of all test runs
and query metadata specific to test. To fetch all test runs you can use ``buildtest report`` command which will displays
output in a table format.

You can fetch the path to report file by running::

    buildtest report path

buildtest can write test results to alternate report file if ``buildtest --report`` is used, you can list all report files by
running::

    buildtest report list

**buildtest rt** is an alias for **buildtest report** command for those that hate typing :-)

We can fetch all pass and failed tests via ``--fail`` and ``--pass``. Let's try running the following::

    buildtest rt --fail
    buildtest rt --pass

Now let's assume you want to know total failed tests in report file, you can use ``--row-count`` option which
displays total row count. Let's run the following and see total fail count::

    buildtest rt --fail --row-count

The ``buildtest rt summary`` can be useful if you want to summary of report file.

buildtest supports paging support with ``buildtest rt`` which can be useful when you
have lots of tests. To enable pagination you can run::

    buildtest rt --pager

Finally we can filter test records and format table columns via ``--filter`` and ``--format`` option. Let's try
running the following command

.. dropdown:: ``buildtest rt --filter tags=python --format name,id,tags``

    .. command-output:: buildtest rt --filter tags=python --format name,id,tags

The ``--format`` option are comma separated list of format fields while ``--filter`` option are **key=value** pair. To see
list of available format and filter fields you can run::

    buildtest rt --helpfilter
    buildtest rt --helpformat

Inspecting Test
-----------------

The ``buildtest inspect`` command can be used to query test details and display metadata for one or more test. First you will
want to see all available test and their corresponding unique identifiers. Let's run the following

.. dropdown:: ``buildtest it list``

    .. command-output:: buildtest it list

In buildtest, test are referred as **builders** which is in format **<name>/<ID>** where each test has a unique identifier
separated by backslash **/** character. To see all builders you can run::

    buildtest it list -b

Note, we will be using the builder notation when querying test via ``buildtest it name`` and ``buildtest it query``. The
command ``buildtest it name`` will display raw JSON record from the report file for a given test. The test names can be positional
arguments so you can query multiple tests simulataneously. Let's run the following::

    buildtest it name hello_world circle_area

The ``buildtest it query`` is used to query test records in human readable format. This command is useful once you
run test via ``buildtest build`` and you want to inspect test result. buildtest can display test content, output and
error file and support multiple test queries including regular expression!!

Let's try running the following

.. dropdown:: ``buildtest it query -o -e -t hello_world``

    .. command-output:: buildtest it query -o -e -t hello_world

You can retrieve paths to given test via ``buildtest path`` that can be useful if you want to navigate to directory or list
contents. By default ``buildtest path`` will retrieve root directory of test. You can retrieve output and error via
``buildtest path -o`` and ``buildtest path -e``. Let's try running::

    buildtest path hello_world
    buildtest path -o hello_world
    buildtest path -e hello_world

We encourage you review :ref:`test_reports` for a detailed guide on how to query test in buildtest.