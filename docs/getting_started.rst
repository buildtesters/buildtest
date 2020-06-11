.. _Getting Started:

Getting Started with buildtest
==============================

Interacting with the client
---------------------------

After you install buildtest, you should find the client on your path::


      $ which buildtest
      ~/.local/bin/buildtest

If you don't see buildtest go back and review section :ref:`Setup`.

 - The test directory is where tests will be written, which defaults to ``$HOME/.buildtest/testdir``.
 - You can store tests (that can be referenced with relative paths) under ``$HOME/.buildtest/site``.


Cloning Tutorials
-----------------

To get started, let's clone the `tutorials <https://github.com/buildtesters/tutorials>`_ repository provided by buildtest
using ``buildtest repo add`` command::


    $ buildtest repo add https://github.com/buildtesters/tutorials.git
    Cloning into '/Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials'...
    remote: Enumerating objects: 106, done.
    remote: Counting objects: 100% (106/106), done.
    remote: Compressing objects: 100% (73/73), done.
    remote: Total 106 (delta 32), reused 97 (delta 25), pack-reused 0
    Receiving objects: 100% (106/106), 20.97 KiB | 5.24 MiB/s, done.
    Resolving deltas: 100% (32/32), done.

This is equivalent to doing this::

    $ mkdir -p $HOME/.buildtest/site/github.com/buildtesters
    $ git clone https://github.com/buildtesters/tutorials.git $HOME/.buildtest/site/github.com/buildtesters/tutorials

For more details see :ref:`buildtest_repo`

Buildspecs
------------

buildtest is able to find and validate all buildspecs in your repos. The
command ``buildtest buildspec`` comes with the following options.

.. program-output:: cat docgen/buildtest_buildspec_--help.txt

To find all buildspecs run ``buildtest buildspec find`` which will discover
all buildspecs in all repos. buildtest will recursively traverse all repos
and seek out all `.yml` extensions so make sure your buildspecs conform to
the file extension.

Shown below is an example output::

    $ buildtest buildspec find

    Detected 21 invalid buildspecs
    Writing invalid buildspecs to file: /Users/siddiq90/Documents/buildtest/docs/buildspec.error

    Name                      Type                      Buildspec
    ________________________________________________________________________________
    iris_user_query           script                    /private/tmp/github.com/buildtesters/buildtest-cori/nersctools/iris.yml
    iris_qos_gpu              script                    /private/tmp/github.com/buildtesters/buildtest-cori/nersctools/iris.yml
    iris_project              script                    /private/tmp/github.com/buildtesters/buildtest-cori/nersctools/iris.yml
    cray_check                script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/cray_env.yml
    nameserver_ping           script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    searchdomain_check        script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    mount_check               script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    filesystem_access         script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/filesystem.yml
    nerschost                 script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/nerschost.yml
    login_nodes               script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/ping_nodes.yml
    data_transfer_nodes       script                    /private/tmp/github.com/buildtesters/buildtest-cori/system/ping_nodes.yml

buildtest will find all buildspecs and validate each file with the appropriate
schema type. buildspecs that pass validation will be displayed on screen.
buildtest will report all invalid buildspecs in a text file for you to review.

If you want to view or edit a buildspec you can type the name of test. Since we
can have more than one test in a buildspec, opening any of the `name` entry
that map to same file will result in same operation.

For example, we can view ``nameserver_ping`` as follows::

   $ buildtest buildspec view nameserver_ping
    version: "1.0"
    nameserver_ping:
      executor: local.bash
      type: script
      description: "Ping nameservers by IP and resolved name"
      run: |
        ping -c 5 -W 60 128.55.146.10
        ping -c 5 -W 60 128.55.199.10
        ping -c 5 -W 60 ns3.nersc.gov
        ping -c 5 -W 60 ns4.nersc.gov

    searchdomain_check:
     executor: local.bash
     type: script
     description: "Check equality for search domain"
     run: |
       domain=`cat /etc/resolv.conf | grep -E "^(search nersc.gov)$"`
       echo $domain
     status:
       regex:
         stream: stdout
         exp: "^(search nersc.gov)$"

