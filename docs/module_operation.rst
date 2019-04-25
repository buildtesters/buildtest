Module Operation
==================

.. contents::
   :backlinks: none

Module Options (``buildtest module --help``)
----------------------------------------------

::

    usage: buildtest module [-h] [--module-load-test] [--diff-trees DIFF_TREES] [-a Module Tree] [-l] [-r Module Tree]

   optional arguments:
     -h, --help            show this help message and exit
     --module-load-test    conduct module load test for all modules defined in BUILDTEST_MODULEPATH
     --diff-trees DIFF_TREES
                           Show difference between two module trees
     -a Module Tree        add a module tree
     -l                    list module trees
     -r Module Tree        remove a module tree



Difference Between Module Trees (``buildtest module --diff-trees``)
--------------------------------------------------------------------

buildtest can report differences between two module trees that can be useful if you deploy your software in a
**stage/prod** module tree and you want to keep these trees in sync.

If your HPC site builds software stack for each architecture and your environment is
heterogeneous then ``--diff-trees`` option will be helpful.


buildtest takes two trees as argument in the form of ``buildtest --diff-tree tree1,tree2``
where trees are separated by a comma. The tree must point to the root of the module tree in your
system and buildtest will walk through the entire tree. We expect this operation to be quick
given that the module tree is on the order of few thousand module files which is a reasonable
count of module files in a large HPC facility.

.. program-output:: cat scripts/module-diff.txt

If your site supports multiple architecture and you want to find difference
between the stacks then you will find ``--diff-trees`` to be handy. If the
stacks are same you will see the following message

.. program-output:: cat scripts/module-diff-v2.txt


Module Load Testing (``buildtest module --module-load-test``)
--------------------------------------------------------------

buildtest provides feature to test ``module load`` functionality on all module files
in a module tree. This assumes you have the module tree in ``MODULEPATH`` in order
for ``module`` command to work properly.

To use this feature specify the appropriate module tree for parameter ``BUILDTEST_MODULEPATH`` in
``config.yaml`` or via environment variable. To use this feature you need to use
``buildtest module --module-load-test``

To demonstrate let's start off with an example where we test module load for a single module tree.

.. code::

  [siddis14@amrndhl1228 buildtest-framework]$ buildtest --show | grep BUILDTEST_MODULEPATH
  BUILDTEST_MODULEPATH                              (C) = /nfs/grid/software/RHEL7/non-easybuild/modules/all


Let's start the test

.. program-output:: cat scripts/module-load.txt


buildtest will attempt to run ``module load`` against each module to verify modules are working properly.

You may specify multiple module trees using ``BUILDTEST_MODULEPATH`` for testing
``buildtest module --module-load-test`` but you may run into module clashing if you have two or more occurrence of
module file in two or more trees. In that case, you may be testing ``module load`` for module file that comes
first in ``MODULEPATH``.

To use this feature properly, it is best to use this with one module tree at a time.


