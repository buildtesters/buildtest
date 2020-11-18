.. _configuring_buildtest:

Configuring buildtest
======================

The buildtest configuration file is used for configuring buildtest.
This is defined by JSON schemafile named `settings.schema.json <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/settings.schema.json>`_.
For more details on all properties see `Settings Schema Documentation <https://buildtesters.github.io/buildtest/pages/schemadocs/settings.html>`_.


Default Configuration
-----------------------

The default buildtest configuration  is located at `buildtest/settings/config.yml <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/settings/config.yml>`_
relative to root of repo. User may override the default configuration by creating
their own buildtest configuration at ``$HOME/.buildtest/config.yml`` and buildtest
will read the user configuration instead.

Shown below is the default configuration provided by buildtest.

.. program-output:: cat ../buildtest/settings/config.yml

.. _configuring_executors:

What is an executor?
----------------------

An executor is responsible for running the test and capture output/error file and
return code. An executor can be local executor which runs tests on local machine or
batch executor that can be modelled as partition/queue. A batch executor is
responsible for **dispatching** job, then **poll** job until its finish, and
**gather** job metrics from scheduler.

Executor Declaration
--------------------

`executors` is a JSON object, the structure looks as follows::

  executors:
    local:
      <local1>:
      <local2>:
      <local3>:
    slurm:
      <slurm1>:
      <slurm2>:
      <slurm3>:
   lsf:
     <lsf1>:
     <lsf2>:
     <lsf3>:

The **LocalExecutors** are defined in section `local` where each executor must be
unique name::

  executors:
    local:

The *LocalExecutors* can be ``bash``, ``sh`` and ``python`` shell and they are
referenced in buildspec using ``executor`` field as follows::

    executor: local.bash

The executor is referenced in buildspec in the format: ``<type>.<name>`` where
**type** is **local**, **slurm**, **lsf** defined in the **executors** section and **name**
is the executor name. In example above `local.bash` refers to the LocalExecutor
using bash shell. Similarly, **SlurmExecutors** and **LSFExecutors** are defined
in similar structure.

In this example below we define a local executor named `bash` that is referenced
in buildspec as ``executor: local.bash``::

    executors:
      local:
        bash:
          shell: bash

The local executors requires the ``shell`` key which takes the pattern
``"^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|sh|bash|csh|tcsh|zsh|python).*"``.
Any buildspec that references ``local.bash`` executor will submit job using ``bash`` shell.

You can pass options to shell which will get passed into each job submission.
For instance if you want bash login executor you can do the following::

    executors:
      local:
        login_bash:
          shell: bash --login

Then you can reference this executor as ``executor: local.login_bash`` and your
tests will be submitted via ``bash --login /path/to/test.sh``.

.. _slurm_executors:

buildtest configuration for Cori @ NERSC
------------------------------------------

