.. _configuration_cli:

Command Line Interface to buildtest configuration
==================================================

Once you have implemented your buildtest configuration, you can query the configuration
details using ``buildtest config`` command. Shown below is the command usage.

.. command-output:: buildtest config --help

Validate buildtest configuration
---------------------------------

First thing you should do once you implement your configuration file  is to make sure your configuration is valid with the schema.
This can be achieved by running ``buildtest config validate``. When you invoke this
command, buildtest will load the configuration and attempt to validate the file with
schema **settings.schema.json**. If validation is successful you will get the following message:

.. command-output:: buildtest config validate

.. Note:: If you defined a user setting (``~/.buildtest/config.yml``) buildtest will validate this file instead of default one.

If there is an error during validation, the output from **jsonschema.exceptions.ValidationError**
will be displayed in terminal. For example the error below indicates that
``moduletool`` property was expecting one of the values
[``environment-modules``, ``lmod``, ``N/A``] but it recieved a value of ``none``:

.. code-block:: console

    $ buildtest config validate
    Traceback (most recent call last):
      File "/Users/siddiq90/Documents/buildtest/bin/buildtest", line 17, in <module>
        buildtest.main.main()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 39, in main
        buildtest_configuration = check_settings(settings_file, retrieve_settings=True)
      File "/Users/siddiq90/Documents/buildtest/buildtest/config.py", line 41, in check_settings
        validate(instance=user_schema, schema=config_schema)
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/lib/python3.7/site-packages/jsonschema/validators.py", line 934, in validate
        raise error
    jsonschema.exceptions.ValidationError: 'none' is not one of ['environment-modules', 'lmod', 'N/A']

    Failed validating 'enum' in schema['properties']['moduletool']:
        {'description': 'Specify modules tool used for interacting with '
                        '``module`` command. ',
         'enum': ['environment-modules', 'lmod', 'N/A'],
         'type': 'string'}

    On instance['moduletool']:
        'none'


View buildtest configuration
------------------------------

If you want to view buildtest configuration you can run ``buildtest config view`` which will print content of buildtest configuration.

.. command-output:: buildtest config view

.. Note:: ``buildtest config view`` will display contents of user buildtest settings ``~/.buildtest/config.yml`` if found, otherwise it will display the default configuration

.. _view_executors:

View Executors
--------------

You can use the command ``buildtest config executors`` to view executors from buildtest
configuration file.  Shown below is the command usage

.. command-output:: buildtest config executors --help

You can run ``buildtest config executors`` without any options and it will report a list of named executors that
you would reference in buildspec using the ``executor`` property. If you prefer json or yaml format you can use ``--json`` or ``--yaml`` option.

.. command-output:: buildtest config executors

View Registered Systems
------------------------

Your buildtest configuration may compose of one or more systems since you can define multiple systems
in a single configuration file to run buildtest for different HPC clusters. You can use
``buildtest config systems`` to report all system details defined in your configuration file.
In this example below we should the ``generic`` system. If you have multiple entries, you will see one
entry per system record.

.. command-output:: buildtest config systems

Configuration Summary
----------------------

You can get a summary of buildtest using ``buildtest config summary``, this will
display information from several sources into one single command along.

.. command-output:: buildtest config summary

Example Configurations
-----------------------

buildtest provides a few example configurations for configuring buildtest this
can be retrieved by running ``buildtest schema -n settings.schema.json --examples``
or short option (``-e``), which will validate each example with schema file
``settings.schema.json``.

.. command-output:: buildtest schema -n settings.schema.json -e

If you want to retrieve full json schema file for buildtest configuration you can
run ``buildtest schema -n settings.schema.json --json`` or short option ``-j``.