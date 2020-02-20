.. _spider:

Understanding Lmod Spider
=================================

This section will cover the fundamentals of how Lmod spider interacts with buildtest. Before you proceed with next
section read the spider `documentation <https://lmod.readthedocs.io/en/latest/136_spider.html>`_ first.


How buildtest implements its module operations
------------------------------------------------

buildtest is able to implement some high-level :ref:`module_operation` such as

- Automating Module Load Test

- Listing of all modules and module file path and sub-trees

- Detect easybuild/spack modules

- List unique software names

- List of all parent modules

- Report all child modules for a given parent

All of this is possible with the help of ``spider``. buildtest will invoke the following command::

  $LMOD_DIR/spider -o spider-json $BUILDTEST_MODULEPATH

buildtest will cache the content of spider in a json file that can be found in root of buildtest under ``var/spider.json``.
This allows bulidtest to process spider record from a single file which is faster as pose to running **spider** command
every time. Almost all operations under ``buildtest module`` rely on spider.

Whenever there is a change to ``BUILDTEST_MODULEPATH`` in configuration, buildtest will rewrite the ``var/spider.json``.
Changes to BUILDTEST_MODULEPATH are done with any of the commands::

    buildtest module tree -a <tree>
    buildtest module tree -s <tree>
    buildtest module tree -r <tree>

If you remove the ``var/spider.json`` file, buildtest will detect it and recreate the file upon next command. buildtest
provides BUILDTEST_MODULEPATH so that user can alter the module trees without changing ``MODULEPATH`` on the system and
potentially corrupt their environment after several changes.

Spider Content
---------------

Shown below is an example spider record for ``flex``

.. code-block::
   :emphasize-lines: 1,2,16-20,22
   :linenos:

    "flex": {
            "/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Compiler/GCCcore/8.1.0/flex/2.6.4.lua": {
                "pV": "000000002.000000006.000000004.*zfinal",
                "Description": "Flex (Fast Lexical Analyzer) is a tool for generating scanners. A scanner, \n sometimes called a tokenizer, is a program which recognizes lexical patterns\n in text.\n",
                "URL": "http://flex.sourceforge.net/",
                "pathA": {
                    "/mxg-hpc/users/ssi29/easybuild-HMNS/software/flex/2.6.4-GCCcore-8.1.0/bin": 1
                },
                "whatis": [
                    "Description: \n Flex (Fast Lexical Analyzer) is a tool for generating scanners. A scanner, \n sometimes called a tokenizer, is a program which recognizes lexical patterns\n in text.\n",
                    "Homepage: http://flex.sourceforge.net/",
                    "URL: http://flex.sourceforge.net/"
                ],
                "wV": "000000002.000000006.000000004.*zfinal",
                "Version": "2.6.4",
                "parentAA": [
                    [
                        "GCCcore/8.1.0"
                    ]
                ],
                "hidden": false,
                "fullName": "flex/2.6.4",
                "help": "\nDescription\n===========\nFlex (Fast Lexical Analyzer) is a tool for generating scanners. A scanner, \n sometimes called a tokenizer, is a program which recognizes lexical patterns\n in text.\n\n\nMore information\n================\n - Homepage: http://flex.sourceforge.net/\n",
                "lpathA": {
                    "/mxg-hpc/users/ssi29/easybuild-HMNS/software/flex/2.6.4-GCCcore-8.1.0/lib": 1
                }
            },
         "/mxg-hpc/users/ssi29/easybuild/modules/all/flex/2.6.4-GCCcore-8.3.0.lua": {
         ...
        }
    }


The top-level key ``flex`` is the unique software name. buildtest can report unique software name by listing all top-level keys
via ``buildtest module -s``. Each key inside ``flex`` is a full path to a module file followed by key/value assignment to
extract details for a specific module file. The full path to module file and ``fullName`` are used to implement the module
list feature ``buildtest module list``.

The full canonical name for module file is defined by ``fullName`` which is the command user must issue to load the module, in
this case ``module load flex/2.6.4``. However, if the record contains ``parentAA``, then user must load the parent modules
before loading ``flex/2.6.4``. The parentAA is a nested list where each list is a set of parent modules to load before loading
flex/2.6.4.

A parent module - is a module that sets MODULEPATH to another tree (sub-tree) often used in **Hierarchical Module Naming Scheme** (HMNS).
The flex module is built with easybuild and the path **/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Compiler/GCCcore/8.1.0/**
is where you will find software built with ``GCCcore/8.1.0`` module.

We can confirm this by viewing content of GCCcore/8.1.0 module (``module show GCCcore/8.1.0``)
and we see that MODULEPATH  is set to the sub-tree where ``flex/2.6.4`` module resides::

    prepend_path("MODULEPATH","/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Compiler/GCCcore/8.1.0")

Now that we have some understanding of how parent modules work in relation to how modules are loaded, buildtest is
able to list all parent modules by parsing ``parentAA`` record. buildtest will add each record in a set to avoid duplicates,
since there are bound to be many parent module entries from a single parent module. Most likely, the parent modules
at any site would be the Compilers + MPI modules and this is true if you build software using easybuild or spack with hierarchical
module naming scheme.


There will be some records that **dont** have a ``parentAA`` field for example the GCCcore/8.1.0 spider record

.. code-block::
   :linenos:

    "/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core/GCCcore/8.1.0.lua": {
        "pV": "000000008.000000001.*zfinal",
        "Description": "The GNU Compiler Collection includes front ends for C, C++, Objective-C, Fortran, Java, and Ada,\n as well as libraries for these languages (libstdc++, libgcj,...).",
        "URL": "http://gcc.gnu.org/",
        "pathA": {
            "/mxg-hpc/users/ssi29/easybuild-HMNS/software/GCCcore/8.1.0/bin": 1
        },
        "whatis": [
            "Description: The GNU Compiler Collection includes front ends for C, C++, Objective-C, Fortran, Java, and Ada,\n as well as libraries for these languages (libstdc++, libgcj,...).",
            "Homepage: http://gcc.gnu.org/",
            "URL: http://gcc.gnu.org/"
        ],
        "wV": "000000008.000000001.*zfinal",
        "Version": "8.1.0",
        "hidden": false,
        "fullName": "GCCcore/8.1.0",
        "help": "\nDescription\n===========\nThe GNU Compiler Collection includes front ends for C, C++, Objective-C, Fortran, Java, and Ada,\n as well as libraries for these languages (libstdc++, libgcj,...).\n\n\nMore information\n================\n - Homepage: http://gcc.gnu.org/\n",
        "lpathA": {
            "/mxg-hpc/users/ssi29/easybuild-HMNS/software/GCCcore/8.1.0/lib": 1,
            "/mxg-hpc/users/ssi29/easybuild-HMNS/software/GCCcore/8.1.0/lib64": 1,
            "/mxg-hpc/users/ssi29/easybuild-HMNS/software/GCCcore/8.1.0/lib/gcc/x86_64-pc-linux-gnu/8.1.0": 1
        }
    },

In this case, this module can be loaded directly, buildtest will detect which records have ``parentAA`` when generating
the module command.

What does this solve?
----------------------

buildtest is able to leverage spider to figure out how to load modules inside test. Let's face it, module names can be long
especially in Flat Naming Scheme, or spack `modules <https://spack.readthedocs.io/en/latest/module_file_support.html>`_ with long hash
which makes it difficult to hard-code module names in test configuration. buildtest is able to find the full module name
and keep test configuration as simple as possible and solves the module load problem.






