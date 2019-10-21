Building Test for SLURM
========================

SLURM Job Example
-------------------

buildtest supports job script for SLURM. Similar to LSF, the test script
will be denoted with extension **.slurm** and start with the keyword
``slurm:`` in configuration. For more details on slurm keys in yaml  file
see :ref:`show_keys`

Here is an example configuration for SLURM job

.. code-block::
    :linenos:
    :emphasize-lines: 5-8

        compiler: gnu
        flags: -O2
        maintainer:
        - shahzeb siddiqui shahzebmsiddiqui@gmail.com
        slurm:
          mem: 200M
          nodes: '4'
          time: 01:00
        source: hello.cpp
        testblock: singlesource


Line 5 ``slurm:`` starts the slurm section. Slurm keys are named based on
``sbatch`` options so it is easy to remember.

.. note:: Only a subset of slurm keys are exposed in yaml

Line 6-8 define the slurm parameters, in this case we request for ``200M``
memory, with ``4`` nodes and walltime of ``1h``.

We can run this as follows

.. program-output:: cat scripts/build-slurm-example.txt