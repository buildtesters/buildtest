Concepts
=========

Modules
---------

buildtest will detect modules installed in your system with the help of
Lmod utility (``spider``). For background details on **spider** check the
official documentation: https://lmod.readthedocs.io/en/latest/136_spider.html

buildtest will run the following command during the setup::

    $LMOD_DIR/spider -o spider-json $BUILDTEST_MODULEPATH

The above output is not readable since it is in json so you can pipe this to
the following::

    $LMOD_DIR/spider -o spider-json $BUILDTEST_MODULEPATH | python -m json.tool

In buildtest we make use of `json <https://docs.python.org/3/library/json
.html>`_ library to convert output to json. The output will look something
like this::

    "libffi": {
        "/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all/libffi/3.2.1-GCCcore-6.4.0.lua": {
            "path": "/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all/libffi/3.2.1-GCCcore-6.4.0.lua",
            "Description": "The libffi library provides a portable, high level programming interface to\n various calling conventions. This allows a programmer to call any function\n specified by a call interface description at run-time.\n",
            "name_lower": "libffi",
            "parent": [
                "default:eb/2018"
            ],
            "epoch": 1528138610,
            "full": "libffi/3.2.1-GCCcore-6.4.0",
            "full_lower": "libffi/3.2.1-gcccore-6.4.0",
            "name": "libffi",
            "help": "\nDescription\n===========\nThe libffi library provides a portable, high level programming interface to\n various calling conventions. This allows a programmer to call any function\n specified by a call interface description at run-time.\n\n\nMore information\n================\n - Homepage: http://sourceware.org/libffi/\n",
            "markedDefault": false,
            "whatis": [
                "Description: \n The libffi library provides a portable, high level programming interface to\n various calling conventions. This allows a programmer to call any function\n specified by a call interface description at run-time.\n",
                "Homepage: http://sourceware.org/libffi/"
            ]
        },
        "/nfs/grid/software/RHEL7/easybuild/modules/all/MPI/intel-CUDA/2017.1.132-GCC-5.4.0-2.27-8.0.44/impi/2017.1.132/libffi/.3.2.1.lua": {
            "path": "/nfs/grid/software/RHEL7/easybuild/modules/all/MPI/intel-CUDA/2017.1.132-GCC-5.4.0-2.27-8.0.44/impi/2017.1.132/libffi/.3.2.1.lua",
            "Description": "The libffi library provides a portable, high level programming interface to various calling\nconventions. This allows a programmer to call any function specified by a call interface description at run-time.",
            "name_lower": "libffi",
            "parent": [
                "default:eb/2017:icc/.2017.1.132-GCC-5.4.0-2.27:CUDA/8.0.44:impi/2017.1.132",
                "default:eb/2017:ifort/.2017.1.132-GCC-5.4.0-2.27:CUDA/8.0.44:impi/2017.1.132",
                "default:icc/.2017.1.132-GCC-5.4.0-2.27:CUDA/8.0.44:impi/2017.1.132",
                "default:ifort/.2017.1.132-GCC-5.4.0-2.27:CUDA/8.0.44:impi/2017.1.132",
                "default:medsci:hpc/eb-2017-core:icc/.2017.1.132-GCC-5.4.0-2.27:CUDA/8.0.44:impi/2017.1.132",
                "default:medsci:hpc/eb-2017-core:ifort/.2017.1.132-GCC-5.4.0-2.27:CUDA/8.0.44:impi/2017.1.132"
            ],
            "epoch": 1505283586,
            "full": "libffi/.3.2.1",
            "full_lower": "libffi/.3.2.1",
            "name": "libffi",
            "help": "\nDescription\n===========\nThe libffi library provides a portable, high level programming interface to various calling\nconventions. This allows a programmer to call any function specified by a call interface description at run-time.\n\n\nMore information\n================\n - Homepage: http://sourceware.org/libffi/\n",
            "markedDefault": false,
            "whatis": [
                "Description: The libffi library provides a portable, high level programming interface to various calling\nconventions. This allows a programmer to call any function specified by a call interface description at run-time.",
                "Homepage: http://sourceware.org/libffi/"
            ]
        }
    }


.. Note:: Please note the output above is from Lmod 6, there are slight difference in the format in Lmod 7 that we will discuss later

In buildtest this is handled by class ``BuildTestModule``. The spider output
returns a dictionary that contains details of all modules based on MODULEPATH,
along with full path to module files, and the metadata for a module.
This captures all the details that you may get when running ``module spider``.

