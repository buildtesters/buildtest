Module Subcommands
==================

.. contents::
   :backlinks: none

Module Options (``buildtest module --help``)
----------------------------------------------

::

    usage: buildtest module [-h] [--module-load-test] [--diff-trees DIFF_TREES] [-a Module Tree] [-l] [-r Module Tree]

   optional arguments:
     -h, --help            show this help message and exit
     --module-load-test    conduct module load test for all modules defined in BUILDTEST_MODULE_ROOT
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

.. code::

   [siddis14@amrndhl1157 buildtest-framework]$ buildtest module --diff-trees /nfs/grid/software/easybuild/2018/Broadwell/redhat/7.3/all,/clust/app/easybuild/2018/SkyLake/redhat/7.3/modules/all
                            Comparing Module Trees for differences in module files
                            -------------------------------------------------------

     Module Tree 1: /nfs/grid/software/easybuild/2018/Broadwell/redhat/7.3/all
     Module Tree 2: /clust/app/easybuild/2018/SkyLake/redhat/7.3/modules/all

     ID       |     Module                                                   |   Module Tree 1    |   Module Tree 2
     ---------|--------------------------------------------------------------|--------------------|----------------------
     1        | OpenMM/7.1.1-intel-2018a-Python-2.7.14                       | FOUND              | NOT FOUND
     2        | BamTools/2.5.1-intel-2018a                                   | FOUND              | NOT FOUND
     3        | SAMtools/1.6-intel-2018a                                     | FOUND              | NOT FOUND
     4        | GLPK/4.61-intel-2018a                                        | FOUND              | NOT FOUND
     5        | BEDTools/2.27.1-intel-2018a                                  | FOUND              | NOT FOUND
     6        | Ruby/2.5.0-intel-2018a                                       | FOUND              | NOT FOUND
     7        | git/2.16.1-intel-2018a                                       | FOUND              | NOT FOUND
     8        | JAGS/4.3.0-intel-2018a                                       | FOUND              | NOT FOUND
     9        | netCDF-Fortran/4.4.4-intel-2018a                             | FOUND              | NOT FOUND
     10       | BWA/0.7.17-intel-2018a                                       | FOUND              | NOT FOUND



If there is no difference between module trees you will get the following.

.. code::


   [siddis14@amrndhl1157 buildtest-framework]$ buildtest module --diff-trees /clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all,/clust/app/easybuild/2018/SkyLake/redhat/7.3/modules/all
   No difference found between module tree:  /clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all and module tree: /clust/app/easybuild/2018/SkyLake/redhat/7.3/modules/all

Module Load Testing (``buildtest module --module-load-test``)
--------------------------------------------------------------

buildtest provides feature to test ``module load`` functionality on all module files
in a module tree. This assumes you have the module tree in ``MODULEPATH`` in order
for ``module`` command to work properly.

To use this feature specify the appropriate module tree for parameter ``BUILDTEST_MODULE_ROOT`` in
``config.yaml`` or via environment variable. To use this feature you need to use
``buildtest module --module-load-test``

To demonstrate let's start off with an example where we test module load for a single module tree.

.. code::

  [siddis14@amrndhl1228 buildtest-framework]$ buildtest --show | grep BUILDTEST_MODULE_ROOT
  BUILDTEST_MODULE_ROOT                              (C) = /nfs/grid/software/RHEL7/non-easybuild/modules/all


Let's start the test

.. code::

  [siddis14@amrndhl1228 buildtest-framework]$ buildtest module --module-load-test
  STATUS: PASSED - Testing module: VNL-ATK/2016.4
  STATUS: PASSED - Testing module: anaconda2/4.2.0-chemistry
  STATUS: PASSED - Testing module: anaconda3/4.2.0-chemistry
  STATUS: PASSED - Testing module: bcl2fastq2/v2.17.1.14
  STATUS: PASSED - Testing module: ccp4/7.0
  STATUS: PASSED - Testing module: ccp4/7.0-nightly
  STATUS: PASSED - Testing module: cellranger/1.2.1
  STATUS: PASSED - Testing module: gaussian/g16.a03.avx
  STATUS: PASSED - Testing module: gaussian/g16.a03.avx2
  STATUS: PASSED - Testing module: gaussian/g16.a03.legacy
  STATUS: PASSED - Testing module: gaussian/g16.a03.sse4
  STATUS: PASSED - Testing module: hmmer/3.1b2
  STATUS: PASSED - Testing module: materialstudios/2018
  STATUS: PASSED - Testing module: openeye/2017
  STATUS: PASSED - Testing module: phenix/dev2666
  STATUS: PASSED - Testing module: rosetta/3.7
  STATUS: PASSED - Testing module: turbomole/7.11
  STATUS: PASSED - Testing module: turbomole/7.12
  STATUS: PASSED - Testing module: xds/20161205


buildtest will attempt to run ``module load`` against each module to verify modules are working properly.

You may specify multiple module trees using ``BUILDTEST_MODULE_ROOT`` for testing
``buildtest module --module-load-test`` but you may run into module clashing if you have two or more occurrence of
module file in two or more trees. In that case, you may be testing ``module load`` for module file that comes
first in ``MODULEPATH``.

To use this feature properly, it is best to use this with one module tree at a time.
