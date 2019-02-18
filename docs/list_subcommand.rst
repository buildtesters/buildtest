List Subcommands (``buildtest list``)
=======================================

.. contents::
   :backlinks: none

List Options (``buildtest list --help``)
-----------------------------------------

.. program-output:: cat scripts/list_subcommand/help.txt


buildtest comes with a set of options for listing useful info such as

-  List Unique software

-  List software-modulefile relationship

-  List of easyconfigs


List Software (``buildtest list -ls``)
---------------------------------------------------------------

buildtest can report the software list by running the following ``buildtest list --list-unique-software`` or
short option ``buildtest list -ls``


buildtest determines the software list based on the module trees specified in ``BUILDTEST_MODULE_ROOT``
and processes each module tree and returns a  unique software list

.. program-output:: head -n 15 scripts/list_subcommand/software.txt


Software Version Relationship (``buildtest list -svr``)
---------------------------------------------------------------

If you want to view a breakdown of all software by version and full path to modulefile
then you want to use ``buildtest list --software-version-relation`` or short option
``buildtest list -svr``

The output will be sorted by software and each entry will correspond to the full path of the modulefile.

.. program-output:: head -n 15 scripts/list_subcommand/software_version.txt

.. _list_easyconfigs:

List easyconfigs from module trees (``buildtest list --easyconfigs``)
-------------------------------------------------------------------------

buildtest can return a list of easyconfigs from module trees defined in ``BUILDTEST_MODULE_ROOT``.
You can run ``buildtest list --easyconfigs`` or short option ``buildtest list -ec``.

buildtest will report full path to easyconfigs and also report any errors if it can't find
any easyconfig. If you specify a module tree that is not built by easybuild you can expect
some **warning** or **error** messages which is intended.

buildtest will attempt to search for any file with ``.eb`` extension  in ``easybuild`` directory
that is part of install directory of each software for every easybuild app.

.. program-output:: head -n 15 scripts/list_subcommand/easyconfigs.txt

If an easyconfig is not found you may get the following message

.. Error::

    Could not find easyconfig in /clust/app/easybuild/2018/IvyBridge/redhat/7.3/software/NWChem/6.8.revision47-intel-2018a-2017-12-14-Python-2.7.14/easybuild


Formatting output (``buildtest list --format``)
------------------------------------------------------

buildtest provides ``--format`` option to control output behavior of ``buildtest list``.
Currently, buildtest only supports json format that can be passed using ``--format=json``


To print output in json let's run ``buildtest list -ls --format=json``

.. program-output:: cat scripts/list_subcommand/software_format_json.txt
