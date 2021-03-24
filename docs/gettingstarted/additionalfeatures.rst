Additional Features
=====================

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


Debug Mode
------------

buildtest can stream logs to ``stdout`` stream for debugging. You can use ``buildtest -d <DEBUGLEVEL>``
or long option ``--debug`` with any buildtest commands. The DEBUGLEVEL are the following:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

buildtest is using `logging.setLevel <https://docs.python.org/3/library/logging.html#logging.Logger.setLevel>`_
to control log level. The content is logged in file **buildtest.log** in your current
directory with default log level of ``DEBUG``. If you want to get all logs use
``-d DEBUG`` with your buildtest command::

    buildtest -d DEBUG <command>

The debug mode can be useful when troubleshooting builds, in this example we
set debug level to ``DEBUG`` for an invalid buildspec.

.. program-output:: cat docgen/getting_started/debug-mode.txt

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