To edit a buildspec you can run ``buildtest buildspec edit <name>`` which
will open file in editor. Once you make change, buildtest will validate the
buildspec upon closure, if there is an issue buildtest will report an error
during validation and you will be prompted to fix issue until it is resolved.

For example we can see an output message after editing file, user will be prompted
to press a key which will open the file in editor::

    $ buildtest buildspec edit nameserver_ping
    version 1.1 is not known for type {'1.0': 'script-v1.0.schema.json', 'latest': 'script-v1.0.schema.json'}. Try using latest.
    Press any key to continue

Build Usage
------------

The ``buildtest build`` command is used for building and running tests. Buildtest will read one or more Buildspecs (YAML)
file that adheres to one of the buildtest schemas. For a complete list of build options, run ``buildtest build --help``

.. program-output:: cat docgen/buildtest_build_--help.txt

Building a Test
----------------

To build a test, we use the ``-b`` to specify the the path to Buildspec file.
buildtest will discover the buildspecs specified by ``-b`` option, later you will
see you can provide more than one buildspec on the command line.

You can specify a full path to buildspec something like::

    buildtest build -b $HOME/.buildtest/github.com/buildtesters/tutorials/system/systemd.yml

Alternately, you can specify a relative path from your current directory. The same
test can be built if you change into directory and run as follows::

    cd $HOME/.buildtest/site/github.com/buildtesters/tutorials
    buildtest build -b system/systemd.yml

Here is an example build::

    $ buildtest build -b system/systemd.yml
    Paths:
    __________
    Prefix: None
    Test Directory: /private/tmp
    Search Path: ['/tmp']

    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials/system/systemd.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    Executor Name             TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    systemd                   script-v1.0.schema.json   local.bash                /private/tmp/systemd_default_target.sh   /Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials/system/systemd.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                           Section                        Status                         Buildspec Path
    ________________________________________________________________________________
    systemd                        systemd_default_target         FAIL                           /Users/siddiq90/.buildtest/site/github.com/buildtesters/tutorials/system/systemd.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 0/1 Percentage: 0.000%
    Failed Tests: 1/1 Percentage: 100.000%

Buildtest supports building multiple Buildspecs, just specify the ``-b`` option
for every Buildspec you want to build. For example let's build the following::

    $ buildtest build -b nerschost.yml -b mountpoint.yml
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Test Directory: /global/u1/s/siddiq90/cache/tests
    Search Path: []

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nerschost.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    Executor Name             TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    mountpoint                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/mount_check.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    nerschost                 script-v1.0.schema.json   local.python              /global/u1/s/siddiq90/cache/tests/nerschost.py /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nerschost.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                           Section                        Status                         Buildspec Path
    ________________________________________________________________________________
    mountpoint                     mount_check                    PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    nerschost                      nerschost                      PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nerschost.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 2 tests
    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%

buildtest can automatically detect Buildspecs based on filepath and directory so
if you know location to where Buildspecs are located you can specify a directory.
For instance, we can build all Buildspecs in a directory ``system`` as follows::

    $ buildtest build -b system/
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Test Directory: /global/u1/s/siddiq90/cache/tests
    Search Path: []

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/ping_nodes.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/cray_env.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nerschost.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/filesystem.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    Executor Name             TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    ping_nodes                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/login_nodes.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/ping_nodes.yml
    ping_nodes                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/data_transfer_nodes.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/ping_nodes.yml
    nameserver                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/nameserver_ping.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    nameserver                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/searchdomain_check.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    cray_env                  script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/cray_check.py /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/cray_env.yml
    nerschost                 script-v1.0.schema.json   local.python              /global/u1/s/siddiq90/cache/tests/nerschost.py /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nerschost.yml
    mountpoint                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/mount_check.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    filesystem                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/filesystem_access.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/filesystem.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                           Section                        Status                         Buildspec Path
    ________________________________________________________________________________
    ping_nodes                     login_nodes                    PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/ping_nodes.yml
    ping_nodes                     data_transfer_nodes            PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/ping_nodes.yml
    nameserver                     nameserver_ping                PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    nameserver                     searchdomain_check             PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    cray_env                       cray_check                     PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/cray_env.yml
    nerschost                      nerschost                      PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nerschost.yml
    mountpoint                     mount_check                    PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    filesystem                     filesystem_access              PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/filesystem.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 8 tests
    Passed Tests: 8/8 Percentage: 100.000%
    Failed Tests: 0/8 Percentage: 0.000%

