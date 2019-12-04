Building Test with Module Collections
======================================

building test with Lmod User Collection
-------------------------------------------

buildtest supports building test with Lmod `user collections <https://lmod
.readthedocs.io/en/latest/010_user.html#user-collections>`_. User collection comes in
handy when testing software with different module sets.

You can run ``module -t savelist`` to see a list of collection. Shown below
is an example::

    $ module -t savelist
    CUDA
    GCC
    GCCPy
    intel
    pgi

To restore a module collection you can run::

    module restore <collection-name>


To build a test with a user collection use the ``--collection`` option which
is a choice field that is the name of the user collection.
To demonstrate, lets build a test with a user collection ``CUDA``.

.. program-output:: cat scripts/build-lmod-collection-example.txt

Note the ``module restore`` command will load the modules from the
collection. To use this feature, you will need to have a module collection
which are typically stored in ``$HOME/.lmod.d/``

.. _build_with_module_collection:

building test with buildtest module collection
------------------------------------------------

buildtest module collection allows users to save modules into a collection
and reference them when building test. If you don't have a module collection first,
see :ref:`module_collection` before proceeding further.

Let's assume we have the following module collections available::

    $ buildtest module collection -l
    0: ['GCCcore/8.3.0', 'Python/3.7.4-GCCcore-8.3.0']
    1: ['bzip2/1.0.8-GCCcore-8.3.0', 'ncurses/6.1-GCCcore-8.3.0', 'libreadline/8.0-GCCcore-8.3.0', 'Tcl/8.6.9-GCCcore-8.3.0', 'SQLite/3.29.0-GCCcore-8.3.0', 'GMP/6.1.2-GCCcore-8.3.0', 'libffi/3.2.1-GCCcore-8.3.0', 'Python/3.7.4-GCCcore-8.3.0', 'zlib/1.2.11-GCCcore-6.4.0', 'binutils/2.28-GCCcore-6.4.0', 'GCC/6.4.0-2.28', 'numactl/2.0.11-GCCcore-6.4.0', 'GCCcore/6.4.0', 'XZ/5.2.3-GCCcore-6.4.0', 'libxml2/2.9.7-GCCcore-6.4.0', 'libpciaccess/0.14-GCCcore-6.4.0', 'hwloc/1.11.8-GCCcore-6.4.0', 'OpenMPI/2.1.2-GCC-6.4.0-2.28']

Each collection will have an index number that can be used to reference the modules
when building them. This can be done by using the option ``--module-collection <ID>`` or
short option ``-mc``. Let's build a test using collection **0**

.. program-output:: cat scripts/build-module-collection-example.txt


The option ``--module-collection`` takes an integer argument that is a
choice field prepopulated by calculating the total index from ``collection.json``

If you pass an invalid index, buildtest will report an error as follows

.. Error::

    buildtest build: error: argument -mc/--module-collection: invalid choice: -1 (choose from 0, 1, 2, 3)

Module Permutation
------------------

buildtest can build a test with all version of a module. What this means is if you are interested
in testing same test for all versions of a particular software you can do this in buildtest. For instance
you have the following versions of GCCcore module::

    $ module -t spider GCCcore
    GCCcore/6.4.0
    GCCcore/7.1.0
    GCCcore/7.4.0
    GCCcore/8.1.0
    GCCcore/8.3.0
    GCCcore/9.2.0

Now instead of loading each module or creating a module collection, you can do this by using option ``--modules <NAME>``
or short option ``-m <NAME>``. The **<NAME>** refers to the name of software similar to ``module -t spider <NAME>``
which is ``GCCcore``.

buildtest will formulate a modified json object stored ``$BUILDTEST_ROOT/var/modules.json`` that is used when finding
all versions of a module.

Let's build a module permutation test for ``GCCcore`` for the following build.

.. program-output:: cat scripts/build-module-permutation-example.txt
