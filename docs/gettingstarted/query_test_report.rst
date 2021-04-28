
.. _test_reports:

Query Test Report
==================

buildtest keeps track of all tests and results in a JSON file that is stored in **$HOME/.buildtest/report.json**. This
file is read by **buildtest report** command to extract certain fields from JSON file and display
them in table format. We use python `tabulate <https://pypi.org/project/tabulate/>`_ library for
pretty print data in tables. Shown below is command usage to query test reports.

.. program-output:: cat docgen/buildtest_report_--help.txt

You may run ``buildtest report`` without any option, and buildtest will display **all** test results
with default format fields. To see a list of all format fields, click :ref:`here <report_format_fields>`.

.. program-output:: cat docgen/report.txt
   :ellipsis: 20

Format Reports
---------------

.. _report_format_fields:

Available Format Fields
~~~~~~~~~~~~~~~~~~~~~~~~


The **buildtest report** command displays a default format fields that can be changed using the
``--format`` option. The report file (JSON) contains many more fields and we expose some of the fields
with the **--format** option. To see a list of available format fields you can run ``buildtest report --helpformat``.
This option will list all format fields and their description.

.. program-output:: cat docgen/report-helpformat.txt

Format Field Usage
~~~~~~~~~~~~~~~~~~~

The ``--format`` field expects field name separated by comma (i.e ``--format <field1>,<field2>``).
In this example we format by fields ``--format id,executor,state,returncode``. Notice how
buildtest will format table columns in the order format options.

.. program-output:: cat docgen/report-format.txt
   :ellipsis: 21

Filter Reports
---------------

The **buildtest report** command will display all tests results, which may not be relevant when
you want to analyze specific tests. Therefore, we introduce a ``--filter`` option
to filter out tests in the output. First, lets see the available filter fields
by run ``buildtest report --helpfilter``.

.. program-output:: cat docgen/report-helpfilter.txt

The ``--filter`` option expects arguments in **key=value** format. You can
specify multiple filter delimited by comma. buildtest will treat multiple
filters as logical **AND** operation. The filter option can be used with
``--format`` field. Let's see some examples to illustrate the point.

Filter by returncode
~~~~~~~~~~~~~~~~~~~~~~

If you want to retrieve all tests with a given returncode, we can use the **returncode**
property. For instance, let's retrieve all tests with returncode of 2 by setting ``--filter returncode=2``.

.. program-output:: cat docgen/report-returncode.txt

.. Note:: buildtest automatically converts returncode to integer when matching returncode, so ``--filter returncode="2"`` will work too

Filter by test name
~~~~~~~~~~~~~~~~~~~~~

If you want to filter by test name, use the **name** attribute in filter option. Let's assume
we want to filter all tests by name ``exit1_pass`` which can be done by
setting ``--filter name=exit1_pass`` as shown below

.. program-output:: cat docgen/report-filter-name.txt

Filter by buildspec
~~~~~~~~~~~~~~~~~~~~~

Likewise, we can filter results by buildspec file using **buildspec** attribute via
``--filter buildspec=<file>``. The **buildspec** attribute must resolve to a file path which can be
relative or absolute path. buildtest will resolve path (absolute path) and find the appropriate
tests that belong to the buildspec file. If file doesn't exist or is not found in cache it will raise an error.

.. program-output:: cat docgen/report-filter-buildspec.txt

Filter by test state
~~~~~~~~~~~~~~~~~~~~~

If you want to filter results by test state, use the **state** property. This can be
useful if you want to know all pass or failed tests. The state property expects
value of ``[PASS|FAIL]`` since these are the two recorded test states marked by buildtest.
We can also pass multiple filter fields for instance if we want to find all **FAIL**
tests for executor **generic.local.sh** we can do the following.

.. program-output:: cat docgen/report-multifilter.txt

Filter Exception Cases
~~~~~~~~~~~~~~~~~~~~~~~~

The ``returncode`` filter field expects an integer value, so if you try a non-integer
returncode you will get the following message::

    $ buildtest report --filter returncode=1.5
    Traceback (most recent call last):
      File "/Users/siddiq90/Documents/buildtest/bin/buildtest", line 17, in <module>
        buildtest.main.main()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 45, in main
        args.func(args)
      File "/Users/siddiq90/Documents/buildtest/buildtest/menu/report.py", line 128, in func_report
        raise BuildTestError(f"Invalid returncode:{filter_args[key]} must be an integer")
    buildtest.exceptions.BuildTestError: 'Invalid returncode:1.5 must be an integer'

The ``state`` filter field expects value of ``PASS`` or ``FAIL`` so if you specify an
invalid state you will get an error as follows::

    $ buildtest report --filter state=UNKNOWN
    filter argument 'state' must be 'PASS' or 'FAIL' got value UNKNOWN

The ``buildspec`` field expects a valid file path, it can be an absolute or relative
path, buildtest will resolve absolute path and check if file exist and is in the report
file. If it's an invalid file we get an error such as::

    $ buildtest report --filter buildspec=/path/to/invalid.yml
    Invalid File Path for filter field 'buildspec': /path/to/invalid.yml

You may have a valid filepath for buildspec filter field such as
``tutorials/invalid_executor.yml``, but there is no record in the report cache
because this test can't be run. In this case you will get the following message::

    $ buildtest report --filter buildspec=tutorials/invalid_executor.yml
    buildspec file: /Users/siddiq90/Documents/buildtest/tutorials/invalid_executor.yml not found in cache

Find Latest or Oldest test
---------------------------

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


.. _inspect_test:

Inspect Tests Records
----------------------

buildtest provides an interface via ``buildtest inspect`` to query test details once
test is recorded in ``var/report.json``. The command usage is the following.

.. program-output:: cat docgen/buildtest_inspect_--help.txt

You can query all test names and corresponding ids using ``buildtest inspect list`` which
retrieves all test records from ``var/report.json``.

.. program-output:: cat docgen/buildtest_inspect_list.txt

The ``buildtest inspect name`` command can query test records based on test **name**
along with all runs for a particular test because a single test may be run multiple times.
Let's see first example of how it looks. buildtest is querying the appropriate record from
``var/report.json`` and display output in console

.. program-output:: cat docgen/buildtest_inspect_names.txt

You can pass multiple test names to ``buildtest inspect name <test1> <test2>`` and buildtest
will find all records for given name. In example below we show how one can inspect test records
for multiple test names in single command.

.. program-output:: cat docgen/buildtest_inspect_multi_names.txt

The ``buildtest inspect id`` works similar to ``buildtest inspect names`` except it
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

Using Alternate Report File
-----------------------------

The ``buildtest report`` and ``buildtest inspect`` command will read from report file $HOME/.buildtest/report.json
which is the central report file. This single file can became an issue if you are running jobs through CI where you
can potentially overwrite same file or remove $HOME/.buildtest as part of CI job that can impact other jobs.

In that case you can write your report file to alternate location using ``buildtest build -r <report>`` and then
specify the path to report file in ``buildtest report -r <report>`` and ``buildtest inspect -r <report>`` command.
The report file must be valid JSON file that buildtest understands in order to use `buildtest report` and
`buildtest inspect` command. Shown below are example usage with **-r** option using **buildtest report**
and **buildtest inspect** command

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

