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

To demonstrate let's kick off a module load test as shown below.

.. program-output:: cat scripts/module-load.txt


buildtest will attempt to run ``module load`` against each module to verify modules are working properly.

You may specify additional module trees using ``BUILDTEST_MODULEPATH`` for
module testing.

If you want to test all modules that were detected by ``spider`` utility,
you can set ``BUILDTEST_SPIDER_VIEW=all`` in your configuration or
environment variable or just run as follows::


    BUILDTEST_SPIDER_VIEW=all buildtest module loadtest

This will test all modules retrieved by spider utility.

Module Collection Operation (``buildtest module collection``)
-------------------------------------------------------------

buildtest keeps track of its own module collection which is stored in
``BUILDTEST_ROOT/vars/collection.json``. This file is  maintained
by buildtest when using ``buildtest module collection`` commands.

buildtest supports adding, removing, updating and listing module collection.
This is synonymous to using user collection from Lmod (i.e ``module save <collection>``).

Shown below is a usage of module collection options in buildtest.

.. program-output:: cat scripts/buildtest-module-collection-help.txt


Adding a module collection (``buildtest module collection -a``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add a module collection, just load modules in your shell environment and
run the following::

    $ buildtest module collection -a

Shown below is an example output

.. program-output:: cat scripts/buildtest-module-collection-add.txt

Once modules are added, you may build a test using a module collection using the
option ``buildtest build --module-collection <ID>``. The <ID> is the index number to reference
the module collection since there can be more than one module collection.


List all module collection (``buildtest module collection -l``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can report a list of all module collections that is easy to interpret
as pose to reading a json file. To get a list of all module collection run the following::

    $ buildtest module collection -l

Shown below is an example output

.. program-output:: cat scripts/buildtest-module-collection-list.txt


Removing a module collection (``buildtest module collection -r <ID>``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To remove a module collection, you will need to specify the index number to the ``-r`` option.
One can check the module collection index by listing module collection using **buildtest module collection -l**.

In this example we will remove module collection **2** as shown below.

.. program-output:: cat scripts/buildtest-module-collection-remove.txt

buildtest will remove the index and update the json file. Note all existing module collection
will update their collection index depending what index number was removed.

Updating a module collection (``buildtest module collection -u <ID>``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to update an existing module collection, just load the modules of interest in
your user environment and buildtest will override them. To update a module collection you will
need the index number of module collection and use the ``-u <INDEX>`` to update the module collection.

Shown below is a listing of module collection and we would like to update index 2 by replacing module ``cmd``
with ``gcc`` module. Shown below is our list of module collections.

.. program-output:: cat scripts/buildtest-module-collection-list-before-update.txt

To perform the update we have the following active modules::

    $ module list

    Currently Loaded Modules:
      1) DefaultModules   2) shared   3) slurm/17.11.8   4) gcc/7.2.0

Now we are ready to update the module collection as shown below

.. program-output:: cat scripts/buildtest-module-collection-update.txt

Module Trees Operation (``buildtest module tree``)
---------------------------------------------------

buildtest supports adding, removing, listing, and setting module trees. Internally, buildtest
is modifying BUILDTEST_MODULEPATH which is synonymous to MODULEPATH though,
buildtest makes use of ``BUILDTEST_MODULEPATH`` when querying modules from ``spider``
command.

At your site, you will need to alter BUILDTEST_MODULEPATH to the root of your module trees where
software stack is present.

By default, BUILDTEST_MODULEPATH is set to an empty list ``[]`` in configuration
file ``$HOME/.buildtest/settings.yml``. In this case, BUILDTEST_MODULEPATH will read
from ``MODULEPATH``.

One could edit the configuration file manually; however, it's preferable to use
``buildtest module tree`` commands to alter BUILDTEST_MODULEPATH to avoid syntax error in
configure file which can break buildtest functionality.

Shown below is a usage of ``buildtest module tree`` command.

.. program-output:: cat scripts/module_tree_help.txt


Listing Module Trees (``buildtest module tree -l``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the module trees in buildtest you can run ``buildtest module tree -l``
which shows one module tree per line

.. program-output:: cat scripts/module_tree_list.txt

For this run, ``BUILDTEST_MODULEPATH`` is not set in configuration file so it is
reading from ``MODULEPATH``

.. code-block:: console

    $ cat ~/.buildtest/settings.yml  | grep -i BUILDTEST_MODULEPATH
    BUILDTEST_MODULEPATH: []

Adding a Module Tree (``buildtest module tree -a``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add new module tree through command line using ``buildtest module
tree -a /path/to/tree`` which will update the configuration file. Use this option
to add software stack into buildtest environment for testing purposes.

.. program-output:: cat scripts/module_tree_add.txt


Removing a Module Tree (``buildtest module tree -r``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly you can remove module tree from your configuration via ``buildtest module tree -r /path/to/tree``.
Use this option to remove a software stack from buildtest environment.

.. program-output:: cat scripts/module_tree_rm.txt

Setting a Module Tree (``buildtest module tree -s``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can set BUILDTEST_MODULEPATH to a tree which will override current value. For instance
you have the following module trees in buildtest

.. program-output:: cat scripts/module_tree_list.txt

Now if we want to set BUILDTEST_MODULEPATH to a tree, let's assume **/usr/share/lmod/lmod/modulefiles/Core** we
can do that as follows

.. program-output:: cat scripts/module_tree_set.txt

Next we can check the list of module trees by issuing the following::

    $ buildtest module tree -l
    /usr/share/lmod/lmod/modulefiles/Core


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

Shown below is a sample run for parent module ``shared``. buildtest
will report the content of the module file and list of modules that are
depended upon the module.

.. program-output:: cat scripts/parent-module.txt

buildtest will auto-populate the choice field for option ``-d`` that is a list of parent modules. If you
are unsure which parent module to choose, just press TAB to get a list of parent modules.



