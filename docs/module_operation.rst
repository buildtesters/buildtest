Module Operation
==================

.. contents::
   :backlinks: none

Module Options (``buildtest module --help``)
----------------------------------------------

.. program-output:: cat scripts/buildtest-module-help.txt



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


Module Load Testing (``buildtest module loadtest``)
--------------------------------------------------------------

buildtest provides feature to test ``module load`` functionality on all module files
in a module tree. This assumes you have the module tree in ``MODULEPATH`` in order
for ``module`` command to work properly.

To use this feature specify the appropriate module tree for parameter ``BUILDTEST_MODULEPATH`` in
``settings.yml`` or via environment variable. To use this feature you need to
use ``buildtest module loadtest``

To demonstrate let's start off with an example where we test module load for a single module tree.

.. code::

  [siddis14@amrndhl1228 buildtest-framework]$ buildtest --show | grep BUILDTEST_MODULEPATH
  BUILDTEST_MODULEPATH                              (C) = /nfs/grid/software/RHEL7/non-easybuild/modules/all


Let's start the test

.. program-output:: cat scripts/module-load.txt


buildtest will attempt to run ``module load`` against each module to verify modules are working properly.

You may specify additional module trees using ``BUILDTEST_MODULEPATH`` for
module testing.

If you want to test all modules that were detected by ``spider`` utility,
you can set ``BUILDTEST_SPIDER_VIEW=all`` in your configuration or
environment variable or just run as follows::


    BUILDTEST_SPIDER_VIEW=all buildtest module loadtest

This will test all modules retrieved by spider utility.


Module Trees Operation
-----------------------

buildtest supports adding, removing and listing module trees. Internally, buildtest
is modifying BUILDTEST_MODULEPATH which is synonymous to MODULEPATH though,
buildtest makes use of ``BUILDTEST_MODULEPATH`` when querying modules using ``spider``
command.

At your site, you may be interested in testing software by each stack.

By default, ``BUILDTEST_MODULEPATH`` is set to an empty list ``[]`` in configuration
file ``$HOME/.buildtest/settings.yml``. In this case, ``BUILDTEST_MODULEPATH``
will read from ``MODULEPATH``.

Listing Module Tree (``buildtest module tree -l``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the module trees in buildtest you can run ``buildtest module tree -l``
which shows one module tree per line

.. program-output:: cat scripts/module_tree_list.txt

For this run, ``BUILDTEST_MODULEPATH`` is not set in configuration file so it is
reading from ``MODULEPATH``

.. code-block:: console

    $ cat ~/.buildtest/settings.yml  | grep -i BUILDTEST_MODULEPATH
    BUILDTEST_MODULEPATH: []

Adding Module Tree (``buildtest module tree -a``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add new module tree through command line using ``buildtest module
tree -a /path/to/tree`` which will update the configuration file

.. program-output:: cat scripts/module_tree_add.txt


Removing Module Tree (``buildtest module tree -r``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly you can remove module tree from your configuration via ``buildtest
module tree -r /path/to/tree``

.. program-output:: cat scripts/module_tree_rm.txt

Report Easybuild Modules (``buildtest module --easybuild``)
------------------------------------------------------------

buildtest can detect modules that are built by `Easybuild <https://easybuild.readthedocs.io/en/latest/>`_.
An easybuild module will contain a string in module file as follows::

    Built with EasyBuild version 3.7.1

buildtest will check all module trees defined by ``BUILDTEST_MODULEPATH`` and search
for string without the version number. To enable this feature use
``buildtest module --easybuild`` or short option ``buildtest module -eb``.

Shown below is the output of easybuild retrieval.

.. program-output:: cat scripts/easybuild-modules.txt

If you want buildtest to retrieve all records from ``spider`` to seek out all
easybuild modules consider setting ``BUILDTEST_SPIDER_VIEW=all`` in
configuration or environment variable. Shown below is an output when running
``BUILDTEST_SPIDER_VIEW=all buildtest module --easybuild``

.. program-output:: tail scripts/easybuild-all-modules.txt


Report Spack Modules (``buildtest module --spack``)
----------------------------------------------------

buildtest can detect `Spack <https://spack.readthedocs.io/en/latest/>`_ modules. A
spack module has a string to denote this module was created by spack with timestamp of module
creation. Shown below is an example::

    Module file created by spack (https://github.com/spack/spack) on 2019-04-11 11:38:31.191604


buildtest will search for string ``Module file created by spack`` in modulefile. buildtest
will run this for all modules in module trees defined by ``BUILDTEST_MODULEPATH``.


.. program-output:: cat scripts/spack-modules.txt

To retrieve all records ``spider`` to find all spack modules in your system
consider running ``BUILDTEST_SPIDER_VIEW=all buildtest module --spack``.

.. program-output:: cat scripts/spack-all-modules.txt

Parent Modules (``buildtest module --module-deps``)
-----------------------------------------------------

Parent modules are modules that set **MODULEPATH** in the modulefile. This
technique is used in **Hierarchical Module Naming Scheme** where modules like
compilers, mpi, numlibs expose new module trees. These modules are called
parent modules.

buildtest can report list of modules depended on a parent module. First,
buildtest will seek out all parent module from file
``BUILDTEST_ROOT/vars/modules.json``.

To seek out modules that depend on parent modules use the option
``buildtest module --module-deps`` or short option ``buildtest module -d``.

Shown below are the list of parent modules that can be used with
``buildtest module -d`` upon tab completion.

::

    (siddis14-TgVBs13r) buildtest-framework[master ?] $ buildtest module -d
    cctsoft                           eb/2018                           GCCcore/.6.2.0                    impi/2017.1.132                   OpenMPI/2.0.1                     RHEL6-apps
    CUDA/8.0.44                       GCC/5.4.0-2.27                    hpc/eb-2017-core                  medsci                            OpenMPI/2.0.2
    deprecated                        GCC/6.2.0-2.27                    icc/.2017.1.132-GCC-5.4.0-2.27    omics                             openmpi/.3.1.3-bs5h3cj
    eb/2017                           GCCcore/.5.4.0                    ifort/.2017.1.132-GCC-5.4.0-2.27  OpenMPI/2.0.0                     pharmsci

Shown below is a sample run for parent module ``OpenMPI/2.0.1``. buildtest
will report the content of the module file and list of modules that are
depended upon the module.

.. program-output:: cat scripts/parent-module.txt

