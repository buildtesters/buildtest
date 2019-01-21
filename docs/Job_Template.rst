.. _Job_Template:

Job Template (``_buildtest build --job-template <template>``)
===============================================================



.. contents::
      :backlinks: none


LSF Job template
-----------------

buildtest provides a default job templates for LSF and SLURM to generate test scripts to be used with batch-scheduler.
The templates can be found at ``$BUILDTEST_ROOT/template/``

Shown below is a LSF Job Template

.. program-output:: cat scripts/Job_Template/job.lsf

Feel free to change or bring or specify your own job template. buildtest will
use job template and create job script for each test script with the same template
configuration, this may work for binary tests where job configuration is not
important. However, this may not work well for parallel jobs (OpenMP, MPI) where
further configuration is needed

Generate Job scripts via buildtest
----------------------------------

buildtest can automatically generate job scripts with a template job script specified
by ``--job-template`` option or with variable ``BUILDTEST_JOB_TEMPLATE``

Let's run the following ``_buildtest build --package firefox --job-template template/job.lsf --enable-job`` to
build LSF job scripts

.. program-output:: cat scripts/Job_Template/firefox_jobscript.txt


Job templates work with option ``--package`` and ``--software``. Let's try another example
building job scripts with a software package ``GCCcore/6.4.0`` with lsf job template


``_buildtest build -s GCCcore/6.4.0 --job-template template/job.lsf --enable-job``

.. program-output:: cat scripts/Job_Template/GCCcore-6.4.0_lsf_job.txt