Get Unique Software
~~~~~~~~~~~~~~~~~~~~

To get a list of unique software you could run ``module -t spider``::

    $ module -t spider | head -n 10
    20140726
    2015-workaround
    20150316
    2016-01-x64
    3212u1
    Advisor/
    Advisor/2017_update1
    Amber/
    Amber/14-AmberTools-15-patchlevel-13-13
    Anaconda2/
    Anaconda2/4.2.0
    Anaconda2/5.1.0
    Anaconda3/
    Anaconda3/4.2.0
    Anaconda3/5.1.0
    Aspera-Connect/
    Aspera-Connect/3.6.1


Though ``module -t spider`` gives you the output it is not the best way to
retrieve the result but rather use the ``spider`` utility. In buildtest you
can get this by calling ``BuildTestModules`` class and invoke the method
``get_unique_modules`` as shown below


.. code-block:: python

    module = BuildTestModule()
    module.get_unique_modules()

The method ``get_unique_modules()`` is returning the keys from the dictionary. It checks
if abspath of module is in one of the module trees in ``BUILDTEST_MODULEPATH``
so that it retrieves unique module only defined by ``BUILDTEST_MODULEPATH``. Typically,
``spider`` will retrieve all modules that may belong to other module trees and we
dont want that.

.. code-block:: python

      def get_unique_modules(self):
        """Return a list of unique full name canonical modules """
        unique_modules_set = set()
        for module in self.module_dict.keys():
            for mpath in self.module_dict[module].keys():
                for tree in config_opts["BUILDTEST_MODULEPATH"]:
                    if tree in mpath:
                        unique_modules_set.add(module)
                        break
        return sorted(list(unique_modules_set))

The above method is typically used by ``buildtest list --software`` to return
a list of unique software.

Get Unique Module Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When users load modules (``module load GCC/5.4.0``) they are loading a specific
software-version. Even when user does ``module load GCC`` without a version.
Lmod will resolve to the default version even if user doesn't specify this.


.. code-block:: python

        module = BuildTestModule()
        module.get_unique_fname_modules()

The method ``get_unique_fname_modules()`` returns a sorted list of module
full name. Recall from the dictionary we are retrieving the keyword ``full``
from the dictionary

.. code-block:: console
    :linenos:
    :emphasize-lines: 9

    "/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all/libffi/3.2.1-GCCcore-6.4.0.lua": {
            "path": "/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all/libffi/3.2.1-GCCcore-6.4.0.lua",
            "Description": "The libffi library provides a portable, high level programming interface to\n various calling conventions. This allows a programmer to call any function\n specified by a call interface description at run-time.\n",
            "name_lower": "libffi",
            "parent": [
                "default:eb/2018"
            ],
            "epoch": 1528138610,
            "full": "libffi/3.2.1-GCCcore-6.4.0",
            "full_lower": "libffi/3.2.1-gcccore-6.4.0",
            "name": "libffi",
            "help": "\nDescription\n===========\nThe libffi library provides a portable, high level programming interface to\n various calling conventions. This allows a programmer to call any function\n specified by a call interface description at run-time.\n\n\nMore information\n================\n - Homepage: http://sourceware.org/libffi/\n",
            "markedDefault": false,
            "whatis": [
                "Description: \n The libffi library provides a portable, high level programming interface to\n various calling conventions. This allows a programmer to call any function\n specified by a call interface description at run-time.\n",
                "Homepage: http://sourceware.org/libffi/"
            ]
        },

The implementation of ``get_unique_fname_modules()`` is shown below.

.. code-block:: python

       def get_unique_fname_modules(self):
        """Return a list of unique canonical fullname of module
        where abspath to module is in one of the
        directories defined by BUILDTEST_MODULEPATH"""
        software_set = set()

        for module in self.get_unique_modules():
            for mpath in self.module_dict[module].keys():
                fname = ""
                if self.major_ver == 6:
                    fname = self.module_dict[module][mpath]["full"]
                elif self.major_ver == 7:
                    fname = self.module_dict[module][mpath]["fullName"]

                # only add module files that belong in directories specified
                #  by BUILDTEST_MODULEPATH.
                for tree in config_opts["BUILDTEST_MODULEPATH"]:
                    if tree in mpath:
                        software_set.add(fname)
                        break

        return sorted(list(software_set))

