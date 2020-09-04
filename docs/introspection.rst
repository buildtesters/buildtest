Introspection Operation
=========================

Config Options (``buildtest config --help``)
-----------------------------------------------

.. program-output:: cat docgen/buildtest_config_--help.txt

The ``buildtest config`` command allows user to see view or edit your buildtest
settings file (``settings.yml``). To see content of your buildtest settings run::

    buildtest config view

Shown below is an example output.

.. program-output:: cat docgen/config-view.txt

Likewise, you can edit the file by running::

    buildtest config edit

To check if your buildtest settings is valid, run ``buildtest config validate``.
This will validate your ``settings.yml`` with the schema **settings.schema.json**.
The output will be the following.

.. program-output:: cat docgen/config-validate.txt

If there is an error during validation, the output from **jsonschema.exceptions.ValidationError**
will be displayed in terminal. For example the error below indicates there was an error
on ``editor`` key in **config** object which expects the editor to be one of the
enum types [``vi``, ``vim``, ``nano``, ``emacs``]::

    $ buildtest config validate
    Traceback (most recent call last):
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/bin/buildtest", line 11, in <module>
        load_entry_point('buildtest', 'console_scripts', 'buildtest')()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 32, in main
        check_settings()
      File "/Users/siddiq90/Documents/buildtest/buildtest/config.py", line 71, in check_settings
        validate(instance=user_schema, schema=config_schema)
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/lib/python3.7/site-packages/jsonschema/validators.py", line 899, in validate
        raise error
    jsonschema.exceptions.ValidationError: 'gedit' is not one of ['vi', 'vim', 'nano', 'emacs']

    Failed validating 'enum' in schema['properties']['config']['properties']['editor']:
        {'default': 'vim',
         'enum': ['vi', 'vim', 'nano', 'emacs'],
         'type': 'string'}

    On instance['config']['editor']:
        'gedit'


You can get a summary of buildtest using ``buildtest config summary``, this will
display information from several sources into one single command along.

.. program-output:: cat docgen/config-summary.txt

.. _buildtest_schemas:

Access to buildtest schemas
-----------------------------

The ``buildtest schema`` command can show you list of available schemas just run
the command with no options and it will show all the json schemas buildtest supports.

.. program-output:: cat docgen/schemas/avail-schemas.txt

Shown below is the command usage of ``buildtest schema``

.. program-output:: cat docgen/buildtest_schema_--help.txt

The json schemas are hosted on the web at https://buildtesters.github.io/schemas/.
buildtest provides a means to display the json schema from the buildtest interface.
Note that buildtest will show the schemas provided in buildtest repo and not
ones provided by `schemas <https://github.com/buildtesters/schemas>`_ repo. This
is because, we let development of schema run independent of the framework.

To select a JSON schema use the ``--name`` option to select a schema, for example
to view a JSON Schema for **script-v1.0.schema.json** run the following::

  $ buildtest schema --name script-v1.0.schema.json --json

Similarly, if you want to view example buildspecs for a schema use the ``--example``
option with a schema. For example to view all example schemas for
**compiler-v1.0.schema.json** run the following::

  $ buildtest schema --name compiler-v1.0.schema.json --example


Query buildspec features
--------------------------

.. program-output:: cat docgen/buildtest_buildspec_--help.txt

The ``buildtest buildspec find`` loads all buildspecs specified in :ref:`buildspec_roots`
from your configuration file. To build your cache just run::

  $ buildtest buildspec find

To rebuild your cache, which you may need to do if you add more directories to ``buildspec_roots``
in your configuration or edit some buildspec run::

    $ buildtest buildspec find --clear

This will rebuild your cache and validate all buildspecs with updated files. Currently,
we don't support automatic rebuild of cache.

Shown below is a list of options for ``buildtest buildspec find`` command.

.. program-output:: cat docgen/buildtest_buildspec_find_--help.txt

If you want to retrieve all unique tags from all buildspecs you can run
``buildtest buildspec find --tags``

.. program-output:: cat docgen/buildtest_buildspec_find_tags.txt

If you want to find all buildspec files in cache run ``buildtest buildspec find --buildspec-files``


.. program-output:: cat docgen/buildtest_buildspec_find_buildspecfiles.txt

To find all executors from cache you can run ``buildtest buildspec find --list-executors``.
This will retrieve the `'executor'` field from all buildspec and any duplicates will
be ignored.

.. program-output:: cat docgen/buildtest_buildspec_find_executors.txt


.. _test_reports:

Test Reports (``buildtest report``)
-------------------------------------

buildtest keeps track of all test results which can be retrieved via
**buildtest report**. Shown below is command usage.

.. program-output:: cat docgen/buildtest_report_--help.txt

You may run ``buildtest report`` and buildtest will display report
with default format fields.

.. program-output:: cat docgen/report.txt

Format Reports
~~~~~~~~~~~~~~~

There are more fields captured in the report, so if you want to see a
list of available format fields run ``buildtest report --helpformat``.

.. program-output:: cat docgen/report-helpformat.txt

You can format report using ``--format`` field which expects field
name separated by comma (i.e **--format <field1>,<field2>**). In this example
we format by fields ``--format name,type,executor,state,returncode``

.. program-output:: cat docgen/report-format.txt

Filter Reports
~~~~~~~~~~~~~~~~

You can also filter reports using the ``--filter`` option, but first let's
check the available filter fields. In order to see available filter fields
run ``buildtest report --helpfilter``.

.. program-output:: cat docgen/report-helpfilter.txt

The ``--filter`` expects arguments in **key=value** format, you can
specify multiple filter fields by a comma. buildtest will treat multiple
filters as logical **AND** operation. The filter option can be used with
``--format`` field. Let's see some examples to illustrate the point.

To see all tests with returncode of 2 we set ``--filter returncode=2``.

.. program-output:: cat docgen/report-returncode.txt

If you want to filter by test name ``exit1_pass`` you can use the
``name=exit1_pass`` field as shown below

.. program-output:: cat docgen/report-filter-name.txt

Likewise, we can filter tests by buildspec file using the ``--filter buildspec=<file>``.
In example below we set ``buildspec=tutorials/pass_returncode.yml``. In this example,
buildtest will resolve path and find the buildspec. If file doesn't exist or is
not found in cache it will raise an error

.. program-output:: cat docgen/report-filter-buildspec.txt

We can also pass multiple filter fields for instance if we want to find all **FAIL**
tests for executor **local.sh** we can do the following

.. program-output:: cat docgen/report-multifilter.txt

The state field expects value of ``PASS`` or ``FAIL`` so if you specify an
invalid state you will get an error as follows::

    $ buildtest report --filter state=UNKNOWN
    filter argument 'state' must be 'PASS' or 'FAIL' got value UNKNOWN


Access to docs
---------------

If you want to access buildtest docs from command line you can run::

  $ buildtest --docs

Similarly, we provide an option to view schemadocs if you run::

  $ buildtest --schemadocs