Let's take a look at Cori buildtest configuration::

    editor: vi
    buildspec_roots:
    - $HOME/buildtest-cori
    moduletool: environment-modules
    executors:
      defaults:
        pollinterval: 10
        launcher: sbatch
        max_pend_time: 90
        account: nstaff
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash
        sh:
          description: submit jobs on local machine using sh shell
          shell: sh
        csh:
          description: submit jobs on local machine using csh shell
          shell: csh
        python:
          description: submit jobs on local machine using python shell
          shell: python
        e4s:
          description: E4S testsuite locally
          shell: bash
          before_script: |
            source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
            cd $SCRATCH/testsuite source setup.sh

      slurm:
        debug:
          description: jobs for debug qos
          qos: debug
          cluster: cori
          max_pend_time: 500
        shared:
          description: jobs for shared qos
          qos: shared
          max_pend_time: 10
        bigmem:
          description: bigmem jobs
          cluster: escori
          qos: bigmem
          max_pend_time: 300
        xfer:
          description: xfer qos jobs
          qos: xfer
          cluster: escori
        gpu:
          description: submit jobs to GPU partition
          options:
          - -C gpu
          cluster: escori
          max_pend_time: 300
        premium:
          description: submit jobs to premium queue
          qos: premium
        e4s:
          description: E4S runner
          cluster: cori
          max_pend_time: 20000
          options:
          - -q regular
          - -C knl
          - -t 10
          - -n 4
          before_script: |
            source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
            cd $SCRATCH/testsuite source setup.sh

    compilers:
      find:
        gcc:
        - gcc
        - PrgEnv-gnu
        cray:
        - PrgEnv-cray
        intel:
        - intel
        - PrgEnv-intel
        pgi:
        - pgi
      compiler:
        gcc:
          builtin:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran
          gcc@6.1.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/6.1.0
          gcc@7.3.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/7.3.0
          gcc@8.1.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/8.1.0
          gcc@8.2.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/8.2.0
          gcc@8.3.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/8.3.0
          gcc@9.2.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/9.2.0
          gcc@9.3.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/9.3.0
          gcc@6.3.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/6.3.0
          gcc@8.1.1-openacc-gcc-8-branch-20190215:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/8.1.1-openacc-gcc-8-branch-20190215
          PrgEnv-gnu@6.0.5:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - PrgEnv-gnu/6.0.5
          PrgEnv-gnu@6.0.6:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - PrgEnv-gnu/6.0.6
          PrgEnv-gnu@6.0.7:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - PrgEnv-gnu/6.0.7
        cray:
          PrgEnv-cray@6.0.5:
            cc: cc
            cxx: CC
            fc: ftn
            modules:
            - PrgEnv-cray/6.0.5
          PrgEnv-cray@6.0.6:
            cc: cc
            cxx: CC
            fc: ftn
            modules:
            - PrgEnv-cray/6.0.6
          PrgEnv-cray@6.0.7:
            cc: cc
            cxx: CC
            fc: ftn
            modules:
            - PrgEnv-cray/6.0.7
        intel:
          intel@18.0.1.163:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/18.0.1.163
          intel@18.0.3.222:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/18.0.3.222
          intel@19.0.3.199:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.0.3.199
          intel@16.0.3.210:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/16.0.3.210
          intel@17.0.1.132:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/17.0.1.132
          intel@17.0.2.174:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/17.0.2.174
          intel@19.0.0.117:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.0.0.117
          intel@19.0.8.324:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.0.8.324
          intel@19.1.0.166:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.1.0.166
          intel@19.1.1.217:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.1.1.217
          intel@19.1.2.254:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.1.2.254
          intel@19.1.2.275:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.1.2.275
          intel@19.1.3.304:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - intel/19.1.3.304
          PrgEnv-intel@6.0.5:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - PrgEnv-intel/6.0.5
          PrgEnv-intel@6.0.6:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - PrgEnv-intel/6.0.6
          PrgEnv-intel@6.0.7:
            cc: icc
            cxx: icpc
            fc: ifort
            modules:
            - PrgEnv-intel/6.0.7
        pgi:
          pgi@18.10:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/18.10
          pgi@19.1:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.1
          pgi@19.3:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.3
          pgi@19.4:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.4
          pgi@19.5:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.5
          pgi@19.7:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.7
          pgi@19.9:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.9
          pgi@19.10:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.10
          pgi@20.1:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/20.1
          pgi@20.4:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/20.4



In this setting, we define the following executors

- LocalExecutors: ``local.bash``, ``local.sh``, ``local.csh``, ``local.python``, ``local.e4s``
- SlurmExecutors: ``slurm.debug``, ``slurm.shared``, ``slurm.bigmem``, ``slurm.xfer``, ``slurm.gpu``, ``slurm.premium``, ``slurm.e4s``


We introduce section ``defaults`` which defines configuration for all executors
as follows::

      defaults:
        pollinterval: 10
        launcher: sbatch
        max_pend_time: 90

