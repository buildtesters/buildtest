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

Interacting with Buildspecs
----------------------------

buildtest supports several ways to interact with buildspecs, such as querying buildspec cache,
validating buildspecs, showing content of buildspecs, and editing buildspecs in editor.
The ``buildtest buildspec`` command contains several subcommands that we will discuss in this
session. To learn more we encourage you see :ref:`buildspec_interface` for detailed guide.

The ``buildtest help`` command can be used to provide a brief help message for each subcommand. Let's run
the following command since there are lots of commands that can be used to query buildspec.

.. dropdown:: ``buildtest help buildspec``

    .. command-output:: buildtest help buildspec

To build the buildspec cache you will need to run the following::

    buildtest buildspec find --rebuild -q

The ``--rebuild`` option will rebuild the cache and ``-q`` will supress output. If you want to see all
valid buildspecs in cache you can run::

    buildtest buildspec find

To retrieve all tags you can run::

    buildtest buildspec find --tags

We can filter tests via ``--filter`` option which expects a **key=value** pair. Let's filter by tagname ``python`` by running::

    buildtest buildspec find --filter tags=python

We can format the columns using ``--format`` option where each field is comma separated. Let's format by fields
``name``, ``tags``, ``description`` ::

    buildtest buildspec find --filter tags=python --format name,tags,description

To see all filter and format fields you can use ``--helpfilter`` and ``--helpformat`` to list all fields and their description.

If you want to see a summary of the buildspec cache you can run::

    buildtest buildspec summary

buildtest has an alias ``buildtest bc`` for **buildtest buildspec** command so let's use this going forward.


To validate a buildspec you can use **buildtest bc validate** command there are several options analogous to ``buildtest build``
for discovering buildspecs such as ``-b``, ``-x``, ``-t``, ``-e``. For instance let's validate the following buildspecs::

    buildtest bc validate -b tutorials/hello_world.yml -b general_tests/configuration
    buildtest bc validate -t python

Let's try validating an invalid buildspec so you can see what happens

.. dropdown:: ``buildtest bc validate -b tutorials/invalid_executor.yml``

    .. command-output:: buildtest bc validate -b tutorials/invalid_executor.yml
       :returncode: 1

To see content of buildspec you can use ``buildtest bc show`` which expects name of test. Note tab completion
is supported.

Let's run the following::

    buildtest bc show sleep hello_world

buildtest uses `rich <https://rich.readthedocs.io/>`_ python library for coloring which is used extensively throughout the buildtest output.
Rich supports several built-in themes that can be used for your preference. The ``buildtest bc show -t <THEME>`` can be used
select a color theme.

Currently, buildtest supports the following themes, feel free to tab complete::

       buildtest bc show -t
    abap                borland             emacs               gruvbox-dark        lovelace            native              paraiso-light       sas                 stata-dark          vs
    algol               bw                  friendly            gruvbox-light       manni               nord                pastie              solarized-dark      stata-light         xcode
    algol_nu            colorful            friendly_grayscale  igor                material            nord-darker         perldoc             solarized-light     tango               zenburn
    arduino             default             fruity              inkpot              monokai             one-dark            rainbow_dash        staroffice          trac
    autumn              dracula             github-dark         lilypond            murphy              paraiso-dark        rrt                 stata               vim

Let's try running the same example with ``emacs`` theme::

    buildtest bc show -t emacs sleep

If you want to see list of invalid buildspecs you can run::

    buildtest bc find invalid

Note, if you fix your invalid buildspec, buildtest will have no way of knowing if buildspec is valid until you
rebuild the buildspec cache ``buildtest bc find --rebuild``.

Buildtest Configuration
------------------------

In order to use buildtest, you need to :ref:`configure buildtest <configuring_buildtest>`. We will not discuss
buildtest configuration in this tutorial, but show how you can interact with configuration file via command line.

Buildtest provides a default configuration file that is sufficient to get started. To view path to configuration file you can run::

    buildtest config path

We have an alias ``buildtest cg`` for **buildtest config** command. If you want to view content of configuration file you can run

.. dropdown:: ``buildtest cg view``

    .. command-output:: buildtest cg view

We also support color themes (``buildtest cg view --theme <theme>``) and paging ``buildtest cg view --pager``.

buildtest configuration file defines one or more :ref:`executors <configuring_executors>` that are used when
writing test. Every test must be run by an executor. To retrieve all executors in a flat-listing you can run::

    buildtest cg executors

buildtest can show executor details in JSON and YAML format, you can fetch the details by running::

    buildtest cg executors --json
    buildtest cg executors --yaml
