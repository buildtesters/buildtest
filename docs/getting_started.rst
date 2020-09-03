.. _Getting Started:

Getting Started with buildtest
==============================

Interacting with the client
---------------------------

After you install buildtest, you should find the client on your path::


      $ which buildtest
      ~/.local/bin/buildtest

If you don't see buildtest go back and review section :ref:`Setup`.

Buildspecs
------------

.. _find_buildspecs:

Finding Buildspecs
~~~~~~~~~~~~~~~~~~~~

buildtest is able to find and validate all buildspecs in your repos. The
command ``buildtest buildspec`` comes with the following options.

.. program-output:: cat docgen/buildtest_buildspec_--help.txt

To find all buildspecs run ``buildtest buildspec find`` which will discover
all buildspecs in all repos. buildtest will recursively traverse all repos
and seek out all `.yml` extensions so make sure your buildspecs conform to
the file extension.


.. program-output:: cat docgen/getting_started/buildspec-find.txt

buildtest will find all buildspecs and validate each file with the appropriate
schema type. buildspecs that pass validation will be displayed on screen.
buildtest will report all invalid buildspecs in a text file for you to review.

buildtest will cache the results in **var/buildspec-cache.json** so subsequent
runs to ``buildtest buildspec find`` will be much faster since we read from cache.
If you make changes to buildspec you may want to rebuild cache using ``buildtest buildspec find --clear``.


Viewing Buildspecs
~~~~~~~~~~~~~~~~~~~~
If you want to view or edit a buildspec you can type the name of test. Since we
can have more than one test in a buildspec, opening any of the `name` entry
that map to same file will result in same operation.

For example, we can view ``systemd_default_target`` as follows

.. program-output:: cat docgen/getting_started/buildspec-view.txt

Editing Buildspecs
~~~~~~~~~~~~~~~~~~~~

To edit a buildspec you can run ``buildtest buildspec edit <name>`` which
will open file in editor. Once you make change, buildtest will validate the
buildspec upon closure, if there is an issue buildtest will report an error
during validation and you will be prompted to fix issue until it is resolved.

For example we can see an output message after editing file, user will be prompted
to press a key which will open the file in editor::

    $ buildtest buildspec edit systemd_default_target
    version 1.1 is not known for type {'1.0': 'script-v1.0.schema.json', 'latest': 'script-v1.0.schema.json'}. Try using latest.
    Press any key to continue

Build Usage
------------

The ``buildtest build`` command is used for building and running tests. Buildtest will read one or more Buildspecs (YAML)
file that adheres to one of the buildtest schemas. For a complete list of build options, run ``buildtest build --help``

.. program-output:: cat docgen/buildtest_build_--help.txt

.. _discover_buildspecs:

Discover Buildspecs
--------------------

The buildspec search resolution is described as follows:

- If file doesn't exist, check for file in :ref:`buildspec_roots` and break after first match

- If buildspec path is a directory, traverse directory recursively to find all ``.yml`` extensions

- If buildspec path is a file, check if file extension is not ``.yml``,  exit immediately

Shown below is a diagram on how buildtest discovers buildspecs. The user
inputs a buildspec via ``--buildspec`` or tags (``--tags``) :ref:`build_by_tags`
which will discover the buildspecs. User can :ref:`exclude_buildspecs`
using ``--exclude`` option which is processed after discovering buildspecs. The
excluded buildspecs are removed from list if found and final list of buildspecs
is processed.

.. image:: _static/DiscoverBuildspecs.jpg

Building a Test
----------------

To build a test, we use the ``--buildspec`` or short option ``-b`` to specify the
path to Buildspec file.


Let's see some examples, first we specify a full path to buildspec file

.. program-output:: cat docgen/getting_started/buildspec-abspath.txt

buildtest won't accept ``.yaml`` file extension for file, this can be demonstrated as
follows::

    $ buildtest build -b tests/examples/buildspecs/os.yaml
    Paths:
    __________
    Prefix: /private/tmp
    Buildspec Search Path: ['/Users/siddiq90/.buildtest/site']
    Test Directory: /private/tmp/tests
    tests/examples/buildspecs/os.yaml does not end in file extension .yml

buildtest can perform a directory build for instance let's build
for directory ``tests/examples/buildspecs`` where buildtest will recursively
search for all ``.yml`` files

.. program-output:: cat docgen/getting_started/buildspec-directory.txt

In next section, you will see, we can build multiple buildspecs and interchange
file and directory with ``-b`` option.


