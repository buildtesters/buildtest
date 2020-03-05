Introspection Operation
=========================


Show Options (``buildtest show --help``)
_________________________________________

.. program-output:: cat docgen/buildtest_show_-h.txt

Show Configuration (``buildtest show --config``)
-------------------------------------------------

buildtest can display it's configuration by running ``buildtest show --config``. The
configuration can be changed by the following:

 1. Command Line
 2. Environment Variable (``BUILDTEST_``)
 3. Configuration File (``settings.yml``)

buildtest will read configuration from ``settings.yml``. User may override any configuration
values by environment variables that start with ``BUILDTEST_``. The command line will
override environment variables and configuration variables runtime.

Shown below is a sample configuration from buildtest by running ``buildtest show --config``.


.. program-output:: cat docgen/buildtest_show_--config.txt

.. _show_keys:

Show YAML Schema (``buildtest show schema``)
----------------------------------------------

buildtest can show YAML schema that is used for writing tests. This can be retrieved by running
``buildtest show schema``

.. program-output:: cat docgen/buildtest_show_schema.txt
