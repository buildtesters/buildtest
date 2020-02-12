Introspection Operation
=========================


List Software (``buildtest module --software``)
---------------------------------------------------------------

buildtest can report the software list by running the following ``buildtest module --software`` or
short option ``buildtest module -s``


buildtest determines the software list based on the module trees specified in ``BUILDTEST_MODULEPATH``
and processes each module tree and returns a  unique software list

.. program-output:: head -n 10 docgen/buildtest_module_--software.txt


Listing Modules (``buildtest module list``)
------------------------------------------------

If you want to view a breakdown of all modules then use ``buildtest module list``. The output will be sorted by software
and each entry will correspond to the full path of the modulefile.

.. program-output:: head -n 10 docgen/buildtest_module_list.txt

For more information see :ref:`buildtest_module_list`

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
