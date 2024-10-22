
.. _test_reports:

Query Test Report
==================

buildtest keeps track of all tests and results in a JSON file.  This file is read by **buildtest report**
command to extract certain fields from JSON file and display
them in table format. Shown below is command usage to query test reports.

.. dropdown:: ``buildtest report --help``

    .. command-output:: buildtest report --help

You may run ``buildtest report`` without any option, and buildtest will display **all** test results
with default format fields. To see a list of all format fields, click :ref:`here <report_format_fields>`.

.. dropdown:: ``buildtest report``

    .. command-output:: buildtest report
       :ellipsis: 20

You can run ``buildtest report path`` command to get the full path to the report file being used. This is helpful when the report file
is not known in that case one can print the file by doing ``cat $(buildtest report path)``.

.. dropdown:: ``buildtest report path``

    .. command-output:: buildtest report path

The ``buildtest report`` command will fetch all records and display them in a table format, if you want to know how many records are displayed in the table you can use ``buildtest report --row-count`` which will display   
a raw count of records in the table. In the example below we will run ``buildtest report --row-count`` which will show number of tests in the report.

.. dropdown:: ``buildtest report --row-count``

    .. command-output:: buildtest report --row-count

You may find it useful to fetch all failed records and determine pass/fail criteria as part of your shell script, this can be done by running ``buildtest report --row-count --fail`` as shown below.

.. dropdown:: ``buildtest report --row-count --fail``

    .. command-output:: buildtest report --row-count --fail

.. note::
   ``buildtest rt`` is an alias for ``buildtest report`` command.

.. _report_format_fields:

Detailed Reports (``buildtest report --detailed``)
---------------------------------------------------

The **buildtest report --detailed** option can be used to show a detailed test report that may be of interest when
examining a test. This option is synonymous to running ``buildtest report --format name,id,user,state,returncode,
runtime,outfile,errfile,buildspec``.
Shown below is an example output.

.. dropdown:: ``buildtest report --detailed``

    .. command-output:: buildtest report --detailed

.. note::
        The ``--detailed`` and ``--format`` options are mutually exclusive options because both options
        will alter the format fields when displaying test results.

You will get the following error if you specify both options as shown below

.. dropdown:: ``buildtest report --detailed --format name``
   :color: warning

    .. command-output:: buildtest report --detailed --format name
       :returncode: 2

Format Reports (``buildtest report --format``)
-----------------------------------------------

The **buildtest report** command displays a default format fields that can be changed using the
``--format`` option. The report file (JSON) contains many more fields and we expose some of the fields
with the **--format** option. To see a list of available format fields you can run ``buildtest report --helpformat``.
This option will list all format fields with their description.

.. dropdown:: ``buildtest report --helpformat``

    .. command-output:: buildtest report --helpformat

To print just the raw format fields use the command ``buildtest report --formatfields``.

.. dropdown:: ``buildtest report --formatfields``

    .. command-output:: buildtest report --formatfields

Format Field Usage
~~~~~~~~~~~~~~~~~~

The ``--format`` field are specified in comma separated format (i.e ``--format <field1>,<field2>``).
In this example we format table by fields ``--format id,executor,state,returncode``.

.. dropdown:: ``buildtest rt --format name,id,executor,state,returncode``

    .. command-output:: buildtest rt --format name,id,executor,state,returncode
       :ellipsis: 21

Filter Reports (``buildtest report --filter``)
-----------------------------------------------

The **buildtest report** command will display all tests results, which can be quite long depending on number of tests
so therefore we need a mechanism to filter the test results. The ``--filter`` option can be used
to filter out tests in the output based on filter fields. First, lets see the available filter fields
by run ``buildtest report --helpfilter`` which shows a list of filter fields and their description.

.. dropdown:: ``buildtest report --helpfilter``

    .. command-output:: buildtest report --helpfilter

To print just the raw filter fields use the command ``buildtest report --filterfields``.

.. dropdown:: ``buildtest report --filterfields``

    .. command-output:: buildtest report --filterfields

The ``--filter`` option expects arguments in **key=value** format. You can
specify multiple filter delimited by comma. buildtest will treat multiple
filters as logical **AND** operation. The filter option can be used with
``--format`` field. Let's see some examples to illustrate the point.

