Running Tests in Containers (Experimental)
==========================================

.. note::

        This feature is experimental and may change in future releases.

In this section, we will discuss how one can run tests in containers. Currently, we support running tests in the following container runtimes:
`docker <https://www.docker.com/>`_, `podman <https://podman.io/>`_ and `singularity <https://sylabs.io/docs/>`_.

Running Commands in Container
-----------------------------

Let's take a look at the following example, we will demonstrate how to run arbitrary Linux command inside a container.
The keyword ``container`` is used to specify the container settings, the ``platform`` will be used to determine the container runtime. This could
be ``docker``, ``podman`` or ``singularity``. The ``image`` is the name of the container image and ``command`` is the command you would like to run
inside the container.

.. literalinclude:: ../tutorials/containers/run_commands.yml
   :language: yaml
   :emphasize-lines: 6-9,20

We will be running ``cat /etc/os-release`` inside the ubuntu container which will show the operating system information. Next, we will ``ls`` on the same
file which we expect to fail, hence we will make this test pass by using ``|| true`` to ensure we have a zero returncode.

In our current system, we are running MacOS so we expect ``/etc/os-release`` will **not** be found. In the second test, we show how one can pass options to
``docker run`` using the ``options`` keyword. In this test, we will specify a custom hostname using ``--hostname`` option and run the **hostname** command in
the container.

Let's run the test and inspect the test results

