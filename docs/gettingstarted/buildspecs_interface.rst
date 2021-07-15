.. _buildspec_interface:

Buildspecs Interface
======================

Now that we learned how to build tests, in this section we will discuss how one can
query a buildspec cache. In buildtest, one can load all buildspecs which is equivalent
to validating all buildspecs with the appropriate schema. Buildtest will ignore all
invalid buildspecs and store them in a separate file.

The ``buildtest buildspec find`` command is used for finding buildspecs from buildspec
cache. This command is also used for generating the buildspec cache. Shown below is a list of options for
``buildtest buildspec find``.

.. command-output:: buildtest buildspec find --help

.. _find_buildspecs:

Finding Buildspecs
--------------------

To find all buildspecs you can run ``buildtest buildspec find`` which will discover
all buildspecs by recursively searching all `.yml` extensions. buildtest will validate each
buildspec file with the json schema and buildtest will display all valid buildspecs in the output,
all invalid buildspecs will be stored in a file for post-processing.

.. command-output:: buildtest buildspec find

buildtest will load all discovered buildspecs in a cache file (JSON) which is created upon
running ``buildtest buildspec find``. Any subsequent runs will read from cache and update
if any new buildspecs are added. If you make changes to buildspec you should rebuild the
buildspec cache by running::

  $ buildtest buildspec find --rebuild

If you want to find all buildspec files in cache you can run ``buildtest buildspec find --buildspec``.
Shown below is an example output.

.. command-output:: buildtest buildspec find --buildspec
   :ellipsis: 11

The ``buildtest buildspec find --paths`` will display a list of root directories buildtest will search for
buildspecs when runninh ``buildtest buildspec find``. One can define these directories in the configuration file
or pass them via command line.

.. command-output:: buildtest buildspec find --paths

buildtest will search buildspecs in :ref:`buildspecs root <buildspec_roots>` defined in your configuration,
which is a list of directory paths to search for buildspecs.
If you want to load buildspecs from a directory path, you can specify a directory
via ``--root`` option in the format: ``buildtest buildspec find --root <path> --rebuild``.
buildtest will load all valid buildspecs into cache and ignore
the rest. It's important to add ``--rebuild`` if you want to regenerate buildspec cache.

Filtering buildspec
~~~~~~~~~~~~~~~~~~~~

Once you have a buildspec cache, we can query the buildspec cache for certain attributes.
When you run **buildtest buildspec find** it will report all buildspecs from cache which can
be difficult to process. Therefore, we have a filter option (``--filter``) to restrict our search.
Let's take a look at the available filter fields that are acceptable with filter option.

.. command-output:: buildtest buildspec find --helpfilter

The ``--filter`` option expects an arguments in **key=value** format as follows::

    buildtest buildspec find --filter key1=value1,key2=value2,key3=value3

We can filter buildspec cache by ``tags=fail`` which will query all tests with
associated tag field in test.

.. command-output:: buildtest buildspec find --filter tags=fail

In addition, we can query buildspecs by schema type using ``type`` property. In this
example we query all tests by **type** property

.. command-output:: buildtest buildspec find --filter type=script
    :ellipsis: 21

Finally, we can combine multiple filter fields separated by comma, in the next example
we can query all buildspecs with ``tags=tutorials``, ``executor=generic.local.sh``, and ``type=script``

.. command-output:: buildtest buildspec find --filter tags=tutorials,executor=generic.local.sh,type=script

We can filter output of buildspec cache by buildspec using ``--filter buildspec=<path>`` which
expects a path to buildspec file.  The buildspec must be in the cache and file path must exist in order to
fetch the result. The path can be absolute or relative path.

In this next example, we will filter cache by file `tutorials/pass_returncode.yml` and use ``--format name,buildspec``
to format columns. The ``--format buildspec`` will show full path to buildspec and ``name`` refers to name of test.
For more details on **--format** see :ref:`format_buildspec`.

.. command-output:: buildtest buildspec find --filter buildspec=tutorials/pass_returncode.yml --format name,buildspec

.. _format_buildspec:

