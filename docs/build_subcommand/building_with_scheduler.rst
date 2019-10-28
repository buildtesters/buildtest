Building Test for Scheduler
============================

buildtest supports creation of job scripts for LSF and SLURM scheduler which can be used to submit jobs to scheduler.

LSF Job Example
----------------

To enable the LSF mode ``scheduler: LSF`` must be set in the test configuration.

Let's see an example configuration for LSF job

.. program-output:: cat ../toolkit/suite/compilers/helloworld/hello_lsf.yml

By setting ``scheduler: LSF`` this enables the ``bsub`` key that is responsible for adding the **#BSUB** directive in
the test script. Shown below is an example build for LSF job.

.. program-output:: cat scripts/build-lsf-example.txt

The ``bsub`` keys are mapped to the #BSUB options which makes it easy to associate #BSUB options to the ``bsub`` dictionary.


You can run ``buildtest show -k singlesource`` to see description of all keys or refer to  :ref:`show_keys` for list of all keys.

SLURM Job Example
------------------

To enable SLURM mode set ``scheduler: SLURM`` in the test configuration.

See example below:

.. program-output:: cat ../toolkit/suite/compilers/helloworld/hello_slurm.yml

The ``scheduler: SLURM`` will enable ``sbatch`` key that is used for adding **#SBATCH** directive in test script. See example
below for a slurm test.

.. program-output:: cat scripts/build-slurm-example.txt