The `launcher` field is applicable for **SlurmExecutor** and **LSFExecutor** in this
case, ``launcher: sbatch`` inherits **sbatch** as the job launcher for all executors.
The ``pollinterval`` field is used  to poll jobs at set interval in seconds
when job is active in queue. The ``max_pend_time`` is **maximum** time job can be pending
within an executor, if it exceeds the limit buildtest will cancel the job. buildtest will
invoke ``scancel`` or ``bkill`` to cancel Slurm or LSF job. The `pollinterval`, `launcher`
and `max_pend_time` have no effect on **LocalExecutors**. The ``account: nstaff``
will instruct buildtest to charge all jobs to account ``nstaff`` from Slurm Executors.
The ``account`` option can be set in ``defaults`` global to all executors or set
per executor instance which overrides the default value.

At Cori, jobs are submitted via qos instead of partition so we model a slurm executor
named by qos. The ``qos`` field instructs which Slurm QOS to use when submitting job.
The ``description`` key is a brief description of the executor only served for
documentation purpose. The ``cluster`` field specifies which slurm cluster to use
(i.e ``sbatch --clusters=<string>``). In-order to use ``bigmem``, ``xfer``,
or ``gpu`` qos at Cori, we need to specify **escori** cluster (i.e
``sbatch --clusters=escori``).

buildtest will detect slurm configuration and check qos, partition, cluster
match with buildtest specification. In addition, buildtest supports multi-cluster
job submission and monitoring from remote cluster. This means if you specify
``cluster`` field buildtest will poll jobs using `sacct` with the
cluster name as follows: ``sacct -M <cluster>``.

The ``options`` field is use to specify any additional options to launcher (``sbatch``)
on command line. For ``slurm.gpu`` executor, we use the ``options: -C gpu``
in order to submit to Cori GPU cluster which requires ``sbatch -M escori -C gpu``.
Any additional **#SBATCH** options are
defined in buildspec for more details see :ref:`batch_support`

The ``max_pend_time`` option can be overridden per executor level for example the
section below overrides the default to 300 seconds::

        bigmem:
          description: bigmem jobs
          cluster: escori
          qos: bigmem
          max_pend_time: 300

The ``max_pend_time`` is used to cancel job only if job is pending in queue, not if it
is in run state. buildtest starts a timer at job submission and every poll interval (``pollinterval`` field)
checks if job has exceeded **max_pend_time** only if job is in **PENDING** (SLURM)
or **PEND** (LSF) state. If job pendtime exceeds `max_pend_time` limit, buildtest will
cancel job using ``scancel`` or ``bkill`` depending on the scheduler. Buildtest
will remove cancelled jobs from poll queue, in addition cancelled jobs won't be
reported in test report.

.. _buildspec_roots:

buildspec roots
-----------------

buildtest can discover buildspec using ``buildspec_roots`` keyword. This field is a list
of directory paths to search for buildspecs. For example we clone the repo
https://github.com/buildtesters/buildtest-cori at **$HOME/buildtest-cori** and assign
this to **buildspec_roots** as follows::

    buildspec_roots:
      - $HOME/buildtest-cori

This field is used with the ``buildtest buildspec find`` command. If you rebuild
your buildspec cache using ``--clear`` option it will detect all buildspecs in defined
in all directories specified by **buildspec_roots**. buildtest will recursively
find all **.yml** extension and validate each buildspec with appropriate schema.
By default buildtest will add the ``$BUILDTEST_ROOT/tutorials`` and ``$BUILDTEST_ROOT/general_tests``
to search path, where $BUILDTEST_ROOT is root of repo.

Configuring Module Tool
------------------------

You should configure the ``moduletool`` property to the module-system installed
at your site. Valid options are the following::

    # environment-modules
    moduletool: environment-modules

    # for lmod
    moduletool: lmod

    # specify N/A if you don't have modules
    moduletool: N/A

If your site has Lmod and you set ``moduletool: lmod``, we will make use of
`Lmodule API <https://lmodule.readthedocs.io/en/latest/>`_ to test modules.


before_script and after_script for executors
---------------------------------------------

