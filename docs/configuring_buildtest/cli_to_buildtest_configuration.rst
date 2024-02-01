.. _configuration_cli:

Command Line Interface to buildtest configuration (``buildtest config``)
========================================================================

Once you have implemented your buildtest configuration, you can query the configuration
details using ``buildtest config`` command. Shown below is the command usage.

.. dropdown:: ``buildtest config --help``

    .. command-output:: buildtest config --help

.. note::
  ``buildtest cg`` is an alias for ``buildtest config`` command.

Validate buildtest configuration (``buildtest config validate``)
------------------------------------------------------------------

First thing you should do once you implement your configuration file  is to make sure your configuration is valid with the schema.
This can be achieved by running ``buildtest config validate``. When you invoke this
command, buildtest will load the configuration and attempt to validate the file with
schema **settings.schema.json**. If validation is successful you will get the following message:

.. command-output:: buildtest config validate

.. Note:: If you defined a user setting (``~/.buildtest/config.yml``) buildtest will validate this file instead of default one.

If there is an error during validation, the output from **jsonschema.exceptions.ValidationError**
will be displayed in terminal. For example the error below indicates that
``moduletool`` property was expecting one of the values
[``environment-modules``, ``lmod``, ``N/A``] but it received a value of ``none``:

.. dropdown:: Invalid buildtest configuration
   :color: warning

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


View buildtest configuration (``buildtest config view``)
----------------------------------------------------------

If you want to view buildtest configuration you can run ``buildtest config view`` which will print content of buildtest configuration.

.. dropdown:: ``buildtest config view``

    .. command-output:: buildtest config view

The ``--theme`` option can be used to change the color theme of the output. The default theme is ``monokai`` and list of
available themes can be retrieved with tab completion for option ``buildtest config view --theme``.

Check path to buildtest configuration file (``buildtest config path``)
-----------------------------------------------------------------------

If you want to check path to buildtest configuration file you can run ``buildtest config path`` which will print path of buildtest configuration file.

.. command-output:: buildtest config path

Edit buildtest configuration (``buildtest config edit``)
----------------------------------------------------------

The ``buildtest config edit`` command is used to open buildtest configuration file in your preferred editor. buildtest will
use the environment **EDITOR** to get the preffered editor; however, one can override the environment variable via command line option
``buildtest --editor``.

.. _view_executors:

View Executors (``buildtest config executors list``)
-----------------------------------------------------

You can use the command ``buildtest config executors list`` to view executors from buildtest
configuration file.  Shown below is the command usage

.. dropdown:: ``buildtest config executors list --help``

    .. command-output:: buildtest config executors list --help

You can run ``buildtest config executors list`` without any options and it will report a list of named executors that
you would reference in buildspec using the ``executor`` property.

.. command-output:: buildtest config executors list

If you want to see the executor details, you may want to use ``--json`` or ``--yaml`` option which will show the executor settings in YAML or JSON format.
Shown below is an example output

.. dropdown:: ``buildtest config executors list --yaml``

    .. command-output:: buildtest config executors list --yaml

.. dropdown:: ``buildtest config executors list --json``

    .. command-output:: buildtest config executors list --json


.. note::

    The command options for ``buildtest config executors list`` are mutually exclusive, so if you
    specify multiple options you will get the following error.

    .. command-output:: buildtest config executors list --json --yaml
        :returncode: 2

Remove Executors (``buildtest config executors remove``)
----------------------------------------------------------

The ``buildtest config executors remove`` command will remove an executor from buildtest configuration file.
The positional arguments are the name of the executor you want to remove. Tab completion is available to retrieve
all available executors (``buildtest config executors list --all``).

Shown below we see tab completion on available executors that can be removed.


.. code-block:: console

      buildtest config executors remove
    generic.local.bash  generic.local.csh   generic.local.sh    generic.local.zsh

Let's try listing all executors and remove ``generic.local.zsh`` executor, you will notice after deletion,
the configuration file is updated and the executor is no longer present.

.. dropdown:: Removing executor 'generic.local.zsh'

    .. command-output:: buildtest --config $BUILDTEST_CI_DIR/config.yml config executors list --all

    .. command-output::  buildtest --config $BUILDTEST_CI_DIR/config.yml config executors remove generic.local.zsh


Upon deletion, buildtest will validate the configuration before writing the changes back to disk, to ensure the
configuration is valid. Shown below we demonstrate an example where we attempt to remove all executors from the configuration file.
Buildtest expects there is atleast 1 executor definition for **local** executor.

.. dropdown:: ``buildtest config executors remove generic.local.bash generic.local.sh generic.local.csh generic.local.zsh``
    :color: warning

    .. command-output:: buildtest config executors remove generic.local.bash generic.local.sh generic.local.csh generic.local.zsh
        :returncode: 1

View Registered Systems (``buildtest config systems``)
-------------------------------------------------------

Your buildtest configuration may compose of one or more systems since you can define multiple systems
in a single configuration file to run buildtest for different HPC clusters. You can use
``buildtest config systems`` to report all system details defined in your configuration file.
In this example below we should the ``generic`` system. If you have multiple entries, you will see one
entry per system record.

.. command-output:: buildtest config systems
