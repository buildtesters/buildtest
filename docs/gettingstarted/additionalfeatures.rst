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

.. command-output:: buildtest history list

The ``buildtest history query`` command is particularly useful when you want to inspect a particular build. This command
expects a *Build Identifier* which can be found by inspecting output column `id` in `buildtest history list`.

Shown below is an output of build ID 0 which reports relevant detail for the build such as input command, username, hostname,
platform, date, etc...

.. command-output:: buildtest history query 0
    :shell:

.. _buildtest_schemas:

buildtest schemas
------------------

buildtest uses JSON Schema for validating buildspecs and :ref:`buildtest configuration file <configuring_buildtest>`.
You can use ``buildtest schema`` command to see the list of schemas
supported by buildtest. The schema files are denoted by ``.schema.json`` file extension.

.. command-output:: buildtest schema

Shown below is the command usage of ``buildtest schema``

.. command-output:: buildtest schema --help

The json schemas are published at https://buildtesters.github.io/buildtest/ and we
provide a command line interface to view schema files and examples. You must use the
``--name`` option to select a schema, for instance if you want to view the JSON Schema for
**script-v1.0.schema.json** you can run the following::

    buildtest schema --name script-v1.0.schema.json --json

Similarly, if you want to view example buildspecs for a schema use the ``--example``
option with a schema. For example to view all example schemas for
**compiler-v1.0.schema.json** run the following::

  buildtest schema --name compiler-v1.0.schema.json --example

To learn more about schema files and and examples click :ref:`here <schema_examples>`.

Accessing buildtest documentation
----------------------------------

We provide two command line options to access main documentation and schema docs. This
will open a browser on your machine.

To access `buildtest docs <https://buildtest.readthedocs.io/>`_ you can run::

  buildtest docs

To access `schema docs <https://buildtesters.github.io/buildtest>`_ you can run::

  buildtest schemadocs

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

.. command-output:: buildtest cdash --help

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

.. command-output:: buildtest cdash upload --help

We can pass an alternate report file using ``-r`` option when uploading tests
to CDASH. This can be useful if you want to map test results to different buildnames in CDASH
perhaps running a different subset of tests via ``buildtest build --tags`` and upload
the test results with different buildname assuming you have different paths to report file.

Let's say we want to build all python tests using tags and store them in a report file which we
want to push to CDASH with buildgroup name ``python`` we can do that as follows

.. command-output:: buildtest build --tags python -r $BUILDTEST_ROOT/python.json
    :shell:

Next we upload the tests using the ``-r`` option to specify the report file

.. command-output:: buildtest cdash upload -r $BUILDTEST_ROOT/python.json python
    :shell:

The ``buildtest cdash view`` command can be used to open CDASH project in a web browser
using the command line. This feature assumes you have set the CDASH setting in your
configuration file.