Building Multiple Buildspecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Buildtest supports building multiple buildspecs, just specify the ``-b`` option
for every Buildspec you want to build. In this example, we specify a file and
directory path. The search resolution is performed for every argument (``-b``)
independently, and accumulated into list.

.. program-output:: cat docgen/getting_started/multi-buildspecs.txt

.. _exclude_buildspecs:

Excluding Buildspecs
~~~~~~~~~~~~~~~~~~~~~

Buildtest provides ``--exclude`` option or short option ``-x`` to exclude
buildspecs which can be useful when you want to build all buildspecs in a directory
but exclude a few buildspecs or exclude a sub-directory.

For example we can build all buildspecs in ``examples`` but exclude file ``examples/systemd.yml``
by running::

    $ buildtest build -b examples -x examples/systemd.yml

buildtest will discover all Buildspecs and then exclude any buildspecs specified
by ``-x`` option. You can specify ``-x`` multiple times just like ``-b`` option.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows::

    $ buildtest build -b examples/ -x examples/
    There are no Buildspec files to process.

Buildtest will stop immediately if there are no Buildspecs to process, this is
true if you were to specify files instead of directory.

.. _build_by_tags:

Building By Tags
~~~~~~~~~~~~~~~~~

buildtest can perform builds by tags by using ``--tags`` option. In order to use this
feature, buildspecs must be in cache so you must run ``buildtest buildspec find``
or see :ref:`find_buildspecs`.

To build all tutorials tests you can perform ``buildtest build --tags tutorials``.
In the buildspec there is a field ``tags: [tutorials]`` to classify tests.
buildtest will read the cache file ``var/buildspec-cache.json`` and see which
buildspecs have a matching tag. You should run ``buildtest buildspec find``
atleast once, in order to detect cache file.

.. program-output::  cat docgen/getting_started/tags.txt

.. _invalid_buildspecs:

Control builds by Stages
-------------------------

You can control behavior of ``buildtest build`` command to stop at certain point
using ``--stage`` option. This takes two values ``parse`` or ``build``, which will
stop buildtest after parsing buildspecs or building the test content.

If you want to know your buildspecs are valid you can use ``--stage=parse`` to stop
after parsing the buildspec. Shown below is an example build where we stop
after parse stage.

.. program-output:: cat docgen/getting_started/stage_parse.txt

Likewise, if you want to troubleshoot your test script without running them you can
use ``--stage=build`` which will stop after building your test script. This can
be extremely useful when writing your buildspecs and not having to run your tests.
In this next example, we stop our after the build stage using ``--stage=build``.

.. program-output:: cat docgen/getting_started/stage_build.txt

Invalid Buildspecs
~~~~~~~~~~~~~~~~~~~~

buildtest will skip any buildspecs that fail to validate, in that case
the test script will not be generated. Here is an example where we have an invalid
buildspec.

.. program-output:: cat docgen/getting_started/invalid-buildspec.txt

buildtest may skip tests from running if buildspec specifies an invalid
executor name since buildtest needs to know this in order to delegate test
to Executor class responsible for running the test. Here is an example
where test failed to run since we provided invalid executor.

.. program-output:: cat docgen/getting_started/invalid-executor.txt

Buildtest Report
-----------------

The ``buildtest report`` command will show result of all tests in a tabular
form. Shown below is an example

.. program-output:: cat docgen/report.txt

buildtest will store result metadata of each test in a file ``var/report.json`` which
is found in root of buildtest. This file is updated upon every ``buildtest build`` command.
For more information see :ref:`test_reports`.

Debug Mode
------------

buildtest can stream logs to ``stdout`` stream for debugging. You can use ``buildtest -d <DEBUGLEVEL>``
or long option ``--debug`` with any buildtest commands. The DEBUGLEVEL are:
``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``,  ``CRITICAL`` which controls
log level to be displayed in console. buildtest is using
`logging.setLevel <https://docs.python.org/3/library/logging.html#logging.Logger.setLevel>`_
to control log level.

The same content is logged in **buildtest.log** with default log level of ``DEBUG``.
If you want to get all logs use ``-d DEBUG`` with your buildtest command::

    buildtest -d DEBUG <command>

Logfile
-------

Currently, buildtest will write the log file for any ``buildtest build`` command
in ``buildtest.log`` of the current directory. The logfile will be overwritten
if you run repeative commands from same directory. A permanent log file location
will be implemented (TBD).
