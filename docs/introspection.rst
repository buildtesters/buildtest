Introspection Operation
=========================

.. contents::
   :backlinks: none

List Options (``buildtest list --help``)
____________________________________________

.. program-output:: cat docgen/buildtest_list_-h.txt


buildtest comes with a set of options for listing useful info such as

-  List Unique software

-  List software-modulefile relationship

-  List of easyconfigs


List Software (``buildtest list --software``)
---------------------------------------------------------------

buildtest can report the software list by running the following ``buildtest list --software`` or
short option ``buildtest list -s``


buildtest determines the software list based on the module trees specified in ``BUILDTEST_MODULEPATH``
and processes each module tree and returns a  unique software list

.. program-output:: head -n 10 docgen/buildtest_list_--software.txt


Listing Modules (``buildtest list --modules``)
------------------------------------------------

If you want to view a breakdown of all modules then use ``buildtest list
--modules`` or short option ``buildtest list -m``

The output will be sorted by software and each entry will correspond to the full path of the modulefile.

.. program-output:: head -n 10 docgen/buildtest_list_--modules.txt

.. _list_easyconfigs:

List easyconfigs from module trees (``buildtest list --easyconfigs``)
-------------------------------------------------------------------------

buildtest can return a list of easyconfigs from module trees defined in ``BUILDTEST_MODULEPATH``.
You can run ``buildtest list --easyconfigs`` or short option ``buildtest list -ec``.

buildtest will report full path to easyconfigs and also report any errors if it can't find
any easyconfig. If you specify a module tree that is not built by easybuild you can expect
some **warning** or **error** messages which is intended.

buildtest will attempt to search for any file with ``.eb`` extension  in ``easybuild`` directory
that is part of install directory of each software for every easybuild app.

.. program-output:: head -n 10 docgen/buildtest_list_--easyconfigs.txt


If an easyconfig is not found you may get the following message

.. Error::

    Could not find easyconfig in /clust/app/easybuild/2018/IvyBridge/redhat/7.3/software/NWChem/6.8.revision47-intel-2018a-2017-12-14-Python-2.7.14/easybuild


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



``buildtest show --config`` will show the updated configuration if you set any ``BUILDTEST_*`` environment
variables.

For instance, if you want to override configuration BUILDTEST_SPIDER_VIEW to
``all`` then ``buildtest show --config`` will report the overridden value denoted with **(E)** to indicate configuration was set
by environment variable.

See example below

.. code-block:: console
    :linenos:
    :emphasize-lines: 9

    $ BUILDTEST_SPIDER_VIEW=all buildtest show -c
         buildtest configuration summary
         (C): Configuration File,  (E): Environment Variable
    BUILDTEST_BINARY                                   (C) = False
    BUILDTEST_CONFIGS_REPO                             (C) = /u/users/ssi29/gpfs/buildtest-framework/toolkit/suite
    BUILDTEST_MODULEPATH                               (C) = /mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core:/mxg-hpc/users/ssi29/spack/modules/linux-rhel7-x86_64/Core:/mxg-hpc/users/ssi29/easybuild/modules/all:/etc/modulefiles:/usr/share/modulefiles:/usr/share/lmod/lmod/modulefiles/Core
    BUILDTEST_MODULE_FORCE_PURGE                       (C) = False
    BUILDTEST_PARENT_MODULE_SEARCH                     (C) = first
    BUILDTEST_SPIDER_VIEW                              (E) = all
    BUILDTEST_SUCCESS_THRESHOLD                        (C) = 1.0
    BUILDTEST_TESTDIR                                  (C) = /tmp/ssi29/buildtest/tests

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


