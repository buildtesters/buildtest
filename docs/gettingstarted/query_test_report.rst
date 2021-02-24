
.. _test_reports:

Query Test Report
==================

buildtest keeps track of all tests and results in a JSON file that is stored in **$BUILDTEST_ROOT/var/report.json**. This
file is read by **buildtest report** command to extract certain fields from JSON file and display
them in table format. We use python `tabulate <https://pypi.org/project/tabulate/>`_ library for
pretty print table data. Shown below is command usage for **buildtest report** command.

.. program-output:: cat docgen/buildtest_report_--help.txt

You may run ``buildtest report`` without any option, and buildtest will display **all** test results
with default format fields. To see a list of all format fields, click :ref:`here <format_fields>`.

.. program-output:: cat docgen/report.txt
   :ellipsis: 20

Format Reports
---------------

.. _format_fields:

Available Format Fields
~~~~~~~~~~~~~~~~~~~~~~~~


The **buildtest report** command displays a default format fields that can be changed using the
``--format`` option. The report file (JSON) contains many more fields and we expose some of the fields
in the `--format` option. To see a list of available format fields run ``buildtest report --helpformat``.

.. program-output:: cat docgen/report-helpformat.txt

Format Field Usage
~~~~~~~~~~~~~~~~~~~

The ``--format`` field expects field name separated by comma (i.e **--format <field1>,<field2>**).
In this example we format by fields ``--format id,executor,state,returncode``. Notice, that
buildtest will display table in order of ``--format`` option.

.. program-output:: cat docgen/report-format.txt
   :ellipsis: 20

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
tests for executor **local.sh** we can do the following.

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

.. code-block::

   $ buildtest report --filter name=hello_f --format name,id,starttime
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
    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 349f3ada | 2021/02/11 18:13:08 |
    +---------+----------+---------------------+


If you want to retrieve the latest test result you can use ``--latest`` option which
will retrieve the last record, in the same example we will retrieve test id `5c87978b`.


.. code-block::

    $ buildtest report --filter name=hello_f --format name,id,starttime --latest
    +---------+----------+---------------------+
    | name    | id       | starttime           |
    +=========+==========+=====================+
    | hello_f | 5c87978b | 2021/02/11 18:13:33 |
    +---------+----------+---------------------+

You may combine **--oldest** and **--latest** options in same command, in this case
buildtest will retrieve the first and last record of every test.

.. code-block::

    $ buildtest report --format name,id,starttime --oldest --latest | more
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

Test Inspection
-----------------

buildtest provides an interface via ``buildtest inspect`` to query test details once
test is recorded in ``var/report.json``. The command usage is the following.

.. program-output:: cat docgen/buildtest_inspect_--help.txt

The ``buildtest inspect`` expects a **unique** test id this can be
retrieve using the ``full_id`` format field if you are not sure::

  $ buildtest report --format name,full_id

For example, let's assume we have the following tests in our report::

    $ buildtest report --format name,full_id
    +-------------------------+--------------------------------------+
    | name                    | full_id                              |
    +=========================+======================================+
    | bash_login_shebang      | eb6e26b2-938b-4913-8b98-e21528c82778 |
    +-------------------------+--------------------------------------+
    | bash_login_shebang      | d7937a9a-d3fb-4d3f-95e1-465488757820 |
    +-------------------------+--------------------------------------+
    | bash_login_shebang      | dea6c6fd-b9a6-4b07-a3fc-b483d02d7ff9 |
    +-------------------------+--------------------------------------+
    | bash_nonlogin_shebang   | bbf94b94-949d-4f97-987a-9a93309f1dc2 |
    +-------------------------+--------------------------------------+
    | bash_nonlogin_shebang   | 7ca9db2f-1e2b-4739-b9a2-71c8cc00249e |
    +-------------------------+--------------------------------------+
    | bash_nonlogin_shebang   | 4c5caf85-6ba0-4ca0-90b0-c769a2fcf501 |
    +-------------------------+--------------------------------------+
    | root_disk_usage         | e78071ef-6444-4228-b7f9-b4eb39071fdd |
    +-------------------------+--------------------------------------+
    | ulimit_filelock         | c6294cfa-c559-493b-b44f-b17b54ec276d |
    +-------------------------+--------------------------------------+
    | ulimit_cputime          | aa5530e2-be09-4d49-b8c0-0e818f855a40 |
    +-------------------------+--------------------------------------+
    | ulimit_stacksize        | 3591925d-7dfa-4bc7-a3b1-fb9dfadf956e |
    +-------------------------+--------------------------------------+
    | ulimit_vmsize           | 4a01f26b-9c8a-4870-8e33-51923c8c46ad |
    +-------------------------+--------------------------------------+
    | ulimit_filedescriptor   | 565b85ac-e51f-46f9-8c6f-c2899a370609 |
    +-------------------------+--------------------------------------+
    | ulimit_max_user_process | 0486c11c-5733-4d8e-822e-c0adddbb2af7 |
    +-------------------------+--------------------------------------+
    | systemd_default_target  | 7cfc9057-6338-403c-a7af-b1301d04d817 |
    +-------------------------+--------------------------------------+

Let's assume we are interested in viewing test ``bash_login_shebang``, since we
have multiple instance for same test we must specify a unique id. In example below
we query the the test id **eb6e26b2-938b-4913-8b98-e21528c82778**::

    $ buildtest inspect eb6e26b2-938b-4913-8b98-e21528c82778
    {
      "id": "eb6e26b2",
      "full_id": "eb6e26b2-938b-4913-8b98-e21528c82778",
      "testroot": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0",
      "testpath": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/stage/generate.sh",
      "command": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/stage/generate.sh",
      "outfile": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/run/bash_login_shebang.out",
      "errfile": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/shebang/bash_login_shebang/0/run/bash_login_shebang.err",
      "schemafile": "script-v1.0.schema.json",
      "executor": "local.bash",
      "tags": "tutorials",
      "starttime": "2020/10/21 16:27:18",
      "endtime": "2020/10/21 16:27:18",
      "runtime": 0.26172968399999996,
      "state": "PASS",
      "returncode": 0
    }



    Output File
    ______________________________
    Login Shell




    Error File
    ______________________________




    Test Content
    ______________________________
    #!/bin/bash -l
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh



    buildspec:  /Users/siddiq90/Documents/buildtest/tutorials/shebang.yml
    ______________________________
    version: "1.0"
    buildspecs:
      bash_login_shebang:
        type: script
        executor: local.bash
        shebang: "#!/bin/bash -l"
        description: customize shebang line with bash login shell
        tags: tutorials
        run: shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'
        status:
          regex:
            exp: "^Login Shell$"
            stream: stdout

      bash_nonlogin_shebang:
        type: script
        executor: local.bash
        shebang: "#!/bin/bash"
        description: customize shebang line with default bash (nonlogin) shell
        tags: tutorials
        run: shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'
        status:
          regex:
            exp: "^Not Login Shell$"
            stream: stdout



buildtest will present the test record from JSON record including contents of
output file, error file, testscript and buildspec file.

User can can specify first few characters of the id and buildtest will detect if
its a unique test id. If buildtest discovers more than one test id, then buildtest
will report all the ids where there is a conflict. In example below we find
two tests with id **7c**::

    $ buildtest inspect 7c
    Detected 2 test records, please specify a unique test id
    7ca9db2f-1e2b-4739-b9a2-71c8cc00249e
    7cfc9057-6338-403c-a7af-b1301d04d817

.. note:: This feature is in development and may change in future
