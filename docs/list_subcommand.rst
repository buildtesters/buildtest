.. _list_operations:

List Operations
================

.. contents::
   :backlinks: none

List Subcommand (``buildtest list``)
---------------------------------------

buildtest comes with a set of options for listing useful info such as

1. Unique software
2. List of toolchain
3. List software-modulefile relationship
4. List of easyconfigs

.. program-output:: cat scripts/List_Subcommand/help.txt


List Software (``buildtest list -ls``)
---------------------------------------------------------------

buildtest can report the software list by running the following ``buildtest list --list-unique-software`` or
short option ``buildtest list -ls``


buildtest determines the software list based on the module trees specified in ``BUILDTEST_MODULE_ROOT``
and processes each module tree and returns a  unique software list

.. program-output:: head -n 15 scripts/List_Subcommand/software.txt

List Toolchains (``buildtest list -lt``)
---------------------------------------------------------------

buildtest can list the easybuild toolchain list by running ``buildtest list --list-toolchain`` or
short option ``buildtest list -lt``

This will get the same result defined by **eb --list-toolchains**, we have
taken the list of toolchains from eb and defined them in buildtest. Any app
built with the any of the toolchains can be used with buildtest to generate
tests.

.. program-output:: head -n 15 scripts/List_Subcommand/toolchain.txt


Software Version Relationship (``buildtest list -svr``)
---------------------------------------------------------------

If you want to view a breakdown of all software by version and full path to modulefile
then you want to use ``buildtest list --software-version-relation`` or short option
``buildtest list -svr``

The output will be sorted by software and each entry will correspond to the full path of the modulefile.

.. program-output:: head -n 15 scripts/List_Subcommand/software_version.txt

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

.. program-output:: head -n 15 scripts/List_Subcommand/easyconfigs.txt

If an easyconfig is not found you may get the following message

::

    Could not find easyconfig in /clust/app/easybuild/2018/IvyBridge/redhat/7.3/software/NWChem/6.8.revision47-intel-2018a-2017-12-14-Python-2.7.14/easybuild

Listing buildtest software (``buildtest list --buildtest-software``)
----------------------------------------------------------------------

buildtest can report the software packages supported by buildtest which are found in
BUILDTEST_CONFIGS_REPO

.. program-output:: head -n 15 scripts/List_Subcommand/buildtest_software.txt


Formatting output (``buildtest list --format``)
------------------------------------------------------

buildtest provides ``--format`` option to control output behavior of ``buildtest list``.
You may let buildtest output to standard output which is the default behavior if
you select ``--format=stdout``.

buildtest also supports json and csv output, where ``--format=json`` and ``--format=csv``
will output result in json or csv format.

Let's run ``buildtest list -ls --format=stdout``

.. program-output:: cat scripts/List_Subcommand/software_format_stdout.txt

buildtest will write content of csv to file. Let's run ``buildtest list -svr --format=csv``

.. program-output:: cat scripts/List_Subcommand/software_format_csv.txt

.. program-output:: head scripts/List_Subcommand/software_list.csv

To print output in json let's run ``buildtest list -ls --format=json``

.. program-output:: cat scripts/List_Subcommand/software_format_json.txt
