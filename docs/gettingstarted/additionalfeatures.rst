Additional Features
=====================

Accessing build history
-------------------------

buildtest keeps track of all builds (``buildtest build``) that can be retrieved using ``buildtest history`` command
which can be useful when you want to analyze or troubleshoot past builds. The `buildtest history` command comes with two
subcommands ``buildtest history list`` and ``buildtest history query``.

If you want to list all builds you should run **buildtest history list** which will report a table style
format of all builds with corresponding build ID to differentiate each build. Shown below is an example output. The build
IDs start at **0** and increment as you run **buildtest build** command.

.. program-output:: cat docgen/buildtest_history_list.txt

The ``buildtest history query`` command is particularly useful when you want to inspect a particular build. This command
expects a *Build Identifier* which can be found by inspecting output column `id` in `buildtest history list`.

Shown below is an output of build ID 0 which reports relevant detail for the build such as input command, username, hostname,
platform, date, etc...


.. program-output:: cat docgen/buildtest_history_query.txt

.. _buildtest_schemas:

buildtest schemas
------------------

buildtest uses JSON Schema for validating buildspecs and :ref:`buildtest configuration file <configuring_buildtest>`.
You can use ``buildtest schema`` command to see the list of schemas
supported by buildtest. The schema files are denoted by ``.schema.json`` file extension.

.. program-output:: cat docgen/schemas/avail-schemas.txt

Shown below is the command usage of ``buildtest schema``

.. program-output:: cat docgen/buildtest_schema_--help.txt

The json schemas are published at https://buildtesters.github.io/buildtest/ and we
provide a command line interface to view schema files and examples.

To select a JSON schema use the ``--name`` option to select a schema, for example
to view a JSON Schema for **script-v1.0.schema.json** run the following::

  $ buildtest schema --name script-v1.0.schema.json --json

Similarly, if you want to view example buildspecs for a schema use the ``--example``
option with a schema. For example to view all example schemas for
**compiler-v1.0.schema.json** run the following::

  $ buildtest schema --name compiler-v1.0.schema.json --example

To learn more about schema files and and examples click :ref:`here <schema_examples>`.


Accessing buildtest documentation
----------------------------------

We provide two command line options to access main documentation and schema docs. This
will open a browser on your machine.

To access `buildtest docs <https://buildtest.readthedocs.io/>`_ you can run::

  $ buildtest docs

To access `schema docs <https://buildtesters.github.io/buildtest>`_ you can run::

  $ buildtest schemadocs

Color Mode
----------

buildtest will display output in color, if you want to disable color you can set
environment variable ``BUILDTEST_COLOR`` to **False** and buildtest will not display
the ANSI codes. This can be useful if you don't want to see ANSI color codes in the
text output.

.. _cdash_integration:

CDASH Integration
-------------------

The ``buildtest cdash`` command is responsible for uploading tests to CDASH server. You will
need to specify :ref:`cdash_configuration` in your configuration file. Shown below is the command
usage.

.. program-output:: cat docgen/buildtest_cdash_--help.txt

The ``buildtest cdash upload`` command is responsible for uploading all tests in `report.json`
into CDASH. You must specify a buildname when using **buildtest cdash upload** in this example we will
specify a buildname called `tutorials`::

    $ buildtest cdash upload tutorials
    Reading configuration file:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/settings/config.yml
    Reading report file:  /Users/siddiq90/.buildtest/report.json
    build name:  tutorials
    site:  generic
    stamp:  20210428-1512-Experimental
    MD5SUM: d7651cb3fbdd19298b0188c441704c3a
    PUT STATUS: 200
    You can view the results at: https://my.cdash.org//viewTest.php?buildid=2004360

We can see the output of these tests in CDASH if we go to url https://my.cdash.org//viewTest.php?buildid=2004360

.. image:: ../_static/CDASH.png

By default buildtest will read the report file in your **$HOME/.buildtest/report.json**, we can
specify an alternate report file. First let's see the available help options for
``buildtest cdash upload``.

.. program-output:: cat docgen/buildtest_cdash_upload_--help.txt

We can pass an alternate report file using ``--report-file`` option when uploading tests
to CDASH. This can be useful if you want to map test results to different buildnames in CDASH
perhaps running a different subset of tests via ``buildtest build --tags`` and upload
the test results with different buildname assuming you have different paths to report file.

Let's say we want to build all python tests using tags and store them in a report file which we
want to push to CDASH with buildgroup name ``python`` we can do that as follows::

    $ buildtest build --tags python -r python.json


    User:  siddiq90
    Hostname:  DOE-7086392.local
    Platform:  Darwin
    Current Time:  2021/04/28 15:36:06
    buildtest path: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
    python version:  3.7.3
    Test Directory:  /Users/siddiq90/.buildtest/var/tests
    Configuration File:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/settings/config.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    Discovered Buildspecs:
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/python-shell.yml
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/python-hello.yml

    BREAKDOWN OF BUILDSPECS BY TAGS

    python
    ----------------------------------------------------------------------------
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/python-shell.yml
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/python-hello.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile              | validstate   | buildspec
    -------------------------+--------------+------------------------------------------------------------------------------
     script-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/python-shell.yml
     script-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/python-hello.yml



    name          description
    ------------  ---------------------------------------
    circle_area   Calculate circle of area given a radius
    python_hello  Hello World python

    +----------------------+
    | Stage: Building Test |
    +----------------------+

     name         | id       | type   | executor             | tags                    | testpath
    --------------+----------+--------+----------------------+-------------------------+--------------------------------------------------------------------------------------------------------
     circle_area  | 6be6c404 | script | generic.local.python | ['tutorials', 'python'] | /Users/siddiq90/.buildtest/var/tests/generic.local.python/python-shell/circle_area/5/stage/generate.sh
     python_hello | f21ba744 | script | generic.local.bash   | python                  | /Users/siddiq90/.buildtest/var/tests/generic.local.bash/python-hello/python_hello/3/stage/generate.sh



    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name         | id       | executor             | status   |   returncode
    --------------+----------+----------------------+----------+--------------
     circle_area  | 6be6c404 | generic.local.python | PASS     |            0
     python_hello | f21ba744 | generic.local.bash   | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%


    Writing Logfile to: /var/folders/1m/_jjv09h17k37mkktwnmbkmj0002t_q/T/buildtest_k6swspn5.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest.log


Next we upload the tests using the ``-r`` option to specify the report file::

    (buildtest) bash-3.2$ buildtest cdash upload -r python.json python
    Reading configuration file:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/settings/config.yml
    Reading report file:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/docs/python.json
    build name:  python
    site:  generic
    stamp:  20210428-1536-Experimental
    MD5SUM: d1c467eaf166999fd6e12b311e767cf9
    PUT STATUS: 200
    You can view the results at: https://my.cdash.org//viewTest.php?buildid=2004362


The ``buildtest cdash view`` command can be used to open CDASH project in a web browser
using the command line. This feature assumes you have set the CDASH setting in your
configuration file.