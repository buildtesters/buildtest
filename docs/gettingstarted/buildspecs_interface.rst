.. _buildspec_interface:

Buildspecs Interface
======================

Now that we learned how to build tests, in this section we will discuss how one can
query a buildspec cache. In buildtest, one can load all buildspecs which is equivalent
to validating all buildspecs with the appropriate schema. Buildtest will ignore all
invalid buildspecs and store them in a separate file.

.. note::
   ``buildtest bc`` is an alias for ``buildtest buildspec`` command.

.. _find_buildspecs:

Finding Buildspecs - ``buildtest buildspec find``
--------------------------------------------------

The ``buildtest buildspec find`` command is used for finding buildspecs from buildspec
cache. This command is also used for generating the buildspec cache. Shown below is a list of options for
provided for this command.

.. command-output:: buildtest buildspec find --help

The ``buildtest buildspec find`` command will discover all buildspecs by recursively searching all `.yml` extensions.
buildtest will validate each buildspec file with the json schema and buildtest will display all valid buildspecs in the output,
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

In this next example, we will filter cache by file `tutorials/test_status/pass_returncode.yml` and use ``--format name,buildspec``
to format columns. The ``--format buildspec`` will show full path to buildspec and ``name`` refers to name of test.
For more details on **--format** see :ref:`format_buildspec`.

.. command-output:: buildtest buildspec find --filter buildspec=tutorials/test_status/pass_returncode.yml --format name,buildspec

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

Terse Output
~~~~~~~~~~~~~

You can use the ``--terse`` option to print output of ``buildtest buildspec find`` in terse format that can
be useful if you want to parse content of file. In example below, we will print output of tags in terse format, the
first entry ``tags`` is the header followed by list of unique tags.  The ``--no-header`` option
can be used to disable printing of header title.

.. command-output:: buildtest buildspec find -t --terse


Invalid Buildspecs - ``buildtest buildspec find invalid``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest will store invalid buildspecs in the cache file which can be retrieved using ``buildtest buildspec find invalid``. buildtest
will attempt to parse each buildspec and store error message for every buildspec. If you run without any options it will
report a list of invalid buildspecs as shown below

.. command-output:: buildtest buildspec find invalid

If you want to see error messages for each buildspec you can pass the ``-e`` or ``--error`` option which will display output of
each buildspec followed by error message.

.. command-output:: buildtest buildspec find invalid -e

.. _buildspec_maintainers:

Query Maintainers (``buildtest buildspec maintainers``)
----------------------------------------------------------

buildtest keeps track of maintainers (i.e authors) for a given buildspec provided that you
specify the ``maintainers`` property. This is stored in the buildspec cache which can be used
to query some interesting details.

Shown below is the help for ``buildtest buildspec maintainers --help``

.. command-output:: buildtest buildspec maintainers --help

If you want to see a listing of all maintainers you can use the ``--list`` as shown below

.. command-output:: buildtest buildspec maintainers --list

If you prefer a machine readable format, then you can use ``--terse`` and ``--no-header``.

.. command-output:: buildtest buildspec maintainers --list --terse --no-header

If you want to see a breakdown of all buildspecs by maintainers you can use `--breakdown` which will
display the following information

.. command-output:: buildtest buildspec maintainers --breakdown

The ``buildtest buildspec maintainers find`` command can be used to report buildspec given a maintainer
name which works similar to `--breakdown` but doesn't report information for all maintainers. Shown
below, we query all buildspecs by maintainer **@shahzebsiddiqui**

.. command-output:: buildtest buildspec maintainers find @shahzebsiddiqui


Cache Summary - ``buildtest buildspec summary``
------------------------------------------------

The ``buildtest buildspec summary`` command can be used to provide a summary of the buildspec cache. This command
can be used assuming your cache is built via ``buildtest buildspec find``. Shown below is a summary of the cache file.

.. command-output:: buildtest buildspec summary


Validate Buildspecs - ``buildtest buildspec validate``
--------------------------------------------------------

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

Show buildspec ``buildtest buildspec show``
--------------------------------------------

buildtest can display content of buildspec file given a test name via ``buildtest buildspec show`` command which expects a
positional argument that is the name of test. This can be quick way to see content of buildspec without remembering the full path
to the buildspec.

In this next example, we will instruct buildtest to show content of buildspec for test name `python_hello`.

.. command-output:: buildtest buildspec show python_hello

You can pass multiple arguments to ``buildtest buildspec show`` to show content of each test

.. command-output:: buildtest buildspec show python_hello circle_area


There is bash completion for this command which will show list of test names available in the cache assuming you have run
``buildtest buildspec find``. If you specify an invalid test name you will get an error followed by list of tests that are available
in the cache

.. command-output:: buildtest buildspec show XYZ123!
   :returncode: 1


