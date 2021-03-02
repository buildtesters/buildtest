
.. _test_reports:

Query Test Report
==================

buildtest keeps track of all tests and results in a JSON file that is stored in **$BUILDTEST_ROOT/var/report.json**. This
file is read by **buildtest report** command to extract certain fields from JSON file and display
them in table format. We use python `tabulate <https://pypi.org/project/tabulate/>`_ library for
pretty print table data. Shown below is command usage to query test reports.

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
with the **--format** option. To see a list of available format fields you can run ``buildtest report --helpformat``.
This option will list all format fields and their description.

.. program-output:: cat docgen/report-helpformat.txt

Format Field Usage
~~~~~~~~~~~~~~~~~~~

The ``--format`` field expects field name separated by comma (i.e ``--format <field1>,<field2>``).
In this example we format by fields ``--format id,executor,state,returncode``. Notice how
buildtest will format table columns in the order format options.

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

Let's assume we have the following tests in our report, we can see a full id for
each test which we can use to inspect a certain test::

    $  buildtest report --format name,full_id
    +------------------------------+--------------------------------------+
    | name                         | full_id                              |
    +==============================+======================================+
    | variables_bash               | a4ce2fd1-7723-4519-8525-0b5061d17d8d |
    +------------------------------+--------------------------------------+
    | variables_bash               | 9fbd7f93-3931-46a7-9095-8821d2553a85 |
    +------------------------------+--------------------------------------+
    | variables_bash               | e2dca3dc-99bc-4122-8231-3ae937681275 |
    +------------------------------+--------------------------------------+
    | variables_bash               | d747549f-261c-4457-ab1b-7fc574cf8fc0 |
    +------------------------------+--------------------------------------+
    | variables_bash               | 43cb7107-906b-455b-8928-4f776333d1bb |
    +------------------------------+--------------------------------------+

Let's assume we are interested in viewing test id **a4ce2fd1-7723-4519-8525-0b5061d17d8d**, we
can use ``buildtest inspect`` and pass the full id. buildtest will display the test record in JSON,
output and error content, content of testscript and buildspec file::

    $ buildtest inspect a4ce2fd1-7723-4519-8525-0b5061d17d8d
    {
      "id": "a4ce2fd1",
      "full_id": "a4ce2fd1-7723-4519-8525-0b5061d17d8d",
      "testroot": "/Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/vars/variables_bash/0",
      "testpath": "/Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/vars/variables_bash/0/stage/generate.sh",
      "stagedir": "/Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/vars/variables_bash/0/stage",
      "rundir": "/Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/vars/variables_bash/0/run",
      "command": "/Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/vars/variables_bash/0/stage/generate.sh",
      "outfile": "/Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/vars/variables_bash/0/run/variables_bash.out",
      "errfile": "/Users/siddiq90/Documents/buildtest/var/tests/generic.local.bash/vars/variables_bash/0/run/variables_bash.err",
      "schemafile": "script-v1.0.schema.json",
      "executor": "generic.local.bash",
      "tags": "tutorials",
      "starttime": "2021/03/01 15:11:09",
      "endtime": "2021/03/01 15:11:11",
      "runtime": 1.6528677349999998,
      "state": "PASS",
      "returncode": 0,
      "output": [
        "1+2= 3\n",
        "this is a literal string ':'\n",
        "singlequote\n",
        "doublequote\n",
        "siddiq90\n",
        "/Users/siddiq90/.anyconnect /Users/siddiq90/.DS_Store /Users/siddiq90/.serverauth.555 /Users/siddiq90/.CFUserTextEncoding /Users/siddiq90/.wget-hsts /Users/siddiq90/.bashrc /Users/siddiq90/.zshrc /Users/siddiq90/.coverage /Users/siddiq90/.serverauth.87055 /Users/siddiq90/.zsh_history /Users/siddiq90/.lesshst /Users/siddiq90/.git-completion.bash /Users/siddiq90/buildtest.log /Users/siddiq90/darhan.log /Users/siddiq90/ascent.yml /Users/siddiq90/.cshrc /Users/siddiq90/github-tokens /Users/siddiq90/.zcompdump /Users/siddiq90/.serverauth.543 /Users/siddiq90/.bash_profile /Users/siddiq90/.Xauthority /Users/siddiq90/.python_history /Users/siddiq90/.gitconfig /Users/siddiq90/output.txt /Users/siddiq90/.bash_history /Users/siddiq90/.viminfo\n"
      ],
      "error": [],
      "job": null
    }



    Output File
    ______________________________
    1+2= 3
    this is a literal string ':'
    singlequote
    doublequote
    siddiq90
    /Users/siddiq90/.anyconnect /Users/siddiq90/.DS_Store /Users/siddiq90/.serverauth.555 /Users/siddiq90/.CFUserTextEncoding /Users/siddiq90/.wget-hsts /Users/siddiq90/.bashrc /Users/siddiq90/.zshrc /Users/siddiq90/.coverage /Users/siddiq90/.serverauth.87055 /Users/siddiq90/.zsh_history /Users/siddiq90/.lesshst /Users/siddiq90/.git-completion.bash /Users/siddiq90/buildtest.log /Users/siddiq90/darhan.log /Users/siddiq90/ascent.yml /Users/siddiq90/.cshrc /Users/siddiq90/github-tokens /Users/siddiq90/.zcompdump /Users/siddiq90/.serverauth.543 /Users/siddiq90/.bash_profile /Users/siddiq90/.Xauthority /Users/siddiq90/.python_history /Users/siddiq90/.gitconfig /Users/siddiq90/output.txt /Users/siddiq90/.bash_history /Users/siddiq90/.viminfo




    Error File
    ______________________________




    Test Content
    ______________________________
    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/generic.local.bash/before_script.sh
    X=1
    Y=2
    literalstring="this is a literal string ':' "

    singlequote='singlequote'
    doublequote="doublequote"
    current_user=$(whoami)
    files_homedir=`find $HOME -type f -maxdepth 1`
    echo "$X+$Y=" $(($X+$Y))
    echo $literalstring
    echo $singlequote
    echo $doublequote

    echo $current_user
    echo $files_homedir
    source /Users/siddiq90/Documents/buildtest/var/executors/generic.local.bash/after_script.sh



    buildspec:  /Users/siddiq90/Documents/buildtest/tutorials/vars.yml
    ______________________________
    version: "1.0"
    buildspecs:
      variables_bash:
        type: script
        executor: generic.local.bash
        description: Declare shell variables in bash
        tags: [tutorials]
        vars:
          X: 1
          Y: 2
          literalstring: |
            "this is a literal string ':' "
          singlequote: "'singlequote'"
          doublequote: "\"doublequote\""
          current_user: "$(whoami)"
          files_homedir: "`find $HOME -type f -maxdepth 1`"

        run: |
          echo "$X+$Y=" $(($X+$Y))
          echo $literalstring
          echo $singlequote
          echo $doublequote

          echo $current_user
          echo $files_homedir

User can specify first few characters of the id and buildtest will detect if
its a unique test id. If buildtest discovers more than one test id, then buildtest
will report all the ids where there is a conflict. In example below we find
two tests with id **7c**::

    $ buildtest inspect 7c
    Detected 2 test records, please specify a unique test id
    7ca9db2f-1e2b-4739-b9a2-71c8cc00249e
    7cfc9057-6338-403c-a7af-b1301d04d817

.. note:: This feature is in development and may change in future