.. dropdown:: buildtest build -b $BUILDTEST_ROOT/tutorials/containers/run_commands.yml

    .. code-block:: console

        ╭────────────────────────────────────────────────────────────────────────── buildtest summary ───────────────────────────────────────────────────────────────────────────╮
        │                                                                                                                                                                        │
        │ User:               siddiq90                                                                                                                                           │
        │ Hostname:           DOE-7086392                                                                                                                                        │
        │ Platform:           Darwin                                                                                                                                             │
        │ Current Time:       2023/10/13 11:04:09                                                                                                                                │
        │ buildtest path:     /Users/siddiq90/Documents/github/buildtest/bin/buildtest                                                                                           │
        │ buildtest version:  1.6                                                                                                                                                │
        │ python path:        /Users/siddiq90/.local/share/virtualenvs/buildtest-Ir4AdrfC/bin/python3                                                                            │
        │ python version:     3.10.12                                                                                                                                            │
        │ Configuration File: /Users/siddiq90/Documents/github/buildtest/buildtest/settings/config.yml                                                                           │
        │ Test Directory:     /Users/siddiq90/Documents/github/buildtest/var/tests                                                                                               │
        │ Report File:        /Users/siddiq90/Documents/github/buildtest/var/report.json                                                                                         │
        │ Command:            /Users/siddiq90/Documents/github/buildtest/bin/buildtest build -b /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_commands.yml │
        │                                                                                                                                                                        │
        ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ───────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────────────────────────────
                                       Discovered buildspecs
        ╔══════════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                        ║
        ╟──────────────────────────────────────────────────────────────────────────────────╢
        ║ /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_commands.yml ║
        ╚══════════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_commands.yml: VALID
        Total builder objects created: 2
                                                                                                               Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                            ┃ type   ┃ executor           ┃ compiler ┃ nodes ┃ procs ┃ description                                      ┃ buildspecs                                                                       ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ container_commands_ubuntu/80e076bc │ script │ generic.local.bash │ None     │ None  │ None  │ run arbitrary linux commands in ubuntu container │ /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_commands.yml │
        ├────────────────────────────────────┼────────┼────────────────────┼──────────┼───────┼───────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
        │ container_options/03ab5773         │ script │ generic.local.bash │ None     │ None  │ None  │ run arbitrary linux commands in ubuntu container │ /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_commands.yml │
        └────────────────────────────────────┴────────┴────────────────────┴──────────┴───────┴───────┴──────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────┘
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        container_commands_ubuntu/80e076bc: Creating test directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc
        container_commands_ubuntu/80e076bc: Creating the stage directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/stage
        container_commands_ubuntu/80e076bc: Writing build script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu_build.sh
        container_options/03ab5773: Creating test directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773
        container_options/03ab5773: Creating the stage directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/stage
        container_options/03ab5773: Writing build script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options_build.sh
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
        container_options/03ab5773 does not have any dependencies adding test to queue
        container_commands_ubuntu/80e076bc does not have any dependencies adding test to queue
               Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder                            ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ container_options/03ab5773         │
        │ container_commands_ubuntu/80e076bc │
        └────────────────────────────────────┘
        container_options/03ab5773: Current Working Directory : /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/stage
        container_options/03ab5773: Running Test via command: bash --norc --noprofile -eo pipefail container_options_build.sh
        container_options/03ab5773: Test completed in 0.661047 seconds
        container_options/03ab5773: Test completed with returncode: 0
        container_options/03ab5773: Writing output file -  /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.out
        container_options/03ab5773: Writing error file - /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.err
        container_commands_ubuntu/80e076bc: Current Working Directory : /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/stage
        container_commands_ubuntu/80e076bc: Running Test via command: bash --norc --noprofile -eo pipefail container_commands_ubuntu_build.sh
        container_commands_ubuntu/80e076bc: Test completed in 0.683467 seconds
        container_commands_ubuntu/80e076bc: Test completed with returncode: 0
        container_commands_ubuntu/80e076bc: Writing output file -  /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.out
        container_commands_ubuntu/80e076bc: Writing error file - /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.err
                                                                   Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                            ┃ executor           ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime  ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ container_commands_ubuntu/80e076bc │ generic.local.bash │ PASS   │ None None None                      │ 0          │ 0.683467 │
        ├────────────────────────────────────┼────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
        │ container_options/03ab5773         │ generic.local.bash │ PASS   │ None None None                      │ 0          │ 0.661047 │
        └────────────────────────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘



        Passed Tests: 2/2 Percentage: 100.000%
        Failed Tests: 0/2 Percentage: 0.000%


        Adding 2 test results to /Users/siddiq90/Documents/github/buildtest/var/report.json
        Writing Logfile to: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_hw24zz0m.log


    Let's inspect the test results, take note of the, output, error and generated test. First you will notice in the generated test the
    ``docker run`` used to run the container. In the output file, you will see the content of `/etc/os-release` from the container and the error file will show that there is no such file on host named `/etc/os-release`.


    .. code-block:: console

         buildtest inspect query -o -e -t  container_commands_ubuntu container_options
        ──────────────────────────────────────────────────────────────────────────────────────── container_options/03ab5773-cff3-48ef-bbf0-a8902646db65 ────────────────────────────────────────────────────────────────────────────────────────
        Executor: generic.local.bash
        Description: run arbitrary linux commands in ubuntu container
        State: PASS
        Returncode: 0
        Runtime: 0.661047 sec
        Starttime: 2023/10/13 11:04:10
        Endtime: 2023/10/13 11:04:10
        Command: bash --norc --noprofile -eo pipefail container_options_build.sh
        Test Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.sh
        Build Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options_build.sh
        Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.out
        Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.err
        Log File: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_hw24zz0m.log
        ────────────────────────────────────────── Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.out ──────────────────────────────────────────
        myhostname
        DOE-7086392

        ────────────────────────────────────────── Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.err ───────────────────────────────────────────

        ─────────────────────────────────────────── Test File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/container_options.sh ────────────────────────────────────────────
        #!/bin/bash
        set -eo pipefail
        # Content of run section
        docker run -v /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_options/03ab5773/stage:/buildtest --hostname myhostname ubuntu:latest hostname
        hostname
        ──────────────────────────────────────────────────────────────────────────────────── container_commands_ubuntu/80e076bc-df06-48a9-8f63-2f40074d4f15 ────────────────────────────────────────────────────────────────────────────────────
        Executor: generic.local.bash
        Description: run arbitrary linux commands in ubuntu container
        State: PASS
        Returncode: 0
        Runtime: 0.683467 sec
        Starttime: 2023/10/13 11:04:10
        Endtime: 2023/10/13 11:04:11
        Command: bash --norc --noprofile -eo pipefail container_commands_ubuntu_build.sh
        Test Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.sh
        Build Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu_build.sh
        Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.out
        Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.err
        Log File: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_hw24zz0m.log
        ────────────────────────────────── Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.out ──────────────────────────────────
        PRETTY_NAME="Ubuntu 22.04.3 LTS"
        NAME="Ubuntu"
        VERSION_ID="22.04"
        VERSION="22.04.3 LTS (Jammy Jellyfish)"
        VERSION_CODENAME=jammy
        ID=ubuntu
        ID_LIKE=debian
        HOME_URL="https://www.ubuntu.com/"
        SUPPORT_URL="https://help.ubuntu.com/"
        BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
        PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
        UBUNTU_CODENAME=jammy

        ────────────────────────────────── Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.err ───────────────────────────────────
        ls: /etc/os-release: No such file or directory

        ─────────────────────────────────── Test File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/container_commands_ubuntu.sh ────────────────────────────────────
        #!/bin/bash
        set -eo pipefail
        # Content of run section
        docker run -v /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_commands/container_commands_ubuntu/80e076bc/stage:/buildtest ubuntu:latest bash -c "cat /etc/os-release"