Let's assume you want to see content of all buildspec that failed test, you can use ``buildtest report`` to extract list of test names
that failed as argument to ``buildtest buildspec show``, for instance we see below we have two tests that failed, using ``--filter state=FAIL`` will
retrieve all failures, you will want to pipe output to **uniq** to get unique listing since output of ``buildtest report`` will show all test runs and
duplicates can occur if same test is run multiple times.

.. code-block:: console

    $ buildtest report --filter state=FAIL --format name --terse --no-header | uniq
    exit1_fail
    returncode_list_mismatch

Next you can use this as argument to ``buildtest buildspec show`` and it will report all buildspec files that correspond to test that failed.

.. code-block:: console

    $ buildtest buildspec show $(buildtest report --filter state=FAIL --format name --terse --no-header | uniq)
    ────────────────────────────────────────────────────────────────────────────── /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/test_status/pass_returncode.yml ───────────────────────────────────────────────────────────────────────────────
    ╭──────────────────────────────────────────────────────────────────────╮
    │ buildspecs:                                                          │
    │                                                                      │
    │   exit1_fail:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 1 by default is FAIL                           │
    │     tags:                                                            │
    │     run: exit 1                                                      │
    │                                                                      │
    │   exit1_pass:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: report exit 1 as PASS                               │
    │     run: exit 1                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1]                                                │
    │                                                                      │
    │   returncode_list_mismatch:                                          │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 2 failed since it failed to match returncode 1 │
    │     run: exit 2                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1, 3]                                             │
    │                                                                      │
    │   returncode_int_match:                                              │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 128 matches returncode 128                     │
    │     run: exit 128                                                    │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: 128                                                │
    │                                                                      │
    ╰──────────────────────────────────────────────────────────────────────╯
    ────────────────────────────────────────────────────────────────────────────── /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/test_status/pass_returncode.yml ───────────────────────────────────────────────────────────────────────────────
    ╭──────────────────────────────────────────────────────────────────────╮
    │ buildspecs:                                                          │
    │                                                                      │
    │   exit1_fail:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 1 by default is FAIL                           │
    │     tags:                                                            │
    │     run: exit 1                                                      │
    │                                                                      │
    │   exit1_pass:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: report exit 1 as PASS                               │
    │     run: exit 1                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1]                                                │
    │                                                                      │
    │   returncode_list_mismatch:                                          │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 2 failed since it failed to match returncode 1 │
    │     run: exit 2                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1, 3]                                             │
    │                                                                      │
    │   returncode_int_match:                                              │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 128 matches returncode 128                     │
    │     run: exit 128                                                    │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: 128                                                │
    │                                                                      │
    ╰──────────────────────────────────────────────────────────────────────╯

Show buildspec ``buildtest buildspec show-fail``
-------------------------------------------------

buildtest can display content of buildspec file of all failed tests via ``buildtest buildspec show-fail`` command. 
This can be quick way to see content of buildspec files that correspond to test that failed.

.. code-block:: console

    $ buildtest buildspec show-fail
    ────────────────────────────────────────────────────────────────────────────── /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/test_status/pass_returncode.yml ───────────────────────────────────────────────────────────────────────────────
    ╭──────────────────────────────────────────────────────────────────────╮
    │ buildspecs:                                                          │
    │                                                                      │
    │   exit1_fail:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 1 by default is FAIL                           │
    │     tags:                                                            │
    │     run: exit 1                                                      │
    │                                                                      │
    │   exit1_pass:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: report exit 1 as PASS                               │
    │     run: exit 1                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1]                                                │
    │                                                                      │
    │   returncode_list_mismatch:                                          │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 2 failed since it failed to match returncode 1 │
    │     run: exit 2                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1, 3]                                             │
    │                                                                      │
    │   returncode_int_match:                                              │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 128 matches returncode 128                     │
    │     run: exit 128                                                    │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: 128                                                │
    │                                                                      │
    ╰──────────────────────────────────────────────────────────────────────╯
    ────────────────────────────────────────────────────────────────────────────── /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/test_status/pass_returncode.yml ───────────────────────────────────────────────────────────────────────────────
    ╭──────────────────────────────────────────────────────────────────────╮
    │ buildspecs:                                                          │
    │                                                                      │
    │   exit1_fail:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 1 by default is FAIL                           │
    │     tags:                                                            │
    │     run: exit 1                                                      │
    │                                                                      │
    │   exit1_pass:                                                        │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: report exit 1 as PASS                               │
    │     run: exit 1                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1]                                                │
    │                                                                      │
    │   returncode_list_mismatch:                                          │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 2 failed since it failed to match returncode 1 │
    │     run: exit 2                                                      │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: [1, 3]                                             │
    │                                                                      │
    │   returncode_int_match:                                              │
    │     executor: generic.local.bash                                     │
    │     type: script                                                     │
    │     description: exit 128 matches returncode 128                     │
    │     run: exit 128                                                    │
    │     tags:                                                            │
    │     status:                                                          │
    │       returncode: 128                                                │
    │                                                                      │
    ╰──────────────────────────────────────────────────────────────────────╯