Often times, you may want to run a set of commands before or after tests for more than
one test. For this reason, we support ``before_script`` and ``after_script`` section
per executor which is of string type where you can specify multi-line commands.

This can be demonstrated with an executor name **local.e4s** responsible for
building `E4S Testsuite <https://github.com/E4S-Project/testsuite>`_::

    e4s:
      description: "E4S testsuite locally"
      shell: bash
      before_script: |
        cd $SCRATCH
        git clone https://github.com/E4S-Project/testsuite.git
        cd testsuite
        source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
        source setup.sh

The `e4s` executor attempts to clone E4S Testsuite in $SCRATCH and activate
a spack environment and run the initialize script ``source setup.sh``. buildtest
will write a ``before_script.sh`` and ``after_script.sh`` for every executor.
This can be found in ``var/executors`` directory as shown below::

    $ tree var/executors/
    var/executors/
    |-- local.bash
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.e4s
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.python
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.sh
    |   |-- after_script.sh
    |   `-- before_script.sh


    4 directories, 8 files

The ``before_script`` and ``after_script`` field is available for all executors and
if its not specified the file will be empty. Every test will source the before
and after script for the given executor.

The ``editor: vi`` is used to open buildspecs in `vi` editor, this is used by commands like
``buildtest buildspec edit``. For more details see :ref:`editing_buildspecs`.
The `editor` field can be `vi`, `vim`, `nano`, or `emacs` depending on your editor
preference.

Compiler Declaration
--------------------

buildtest provides a mechanism to declare compilers in your configuration file, this
is defined in ``compilers`` top-level section. Shown below is an example section::

    compilers:
      compiler:
        gcc:
          builtin:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran

The compiler declaration is defined in section ``compiler`` followed by name
of compiler in this case ``gcc``. In the gcc section one can define all gnu compilers,
which includes the name of the compiler in this example we call ``builtin`` as
system compiler that defines C, C++ and Fortran compilers using ``cc``, ``cxx`` and
``fc``.

One can retrieve all compilers using ``buildtest config compilers``, there are few
options for this command.

.. program-output:: cat docgen/buildtest_config_compilers_--help.txt

buildtest can represent compiler output in JSON, YAML or list using the ``--json``,
``--yaml``, and ``--list`` option. Depending on your preference one can view
compiler section with any of these options. Shown below is an example output with
these options::

    $ buildtest config compilers --json
    {
      "gcc": {
        "builtin": {
          "cc": "/usr/bin/gcc",
          "cxx": "/usr/bin/g++",
          "fc": "/usr/bin/gfortran"
        }
      }
    }

    $ buildtest config compilers --yaml
    gcc:
      builtin:
        cc: /usr/bin/gcc
        cxx: /usr/bin/g++
        fc: /usr/bin/gfortran

    $ buildtest config compilers --list
    builtin

Detect Compilers (Experimental Feature)
----------------------------------------

buildtest can detect compilers based on modulefiles and generate compiler section
with compiler instance. This can be done via ``buildtest config compilers find``
option. First we declare a compiler ``find`` section that expects a dictionary
of key/value mapping between compiler names and their module names.

Shown below is an example where we expect to find gcc and pgi modules with name
``gcc`` and ``pgi``. We can specify a list of module names, currently buildtest will
add a compiler if modulename starts with the corresponding string.

.. Note:: This feature will be updated to allow regular expression in near future

::

    compilers:
      find:
        gcc: [gcc]
        pgi: [pgi]
      compiler:
        gcc:
          builtin:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran

Next we find all compiler modules using ``buildtest config compilers find`` which
will detect and test all modules. Any modules with non-zero exit code will be ignored,
and buildtest will generate a compiler instance per module found assuming there
is no compiler instance defined. buildtest will define a compiler instance for
``gcc/4.8.5`` --> ``gcc@4.8.5`` by renaming leading **/** with a **@**.

Shown below is an example output::

    $ buildtest config compilers find
    Discovered Modules:
    {
      "gcc": [
        "gcc/4.8.5",
        "gcc/6.4.0",
        "gcc/8.1.0",
        "gcc/10.1.0",
        "gcc/7.4.0",
        "gcc/8.1.1",
        "gcc/5.4.0"
      ],
      "pgi": [
        "pgi/20.1",
        "pgi/19.10",
        "pgi/18.7",
        "pgi/18.10",
        "pgi/19.9",
        "pgi/.18.5",
        "pgi/19.4",
        "pgi/19.5",
        "pgi/19.1"
      ]
    }



    Testing Modules:
    [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/4.8.5  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/6.4.0  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/8.1.0  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/10.1.0  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/7.4.0  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/8.1.1  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/5.4.0  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/20.1  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/19.10  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/18.7  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/18.10  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/19.9  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/.18.5  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/19.4  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/19.5  "
    [DEBUG] Return Code: 0
    [DEBUG] Executing module command: bash -l -c "module purge && module load pgi/19.1  "
    [DEBUG] Return Code: 0
    editor: vi
    buildspec_roots:
    - $HOME/buildtest-ascent
    moduletool: lmod
    executors:
      defaults:
        launcher: bsub
        pollinterval: 10
        max_pend_time: 60
        account: gen014ecpci
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash
        sh:
          description: submit jobs on local machine using sh shell
          shell: sh
        csh:
          description: submit jobs on local machine using csh shell
          shell: csh
        python:
          description: submit jobs on local machine using python shell
          shell: python
      lsf:
        batch:
          queue: batch
        test:
          queue: test
    compilers:
      find:
        gcc:
        - gcc
        pgi:
        - pgi
      compiler:
        gcc:
          builtin:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran
          gcc@4.8.5:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/4.8.5
          gcc@6.4.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/6.4.0
          gcc@8.1.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/8.1.0
          gcc@10.1.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/10.1.0
          gcc@7.4.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/7.4.0
          gcc@8.1.1:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/8.1.1
          gcc@5.4.0:
            cc: gcc
            cxx: g++
            fc: gfortran
            modules:
            - gcc/5.4.0
        pgi:
          pgi@20.1:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/20.1
          pgi@19.10:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.10
          pgi@18.7:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/18.7
          pgi@18.10:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/18.10
          pgi@19.9:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.9
          pgi@.18.5:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/.18.5
          pgi@19.4:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.4
          pgi@19.5:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.5
          pgi@19.1:
            cc: pgcc
            cxx: pgc++
            fc: pgfortran
            modules:
            - pgi/19.1

    Updating settings file:  /ccsopen/home/shahzebsiddiqui/.buildtest/config.yml

buildtest will update the configuration file after running ``buildtest config compilers find``.
There will a be a unique compiler entry organized by compiler group (``gcc``, ``pgi``). The
``modules`` property is a list of modules to load per compiler group. This can be
tweaked as needed.


buildtest configuration for Ascent @ OLCF
------------------------------------------

`Ascent <https://docs.olcf.ornl.gov/systems/ascent_user_guide.html>`_ is a training
system for Summit at OLCF, which is using a IBM Load Sharing
Facility (LSF) as their batch scheduler. Ascent has two
queues **batch** and **test**. To declare LSF executors we define them under ``lsf``
section within the ``executors`` section.