Buildtest will recursively find all ``.yml`` files when you specify a directory
and process each Buildspec iteratively. You may mix file and directory with
``-b`` option to control what Buildspecs to build.

Buildtest provides ``-x`` option to exclude Buildspecs which can be useful when
you want to build in a directory and exclude a few files. For example we can do
the following to exclude ``mountpoint.yml`` but build all buildspecs
in ``system`` directory::

    $ buildtest build -b system -x system/mountpoint.yml

buildtest will discover all Buildspecs defined by ``-b`` option followed by
excluding tests that were discovered by option ``-x``. You can specify ``-x``
multiple times as you like to exclude a file or directory.

For example, we can undo discovery by passing same option to ``-b`` and ``-x``  as follows::

    $ buildtest build -b system/ -x system/
    There are no Buildspec files to process.

Buildtest will stop immediately if there are no Buildspecs to process, this is true if you were to specify files instead of
directory.

buildtest will skip any buildspecs that fail to validate, in that case
the test script will not be generated. Here is an example where only one buildspec
``system/mountpoint.yml`` was successfully built and run::

    $ buildtest build -b system/mountpoint.yml -b slurm/
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Test Directory: /global/u1/s/siddiq90/cache/tests
    Search Path: []

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/sacctmgr.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/squeue.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/slurm_check.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/partition.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/utils/sqs.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/sinfo.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/scontrol.yml
    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    Executor Name             TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    mountpoint                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/mount_check.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml
    Skipping /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/sacctmgr.yml since it failed to validate
    Skipping /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/squeue.yml since it failed to validate
    Skipping /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/slurm_check.yml since it failed to validate
    Skipping /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/partition.yml since it failed to validate
    Skipping /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/utils/sqs.yml since it failed to validate
    Skipping /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/sinfo.yml since it failed to validate
    Skipping /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/slurm/scontrol.yml since it failed to validate

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                           Section                        Status                         Buildspec Path
    ________________________________________________________________________________
    mountpoint                     mount_check                    PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/mountpoint.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%

buildtest may skip tests from running if buildspec specifies an invalid
executor name since buildtest needs to know this in order to delegate test
to Executor class responsible for running the test. Here is an example
where one of the test is skiped since ``local.bash1`` is not a valid executor::

    $ buildtest build -b system/nameserver.yml
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Test Directory: /global/u1/s/siddiq90/cache/tests
    Search Path: []

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    Executor Name             TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    nameserver                script-v1.0.schema.json   local.bash1               /global/u1/s/siddiq90/cache/tests/nameserver_ping.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml
    nameserver                script-v1.0.schema.json   local.bash                /global/u1/s/siddiq90/cache/tests/searchdomain_check.sh /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                           Section                        Status                         Buildspec Path
    ________________________________________________________________________________
    nameserver                     searchdomain_check             PASS                           /global/u1/s/siddiq90/cache/repos/github.com/buildtesters/buildtest-cori/system/nameserver.yml


    [nameserver]: executor local.bash1 is not defined in /global/homes/s/siddiq90/.buildtest/settings.yml



    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%