Also note we make use of set to avoid duplicate entries and only add modules to
set whose filepath is in ``BUILDTEST_MODULEPATH``.

.. note:: Lmod 6 and 7 have some difference in the dictionary, just to name a
    few. The key ``full`` has been changed to ``fullName`` in Lmod 7. Here is an example
    dictionary format from Lmod 7

.. code-block:: console
    :linenos:
    :emphasize-lines: 19

         "gompi": {
            "/gpfs/apps/easybuild/2019/SkyLake/redhat/7.5/modules/all/gompi/2018b.lua": {
                "pV": "000002018.*b.*zfinal",
                "Description": "GNU Compiler Collection (GCC) based compiler toolchain,\n including OpenMPI for MPI support.",
                "whatis": [
                    "Description: GNU Compiler Collection (GCC) based compiler toolchain,\n including OpenMPI for MPI support.",
                    "Homepage: (none)"
                ],
                "wV": "000002018.*b.*zfinal",
                "help": "\nDescription\n===========\nGNU Compiler Collection (GCC) based compiler toolchain,\n including OpenMPI for MPI support.\n\n\nMore information\n================\n - Homepag
    e: (none)\n",
                "parentAA": [
                    [
                        "eb/2019"
                    ]
                ],
                "hidden": false,
                "Version": "2018b",
                "fullName": "gompi/2018b"
            }
        },


Due to this slight change, buildtest will check the Lmod version before
checking for the full module name retrieved by key ``full`` in Lmod 6 or
``fullName`` in Lmod 7.

Module File Path
~~~~~~~~~~~~~~~~~

To retrieve the absolute path to a module file you can retrieve the inner keys.
The dictionary is categorized by software and each key represents full path
to module file.

The lines of interest are the following

.. code-block:: console
    :linenos:
    :emphasize-lines: 2,5,10

    "Autoconf": {
        "/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all/Autoconf/2.69-GCCcore-6.4.0.lua": {
            <METADATA>
        },
        "/nfs/grid/software/RHEL7/easybuild/modules/all/Compiler/GCC/5.4.0-2.27/Autoconf/.2.69.lua": {
            <METADATA>
        }
    }
     "Automake": {
        "/clust/app/easybuild/2018/Broadwell/redhat/7.3/modules/all/Automake/1.15.1-GCCcore-6.4.0.lua": {
            <METADATA>
        }
    }


Implementation for ``get_modulefile_path()`` is described below.

.. code-block:: python

      def get_modulefile_path(self):
        """Return a list of absolute path for all module files"""
        module_path_list  = []
        for k in self.get_unique_modules():
            for tree in config_opts["BUILDTEST_MODULEPATH"]:
                for mpath in self.module_dict[k].keys():
                    if tree in mpath:
                        module_path_list.append(mpath)

        return module_path_list

This method is used to return a list of modulefile paths in ``BUILDTEST_MODULEPATH``.


Get Parent Modules
~~~~~~~~~~~~~~~~~~~

Parent modules are modules that need to be loaded first before loading the
module of interest. In *Hiearchical Module Naming Scheme* you will have some
modules that load another module tree (**MODULEPATH**) typically these are
set in compilers, mpi, numlibs modules.

Luckily ``spider`` has way to retrieve parent modules for any module
defined by the key ``parent`` in the json object.

.. code-block:: console
    :linenos:
    :emphasize-lines: 10-13

    "/nfs/grid/software/RHEL7/easybuild/modules/all/MPI/GCC/5.4.0-2.27/OpenMPI/2.0.0/zlib/.1.2.8.lua": {
            "Description": "zlib is designed to be a free, general-purpose, legally unencumbered -- that is,\n not covered by any patents -- lossless data-compression library for use on virtually any\n computer hardware and operating system.",
            "epoch": 1506614076,
            "full": "zlib/.1.2.8",
            "full_lower": "zlib/.1.2.8",
            "help": "\nDescription\n===========\nzlib is designed to be a free, general-purpose, legally unencumbered -- that is,\n not covered by any patents -- lossless data-compression library for use on virtually any\n computer hardware and operating system.\n\n\nMore information\n================\n - Homepage: http://www.zlib.net/\n",
            "markedDefault": false,
            "name": "zlib",
            "name_lower": "zlib",
            "parent": [
                "default:eb/2017:GCC/5.4.0-2.27:OpenMPI/2.0.0",
                "default:medsci:hpc/eb-2017-core:GCC/5.4.0-2.27:OpenMPI/2.0.0"
            ],
            "path": "/nfs/grid/software/RHEL7/easybuild/modules/all/MPI/GCC/5.4.0-2.27/OpenMPI/2.0.0/zlib/.1.2.8.lua",
            "whatis": [
                "Description: zlib is designed to be a free, general-purpose, legally unencumbered -- that is,\n not covered by any patents -- lossless data-compression library for use on virtually any\n computer hardware and operating system.",
                "Homepage: http://www.zlib.net/"
            ]
        },