Format buildspec cache
~~~~~~~~~~~~~~~~~~~~~~~

We have seen how one can filter buildspecs, but we can also configure which columns to display
in the output of **buildtest buildspec find**. By default, we show a pre-selected format fields
in the output, however there are more format fields available that can be configured at the command line.

The format fields are specified in comma separated format such as ``buildtest buildspec find --format <field1>,<field2>,...``.
You can see a list of all format fields by ``--helpformat`` option as shown below

.. command-output:: buildtest buildspec find --helpformat

In the next example, we utilize ``--format`` field with ``--filter`` option to show
how format fields affect table columns. buildtest will display the table in order of
format fields specified in command line.

.. command-output:: buildtest buildspec find --format name,description,buildspec --filter tags=tutorials,executor=generic.local.sh

buildtest makes use of python library named `tabulate <https://pypi.org/project/tabulate/>`_
to generate these tables which are found in commands line like ``buildtest buildspec find``
and ``buildtest report``.

.. _buildspec_tags:

Querying buildspec tags
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to retrieve all unique tags from all buildspecs you can run
``buildtest buildspec find --tags``. This can be useful if you want to know available
tags in your buildspec cache.

.. command-output:: buildtest buildspec find --tags

In addition, buildtest can group tests by tags via ``buildtest buildspec find --group-by-tags``
which can be useful if you want to know which tests get executed when running ``buildtest build --tags``.
The output is grouped by tag names, followed by name of test and description.

.. command-output:: buildtest buildspec find --group-by-tags
   :ellipsis: 41

.. _buildspec_executor:

Querying buildspec executor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to know all executors in your buildspec cache use the
``buildtest buildspec find --executors`` command. This can be useful when
you want to build by executors (``buildtest build --executor``).

.. command-output:: buildtest buildspec find --executors

Similar to ``--group-by-tags``, buildtest has an option to group tests by executor
using ``--group-by-executor`` option. This will show tests grouped by executor,
name of test and test description. Shown below is an example output.

.. command-output:: buildtest buildspec find --group-by-executor
    :ellipsis: 31


Query Maintainers in buildspecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you are writing your buildspecs, you can specify the ``maintainers`` field to assign
authors to buildspecs. buildtest can query the maintainers from the cache
once buildspecs are loaded. You can retrieve all maintainers using ``--maintainers`` option or ``-m``
short option. In this example, we show all maintainers for buildspecs in buildspec
cache

.. command-output:: buildtest buildspec find --maintainers

If you want to see a breakdown of maintainers by buildspec file you can use ``--maintainers-by-buildspecs``
or ``-mb`` short option. This can be useful to get correlation between maintainers and the buildspec file.

.. command-output:: buildtest buildspec find -mb


Validate Buildspecs
---------------------

buildtest can validate buildspecs through the ``buildtest buildspec validate`` command which provides
analogous options for ``buildtest build`` for selecting buildspecs such as ``-b``, ``-e``, ``-t`` and ``-e``.
This command can be used to validate buildspecs with the JSON Schema which can be useful if you are writing a buildspec
and want to validate the buildspec without running the test.

Shown below are the available command options.

.. command-output:: buildtest buildspec validate --help

The `-b` option can be used to specify path to buildspec file or directory to validate buildspecs. If its a directory,
buildtest will traverse all directories recursively and find any **.yml** file extensions and attempt to validate each buildspec.
Shown below is an example output of what it may look like

.. command-output:: buildtest buildspec validate -b tutorials/vars.yml

If buildtest detects an error during validation, the error message will be displayed to screen as we see in this example

.. command-output:: buildtest buildspec validate -b tutorials/invalid_tags.yml

Similarly we can search buildspecs based on tags if you want to validate a group of buildspecs using the ``-t`` option. We can
append ``-t`` option multiple times to search by multiple tag names. In this next example, we
will validate all buildspecs for **python** and **pass** tags.

.. command-output:: buildtest buildspec validate -t python -t pass

Finally we can also search by executors using the ``-e`` option which can be appended to search by
multiple executors.

.. command-output:: buildtest buildspec validate -e generic.local.csh