Filter by returncode (``--filter returncode``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to retrieve all tests with a given returncode, we can use the **returncode**
property. For instance, let's retrieve all tests with returncode of 2 by setting ``--filter returncode=2``.

.. dropdown:: ``buildtest rt --filter returncode=2 --format=name,id,returncode``

    .. command-output:: buildtest rt --filter returncode=2 --format=name,id,returncode

.. Note:: buildtest automatically converts returncode to integer when matching returncode, so ``--filter returncode="2"`` will work too

Filter by test name (``--filter name``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to filter by test name, use the **name** attribute in filter option. Let's assume
we want to filter all tests by name ``exit1_pass``, this can be achieved by setting filter
field as follows: ``--filter name=exit1_pass``. Shown below is an example using **name** filter field
to filter test results.

.. dropdown:: ``buildtest rt --filter name=exit1_pass --format=name,id,returncode,state``

    .. command-output:: buildtest rt --filter name=exit1_pass --format=name,id,returncode,state

Filter by buildspec (``--filter buildspec``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Likewise, we can filter results by buildspec file using **buildspec** attribute via
``--filter buildspec=<file>``. The **buildspec** attribute must resolve to a file path which can be
relative or absolute path. buildtest will resolve path (absolute path) and find the appropriate
tests that belong to the buildspec file. If file doesn't exist or is not found in cache it will raise an error.

.. dropdown:: ``buildtest rt --filter buildspec=tutorials/python-hello.yml --format=name,id,state,buildspec``

    .. command-output:: buildtest rt --filter buildspec=tutorials/python-hello.yml --format=name,id,state,buildspec


Filter by test state (``--filter state``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to filter results by test state, use the **state** property. This can be
useful if you want to know all pass or failed tests. The state property expects
value of ``[PASS|FAIL]`` since these are the two recorded test states marked by buildtest.
We can also pass multiple filter fields for instance if we want to find all **FAIL**
tests for executor **generic.local.sh** we can do the following.

.. dropdown:: ``buildtest rt --filter state=FAIL,executor=generic.local.sh --format=name,id,state,executor``

    .. command-output:: buildtest rt --filter state=FAIL,executor=generic.local.sh --format=name,id,state,executor

Filter Exception Cases
~~~~~~~~~~~~~~~~~~~~~~~~

The ``returncode`` filter field expects an integer value, so if you try a non-integer
returncode you will get the following message

.. dropdown:: ``buildtest rt --filter returncode=1.5``
    :color: warning

    .. command-output:: buildtest rt --filter returncode=1.5
        :returncode: 1

The ``state`` filter field expects value of ``PASS`` or ``FAIL`` so if you specify an
invalid state you will get an error as follows.

.. dropdown:: ``buildtest rt --filter state=UNKNOWN``
    :color: warning

    .. command-output:: buildtest rt --filter state=UNKNOWN
        :returncode: 1

The ``buildspec`` field expects a valid file path, it can be an absolute or relative
path, buildtest will resolve absolute path and check if file exist and is in the report
file. If it's an invalid file we get an error such as

.. dropdown:: ``buildtest rt --filter buildspec=/path/to/invalid.yml``
    :color: warning

    .. command-output:: buildtest rt --filter buildspec=/path/to/invalid.yml
        :returncode: 1

You may have a valid filepath for buildspec filter field such as
``$BUILDTEST_ROOT/tutorials/invalid_executor.yml``, but there is no record of a test in the report cache
because this test wasn't run. In this case you will get the following message.

.. dropdown:: ``buildtest rt --filter buildspec=$BUILDTEST_ROOT/tutorials/invalid_executor.yml``
   :color: warning

    .. command-output:: buildtest rt --filter buildspec=$BUILDTEST_ROOT/tutorials/invalid_executor.yml
        :returncode: 1

Find Latest or Oldest test
--------------------------

We can search for oldest or latest test for any given test. This can be useful if you
want to see first or last test run for a particular test. If you want to retrieve the oldest
test you can use ``--oldest`` option, likewise you can retrieve the latest run via ``--latest`` option.

Let's take a look at this example, we filter by test name ``exit1_pass`` which retrieves all
test runs. In subsequent example we filter by latest and oldest run.

.. dropdown:: Show oldest run

    .. command-output:: buildtest report --filter name=exit1_pass --format name,id,starttime

    .. command-output:: buildtest report --filter name=exit1_pass --format name,id,starttime --oldest

.. dropdown:: Show latest run

    .. command-output:: buildtest report --filter name=exit1_pass --format name,id,starttime --latest

You may combine **--oldest** and **--latest** options in same command, in this case
buildtest will retrieve the first and last record of every test.

.. dropdown:: Show oldest and latest run

    .. command-output:: buildtest report --filter name=exit1_pass --format name,id,starttime --oldest --latest

.. _buildtest_report_fail:

Find all Failed Tests (``buildtest report --fail``)
--------------------------------------------------------

The ``buildtest report --fail`` command can be used to retrieve all failed tests which is equivalent to filtering tests
by **state=FAIL** since test state is determined by **state** property. This command can be useful to pin-point failures.

Let's take a look at next two example, the first command will query report and limit output to 6 rows which can retrieve both pass
and failed test. The second command will run same example with ``--fail`` and only retrieve failed tests.
Take note of the **state** property in table, in second example buildtest will filter test and report all **FAIL** tests.

.. dropdown:: Show fail tests

    .. command-output:: buildtest report --format name,id,state --count=6

    .. command-output:: buildtest report --format name,id,state --fail --count=6

Find all Passed Tests (``buildtest report --pass``)
--------------------------------------------------------

The ``buildtest report --pass``, works similar to ``buildtest report --fail`` where it will filter test by **state=PASS** which can be used to find all passed tests.

We can see in example below, that buildtest will retrieve only PASS tests which can be determined by the ``state`` property

.. dropdown:: Show pass tests

    .. command-output:: buildtest report --format name,id,state --pass --count=6

.. Note::
    The ``--pass`` and ``--fail`` are mutually exclusive option which will query all PASS or FAIL test from report file, if you try to
    specify both options on command line you will get an error

    .. command-output:: buildtest report --pass --fail
        :returncode: 2

Find Tests by Start and End Date (``buildtest report --start --end``)
------------------------------------------------------------------------

The ``buildtest report --start`` and ``buildtest report --end`` command can be used to retrieve test records based on start and end date.

Let's take a look at these two example, the first test queries report by filtering by **state** and **name**. The second command
will run same example with ``--start --end`` option. Take note of the **starttime** and **endtime** properties in table, in second example buildtest will
filter test and only report tests in the range of [start, end] dates.

.. dropdown:: Filter by start and end date

    .. code-block:: console

        $ buildtest report --filter state=FAIL,name=exit1_fail --format name,state,starttime,endtime
        Report File: /home/docs/checkouts/readthedocs.org/user_builds/buildtest/checkout
                                     s/1082/var/report.json
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ name                                                   ┃ state        ┃ starttime                                ┃ endtime                                 ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ exit1_fail                                             │ FAIL         │ 2022/06/09 17:51:50                      │ 2022/06/09 17:51:50                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/09 17:51:51                      │ 2022/06/09 17:51:51                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/09 17:51:53                      │ 2022/06/09 17:51:53                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/09 17:52:01                      │ 2022/06/09 17:52:01                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:51:50                      │ 2022/06/10 17:51:50                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:51:52                      │ 2022/06/10 17:51:52                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:51:52                      │ 2022/06/10 17:51:52                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:52:01                      │ 2022/06/10 17:52:01                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:57                      │ 2022/06/11 17:51:57                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:59                      │ 2022/06/11 17:51:59                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:57                      │ 2022/06/11 17:51:57                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:59                      │ 2022/06/11 17:51:59                     │
        └────────────────────────────────────────────────────────┴──────────────┴──────────────────────────────────────────┴─────────────────────────────────────────┘

    .. code-block:: console

        $ buildtest report --filter state=FAIL,name=exit1_fail --format name,state,starttime,endtime --start 2022-06-10 --end 2022-06-11
        Report File: /home/docs/checkouts/readthedocs.org/user_builds/buildtest/checkout
                                     s/1082/var/report.json
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ name                                                   ┃ state        ┃ starttime                                ┃ endtime                                 ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:51:50                      │ 2022/06/10 17:51:50                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:51:52                      │ 2022/06/10 17:51:52                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:51:52                      │ 2022/06/10 17:51:52                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/10 17:52:01                      │ 2022/06/10 17:52:01                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:57                      │ 2022/06/11 17:51:57                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:59                      │ 2022/06/11 17:51:59                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:57                      │ 2022/06/11 17:51:57                     │
        ├────────────────────────────────────────────────────────┼──────────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
        │ exit1_fail                                             │ FAIL         │ 2022/06/11 17:51:59                      │ 2022/06/11 17:51:59                     │
        └────────────────────────────────────────────────────────┴──────────────┴──────────────────────────────────────────┴─────────────────────────────────────────┘

Limit number of test records (``buildtest report --count``)
-------------------------------------------------------------

The ``buildtest report`` command will show all test results from the report file and the output can be quite long. 
If you want to limit the number of records that get printed then you can use ``buildtest report --count`` 
where ``--count`` is number of rows that that get printed. Shown below is the output of 2 records in table format

.. dropdown:: ``buildtest report --count 2``

    .. command-output:: buildtest report --count 2

The ``--count`` option also works with terse mode ``--terse``, shown below is the same output 

.. dropdown:: ``buildtest report --terse --count 2``

    .. command-output:: buildtest report --terse --count 2

If you set ``--count=0`` no records will be displayed; however, if you set any negative
value for ``--count`` then all records will be displayed.

.. dropdown:: Query tests with ``--count`` at 0 and negative value

    .. command-output:: buildtest report --count=0 --no-header --terse | wc -l
       :shell:

    .. command-output:: buildtest report --count=-5 --no-header --terse | wc -l
       :shell:

Terse Output (``buildtest report --terse``)
--------------------------------------------

If you would like to parse the result of ``buildtest report``, you can use the ``--terse`` or ``-t`` option which
will print the report in machine readable format that shows the name of each column followed by each entry. Each entry
is delimited by PIPE symbol (``|``). The ``--terse`` option works with ``--format`` and ``--filter`` option. In this
next example, we report all FAIL tests in terse output. The first line is the header of tables followed by
output, if you want to disable output of header you can use ``--no-header`` option.

.. dropdown:: ``buildtest report --filter state=FAIL --format=name,id,state --terse``

    .. command-output:: buildtest report --filter state=FAIL --format=name,id,state --terse

Report Summary (``buildtest report summary``)
----------------------------------------------

The ``buildtest report summary`` command can be used to provide a short summary of the test report.

Shown below is an example output from the report summary.

.. dropdown:: ``buildtest report summary``

    .. command-output:: buildtest report summary

The ``buildtest report summary --detailed`` command can be used to provide a summary of the test report
with breakdown statistics of tests including all fail tests, number of tests by name, test runs
and buildspecs in report file. To see a short report use 

Shown below is an example output from the report summary --detailed.

.. dropdown:: ``buildtest report summary --detailed``

    .. command-output:: buildtest report summary --detailed


.. _inspect_test:

Inspect Tests Records via ``buildtest inspect``
-------------------------------------------------

.. note::
   ``buildtest it`` is an alias for ``buildtest inspect`` command.

In previous examples we saw how we can retrieve test records using  ``buildtest report`` which
is printed in table format. We have limited the output to a limited fields however, if you want to analyze a particular,
we have a separate command called ``buildtest inspect`` that can be used for inspecting a test record
based on name or id. Shown below is the command usage for `buildtest inspect` command.

.. dropdown:: ``buildtest inspect --help``

    .. command-output:: buildtest inspect --help

You can report all test names and corresponding ids using ``buildtest inspect list`` which
will be used for querying tests by name or id.

.. dropdown:: ``buildtest inspect list``

    .. command-output:: buildtest inspect list
       :ellipsis: 20

You can fetch all builder names via ``buildtest inspect list --builder`` which is the format used for
querying test records via :ref:`buildtest inspect name <inspect_by_name>` or :ref:`buildtest inspect query <inspect_query>`.

.. dropdown:: ``buildtest inspect list --builder``

    .. command-output:: buildtest inspect list --builder
        :ellipsis: 5

If you are interested in parsing output of ``buildtest inspect list``, you can may find the ``--terse`` option useful. The output will show
headers followed by entries, the headers can be omitted by specifying ``--no-header`` option.

.. dropdown:: ``buildtest inspect list --terse``

    .. command-output:: buildtest inspect list --terse
       :ellipsis: 5

.. _inspect_by_name:

Inspecting Test by Name via ``buildtest inspect name``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildtest inspect name`` expects a list of positional argument that correspond to name
of test you want to query and buildtest will fetch the **last** record for each named test. Let's see an example to
illustrate the point. We can see that each test is stored as a JSON format and buildtest keeps track of
metadata for each test such as `user`, `hostname`, `command`, path to output and error file, content of test,
state of test, returncode, etc... In this example, we will retrieve record for test name **circle_area** which
will print the raw content of the test in JSON format.

.. dropdown:: ``buildtest inspect name circle_area``

    .. command-output:: buildtest inspect name circle_area

You can query multiple tests as positional arguments in the format: ``buildtest inspect name <test1> <test2>``
In this next example, we will retrieve test records for ``bash_shell`` and  ``python_hello``.

.. dropdown:: ``buildtest inspect name bash_shell python_hello``

    .. command-output:: buildtest inspect name bash_shell python_hello

If you want to query all test records for a given name you can use the ``--all`` option which is applied to all positional
arguments.

Inspect Test by buildspec via ``buildtest inspect buildspec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can fetch records based on buildspec via ``buildtest inspect buildspec`` which expects
a list of buildspecs. By default, buildtest will fetch the latest record of each test, but if you
want to fetch all records you can pass the ``--all`` option.

In example below we will fetch latest record for all tests in **tutorials/vars.yml**

.. dropdown:: ``buildtest it buildspec tutorials/vars.yml``

    .. command-output:: buildtest it buildspec tutorials/vars.yml

buildtest will report an error if an input buildspec is invalid filepath such as one below

.. command-output:: buildtest it buildspec /tmp/buildspec.yml
   :returncode: 1

You can also pass multiple buildspes on the command line and fetch all records for a test. In example
below we will fetch all records from buildspecs **tutorials/vars.yml** and **tutorials/hello_world.yml**

.. command-output:: buildtest it buildspec --all tutorials/vars.yml tutorials/hello_world.yml

.. note::

    If you pass a valid filepath but file is not in cache you will get an error as follows

    .. command-output:: buildtest it buildspec $BUILDTEST_ROOT/README.rst
       :shell:
       :returncode: 1

.. _inspect_query:

Query Test Records via ``buildtest inspect query``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildtest inspect query`` command can allow you to retrieve query certain fields from
each test records that can be useful when you are inspecting a test. Currently, we can
fetch content of output file, error file, testpath, and build script. Shown below are the list
of available options for ``buildtest inspect query``.

.. dropdown:: ``buildtest inspect --help``

    .. command-output:: buildtest inspect query --help

The ``buildtest inspect query`` command expects positional arguments that are name of tests
which you can get by running ``buildtest inspect list``.

For instance, let's query the test ``circle_area`` by running the following:

.. dropdown:: ``buildtest inspect query circle_area``

    .. command-output:: buildtest inspect query circle_area

buildtest will display metadata for each test. By default, buildtest will report the last run
for each test that is specified as a positional argument.

You can retrieve content of output file via ``--output`` or short option ``-o``. In this command, we retrieve the last run for ``circle_area`` and
print content of output file

.. dropdown:: ``buildtest inspect query -o circle_area``

    .. command-output:: buildtest inspect query -o circle_area

If you want to see content of error file use the ``-e`` or ``--error`` flag. It would be useful to inspect
content of build script and generated test, which can be retrieved using ``-t`` and ``--buildscript``. Let's
query test ``circle_area`` and report all of the content fields

.. dropdown:: ``buildtest inspect query -o -e -t -b circle_area``

    .. command-output:: buildtest inspect query -o -e -t -b circle_area

We can query multiple tests using ``buildtest inspect query`` since each test is a positional argument. Any
options specified to `buildtest inspect query` will be applied to all test. For instance, let's fetch the output the
of test names ``root_disk_usage`` and ``python_hello``

.. dropdown:: ``buildtest inspect query -o root_disk_usage python_hello``

    .. command-output:: buildtest inspect query -o root_disk_usage python_hello

If you want to query specific test ID, you can specify name of test followed by `/` and test ID. You don't need to specify
the full ID however tab completion is available to help fill in the names. For example if you want to query test record for
``circle_area/566399ce-e25b-4630-8bb8-fbf09f6de7d0`` shown in tab completion you can type a first few characters to query the record

.. code-block:: console

    $ buildtest inspect query circle_area/
    circle_area/566399ce-e25b-4630-8bb8-fbf09f6de7d0  circle_area/69b29a2c-55ee-47d0-ac8c-aaa23566619b  circle_area/a6df47b6-4db4-4e5b-b5c4-fadb510ee1d2  circle_area/ace1b02f-1761-443d-b3d8-b6f9ba20291d


    $ buildtest inspect query circle_area/56
    ──────────────────────────────────────────────────────────────────────────────────────── circle_area/566399ce-e25b-4630-8bb8-fbf09f6de7d0 ─────────────────────────────────────────────────────────────────────────────────────────
    Executor: generic.local.bash
    Description: Calculate circle of area given a radius
    State: PASS
    Returncode: 0
    Runtime: 0.318187 sec
    Starttime: 2024/10/22 12:39:00
    Endtime: 2024/10/22 12:39:00
    Command: bash circle_area_build.sh
    Test Script: /Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/python-shell/circle_area/566399ce/circle_area.sh
    Build Script: /Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/python-shell/circle_area/566399ce/circle_area_build.sh
    Output File: /Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/python-shell/circle_area/566399ce/circle_area.out
    Error File: /Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/python-shell/circle_area/566399ce/circle_area.err
    Log File: /Users/siddiq90/Documents/buildtest/var/logs/buildtest_t6dmyvv3.log
    ───────────────────────────────────────────────────────────────────────── Buildspec File: /Users/siddiq90/Documents/buildtest/tutorials/python-shell.yml  ─────────────────────────────────────────────────────────────────────────
    buildspecs:
      circle_area:
        executor: generic.local.bash
        type: script
        shell: python
        description: "Calculate circle of area given a radius"
        tags: [tutorials, python]
        run: |
          import math
          radius = 2
          area = math.pi * radius * radius
          print("Circle Radius ", radius)
          print("Area of circle ", area)

    ─────────────────────────────────────────────────────────────────────────────────────────────────

buildtest will search for test ID using `re.match <https://docs.python.org/3/library/re.html#re.match>`_ so it is possible to apply a regular expression to seek
out multiple test records. The tests must be enclosed in quotes ``"`` in-order to have a valid regular expression. Here are few examples that can be useful

.. code-block::

    # retrieve all test records for name `circle_area`
    buildtest inspect query circle_area/

    # retrieve test records starting with ID `8a` and `bc` for test name `exit1`
    buildtest inspect query "exit1/(8a|bc)"

Using Alternate Report File
-----------------------------

The ``buildtest report`` and ``buildtest inspect`` command will read from the report file tracked by buildtest which is
stored in **$BUILDTEST_ROOT/var/report.json**. This single file can became an issue if you are running jobs through CI where you
can potentially overwrite same file or if you want separate report files for each set of builds. Luckily we have an option to handle
this using the ``buildtest -r <report_path> build -b <buildspec_path>`` option which can be used to specify an alternate location to report file.

buildtest will write the report file in the desired location, then you can specify the path to report file via
``buildtest -r <report_path> report`` and ``buildtest -r <report_path> inspect`` to load the report file when reporting tests.

The report file must be valid JSON file that buildtest understands in order to use `buildtest report` and
`buildtest inspect` command. Shown below are some examples using the alternate report file using ``buildtest report`` and
``buildtest inspect`` command.

.. code-block:: console

    $ buildtest -r $BUILDTEST_ROOT/python.json report --format name,id
                          Report File: /Users/siddiq90/Documents/GitHubDesktop/buildtest/python.json
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ name                                                               ┃ id                                            ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ circle_area                                                        │ a2814554                                      │
    ├────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────┤
    │ python_hello                                                       │ dd447e43                                      │
    └────────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────┘

You can view path to all report files via ``buildtest report list`` which keeps track of any new report files created when using ``buildtest -r <report_file> build`` option.

.. command-output:: buildtest report list
