Building Test for Scheduler
============================

buildtest supports creation of job scripts for LSF and SLURM scheduler which can be used to submit jobs to scheduler.

LSF Job Example
----------------

To enable the LSF mode ``scheduler: LSF`` must be set in the test configuration.

Let's see an example configuration for LSF job

.. command-output:: cat ${BUILDTEST_ROOT}/toolkit/suite/tutorial/compilers/hello_lsf.yml
   :shell:

By setting ``scheduler: LSF`` this enables the ``bsub`` key that is responsible for adding the **#BSUB** directive in
the test script. Shown below is an example build for LSF job.

.. program-output:: cat docgen/tutorial.compilers.hello_lsf.yml.txt

The ``bsub`` keys are mapped to the #BSUB options which makes it easy to associate #BSUB options to the ``bsub`` dictionary.


You can run ``buildtest show -k singlesource`` to see description of all keys or refer to  :ref:`show_keys` for list of all keys.

Submitting Jobs to LSF
-----------------------

.. Note:: This is an experimental feature

buildtest provides a wrapper to **bsub** command that allows buildtest to submit jobs to scheduler.
This can be achieved by using ``buildtest build bsub`` command. Shown below are the list of options available
with bsub.

.. program-output:: cat docgen/buildtest_build_bsub_-h.txt

To see the bsub command without submitting to scheduler use the ``--dry-run`` option. buildtest will
require a **build ID** in order to submit job. buildtest will use the build ID to fetch the test script
that will be submitted to LSF.

Here are a few examples.

1. Submitting a job to **admin** queue with **10 minute** walltime, requesting **50M** of memory
and job name is **testjob** for build **ID=0**::

    $ buildtest build bsub -q admin -W 00:10 -M 50M -J testjob 0 --dry-run
    bsub -q admin -M 50M -J testjob -W 00:10 < /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_0/args.c.yml.0xe93836d1.sh

2. Submitting a job to **admin** queue with 2 tasks on resource of **type=X86_64**::

    $ buildtest build bsub -q admin -n 2 -R "type==X86_64"  2
    bsub -q admin -n 2 -R type==X86_64 < /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_2/args.c.yml.0x722fa01.sh
    Job <54218287> is submitted to queue <admin>.
    Submitting Job: /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_2/args.c.yml.0x722fa01.sh to scheduler

Options to bsub wrapper in buildtest are of type string which are passed in directly to ``bsub`` command.
This was intended to leverage bsub syntax as users are accustomed to without reinventing a new
syntax language. For example, ``bsub -R`` has a very complex syntax requirement that requires a
string format to process the information.


SLURM Job Example
------------------

To enable SLURM mode set ``scheduler: SLURM`` in the test configuration.

The following test highlights how SLURM configuration can be specified in the test configuration

.. program-output:: cat ../toolkit/suite/tutorial/compilers/hello_slurm.yml

The ``scheduler: SLURM`` will enable ``sbatch`` key that is used for adding **#SBATCH** directive in test script.
Also note that ``cxxflags:`` will be used for passing options to C++ compiler (g++)

.. program-output:: cat docgen/tutorial.compilers.hello_slurm.yml.txt