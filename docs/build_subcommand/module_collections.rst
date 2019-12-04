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
    corrupt
    corrupt2
    default
    intelmpi

To restore a module collection you can run::

    module restore <collection-name>


To build a test with a user collection use the ``--collection`` option which
is a choice field that is the name of the user collection.
To demonstrate, lets build a test with a user collection ``intelmpi``.

.. program-output:: cat scripts/build-lmod-collection.txt

Note the ``module restore`` command will load the modules from the
collection. To use this feature, you will need to have a module collection
which are typically stored in ``$HOME/.lmod.d/``

.. _build_with_module_collection:

building test with buildtest module collection
------------------------------------------------

buildtest module collection allows users to save modules into a collection
and reference them when building test. If you don't have a module collection first,
see :ref:`module_collection` before proceeding further.

Let's assume we have the following module collections available

.. program-output:: cat docgen/module_collection_list_add.txt

Each collection will have an index number that can be used to reference the modules
when building them. This can be done by using the option ``--module-collection <ID>`` or
short option ``-mc``.

.. program-output:: cat scripts/build-openmpi-example1.txt


The option ``--module-collection`` takes an integer argument that is a
choice field prepopulated by finding the total index in the ``collection``
key in file ``collection.json``

If you pass an invalid index, buildtest will report an error as you can see

.. Error::

    buildtest build: error: argument -mc/--module-collection: invalid choice: -1 (choose from 0, 1, 2, 3)

Module Permutation
------------------

buildtest can build a single test configuration with all version of a module
. The ``spider`` utility by Lmod keeps track of metadata for all modules in
your system as a json object. buildtest will formulate a modified json
object that is written in ``$BUILDTEST_ROOT/var/modules.json``.

Here is an example json object for **intel**::

    "intel": {
        "/gpfs/apps/medsci/stacks/noOS/modules/intel/2018.3": {
            "fullName": "intel/2018.3",
            "parent": [
                [
                    "medsci/.2019.1"
                ],
                [
                    "medsci/2019.2"
                ]
            ]
        },
        "/gpfs/apps/easybuild/2019/SkyLake/redhat/7.5/modules/all/intel/2018b.lua": {
            "fullName": "intel/2018b",
            "parent": [
                [
                    "eb/2019"
                ]
            ]
        }
    },

Shown below is a list of intel modules available in this system::

    $ module -t spider intel
    intel/2018b
    intel/2018.3



To demonstrate an example, let's build a test using the module permutation
option ``--modules`` on all ``intel`` modules.

.. program-output:: cat scripts/build-module-permute.txt

Each test will be uniquely identified with a 128 random number in the test
script to avoid name conflicts.

In this example, buildtest is building the test for every ``intel`` modules
found in the system.



buildtest will select the ``first`` parent combination should there be
multiple parent combination to load the module. This is controlled by variable
``BUILDTEST_PARENT_MODULE_SEARCH`` that is defined in configuration file.

The default configuration for ``BUILDTEST_PARENT_MODULE_SEARCH`` is ``first``
which will select the first parent combination. The other option is ``all`` which
will select all parent combination when building test.

Shown below is a snapshot of ``vmd`` record from ``modules.json``::


    "vmd": {
        "/gpfs/apps/medsci/stacks/noOS/modules/vmd/1.9.4.lua": {
            "fullName": "vmd/1.9.4",
            "parent": [
                [
                    "medsci/.2019.1"
                ],
                [
                    "medsci/2019.2"
                ]
            ]
        }
    },



The ``fullName`` and ``parent`` key define how to load a module with all the
parent combinations which you are required in order to load the desired
module.

To demonstrate let's build a test with all parent combination for ``vmd``
module.

.. program-output:: cat scripts/build-module-all-permute.txt

Note all parent combination for ``vmd`` module were
used when writing the test. It is worth noting, that *any parent combination
is sufficient* when loading the desired module.