Please note that ``command`` keyword must be properly formulated to run commands in container which can vary depending on how the container is setup.

Running Scripts in Container
----------------------------

In this section, we will discuss how to run scripts inside container, which would be a typical use case for running an application test in container.
Buildtest will automatically volume mount the stage directory in the container which allows one to access the files in the container. The volume mount is
setup in ``/buildtest`` directory. In the next example, we will run a simple python script that will display the version of python.

.. literalinclude:: ../tutorials/containers/script.py
   :language: python

The example buildspec is the following, take note of the ``command`` section, we will invoke the script in the container at ``/buildtest/script.py`` which
will be present since stage directory is mounted in container. We will run the same script on the host system specified in the ``run`` section.

.. literalinclude:: ../tutorials/containers/run_script.yml
   :language: yaml
   :emphasize-lines: 8-11

Let's run the test and inspect the test results

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/containers/run_script.yml``

    .. code-block:: console

          buildtest build -b $BUILDTEST_ROOT/tutorials/containers/run_script.yml
        ╭───────────────────────────────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────────────────────────────╮
        │                                                                                                                                                                      │
        │ User:               siddiq90                                                                                                                                         │
        │ Hostname:           DOE-7086392                                                                                                                                      │
        │ Platform:           Darwin                                                                                                                                           │
        │ Current Time:       2023/10/11 13:21:09                                                                                                                              │
        │ buildtest path:     /Users/siddiq90/Documents/github/buildtest/bin/buildtest                                                                                         │
        │ buildtest version:  1.6                                                                                                                                              │
        │ python path:        /Users/siddiq90/.local/share/virtualenvs/buildtest-Ir4AdrfC/bin/python3                                                                          │
        │ python version:     3.10.12                                                                                                                                          │
        │ Configuration File: /Users/siddiq90/Documents/github/buildtest/buildtest/settings/config.yml                                                                         │
        │ Test Directory:     /Users/siddiq90/Documents/github/buildtest/var/tests                                                                                             │
        │ Report File:        /Users/siddiq90/Documents/github/buildtest/var/report.json                                                                                       │
        │ Command:            /Users/siddiq90/Documents/github/buildtest/bin/buildtest build -b /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_script.yml │
        │                                                                                                                                                                      │
        ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ───────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────────────────────────────
                                      Discovered buildspecs
        ╔════════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                      ║
        ╟────────────────────────────────────────────────────────────────────────────────╢
        ║ /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_script.yml ║
        ╚════════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_script.yml: VALID
        Total builder objects created: 1
                                                                                                     Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                          ┃ type   ┃ executor           ┃ compiler ┃ nodes ┃ procs ┃ description                      ┃ buildspecs                                                                     ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ run_script_in_container/2319c470 │ script │ generic.local.bash │ None     │ None  │ None  │ run a python script in container │ /Users/siddiq90/Documents/github/buildtest/tutorials/containers/run_script.yml │
        └──────────────────────────────────┴────────┴────────────────────┴──────────┴───────┴───────┴──────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────┘
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        run_script_in_container/2319c470: Creating test directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_script/run_script_in_container/2319c470
        run_script_in_container/2319c470: Creating the stage directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_script/run_script_in_container/2319c470/stage
        run_script_in_container/2319c470: Writing build script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_script/run_script_in_container/2319c470/run_script_in_container_build.sh
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
        run_script_in_container/2319c470 does not have any dependencies adding test to queue
              Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder                          ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ run_script_in_container/2319c470 │
        └──────────────────────────────────┘
        run_script_in_container/2319c470: Current Working Directory : /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_script/run_script_in_container/2319c470/stage
        run_script_in_container/2319c470: Running Test via command: bash --norc --noprofile -eo pipefail run_script_in_container_build.sh
        run_script_in_container/2319c470: Test completed in 1.02662 seconds
        run_script_in_container/2319c470: Test completed with returncode: 0
        run_script_in_container/2319c470: Writing output file -  /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_script/run_script_in_container/2319c470/run_script_in_container.out
        run_script_in_container/2319c470: Writing error file - /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/run_script/run_script_in_container/2319c470/run_script_in_container.err
                                                                 Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder                          ┃ executor           ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ run_script_in_container/2319c470 │ generic.local.bash │ PASS   │ None None None                      │ 0          │ 1.02662 │
        └──────────────────────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


        Adding 1 test results to /Users/siddiq90/Documents/github/buildtest/var/report.json
        Writing Logfile to: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_58pkmkc3.log

    This test is expected to run inside a python container so we should see different versions of python in the output file. Let's inspect the
    test results using ``buildtest inspect query`` command as shown below

        .. code-block:: console

             buildtest inspect query -o -e -t  run_script_in_container
            ───────────────────────────────────────────────────────────────────────────────────── run_script_in_container/b987e2b9-1395-411d-bd05-e77e896a01f1 ─────────────────────────────────────────────────────────────────────────────────────
            Executor: generic.local.bash
            Description: run a python script in container
            State: PASS
            Returncode: 0
            Runtime: 0.704285 sec
            Starttime: 2023/10/11 11:56:48
            Endtime: 2023/10/11 11:56:49
            Command: bash --norc --noprofile -eo pipefail run_script_in_container_build.sh
            Test Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/run_script_in_container.sh
            Build Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/run_script_in_container_build.sh
            Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/run_script_in_container.out
            Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/run_script_in_container.err
            Log File: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_bu89pzha.log
            ───────────────────────────────── Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/run_script_in_container.out ─────────────────────────────────
            Python version:  3.12.0 (main, Oct  3 2023, 01:48:15) [GCC 12.2.0]
            Python version:  3.10.12 (main, Jun 15 2023, 07:13:36) [Clang 14.0.3 (clang-1403.0.22.14.1)]

            ───────────────────────────────── Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/run_script_in_container.err ──────────────────────────────────

            ────────────────────────────────── Test File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/run_script_in_container.sh ───────────────────────────────────
            #!/bin/bash
            set -eo pipefail
            # Content of run section
            docker run -v /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/container_commands/run_script_in_container/b987e2b9/stage:/buildtest python:latest bash -c "python /buildtest/script.py"
            python script.py

