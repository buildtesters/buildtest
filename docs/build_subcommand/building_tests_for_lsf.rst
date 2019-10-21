Building Test for LSF
======================

LSF Job Example
----------------

buildtest supports creation of job scripts for LSF batch scheduler.
Test scripts with the extension **.lsf** will denote the test script is LSF job
scripts.

Let's see an example configuration for LSF job

.. code-block:: console
    :linenos:
    :emphasize-lines: 3-7

        compiler: gnu
        flags: -O2
        lsf:
          M: 200M
          R: sandybridge
          W: 01:00
          n: '4'
        maintainer:
        - shahzeb siddiqui shahzebmsiddiqui@gmail.com
        source: hello.c
        testblock: singlesource


The lsf section starts with keyword ``lsf:`` defined in line 3. The LSF keys
are named based on ``bsub`` options which makes it easy to associate the key to
the equivalent bsub command. In this example above lines **4-7** describe the
LSF parameters . These include ``200MB`` of memory with ``1hr`` walltime, ``4``
tasks and requesting ``sandybridge`` resource.

.. note:: Only a subset of lsf keys are exposed in yaml

You can run ``buildtest show -k singlesource`` to see description of all
keys or refer to  :ref:`show_keys`

We can run this as follows


.. program-output:: cat scripts/build-lsf-example.txt