The default launcher is `bsub` which can be defined under ``defaults``. The
``pollinterval`` will poll LSF jobs every 10 seconds using ``bjobs``. The
``pollinterval`` accepts a range between `10` - `300` seconds as defined in
schema. In order to avoid polling scheduler excessively pick a number that is best
suitable for your site::

    editor: vi
    executors:
      defaults:
        launcher: bsub
        pollinterval: 10
        max_pend_time: 45

      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

        sh:
          description: submit jobs on local machine using sh shell
          shell: sh

        csh:
          description: submit jobs on local machine using csh shell
          shell: csh

        python:
          description: submit jobs on local machine using python shell
          shell: python
      lsf:
        batch:
          queue: batch
          description: Submit job to batch queue

        test:
          queue: test
          description: Submit job to test queue


buildtest configuration for JLSE @ ANL
---------------------------------------

`Joint Laboratory for System Evaluation (JLSE) <https://www.jlse.anl.gov/>`_ provides
a testbed of emerging HPC systems, the default scheduler is Cobalt, this is
defined in the ``cobalt`` section defined in the executor field.

We set default launcher to qsub defined with ``launcher: qsub``. This is inherited
for all batch executors. In each cobalt executor the ``queue`` property will specify
the queue name to submit job, for instance the executor ``yarrow`` with ``queue: yarrow``
will submit job using ``qsub -q yarrow`` when using this executor.

