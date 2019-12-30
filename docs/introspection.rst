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

Variables denoted with **(C)** are coming from configuration file (``settings.yml``) likewise,
variables set from environment variable (i.e **BUILDTEST_**) will be denoted with a **(E)**.

.. Note:: if you plan to customize your buildtest configuration with configuration file
    and environment variable, always check your shell environment first to avoid having
    values overridden accidentally

.. _show_keys:

Show Keys
-----------

buildtest can show YAML keys based on testblock. Currently, there is one testblock
defined **singlesource**.

To show yaml keys you can run ``buildtest show -k singlesource`` to view all the YAML
keys that pertain to ``testtype: singlesource`` found in YAML files

.. program-output:: cat docgen/buildtest_show_-k_singlesource.txt


System Options (``buildtest system --help``)
_____________________________________________

.. program-output:: cat docgen/buildtest_system_-h.txt

buildtest will detect system configuration and store the content in ``var/system.json``. This file contains
useful information about the scheduler details that can be used for submitting jobs.

To fetch the latest system configuration run the following::

    $ buildtest system fetch

This will update the system.json with the latest configuration. Typically you may only need to run this command to get the
latest scheduler changes but don't worry if you forget to run this as it is not critical to buildtest.

.. program-output:: cat docgen/buildtest_system_fetch.txt

To view the system configuration you can run the following::

    $ buildtest system view

This will display the content of ``system.json``.

.. program-output:: head -n 50 docgen/buildtest_system_view.txt