Editing buildspecs in your preferred editor
--------------------------------------------

buildtest provides an interface to automatically open your buildspecs in editor and validate them after closing file.
You are welcome to open your buildspec in your editor (`vim`, `emacs`, `nano`) but you won't be able to validate the buildspec
unless you explicitly run the test or use **buildtest buildspec validate** to see if your buildspec is valid. buildtest comes
with two commands to edit your buildspecs ``buildtest buildspec edit-test`` and ``buildtest buildspec edit-file`` which we will
discuss below.

Editing by Test ``buildtest buildspec edit-test``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildtest buildspec edit-test`` allows one to specify a list of test as positional
arguments to edit-test in your preferred editor. buildtest will provide tab completion for this
command to show all test available in cache which works similar to ``buildtest buildspec show`` command.

For instance, we can see the following test are available as part of command completion

.. code-block:: console

    $ buildtest buildspec edit-test
    _bin_bash_shell                 download_stream                 nodes_state_down                show_host_groups                string_tag
    _bin_sh_shell                   executor_regex_script_schema    nodes_state_idle                show_jobs                       systemd_default_target
    add_numbers                     executors_sbatch_declaration    nodes_state_reboot              show_lsf_configuration          tcsh_env_declaration
    always_fail                     executors_vars_env_declaration  pullImage_dockerhub             show_lsf_models                 test_fail_returncode_match
    always_pass                     exit1_fail                      pullImage_shub                  show_lsf_queues                 test_pass_returncode_mismatch
    bash_env_variables              exit1_pass                      pullImage_sylabscloud           show_lsf_queues_current_user    timelimit_max
    bash_login_shebang              foo_bar                         python_hello                    show_lsf_queues_formatted       timelimit_max_fail
    bash_nonlogin_shebang           gcc_version                     qdel_version                    show_lsf_resources              timelimit_min
    bash_shell                      get_partitions                  qmove_version                   show_lsf_user_groups            timelimit_min_fail
    bhosts_version                  hello_world                     qselect_version                 show_partition                  timelimit_min_max
    build_remoteimages              inspect_image                   qsub_version                    show_qos                        ulimit_cputime_unlimited
    build_sandbox_image             jobA                            returncode_int_match            show_queues                     ulimit_filedescriptor_4096
    build_sif_from_dockerimage      jobB                            returncode_list_mismatch        show_tres                       ulimit_filelock_unlimited
    circle_area                     jobC                            root_disk_usage                 show_users                      ulimit_max_user_process_2048
    cqsub_version                   kernel_swapusage                runImage                        sinfo_version                   ulimit_stacksize_unlimited
    csh_env_declaration             list_of_strings_tags            run_stream                      skip                            ulimit_vmsize_unlimited
    csh_shell                       lsf_version                     selinux_disable                 sleep                           unskipped
    current_user_queue              metric_regex_example            sh_shell                        slurm_config                    variables_bash
    dead_nodes                      node_down_fail_list_reason      shell_options                   status_regex_fail
    display_hosts_format            nodes_state_allocated           show_accounts                   status_regex_pass
    display_lsf_hosts               nodes_state_completing          show_all_jobs                   status_returncode_by_executors

Let's take for instance we want to edit the following test, buildtest will search the buildspec cache and find the buildspec file, open
in editor and once changes are written to disk, the next file will be processed until all files are written to disk.

.. code-block:: console

    $ buildtest buildspec edit-test sleep _bin_bash_shell add_numbers
    Writing file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/sleep.yml
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/sleep.yml is valid
    Writing file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/shell_examples.yml
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/shell_examples.yml is valid
    Writing file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/add_numbers.yml
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/add_numbers.yml is valid

If you specify an invalid test, then buildtest will ignore the test and report a message and skip to next test as shown below

.. code-block:: console

    $ buildtest buildspec edit-test invalid_test sleep
    Unable to find test invalid_test in cache
    Writing file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/sleep.yml
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/sleep.yml is valid

Edit buildspecs ``buildtest buildspec edit-file``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildtest buildspec edit-file`` command can be used to edit buildspec based on filename as pose to testname.
This command works similar to ``buildtest buildspec edit-test`` where each file is open in editor and validated upon completion.
You can use this command to create new buildspec whereas ``buildtest buildspec edit-test`` only works on existing buildspecs loaded
in cache. You can pass multiple filenames as arguments if you want to edit several files.

.. code-block:: console

    $ buildtest buildspec edit-file $BUILDTEST_ROOT/tutorials/sleep.yml
      Writing file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/sleep.yml
      /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/sleep.yml is valid