::

    editor: vi
    buildspec_roots:
      - $HOME/jlse_tests
    executors:
      defaults:
         launcher: qsub
         pollinterval: 10
         max_pend_time: 10

      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

        sh:
          description: submit jobs on local machine using sh shell
          shell: sh

        csh:
          description: submit jobs on local machine using csh shell
          shell: csh

        python:
          description: submit jobs on local machine using python shell
          shell: python

      cobalt:
        yarrow:
          queue: yarrow

        yarrow_debug:
          queue: yarrow_debug

        iris:
          queue: iris

        iris_debug:
          queue: iris_debug

CLI to buildtest configuration
-----------------------------------------------

The ``buildtest config`` command provides access to buildtest configuration, shown
below is the command usage.


.. program-output:: cat docgen/buildtest_config_--help.txt


View buildtest configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to view buildtest configuration you can run the following

.. program-output:: cat docgen/config-view.txt

.. Note:: ``buildtest config view`` will display contents of user buildtest settings ``~/.buildtest/config.yml`` if found, otherwise it will display the default configuration


Validate buildtest configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if your buildtest settings is valid, run ``buildtest config validate``.
This will validate your configuration with the schema **settings.schema.json**.
The output will be the following.

.. program-output:: cat docgen/config-validate.txt

.. Note:: If you defined a user setting (``~/.buildtest/config.yml``) buildtest will validate this file instead of default one.

If there is an error during validation, the output from **jsonschema.exceptions.ValidationError**
will be displayed in terminal. For example the error below indicates there was an error
on ``editor`` key in **config** object which expects the editor to be one of the
enum types [``vi``, ``vim``, ``nano``, ``emacs``]::

    $ buildtest config validate
    Traceback (most recent call last):
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/bin/buildtest", line 11, in <module>
        load_entry_point('buildtest', 'console_scripts', 'buildtest')()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 32, in main
        check_settings()
      File "/Users/siddiq90/Documents/buildtest/buildtest/config.py", line 71, in check_settings
        validate(instance=user_schema, schema=config_schema)
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/lib/python3.7/site-packages/jsonschema/validators.py", line 899, in validate
        raise error
    jsonschema.exceptions.ValidationError: 'gedit' is not one of ['vi', 'vim', 'nano', 'emacs']

    Failed validating 'enum' in schema['properties']['config']['properties']['editor']:
        {'default': 'vim',
         'enum': ['vi', 'vim', 'nano', 'emacs'],
         'type': 'string'}

    On instance['config']['editor']:
        'gedit'


Configuration Summary
~~~~~~~~~~~~~~~~~~~~~~

You can get a summary of buildtest using ``buildtest config summary``, this will
display information from several sources into one single command along.

.. program-output:: cat docgen/config-summary.txt


Example Configurations
-------------------------

buildtest provides a few example configurations for configuring buildtest this
can be retrieved by running ``buildtest schema -n settings.schema.json --examples``
or short option (``-e``), which will validate each example with schema file
``settings.schema.json``.

.. program-output:: cat docgen/schemas/settings-examples.txt

If you want to retrieve full json schema file for buildtest configuration you can
run ``buildtest schema -n settings.schema.json --json`` or short option ``-j``.
