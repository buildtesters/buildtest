Site Examples
==============

Ascent @ OLCF
---------------

`Ascent <https://docs.olcf.ornl.gov/systems/ascent_user_guide.html>`_ is a training
system for Summit at OLCF, which is using a IBM Load Sharing
Facility (LSF) as their batch scheduler. Ascent has two
queues **batch** and **test**. To declare LSF executors we define them under ``lsf``
section within the ``executors`` section.

The default launcher is `bsub` which can be defined under ``defaults``. The
``pollinterval`` will poll LSF jobs every 10 seconds using ``bjobs``. The
``pollinterval`` accepts a range between **10 - 300** seconds as defined in
schema. In order to avoid polling scheduler excessively pick a number that is best
suitable for your site

.. code-block:: yaml

    system:
      ascent:
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
            gcc: ^(gcc)
            pgi: ^(pgi)
            cuda: ^(cuda)
          compiler:
            gcc:
              builtin_gcc:
                cc: /usr/bin/gcc
                cxx: /usr/bin/g++
                fc: /usr/bin/gfortran

JLSE @ ANL
-----------

`Joint Laboratory for System Evaluation (JLSE) <https://www.jlse.anl.gov/>`_ provides
a testbed of emerging HPC systems, the default scheduler is Cobalt, this is
defined in the ``cobalt`` section defined in the executor field.

We set default launcher to qsub defined with ``launcher: qsub``. This is inherited
for all batch executors. In each cobalt executor the ``queue`` property will specify
the queue name to submit job, for instance the executor ``yarrow`` with ``queue: yarrow``
will submit job using ``qsub -q yarrow`` when using this executor.

.. code-block:: yaml

    system:
      jlse:
        hostnames:
        - jlselogin*
        moduletool: environment-modules
        executors:
          defaults:
            launcher: qsub
            pollinterval: 10
            max_pend_time: 300
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
