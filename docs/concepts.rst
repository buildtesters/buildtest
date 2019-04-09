Concepts
=========

Modules
---------

buildtest will detect modules installed in your system with the help of
Lmod utility (``spider``). For background details on **spider** check the
official documentation: https://lmod.readthedocs.io/en/latest/136_spider.html

buildtest will run the following command during the setup::

    $LMOD_DIR/spider -o spider-json $MODULEPATH

The above output is not readable since it is in json so you can pipe this to
the following::

    $LMOD_DIR/spider -o spider-json | python -m json.tool

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


In buildtest this is handled by class ``BuildTestModule``. The spider output
returns a dictionary that contains details of all modules based on MODULEPATH,
along with full path to module files, and the metadata for a module.
This captures all the details that you may get when running ``module spider``.

Get Unique Software
~~~~~~~~~~~~~~~~~~~~

To get a list of unique software you could run ``module -t spider``::

    buildtest-framework[master !?+] $ module -t spider | head -n 10
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

The method ``get_unique_modules()`` is returning the keys from the dictionary

.. code-block:: python

      def get_unique_modules(self):
        """Return a list of unique full name canonical modules """
        return sorted(self.module_dict.keys())

``buildtest list --list-software`` will return a list of unique software

Get Unique Module Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When users load modules (``module load GCC/5.4.0``) they are loading a specific
software-version. Even when user does ``module load GCC`` without a version.
Lmod will resolve to the default version even if user doesn't specify this.


.. code-block:: python

        module = BuildTestModule()
        module.get_unique_software_modules()

The method ``get_unique_software_modules()`` returns a sorted list of module
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

The implementation of ``get_unique_software_modules()`` is shown below

.. code-block:: python

        def get_unique_software_modules(self):
            """Return a set with list of unique software module names"""
            software_set = set()
            sorted_keys = sorted(self.module_dict.keys())
            for k in sorted_keys:
                for mod_file in self.module_dict[k].keys():
                    software_set.add(self.module_dict[k][mod_file]["full"])

            return sorted(list(software_set))

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


Implementation for ``get_modulefile_path()`` is described below

.. code-block:: python

        def get_modulefile_path(self):
            """Return a list of absolute path for all module files"""
            module_path_list  = []
            for k in self.get_unique_modules():
                module_path_list += self.module_dict[k].keys()
            return module_path_list

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

We can confirm this by running the second combination to load ``zlib/.1.2.8``

.. code-block:: console

    (siddis14-TgVBs13r) docs[master !?] $ ml
    No modules loaded
    (siddis14-TgVBs13r) docs[master !?] $ ml medsci hpc/eb-2017-core GCC/5.4.0-2.27 OpenMPI/2.0.0 zlib/.1.2.8
    (siddis14-TgVBs13r) docs[master !?] $ ml

    Currently Loaded Modules:
      1) medsci             3) GCCcore/.5.4.0   5) GCC/5.4.0-2.27   7) hwloc/1.11.3    9) OpenBLAS/0.2.19-LAPACK-3.6.0  11) ScaLAPACK/2.0.2-OpenBLAS-0.2.19-LAPACK-3.6.0
      2) hpc/eb-2017-core   4) binutils/.2.27   6) numactl/2.0.11   8) OpenMPI/2.0.0  10) FFTW/3.3.4                    12) zlib/.1.2.8




In buildtest we can get the parent for any module with the following code

.. code-block:: python

    module_name = "GCC/5.4.0-2.27"
    module = BuildTestModule
    parent_module = module.get_parent_modules(module_name)

The method ``get_parent_modules`` returns a list of modules to be loaded for
the specified module. In the implementation we only get the first entry of
the ``parent`` key since it doesn't matter which parent modules are loaded.

The implementation for ``get_parent_modules`` can be shown below

.. code-block:: python

    def get_parent_modules(self,modname):
        """Get Parent module for specified module file."""
        for key in self.module_dict.keys():
            for mod_file in self.module_dict[key].keys():
                if modname == self.module_dict[key][mod_file]["full"]:

                    mod_parent_list = self.module_dict[key][mod_file]["parent"]
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
via yaml file, user can specify a module file via ``buildtest build -s
<module>`` to insert module into the script.

For instance, running a binary test such as the utility ``ompi_info`` from
OpenMPI can be done as follows

::

    (siddis14-TgVBs13r) buildtest-framework[master !?] $ buildtest build -s  OpenMPI/2.0.0
    Detecting Software:  OpenMPI/2.0.0
    Detecting Software:OpenMPI/2.0.0
    Generating  12  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/OpenMPI/2.0.0
    Writing Log file:  /home/siddis14/buildtest/OpenMPI/2.0.0/buildtest_16_05_09_04_2019.log

The binary test are written in ``/home/siddis14/buildtest/software/OpenMPI/2.0.0``
and as you see the ``ompi_info.sh`` will load the parent modules before loading
``OpenMPI/2.0.0``

::

    (siddis14-TgVBs13r) buildtest-framework[master !?] $ cat /home/siddis14/buildtest/software/OpenMPI/2.0.0/ompi_info.sh
    #!/bin/sh

    module try-load eb/2017;module try-load GCC/5.4.0-2.27;
    module load OpenMPI/2.0.0
    which ompi_info