Specify Addition Volume Mounts
------------------------------

In this section, we will discuss how to specify additional volume mounts in the container. This is useful if you need to access additional files in the container from the host
system that are typically not present in the container.

To specify additional volume mounts, you can use the ``mounts`` keyword which is a string type that allows one to specify list of directories that need to be bind mounted.
It's up to user to specify the correct directory path and syntax. In **docker** or **podman** this would translate to ``docker run -v /host/path:/container/path`` or ``podman -v /host/path:/container/path``.
In **singularity** this would translate to ``singularity exec -B /host/path:/container/path``.

Let's take a look at the following example, where we will bind mount ``/tmp`` from host into the container at ``/tmp``. We will execute
``echo 'hello world' > /tmp/hello.txt`` which will write the content to ``/tmp/hello.txt`` which will be present on host system. Next, we will
``cat`` the content of ``/tmp/hello.txt`` on host system specified in the ``run`` section.

.. literalinclude:: ../tutorials/containers/bind_mounts.yml
   :language: yaml
   :emphasize-lines: 9-12

Let's try running this script

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/containers/bind_mounts.yml``

    .. code-block:: console

          buildtest build -b $BUILDTEST_ROOT/tutorials/containers/bind_mounts.yml
        ╭────────────────────────────────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────────────────────────────╮
        │                                                                                                                                                                       │
        │ User:               siddiq90                                                                                                                                          │
        │ Hostname:           DOE-7086392                                                                                                                                       │
        │ Platform:           Darwin                                                                                                                                            │
        │ Current Time:       2023/10/11 13:33:21                                                                                                                               │
        │ buildtest path:     /Users/siddiq90/Documents/github/buildtest/bin/buildtest                                                                                          │
        │ buildtest version:  1.6                                                                                                                                               │
        │ python path:        /Users/siddiq90/.local/share/virtualenvs/buildtest-Ir4AdrfC/bin/python3                                                                           │
        │ python version:     3.10.12                                                                                                                                           │
        │ Configuration File: /Users/siddiq90/Documents/github/buildtest/buildtest/settings/config.yml                                                                          │
        │ Test Directory:     /Users/siddiq90/Documents/github/buildtest/var/tests                                                                                              │
        │ Report File:        /Users/siddiq90/Documents/github/buildtest/var/report.json                                                                                        │
        │ Command:            /Users/siddiq90/Documents/github/buildtest/bin/buildtest build -b /Users/siddiq90/Documents/github/buildtest/tutorials/containers/bind_mounts.yml │
        │                                                                                                                                                                       │
        ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ───────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────────────────────────────
                                       Discovered buildspecs
        ╔═════════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                       ║
        ╟─────────────────────────────────────────────────────────────────────────────────╢
        ║ /Users/siddiq90/Documents/github/buildtest/tutorials/containers/bind_mounts.yml ║
        ╚═════════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /Users/siddiq90/Documents/github/buildtest/tutorials/containers/bind_mounts.yml: VALID
        Total builder objects created: 1
                                                                                                     Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                          ┃ type   ┃ executor           ┃ compiler ┃ nodes ┃ procs ┃ description                      ┃ buildspecs                                                                      ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ bind_mount_in_container/51c5e402 │ script │ generic.local.bash │ None     │ None  │ None  │ run a python script in container │ /Users/siddiq90/Documents/github/buildtest/tutorials/containers/bind_mounts.yml │
        └──────────────────────────────────┴────────┴────────────────────┴──────────┴───────┴───────┴──────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────┘
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        bind_mount_in_container/51c5e402: Creating test directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402
        bind_mount_in_container/51c5e402: Creating the stage directory: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/stage
        bind_mount_in_container/51c5e402: Writing build script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container_build.sh
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
        bind_mount_in_container/51c5e402 does not have any dependencies adding test to queue
              Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder                          ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ bind_mount_in_container/51c5e402 │
        └──────────────────────────────────┘
        bind_mount_in_container/51c5e402: Current Working Directory : /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/stage
        bind_mount_in_container/51c5e402: Running Test via command: bash --norc --noprofile -eo pipefail bind_mount_in_container_build.sh
        bind_mount_in_container/51c5e402: Test completed in 0.730255 seconds
        bind_mount_in_container/51c5e402: Test completed with returncode: 0
        bind_mount_in_container/51c5e402: Writing output file -  /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container.out
        bind_mount_in_container/51c5e402: Writing error file - /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container.err
                                                                  Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                          ┃ executor           ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime  ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ bind_mount_in_container/51c5e402 │ generic.local.bash │ PASS   │ None None None                      │ 0          │ 0.730255 │
        └──────────────────────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


        Adding 1 test results to /Users/siddiq90/Documents/github/buildtest/var/report.json
        Writing Logfile to: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_7radfslq.log


    Let's inspect the test result, and take notice of the ``docker run -v`` option where we specify the volume mount for `/tmp`. The output file
    will contain the result of the ``echo`` command that was written to ``/tmp/hello.txt``

    .. code-block:: console

          buildtest inspect query -o -t bind_mount_in_container
        ───────────────────────────────────────────────────────────────────────────────────── bind_mount_in_container/51c5e402-dfaa-4af6-979e-b4a432ec2168 ─────────────────────────────────────────────────────────────────────────────────────
        Executor: generic.local.bash
        Description: run a python script in container
        State: PASS
        Returncode: 0
        Runtime: 0.730255 sec
        Starttime: 2023/10/11 13:33:22
        Endtime: 2023/10/11 13:33:23
        Command: bash --norc --noprofile -eo pipefail bind_mount_in_container_build.sh
        Test Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container.sh
        Build Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container_build.sh
        Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container.out
        Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container.err
        Log File: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_7radfslq.log
        ──────────────────────────────────── Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container.out ─────────────────────────────────────
        hello world

        ────────────────────────────────────── Test File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/bind_mount_in_container.sh ──────────────────────────────────────
        #!/bin/bash
        set -eo pipefail
        # Content of run section
        docker run -v /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/bind_mounts/bind_mount_in_container/51c5e402/stage:/buildtest -v /tmp:/tmp ubuntu:latest bash -c "echo 'hello world' > /tmp/hello.txt"
        cat /tmp/hello.txt


