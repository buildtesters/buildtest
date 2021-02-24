
Buildspecs Interface
======================

Now that we learned how to build tests, in this section we will discuss how one can
query a buildspec cache. In buildtest, one can load all buildspecs which is equivalent
to validating all buildspecs with the appropriate schema. Buildtest will ignore all
invalid buildspecs and store them in a separate file.

The ``buildtest buildspec find`` command is used for finding buildspecs from buildspec
cache. This command is also used for generating the buildspec cache. Shown below is a list of options for
``buildtest buildspec find``.

.. program-output:: cat docgen/buildtest_buildspec_find_--help.txt

.. _find_buildspecs:

Finding Buildspecs
--------------------

To find all buildspecs run ``buildtest buildspec find`` which will discover
all buildspecs in all repos by recursively finding all `.yml` extensions.

.. program-output:: cat docgen/getting_started/buildspec-find.txt

buildtest will validate each buildspec file with the appropriate
schema type. buildspecs that pass validation will be displayed on screen.
buildtest will report all invalid buildspecs in a text file for you to review.

buildtest will cache the results in **var/buildspec-cache.json** so subsequent
runs to ``buildtest buildspec find`` will be much faster because it is read from cache.
If you make changes to buildspec you may want to rebuild the buildspec cache then
run::

  $ buildtest buildspec find --rebuild

If you want to find all buildspec files in cache run ``buildtest buildspec find --buildspec-files``

.. program-output:: cat docgen/buildspec_find_buildspecfiles.txt
     :ellipsis: 30

If you want to find root directories of buildspecs loaded in buildspec cache use the
``buildtest buildspec find --paths`` option.

::

    $ buildtest buildspec find --paths
    /Users/siddiq90/Documents/buildtest/tutorials
    /Users/siddiq90/Documents/buildtest/general_tests


buildtest will search buildspecs in :ref:`buildspecs root <buildspec_roots>` defined in your configuration,
which is a list of directory paths to search for buildspecs.
If you want to load buildspecs from a directory path, one can run specify a directory
path via ``--root`` such as ``buildtest buildspec find --root <path> --rebuild``.
buildtest will load all valid buildspecs into cache and ignore
the rest. It's important to add ``--rebuild`` if you want to regenerate buildspec cache.

Filtering buildspec
--------------------

Once you have a buildspec cache, we can query the buildspec cache for certain attributes.
When you run **buildtest buildspec find** it will report all buildspecs from cache which can
be difficult to process. Therefore, we have a filter option (``--filter``) to restrict our search.
Let's take a look at the available filter fields that are acceptable with filter option.

.. program-output:: cat docgen/buildspec-filter.txt

The ``--filter`` option expects arguments in **key=value** format as follows::

    buildtest buildspec find --filter key1=value1,key2=value2,key3=value3

We can filter buildspec cache by ``tags=fail`` which will query all tests with
associated tag field in test.

.. program-output:: cat docgen/buildspec_filter_tags.txt

In addition, we can query buildspecs by schema type using ``type`` property. In this
example we query all tests by `type` property

.. program-output:: cat docgen/buildspec_filter_type.txt
   :ellipsis: 20

Finally, we can combine multiple filter fields separated by comma, in the next example
we query all buildspecs with ``tags=tutorials``, ``executor=local.sh``, and ``type=script``

.. program-output:: cat docgen/buildspec_multifield_filter.txt


Format buildspec cache
-----------------------

We have seen how one can filter buildspecs, but we can also configure which columns to display
in the output of **buildtest buildspec find**. By default, we show few format fields
in the output, however there are more format fields hidden from the default output.

The format fields are specified comma separated using format: ``--format <field1>,<field2>,...``.
You can see a list of all format fields by ``--helpformat`` option as shown below

.. program-output:: cat docgen/buildspec-format.txt


In the next example, we utilize ``--format`` field with ``--filter`` option to show
how format fields affect table columns. buildtest will display the table in order of
format fields specified in command line.

.. program-output:: cat docgen/buildspec_format_example.txt

buildtest makes use of python library named `tabulate <https://pypi.org/project/tabulate/>`_
to generate these tables which are found in commands line like ``buildtest buildspec find``
and ``buildtest report``.

.. _buildspec_tags:

Querying buildspec tags
------------------------

If you want to retrieve all unique tags from all buildspecs you can run
``buildtest buildspec find --tags``. This can be useful if you want to know available
tags in your buildspec cache.

.. program-output:: cat docgen/buildspec_find_tags.txt

In addition, buildtest can group tests by tags via ``buildtest buildspec find --group-by-tags``
which can be useful if you want to know which tests get executed when running ``buildtest build --tags``.
The output is grouped by tag names, followed by name of test and description.

.. program-output:: cat docgen/buildspec_find_group_by_tags.txt


.. _buildspec_executor:

Querying buildspec executor
---------------------------

If you want to know all executors in your buildspec cache use the
``buildtest buildspec find --list-executors`` command. This can be useful when
you want to build by executors (``buildtest build --executor``).

.. program-output:: cat docgen/buildspec_find_executors.txt

Similar to ``--group-by-tags``, buildtest has an option to group tests by executor
using ``--group-by-executor`` option. This will show tests grouped by executor,
name of test and test description. Shown below is an example output.

.. program-output:: cat docgen/buildspec_find_group_by_executor.txt


Query Maintainers in buildspecs
--------------------------------

The ``maintainers`` field can be used for identifying author for buildspec
file which can be useful if you want to find out who is responsible for the test.
You can retrieve all buildspec maintainers using ``--maintainers`` option or ``-m``
short option. The command below will show all maintainers for buildspecs in buildspec
cache

.. program-output:: cat docgen/buildspec_find_maintainers.txt


If you want to see a breakdown of maintainers by buildspec file you can use ``--maintainers-by-buildspecs``
or ``-mb`` short option. This can be useful when tracking maintainers by buildspec files.

.. program-output:: cat docgen/buildspec_find_maintainers_by_buildspecs.txt