.. Note:: The output above is from Lmod 6 and ``parent`` key is one of those
 keys that has changed in Lmod 7 which will be discussed later

In this example, the module ``zlib/.1.2.8`` is in a Hierarchical Tree built
by ``GCC/5.4.0`` and ``OpenMPI/2.0.0``. The ``parent`` key is a list of
different module combination that can be used to load this module.

Shown below is one way to load ``zlib/.1.2.8`` using the first combination
of parent modules.

.. code-block:: console

    buildtest-framework[master !?] $ ml
    No modules loaded
    buildtest-framework[master !?] $ ml eb/2017 GCC/5.4.0-2.27 OpenMPI/2.0.0 zlib/.1.2.8
    buildtest-framework[master !?] $ ml

    Currently Loaded Modules:
      1) eb/2017          3) binutils/.2.27   5) numactl/2.0.11   7) OpenMPI/2.0.0                  9) FFTW/3.3.4                                    11) zlib/.1.2.8
      2) GCCcore/.5.4.0   4) GCC/5.4.0-2.27   6) hwloc/1.11.3     8) OpenBLAS/0.2.19-LAPACK-3.6.0  10) ScaLAPACK/2.0.2-OpenBLAS-0.2.19-LAPACK-3.6.0

We can confirm this by running the second parent combination to load ``zlib/.1.2.8``

.. code-block:: console

    (siddis14-TgVBs13r) docs[master !?] $ ml
    No modules loaded
    (siddis14-TgVBs13r) docs[master !?] $ ml medsci hpc/eb-2017-core GCC/5.4.0-2.27 OpenMPI/2.0.0 zlib/.1.2.8
    (siddis14-TgVBs13r) docs[master !?] $ ml

    Currently Loaded Modules:
      1) medsci             3) GCCcore/.5.4.0   5) GCC/5.4.0-2.27   7) hwloc/1.11.3    9) OpenBLAS/0.2.19-LAPACK-3.6.0  11) ScaLAPACK/2.0.2-OpenBLAS-0.2.19-LAPACK-3.6.0
      2) hpc/eb-2017-core   4) binutils/.2.27   6) numactl/2.0.11   8) OpenMPI/2.0.0  10) FFTW/3.3.4                    12) zlib/.1.2.8


Recall in Lmod 6, ``parent`` is a list with modules separated by colon
separator (``:``) and each entry starts with word ``default``.

In Lmod 7 the parent key is renamed to ``parentAA`` see below

.. code-block:: console
    :linenos:
    :emphasize-lines: 12-16

         "gompi": {
            "/gpfs/apps/easybuild/2019/SkyLake/redhat/7.5/modules/all/gompi/2018b.lua": {
                "pV": "000002018.*b.*zfinal",
                "Description": "GNU Compiler Collection (GCC) based compiler toolchain,\n including OpenMPI for MPI support.",
                "whatis": [
                    "Description: GNU Compiler Collection (GCC) based compiler toolchain,\n including OpenMPI for MPI support.",
                    "Homepage: (none)"
                ],
                "wV": "000002018.*b.*zfinal",
                "help": "\nDescription\n===========\nGNU Compiler Collection (GCC) based compiler toolchain,\n including OpenMPI for MPI support.\n\n\nMore information\n================\n - Homepag
    e: (none)\n",
                "parentAA": [
                    [
                        "eb/2019"
                    ]
                ],
                "hidden": false,
                "Version": "2018b",
                "fullName": "gompi/2018b"
            }
        },


The ``parentAA`` is now a **list of list** where each list corresponds to a
set of parent modules to be loaded before loading actual module.


In buildtest we can get the parent for any module with the following code

.. code-block:: python

    module_name = "GCC/5.4.0-2.27"
    module = BuildTestModule
    parent_module = module.get_parent_modules(module_name)