Container Runs without arguments
---------------------------------

Sometimes you will have containers that are meant to run without any argument. An example of this is the ``hello-world`` container which will
print this message

.. code-block:: console

      docker run hello-world

    Hello from Docker!
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
        (amd64)
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.

    To try something more ambitious, you can run an Ubuntu container with:
     $ docker run -it ubuntu bash

    Share images, automate workflows, and more with a free Docker ID:
     https://hub.docker.com/

    For more examples and ideas, visit:
     https://docs.docker.com/get-started/

However, if you try running arbitrary commands inside the container, you will typically get an error

    .. code-block:: console

         docker run -it hello-world /bin/bash
        docker: Error response from daemon: OCI runtime create failed: container_linux.go:367: starting container process caused: exec: "/bin/bash": stat /bin/bash: no such file or directory: unknown.
        ERRO[0000] error waiting for container: context canceled


That being said, the ``command`` keyword is an optional property and inorder to run the hello-world container we have the following buildspec that can
achieve this task.

.. literalinclude:: ../tutorials/containers/hello_world.yml
   :language: yaml
   :emphasize-lines: 6-8


You can run this test by running ``buildtest build -b $BUILDTEST_ROOT/tutorials/containers/hello_world.yml``. Upon completion of test, you can query
the test result and you will notice the container was executed successfully.

