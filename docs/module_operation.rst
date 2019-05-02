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

Module Trees Operation
-----------------------

buildtest supports adding, removing and listing module trees. Internally, buildtest
is modifying ``BUILDTEST_MODULEPATH`` which is synonymous to ``MODULEPATH`` though,
buildtest makes use of ``BUILDTEST_MODULEPATH`` when querying modules using ``spider``
command.

At your site, you may be interested in testing software by each stack.

By default, ``BUILDTEST_MODULEPATH`` is set to an empty list ``[]`` in configuration
file ``$HOME/.buildtest/settings.yml``. In this case, ``BUILDTEST_MODULEPATH``
will read from ``MODULEPATH``.

Listing Module Tree
~~~~~~~~~~~~~~~~~~~~

To list the module trees in buildtest you can run ``buildtest module -l`` which
shows one module tree per line

.. code-block:: console

    $ buildtest module -l
    /nfs/grid/software/moduledomains
    /etc/modulefiles
    /usr/share/modulefiles
    /usr/share/lmod/lmod/modulefiles/Core

For this run, ``BUILDTEST_MODULEPATH`` is not set in configuration file so it is
reading from ``MODULEPATH``

.. code-block:: console

    $ cat ~/.buildtest/settings.yml  | grep -i BUILDTEST_MODULEPATH
    BUILDTEST_MODULEPATH: []

Adding Module Tree
~~~~~~~~~~~~~~~~~~~~

You can add new module tree through command line using ``buildtest module -a /path/to/tree``
which will update the configuration file::

    $ buildtest module -a /usr/share/lmod/lmod/modulefiles/Core
    Adding module tree: /usr/share/lmod/lmod/modulefiles/Core
    Configuration File: /home/siddis14/.buildtest/settings.yml has been updated


Removing Module Tree
~~~~~~~~~~~~~~~~~~~~~

Similarly you can remove module tree from your configuration via ``buildtest module -r /path/to/tree``::

    (siddis14-TgVBs13r) buildtest-framework[master !?] $ buildtest module -r /etc/modulefiles
    Removing module tree: /etc/modulefiles
    Configuration File: /home/siddis14/.buildtest/settings.yml has been updated


Report Easybuild Modules
--------------------------

buildtest can detect modules that are built by `Easybuild <https://easybuild.readthedocs.io/en/latest/>`_.
An easybuild module will contain a string in module file as follows::

    Built with EasyBuild version 3.7.1

buildtest will check all module trees defined by ``BUILDTEST_MODULEPATH`` and search
for string without the version number. To enable this feature you can
run ``buildtest module -eb`` or long option ``buildtest module --easybuild``.

Shown below is the ``tail`` output of the command.

.. program-output:: tail scripts/easybuild-modules.txt

Report Spack Modules
--------------------

buildtest can detect `Spack <https://spack.readthedocs.io/en/latest/>`_ modules. A
spack module has a string to denote this module was created by spack with timestamp of module
creation. Shown below is an example::

    Module file created by spack (https://github.com/spack/spack) on 2019-04-11 11:38:31.191604


buildtest will search for string ``Module file created by spack`` in modulefile. buildtest
will run this for all modules in module trees defined by ``BUILDTEST_MODULEPATH``.




