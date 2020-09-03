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

Schemas (``buildtest schema``)
-------------------------------

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

.. _test_reports:

Test Reports (``buildtest report``)
-------------------------------------

buildtest keeps track of all test results which can be retrieved via
**buildtest report**. Shown below is command usage.

.. program-output:: cat docgen/buildtest_report_--help.txt

You may run ``buildtest report`` and buildtest will display report
with default format fields.

.. program-output:: cat docgen/report.txt

There are more fields captured in the report, so if you want to see a
list of available format fields run ``buildtest report --helpformat``.

.. program-output:: cat docgen/report-helpformat.txt

You can filter report using ``--format`` field which expects field
name separated by comma (i.e **--format <field1>,<field2>**). In this example
we format by fields ``--format name,type,executor,state,returncode``

.. program-output:: cat docgen/report-format.txt