.. code-block:: console

      buildtest it query -o -t  hello_world_container_no_commands
    ──────────────────────────────────────────────────────────────────────────────── hello_world_container_no_commands/37a26900-2a01-4abc-a060-9645357558f8 ────────────────────────────────────────────────────────────────────────────────
    Executor: generic.local.bash
    Description: run container with no commands
    State: PASS
    Returncode: 0
    Runtime: 0.612196 sec
    Starttime: 2023/10/11 14:20:34
    Endtime: 2023/10/11 14:20:35
    Command: bash --norc --noprofile -eo pipefail hello_world_container_no_commands_build.sh
    Test Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/no_commands/hello_world_container_no_commands/37a26900/hello_world_container_no_commands.sh
    Build Script: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/no_commands/hello_world_container_no_commands/37a26900/hello_world_container_no_commands_build.sh
    Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/no_commands/hello_world_container_no_commands/37a26900/hello_world_container_no_commands.out
    Error File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/no_commands/hello_world_container_no_commands/37a26900/hello_world_container_no_commands.err
    Log File: /Users/siddiq90/Documents/github/buildtest/var/logs/buildtest_jrpeoqxg.log
    ────────────────────────── Output File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/no_commands/hello_world_container_no_commands/37a26900/hello_world_container_no_commands.out ───────────────────────────
    Hello from Docker!
    This message shows that your installation appears to be working correctly.
    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
        (amd64)
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.
    To try something more ambitious, you can run an Ubuntu container with:
     $ docker run -it ubuntu bash
    Share images, automate workflows, and more with a free Docker ID:
     https://hub.docker.com/
    For more examples and ideas, visit:
     https://docs.docker.com/get-started/
    Test Complete!

    ──────────────────────────── Test File: /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/no_commands/hello_world_container_no_commands/37a26900/hello_world_container_no_commands.sh ────────────────────────────
    #!/bin/bash
    set -eo pipefail
    # Content of run section
    docker run -v /Users/siddiq90/Documents/github/buildtest/var/tests/generic.local.bash/no_commands/hello_world_container_no_commands/37a26900/stage:/buildtest hello-world
    echo 'Test Complete!'