
.. _test_reports:

Query Test Report
==================

buildtest keeps track of all tests and results in a JSON file.  This file is read by **buildtest report**
command to extract certain fields from JSON file and display
them in table format. We use python `tabulate <https://pypi.org/project/tabulate/>`_ library for
pretty print data in tables. Shown below is command usage to query test reports.

.. command-output:: buildtest report --help

You may run ``buildtest report`` without any option, and buildtest will display **all** test results
with default format fields. To see a list of all format fields, click :ref:`here <report_format_fields>`.

.. command-output:: buildtest report
   :ellipsis: 20

Format Reports (``buildtest report --format``)
-----------------------------------------------

.. _report_format_fields:

Available Format Fields (``buildtest report --helpformat``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The **buildtest report** command displays a default format fields that can be changed using the
``--format`` option. The report file (JSON) contains many more fields and we expose some of the fields
with the **--format** option. To see a list of available format fields you can run ``buildtest report --helpformat``.
This option will list all format fields with their description.

.. command-output:: buildtest report --helpformat

Format Field Usage
~~~~~~~~~~~~~~~~~~

The ``--format`` field are specified in comma separated format (i.e ``--format <field1>,<field2>``).
In this example we format table by fields ``--format id,executor,state,returncode``.

.. command-output:: buildtest report --format name,id,executor,state,returncode
   :ellipsis: 21

Filter Reports (``buildtest report --filter``)
-----------------------------------------------

The **buildtest report** command will display all tests results, which can be quite long depending on number of tests
so therefore we need a mechanism to filter the test results. The ``--filter`` option can be used
to filter out tests in the output based on filter fields. First, lets see the available filter fields
by run ``buildtest report --helpfilter`` which shows a list of filter fields and their description.

.. command-output:: buildtest report --helpfilter

The ``--filter`` option expects arguments in **key=value** format. You can
specify multiple filter delimited by comma. buildtest will treat multiple
filters as logical **AND** operation. The filter option can be used with
``--format`` field. Let's see some examples to illustrate the point.

Filter by returncode (``--filter returncode``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to retrieve all tests with a given returncode, we can use the **returncode**
property. For instance, let's retrieve all tests with returncode of 2 by setting ``--filter returncode=2``.

.. command-output:: buildtest report --filter returncode=2 --format=name,id,returncode

.. Note:: buildtest automatically converts returncode to integer when matching returncode, so ``--filter returncode="2"`` will work too

Filter by test name (``--filter name``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to filter by test name, use the **name** attribute in filter option. Let's assume
we want to filter all tests by name ``exit1_pass``, this can be achieved by setting filter
field as follows: ``--filter name=exit1_pass``. Shown below is an example using **name** filter field
to filter test results.

.. command-output:: buildtest report --filter name=exit1_pass --format=name,id,returncode,state

Filter by buildspec (``--filter buildspec``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Likewise, we can filter results by buildspec file using **buildspec** attribute via
``--filter buildspec=<file>``. The **buildspec** attribute must resolve to a file path which can be
relative or absolute path. buildtest will resolve path (absolute path) and find the appropriate
tests that belong to the buildspec file. If file doesn't exist or is not found in cache it will raise an error.

.. command-output:: buildtest report --filter buildspec=tutorials/python-hello.yml --format=name,id,state,buildspec


Filter by test state (``--filter state``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to filter results by test state, use the **state** property. This can be
useful if you want to know all pass or failed tests. The state property expects
value of ``[PASS|FAIL]`` since these are the two recorded test states marked by buildtest.
We can also pass multiple filter fields for instance if we want to find all **FAIL**
tests for executor **generic.local.sh** we can do the following.

.. command-output:: buildtest report --filter state=FAIL,executor=generic.local.sh --format=name,id,state,executor

Filter Exception Cases
~~~~~~~~~~~~~~~~~~~~~~~~

The ``returncode`` filter field expects an integer value, so if you try a non-integer
returncode you will get the following message

.. command-output:: buildtest report --filter returncode=1.5
    :returncode: 1

The ``state`` filter field expects value of ``PASS`` or ``FAIL`` so if you specify an
invalid state you will get an error as follows.

.. command-output:: buildtest report --filter state=UNKNOWN
    :returncode: 0

The ``buildspec`` field expects a valid file path, it can be an absolute or relative
path, buildtest will resolve absolute path and check if file exist and is in the report
file. If it's an invalid file we get an error such as

.. command-output:: buildtest report --filter buildspec=/path/to/invalid.yml
    :returncode: 0

You may have a valid filepath for buildspec filter field such as
``$BUILDTEST_ROOT/tutorials/invalid_executor.yml``, but there is no record of a test in the report cache
because this test wasn't run. In this case you will get the following message.

.. command-output:: buildtest report --filter buildspec=$BUILDTEST_ROOT/tutorials/invalid_executor.yml
    :returncode: 0

Find Latest or Oldest test
--------------------------

We can search for oldest or latest test for any given test. This can be useful if you
want to see first or last test run. If you want to retrieve the oldest
test you can use ``--oldest`` option. buildtest will append tests, therefore last
record in dictionary will be latest record, similarly first record is the oldest record.

Let's take a look at this example, we filter by test name ``hello_f`` which retrieves
three entries. Now let's filter by oldest record by specifying **--oldest** option
and it will retrieve the first record which is test id **349f3ada**.

.. code-block:: console

   $ buildtest report --filter name=hello_f --format name,id,starttime
    Reading Report File: /Users/siddiq90/.buildtest/report.json

    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 349f3ada | 2021/02/11 18:13:08 |
    +---------+----------+---------------------+
    | hello_f | ecd4a3f2 | 2021/02/11 18:13:18 |
    +---------+----------+---------------------+
    | hello_f | 5c87978b | 2021/02/11 18:13:33 |
    +---------+----------+---------------------+

    $ buildtest report --filter name=hello_f --format name,id,starttime --oldest
    Reading Report File: /Users/siddiq90/.buildtest/report.json

    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 349f3ada | 2021/02/11 18:13:08 |
    +---------+----------+---------------------+


If you want to retrieve the latest test result you can use ``--latest`` option which
will retrieve the last record, in the same example we will retrieve test id `5c87978b`.


.. code-block:: console

    $ buildtest report --filter name=hello_f --format name,id,starttime --latest
    Reading Report File: /Users/siddiq90/.buildtest/report.json

    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 5c87978b | 2021/02/11 18:13:33 |
    +---------+----------+---------------------+

You may combine **--oldest** and **--latest** options in same command, in this case
buildtest will retrieve the first and last record of every test.

.. code-block:: console

    $ buildtest report --format name,id,starttime --oldest --latest | more
    Reading Report File: /Users/siddiq90/.buildtest/report.json

    +------------------------------+----------+---------------------+
    | name                         | id       | starttime           |
    +==============================+==========+=====================+
    | variables_bash               | 750f48bc | 2021/02/11 18:13:03 |
    +------------------------------+----------+---------------------+
    | variables_bash               | 1bdfd403 | 2021/02/11 18:13:32 |
    +------------------------------+----------+---------------------+
    | ulimit_filelock_unlimited    | b7b852e4 | 2021/02/11 18:13:03 |
    +------------------------------+----------+---------------------+
    | ulimit_filelock_unlimited    | 56345a43 | 2021/02/11 18:13:18 |
    +------------------------------+----------+---------------------+

Terse Output
-------------

If you would like to parse the result of ``buildtest report``, you can use the ``--terse`` or ``-t`` option which
will print the report in machine readable format that shows the name of each column followed by each entry. Each entry
is delimited by PIPE symbol (``|``). The ``--terse`` option works with ``--format`` and ``--filter`` option. In this
next example, we report all FAIL tests in terse output. The first line is the header of tables followed by
output, if you want to disable output of header you can use ``--no-header`` option.

.. command-output:: buildtest report --filter state=FAIL --format=name,id,state -t

Report Summary (``buildtest report summary``)
----------------------------------------------

The ``buildtest report summary`` command can be used to provide a summary of the test report
with breakdown statistics of tests including all fail tests, number of tests by name, test runs
and buildspecs in report file.

Shown below is an example output from the report summary.

.. command-output:: buildtest report summary

.. _inspect_test:

Inspect Tests Records via ``buildtest inspect``
-------------------------------------------------

In previous examples we saw how we can retrieve test records using  ``buildtest report`` which
is printed in table format. We have limited the output to a limited fields however, if you want to analyze a particular,
we have a separate command called ``buildtest inspect`` that can be used for inspecting a test record
based on name or id. Shown below is the command usage for `buildtest inspect` command.

.. command-output:: buildtest inspect --help

You can report all test names and corresponding ids using ``buildtest inspect list`` which
will be used for querying tests by name or id.

.. command-output:: buildtest inspect list
   :ellipsis: 20

.. _inspect_by_name:

Inspecting Test by Name via ``buildtest inspect name``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildtest inspect name`` expects a list of positional argument that correspond to name
of test you want to query and buildtest will fetch the **last** record for each named test. Let's see an example to
illustrate the point. We can see that each test is stored as a JSON format and buildtest keeps track of
metadata for each test such as `user`, `hostname`, `command`, path to output and error file, content of test,
state of test, returncode, etc... In this example, we will retrieve record for test name **circle_area** which
will print the raw content of the test in JSON format.

.. command-output:: buildtest inspect name circle_area

You can query multiple tests as positional arguments in the format: ``buildtest inspect name <test1> <test2>``
In this next example, we will retrieve test records for ``bash_shell`` and  ``python_hello``.

.. command-output:: buildtest inspect name bash_shell python_hello

If you want to query all test records for a given name you can use the ``--all`` option which is applied to all positional
arguments.

Inspect Test by buildspec via ``buildtest inspect buildspec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can fetch records based on buildspec via ``buildtest inspect buildspec`` which expects
a list of buildspecs. By default, buildtest will fetch the latest record of each test, but if you
want to fetch all records you can pass the ``--all`` option.

In example below we will fetch latest record for all tests in **tutorials/vars.yml**

.. command-output:: buildtest inspect buildspec tutorials/vars.yml

buildtest will report an error if an input buildspec is invalid filepath such as one below

.. command-output:: buildtest inspect buildspec /tmp/buildspec.yml
   :returncode: 1

You can also pass multiple buildspes on the command line and fetch all records for a test. In example
below we will fetch all records from tests **tutorials/hello_world/yml** and **tutorials/regex_status.yml**

.. command-output:: buildtest inspect buildspec --all tutorials/vars.yml tutorials/status_regex.yml

If you pass a valid filepath but file is not in cache you will get an error as follows

.. command-output:: buildtest inspect buildspec $BUILDTEST_ROOT/README.rst
   :shell:
   :returncode: 1

.. _inspect_by_id:

Inspecting Test by ID via ``buildtest inspect id``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildtest inspect id`` works similar to ``buildtest inspect name`` except that it
operates on test id. This can be useful if you want to extract a particular test record and not
see all test records at once.

You only need to specify a few characters and buildtest will resolve full test id if there is a match.
The ``buildtest inspect id`` can operate on single or multiple ids if you want to specify multiple
ids in single command you can do ``buildtest inspect id <identifier1> <identifier2>``.

Let's see an example where we query a single test record. Notice, that we only specify
a few characters **fee** and buildtest found a matching record **fee66c67-db4e-4d35-8c6d-28ac5cbbaba0**

.. code-block:: console

    $ buildtest inspect id fee
    Reading Report File: /Users/siddiq90/.buildtest/report.json

    {
      "fee66c67-db4e-4d35-8c6d-28ac5cbbaba0": {
        "id": "fee66c67",
        "full_id": "fee66c67-db4e-4d35-8c6d-28ac5cbbaba0",
        "schemafile": "script-v1.0.schema.json",
        "executor": "generic.local.bash",
        "compiler": null,
        "hostname": "DOE-7086392.local",
        "user": "siddiq90",
        "testroot": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/python-hello/python_hello/2",
        "testpath": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/python-hello/python_hello/2/stage/generate.sh",
        "stagedir": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/python-hello/python_hello/2/stage",
        "rundir": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/python-hello/python_hello/2/run",
        "command": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/python-hello/python_hello/2/stage/generate.sh",
        "outfile": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/python-hello/python_hello/2/run/python_hello.out",
        "errfile": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/python-hello/python_hello/2/run/python_hello.err",
        "buildspec_content": "version: \"1.0\"\nbuildspecs:\n  python_hello:\n    type: script\n    description: Hello World python\n    executor: generic.local.bash\n    tags: python\n    run: python hello.py\n\n",
        "test_content": "#!/bin/bash \nsource /Users/siddiq90/Documents/github/buildtest/var/executors/generic.local.bash/before_script.sh\npython hello.py\nsource /Users/siddiq90/Documents/github/buildtest/var/executors/generic.local.bash/after_script.sh",
        "tags": "python",
        "starttime": "2021/03/31 11:18:21",
        "endtime": "2021/03/31 11:18:21",
        "runtime": 0.104714,
        "state": "PASS",
        "returncode": 0,
        "output": "Hello World\n",
        "error": "",
        "job": null
      }
    }

We can pass multiple IDs to ``buildtest inspect id`` and buildtest will retrieve test
record if there is a match. You only need to specify a few characters to ensure we have a unique test
ID and buildtest will retrieve the record.


.. code-block:: console

   $ buildtest inspect id 944 a76
    Reading Report File: /Users/siddiq90/.buildtest/report.json

    {
      "a76799db-f11e-4050-8dcb-8b147092c536": {
        "id": "a76799db",
        "full_id": "a76799db-f11e-4050-8dcb-8b147092c536",
        "schemafile": "script-v1.0.schema.json",
        "executor": "generic.local.bash",
        "compiler": null,
        "hostname": "DOE-7086392.local",
        "user": "siddiq90",
        "testroot": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/disk_usage/root_disk_usage/0",
        "testpath": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/disk_usage/root_disk_usage/0/stage/generate.sh",
        "stagedir": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/disk_usage/root_disk_usage/0/stage",
        "rundir": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/disk_usage/root_disk_usage/0/run",
        "command": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/disk_usage/root_disk_usage/0/stage/generate.sh",
        "outfile": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/disk_usage/root_disk_usage/0/run/root_disk_usage.out",
        "errfile": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/disk_usage/root_disk_usage/0/run/root_disk_usage.err",
        "buildspec_content": "version: \"1.0\"\nbuildspecs:\n  root_disk_usage:\n    executor: generic.local.bash\n    type: script\n    tags: [filesystem, storage]\n    description: Check root disk usage and report if it exceeds threshold\n    env:\n      threshold: 90\n    run: |\n      root_disk_usage=`df -a / | tail -n 1 |  awk '{print $5'} | sed 's/[^0-9]*//g'`\n      # if root exceeds threshold\n      if [ \"$root_disk_usage\" -gt \"$threshold\" ]; then\n        echo \"[WARNING] Root Disk Usage: $root_disk_usage% exceeded threshold of $threshold%\"\n        exit 1\n      fi\n      echo \"[OK] Root disk is below threshold of $threshold%\"\n",
        "test_content": "#!/bin/bash \nsource /Users/siddiq90/Documents/github/buildtest/var/executors/generic.local.bash/before_script.sh\nexport threshold=90\nroot_disk_usage=`df -a / | tail -n 1 |  awk '{print $5'} | sed 's/[^0-9]*//g'`\n# if root exceeds threshold\nif [ \"$root_disk_usage\" -gt \"$threshold\" ]; then\n  echo \"[WARNING] Root Disk Usage: $root_disk_usage% exceeded threshold of $threshold%\"\n  exit 1\nfi\necho \"[OK] Root disk is below threshold of $threshold%\"\n\nsource /Users/siddiq90/Documents/github/buildtest/var/executors/generic.local.bash/after_script.sh",
        "tags": "filesystem storage",
        "starttime": "2021/03/31 11:17:50",
        "endtime": "2021/03/31 11:17:50",
        "runtime": 0.114321,
        "state": "PASS",
        "returncode": 0,
        "output": "[OK] Root disk is below threshold of 90%\n",
        "error": "",
        "job": null
      },
      "944f6399-b82b-47f9-bb15-8f529dedd4e6": {
        "id": "944f6399",
        "full_id": "944f6399-b82b-47f9-bb15-8f529dedd4e6",
        "schemafile": "script-v1.0.schema.json",
        "executor": "generic.local.python",
        "compiler": null,
        "hostname": "DOE-7086392.local",
        "user": "siddiq90",
        "testroot": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0",
        "testpath": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0/stage/generate.sh",
        "stagedir": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0/stage",
        "rundir": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0/run",
        "command": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0/stage/generate.sh",
        "outfile": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0/run/circle_area.out",
        "errfile": "/Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0/run/circle_area.err",
        "buildspec_content": "version: \"1.0\"\nbuildspecs:\n  circle_area:\n    executor: generic.local.python\n    type: script\n    shell: python\n    description: \"Calculate circle of area given a radius\"\n    tags: [tutorials, python]\n    run: |\n      import math\n      radius = 2\n      area = math.pi * radius * radius\n      print(\"Circle Radius \", radius)\n      print(\"Area of circle \", area)\n",
        "test_content": "#!/bin/bash\nsource /Users/siddiq90/Documents/github/buildtest/var/executors/generic.local.python/before_script.sh\npython /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.python/python-shell/circle_area/0/stage/circle_area.py\nsource /Users/siddiq90/Documents/github/buildtest/var/executors/generic.local.python/after_script.sh",
        "tags": "tutorials python",
        "starttime": "2021/03/31 11:18:00",
        "endtime": "2021/03/31 11:18:00",
        "runtime": 0.144171,
        "state": "PASS",
        "returncode": 0,
        "output": "Circle Radius  2\nArea of circle  12.566370614359172\n",
        "error": "",
        "job": null
      }
    }

If you specify an invalid test id using ``buildtest inspect id`` you will get an error
message as follows.

.. code-block:: console

    $ buildtest inspect id lad

    Unable to find any test records based on id: ['lad'], please run 'buildtest inspect list' to see list of ids.

You will see similar message if you specify an invalid test name using ``buildtest inspect name`` command.

.. _inspect_query:

Query Test Records via ``buildtest inspect query``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildtest inspect query`` command can allow you to retrieve query certain fields from
each test records that can be useful when you are inspecting a test. Currently, we can
fetch content of output file, error file, testpath, and build script. Shown below are the list
of available options for ``buildtest inspect query``.

.. command-output:: buildtest inspect query --help

The ``buildtest inspect query`` command expects positional arguments that are name of tests
which you can get by running ``buildtest inspect list``.

For instance, let's query the test ``circle_area`` by running the following:

.. command-output:: buildtest inspect query circle_area

buildtest will display metadata for each test. By default, buildtest will report the latest record
for each test that is specified as a positional argument. If you want to see all runs for a particular test
you can use ``-d all`` or ``--display all`` which will report all records. By default, it will use ``-d last`` which
reports the last record. You can retrieve the first record by running ``-d first`` which is the oldest record.


Now as you run test, you want to inspect the output file, this can be done by passing ``-o`` or ``--output``. Let's take
what we learned and see the following. In this command, we retrieve all records for ``circle_area`` and
print content of output file

.. command-output:: buildtest inspect query -d all -o circle_area

If you want to see content of error file use the ``-e`` or ``--error`` flag. It would be useful to inspect
content of build script and generated test, which can be retrieved using ``--testpath`` and ``--buildscript``. Let's
see query the first record of ``circle_area`` and report all of the content fields

.. command-output:: buildtest inspect query -d first -o -e -t -b circle_area

We can query multiple tests using ``buildtest inspect query`` since each test is a positional argument. Any
options specified to `buildtest inspect query` will be applied to all test. For instance, let's fetch the output the
of test names ``root_disk_usage`` and ``python_hello``

.. command-output:: buildtest inspect query -o  root_disk_usage python_hello

Using Alternate Report File
-----------------------------

The ``buildtest report`` and ``buildtest inspect`` command will read from the report file tracked by buildtest which is
stored in **$BUILDTEST_ROOT/var/report.json**. This single file can became an issue if you are running jobs through CI where you
can potentially overwrite same file or if you want separate report files for each set of builds. Luckily we have an option to handle
this using the ``buildtest build -r /path/to/report`` option which can be used to specify an alternate location to report file.

buildtest will write the report file in the desired location, then you can specify the path to report file via
``buildtest report -r /path/to/report`` and ``buildtest inspect -r /path/to/report`` to load the report file when reporting tests.

The report file must be valid JSON file that buildtest understands in order to use `buildtest report` and
`buildtest inspect` command. Shown below are some examples using the alternate report file using ``buildtest report`` and
``buildtest inspect`` command.

.. code-block:: console

    $ buildtest report -r python.json --format name,id
    Reading report file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/docs/python.json

    +--------------+----------+
    | name         | id       |
    +==============+==========+
    | circle_area  | 6be6c404 |
    +--------------+----------+
    | python_hello | f21ba744 |
    +--------------+----------+


.. code-block:: console

    $ buildtest inspect -r test.json name variables_bash
    Reading Report File: /Users/siddiq90/Documents/GitHubDesktop/buildtest/test.json

    {
      "variables_bash": [
        {
          "id": "cd0511ce",
          "full_id": "cd0511ce-377e-4ed2-95f4-f244e5518732",
          "schemafile": "script-v1.0.schema.json",
          "executor": "generic.local.bash",
          "compiler": null,
          "hostname": "DOE-7086392.local",
          "user": "siddiq90",
          "testroot": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/1",
          "testpath": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/1/stage/generate.sh",
          "stagedir": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/1/stage",
          "rundir": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/1/run",
          "command": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/1/stage/generate.sh",
          "outfile": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/1/run/variables_bash.out",
          "errfile": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/1/run/variables_bash.err",
          "buildspec_content": "version: \"1.0\"\nbuildspecs:\n  variables_bash:\n    type: script\n    executor: generic.local.bash\n    description: Declare shell variables in bash\n    tags: [tutorials]\n    vars:\n      X: 1\n      Y: 2\n      literalstring: |\n        \"this is a literal string ':' \"\n      singlequote: \"'singlequote'\"\n      doublequote: \"\\\"doublequote\\\"\"\n      current_user: \"$(whoami)\"\n      files_homedir: \"`find $HOME -type f -maxdepth 1`\"\n\n    run: |\n      echo \"$X+$Y=\" $(($X+$Y))\n      echo $literalstring\n      echo $singlequote\n      echo $doublequote\n\n      echo $current_user\n      echo $files_homedir",
          "test_content": "#!/bin/bash \nsource /Users/siddiq90/.buildtest/executor/generic.local.bash/before_script.sh\nX=1\nY=2\nliteralstring=\"this is a literal string ':' \"\n\nsinglequote='singlequote'\ndoublequote=\"doublequote\"\ncurrent_user=$(whoami)\nfiles_homedir=`find $HOME -type f -maxdepth 1`\necho \"$X+$Y=\" $(($X+$Y))\necho $literalstring\necho $singlequote\necho $doublequote\n\necho $current_user\necho $files_homedir\nsource /Users/siddiq90/.buildtest/executor/generic.local.bash/after_script.sh",
          "tags": "tutorials",
          "starttime": "2021/04/16 14:29:25",
          "endtime": "2021/04/16 14:29:25",
          "runtime": 0.213196,
          "state": "PASS",
          "returncode": 0,
          "output": "1+2= 3\nthis is a literal string ':'\nsinglequote\ndoublequote\nsiddiq90\n/Users/siddiq90/buildtest_e7yxgttm.log /Users/siddiq90/.anyconnect /Users/siddiq90/buildtest_utwigb8w.log /Users/siddiq90/.DS_Store /Users/siddiq90/.serverauth.555 /Users/siddiq90/.CFUserTextEncoding /Users/siddiq90/.wget-hsts /Users/siddiq90/.bashrc /Users/siddiq90/.zshrc /Users/siddiq90/.coverage /Users/siddiq90/.serverauth.87055 /Users/siddiq90/buildtest_r7bck5zh.log /Users/siddiq90/.zsh_history /Users/siddiq90/.lesshst /Users/siddiq90/calltracker.py /Users/siddiq90/.git-completion.bash /Users/siddiq90/buildtest_wvjaaztp.log /Users/siddiq90/buildtest.log /Users/siddiq90/darhan.log /Users/siddiq90/ascent.yml /Users/siddiq90/.cshrc /Users/siddiq90/buildtest_nyq22whj.log /Users/siddiq90/github-tokens /Users/siddiq90/buildtest_ozb8b52z.log /Users/siddiq90/.zcompdump /Users/siddiq90/buildtest_nab_ckph.log /Users/siddiq90/.serverauth.543 /Users/siddiq90/.s.PGSQL.15007.lock /Users/siddiq90/.bash_profile /Users/siddiq90/.Xauthority /Users/siddiq90/.python_history /Users/siddiq90/.gitconfig /Users/siddiq90/output.txt /Users/siddiq90/.bash_history /Users/siddiq90/.viminfo\n",
          "error": "",
          "job": null
        },
        {
          "id": "e0901505",
          "full_id": "e0901505-a66b-4c91-9b29-d027cb6fabb6",
          "schemafile": "script-v1.0.schema.json",
          "executor": "generic.local.bash",
          "compiler": null,
          "hostname": "DOE-7086392.local",
          "user": "siddiq90",
          "testroot": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/2",
          "testpath": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/2/stage/generate.sh",
          "stagedir": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/2/stage",
          "rundir": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/2/run",
          "command": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/2/stage/generate.sh",
          "outfile": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/2/run/variables_bash.out",
          "errfile": "/Users/siddiq90/.buildtest/var/tests/generic.local.bash/vars/variables_bash/2/run/variables_bash.err",
          "buildspec_content": "version: \"1.0\"\nbuildspecs:\n  variables_bash:\n    type: script\n    executor: generic.local.bash\n    description: Declare shell variables in bash\n    tags: [tutorials]\n    vars:\n      X: 1\n      Y: 2\n      literalstring: |\n        \"this is a literal string ':' \"\n      singlequote: \"'singlequote'\"\n      doublequote: \"\\\"doublequote\\\"\"\n      current_user: \"$(whoami)\"\n      files_homedir: \"`find $HOME -type f -maxdepth 1`\"\n\n    run: |\n      echo \"$X+$Y=\" $(($X+$Y))\n      echo $literalstring\n      echo $singlequote\n      echo $doublequote\n\n      echo $current_user\n      echo $files_homedir",
          "test_content": "#!/bin/bash \nsource /Users/siddiq90/.buildtest/executor/generic.local.bash/before_script.sh\nX=1\nY=2\nliteralstring=\"this is a literal string ':' \"\n\nsinglequote='singlequote'\ndoublequote=\"doublequote\"\ncurrent_user=$(whoami)\nfiles_homedir=`find $HOME -type f -maxdepth 1`\necho \"$X+$Y=\" $(($X+$Y))\necho $literalstring\necho $singlequote\necho $doublequote\n\necho $current_user\necho $files_homedir\nsource /Users/siddiq90/.buildtest/executor/generic.local.bash/after_script.sh",
          "tags": "tutorials",
          "starttime": "2021/04/16 14:29:58",
          "endtime": "2021/04/16 14:29:58",
          "runtime": 0.075224,
          "state": "PASS",
          "returncode": 0,
          "output": "1+2= 3\nthis is a literal string ':'\nsinglequote\ndoublequote\nsiddiq90\n/Users/siddiq90/buildtest_e7yxgttm.log /Users/siddiq90/.anyconnect /Users/siddiq90/buildtest_utwigb8w.log /Users/siddiq90/.DS_Store /Users/siddiq90/.serverauth.555 /Users/siddiq90/.CFUserTextEncoding /Users/siddiq90/.wget-hsts /Users/siddiq90/.bashrc /Users/siddiq90/.zshrc /Users/siddiq90/.coverage /Users/siddiq90/.serverauth.87055 /Users/siddiq90/buildtest_r7bck5zh.log /Users/siddiq90/.zsh_history /Users/siddiq90/.lesshst /Users/siddiq90/calltracker.py /Users/siddiq90/.git-completion.bash /Users/siddiq90/buildtest_wvjaaztp.log /Users/siddiq90/buildtest.log /Users/siddiq90/darhan.log /Users/siddiq90/ascent.yml /Users/siddiq90/.cshrc /Users/siddiq90/buildtest_nyq22whj.log /Users/siddiq90/github-tokens /Users/siddiq90/buildtest_ozb8b52z.log /Users/siddiq90/.zcompdump /Users/siddiq90/buildtest_nab_ckph.log /Users/siddiq90/.serverauth.543 /Users/siddiq90/.s.PGSQL.15007.lock /Users/siddiq90/.bash_profile /Users/siddiq90/.Xauthority /Users/siddiq90/.python_history /Users/siddiq90/.gitconfig /Users/siddiq90/output.txt /Users/siddiq90/.bash_history /Users/siddiq90/.viminfo\n",
          "error": "",
          "job": null
        }
      ]
    }