The method ``get_parent_modules`` returns a list of modules to be loaded for
the specified module. In the implementation we only get the first parent
combination of modules.

The implementation for ``get_parent_modules`` can be shown below

.. code-block:: python

     def get_parent_modules(self,modname):
        """Get Parent module for specified module file."""
        for key in self.module_dict.keys():
            for mod_file in self.module_dict[key].keys():
                mod_full_name = parent_mod_name = ""

                if self.major_ver == 6:
                    mod_full_name = self.module_dict[key][mod_file]["full"]
                elif self.major_ver == 7:
                    mod_full_name = self.module_dict[key][mod_file]["fullName"]

                if modname == mod_full_name:
                    if self.major_ver == 6:
                        parent_mod_name = self.module_dict[key][mod_file]["parent"]
                    elif self.major_ver == 7:
                        # for modules that dont have any parent the dictionary
                        # does not declare parentAA key in Lmod 7. in that
                        # case return empty list
                        if "parentAA" not in self.module_dict[key][mod_file]:
                            parent_mod_name = []
                        # otherwise retrieve first index from parentAA.
                        # ParentAA is a list of list
                        else:
                            parent_mod_name = self.module_dict[key][mod_file]["parentAA"][0]

                        return parent_mod_name

                    mod_parent_list = parent_mod_name
                    parent_module = []
                    # parent: is a list, only care about one entry which
                    # contain list of modules to be loaded separated by :
                    # First entry is default:<mod1>:<mod2> so skip first
                    # element
                    for entry in mod_parent_list[0].split(":")[1:]:
                        parent_module.append(entry)

                    return parent_module

        return []

How does buildtest leverage modules
------------------------------------

buildtest will inject modules when writing test script. When you build a test
from a configuration file you can load modules into
your test script. See :ref:`Testing_With_Modules` for more details.


For instance, running a binary test such as the utility ``ompi_info`` from
OpenMPI can be done by loading the openmpi module and running the binary
test via ``buildtest build --binary`` or set ``BUILDTEST_BINARY=True``.

Below is a list of modules when loading openmpi

::

    (siddis14-TgVBs13r) buildtest-framework[master !?+] $ ml

    Currently Loaded Modules:
      1) eb/2018         3) binutils/2.28-GCCcore-6.4.0   5) zlib/1.2.11-GCCcore-6.4.0      7) hwloc/1.11.8-GCCcore-6.4.0
      2) GCCcore/6.4.0   4) GCC/6.4.0-2.28                6) numactl/2.0.11-GCCcore-6.4.0   8) OpenMPI/3.0.0-GCC-6.4.0-2.28

Let's run the binary test, buildtest will attempt to test every module.

::

    (siddis14-TgVBs13r) buildtest-framework[master !?+] $ buildtest build -b
    Detecting Software:eb/2018
    No $PATH set in your module  eb/2018   so no possible binaries can be found
    There are no binaries for package: eb/2018
    Detecting Software:GCCcore/6.4.0
    Generating  19  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/GCCcore/6.4.0
    Detecting Software:binutils/2.28-GCCcore-6.4.0
    Generating  18  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/binutils/2.28-GCCcore-6.4.0
    Detecting Software:GCC/6.4.0-2.28
    No $PATH set in your module  GCC/6.4.0-2.28   so no possible binaries can be found
    There are no binaries for package: GCC/6.4.0-2.28
    Detecting Software:zlib/1.2.11-GCCcore-6.4.0
    No $PATH set in your module  zlib/1.2.11-GCCcore-6.4.0   so no possible binaries can be found
    There are no binaries for package: zlib/1.2.11-GCCcore-6.4.0
    Detecting Software:numactl/2.0.11-GCCcore-6.4.0
    Generating  6  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/numactl/2.0.11-GCCcore-6.4.0
    Detecting Software:hwloc/1.11.8-GCCcore-6.4.0
    Generating  15  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/hwloc/1.11.8-GCCcore-6.4.0
    Detecting Software:OpenMPI/3.0.0-GCC-6.4.0-2.28
    Generating  11  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/OpenMPI/3.0.0-GCC-6.4.0-2.28



The test for ``ompi_info`` is written with the appropriate module.

::

   $ cat /home/siddis14/buildtest/software/OpenMPI/3.0.0-GCC-6.4.0-2.28/ompi_info.sh
    #!/bin/sh


    module load OpenMPI/3.0.0-GCC-6.4.0-2.28
    which ompi_info