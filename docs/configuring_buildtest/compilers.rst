.. _compilers:

Defining Compilers at your site
=================================

buildtest provides a mechanism to declare compilers in your configuration file, this
is defined in ``compilers`` top-level section. The compilers should reflect compilers
installed at your site. The compilers are used if you are writing a buildspec
with :ref:`compiler schema <compiler_schema>` that needs to reference a particular compiler.
The compilers are declared within scope of a system since we assume compilers will vary across
different HPC clusters.

Compiler Declaration
---------------------


Shown below is a declaration of ``builtin_gcc`` provided by default.

.. code-block:: yaml

    compilers:
      compiler:
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran

The compiler declaration is defined in section ``compiler`` followed by name
of compiler in this case ``gcc``. In the gcc section one can define all gnu compilers,
which includes the name of the compiler in this example we call ``builtin_gcc`` as
system compiler that defines C, C++ and Fortran compilers using ``cc``, ``cxx`` and
``fc``.

One can retrieve all compilers using ``buildtest config compilers``, there are few
options for this command.

.. command-output:: buildtest config compilers --help

buildtest can represent compiler output in JSON, YAML using the ``--json`` and ``--yaml``.
Shown below is an example output with these options::

    $ buildtest config compilers --json
    {
      "gcc": {
        "builtin_gcc": {
          "cc": "/usr/bin/gcc",
          "cxx": "/usr/bin/g++",
          "fc": "/usr/bin/gfortran"
        }
      }
    }

    $ buildtest config compilers --yaml
    gcc:
      builtin_gcc:
        cc: /usr/bin/gcc
        cxx: /usr/bin/g++
        fc: /usr/bin/gfortran

    $ buildtest config compilers
    builtin_gcc

.. _detect_compilers:

Detect Compilers (Experimental Feature)
----------------------------------------

buildtest can detect compilers based on modulefiles and generate compiler section
that way you don't have to specify each compiler manually.
This can be done via ``buildtest config compilers find`` command. Buildtest expects
a key/value mapping when searching compiler names and regular expression using `re.match <https://docs.python.org/3/library/re.html#re.match>`_
for discovering compiler modules.

This can be demonstrated, by defining search pattern in the ``find`` section
that expects a dictionary of key/value mapping between compiler names and their module names.

In example, below we define a pattern for gcc modules as ``^(gcc)`` which will
find all modules that start with name `gcc`.

.. code-block:: yaml

    compilers:
      find:
        gcc: "^(gcc)"
      compiler:
        gcc:
          builtin:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran


In this system, we have two gcc modules installed via `spack <https://spack.readthedocs.io/en/latest/>`_
package manager, we will attempt to add both modules as compiler instance in buildtest.

.. code-block:: console

    $ module -t av gcc
    /Users/siddiq90/projects/spack/share/spack/lmod/darwin-catalina-x86_64/Core:
    gcc/9.3.0-n7p74fd
    gcc/10.2.0-37fmsw7


Next we run ``buildtest config compilers find`` which will search all modules based on
regular expression and add compilers in their respective group. In this example, buildtest
automatically add ``gcc/9.2.0-n7p74fd`` and ```gcc/10.2.0-37fmsw7`` modules as compiler
instance. Depending on the compiler group, buildtest will apply the compiler wrapper
``cc``, ``cxx``, ``fc`` however these can be updated manually. The module section
is generated with the module to load. One can further tweak the module behavior
along with purging or swap modules.

.. code-block:: console

    $ buildtest config compilers find
    MODULEPATH: /Users/siddiq90/projects/spack/share/spack/lmod/darwin-catalina-x86_64/Core:/usr/local/Cellar/lmod/8.4.12/modulefiles/Darwin:/usr/local/Cellar/lmod/8.4.12/modulefiles/Core
    Configuration File: /Users/siddiq90/.buildtest/config.yml
    ________________________________________________________________________________
    moduletool: lmod
    load_default_buildspecs: true
    executors:
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash
        sh:
          description: submit jobs on local machine using sh shell
          shell: sh
        csh:
          description: submit jobs on local machine using csh shell
          shell: csh
        python:
          description: submit jobs on local machine using python shell
          shell: python
    compilers:
      find:
        gcc: ^(gcc)
        pgi: ^(pgi)
      compiler:
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/local/bin/gfortran
          gcc/9.3.0-n7p74fd:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/9.3.0-n7p74fd
              purge: false
          gcc/10.2.0-37fmsw7:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/10.2.0-37fmsw7
              purge: false

    ________________________________________________________________________________
    Updating settings file:  /Users/siddiq90/.buildtest/config.yml


This feature relies on module system (Lmod, environment-modules) to search modulefiles
and one must specify **moduletool** property to indicate how buildtest will search modules.
If ``moduletool: lmod`` is set, buildtest will rely on Lmod spider using `Lmodule  <http://lmodule.readthedocs.io/>`_
API to detect and test all modules. If ``moduletool: environment-modules`` is set, buildtest
will retrieve modules using output of ``module -t av``.

Test Compilers (Experimental Feature)
--------------------------------------

Next we run ``buildtest config compilers test`` which test each compiler instance by performing 
module load test and show an output of each compiler.

.. code-block:: console

    $ buildtest config compilers test

                    Compilers Test Pass
    ┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
    ┃ No. ┃ Compiler Name                   ┃ Status ┃
    ┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩                                                                                                    [0/1858]
    │ 1   │ PrgEnv-gnu/6.0.5                │     ✅ │
    │ 2   │ PrgEnv-gnu/6.0.10               │     ✅ │
    │ 3   │ gcc/7.3.0                       │     ✅ │
    │ 4   │ gcc/8.1.0                       │     ✅ │
    │ 5   │ gcc/8.3.0                       │     ✅ │
    │ 6   │ gcc/10.3.0                      │     ✅ │
    │ 7   │ gcc/11.2.0                      │     ✅ │
    │ 8   │ PrgEnv-cray/6.0.5               │     ✅ │
    │ 9   │ PrgEnv-cray/6.0.10              │     ✅ │
    │ 10  │ PrgEnv-intel/6.0.5              │     ✅ │
    │ 11  │ PrgEnv-intel/6.0.10             │     ✅ │
    │ 12  │ intel/19.0.3.199                │     ✅ │
    │ 13  │ intel/19.1.2.254                │     ✅ │
    │ 14  │ intel/19.1.0.166                │     ✅ │
    │ 15  │ intel/19.1.1.217                │     ✅ │
    │ 16  │ intel/19.1.2.275                │     ✅ │
    │ 17  │ intel/19.1.3.304                │     ✅ │
    │ 18  │ upcxx/2021.9.0                  │     ✅ │
    │ 19  │ upcxx/2022.3.0                  │     ✅ │
    │ 20  │ upcxx/bleeding-edge             │     ✅ │
    │ 21  │ upcxx/nightly                   │     ✅ │
    │ 22  │ upcxx-bupc-narrow/2021.9.0      │     ✅ │
    │ 23  │ upcxx-bupc-narrow/2022.3.0      │     ✅ │
    │ 24  │ upcxx-bupc-narrow/bleeding-edge │     ✅ │
    │ 25  │ upcxx-extras/2020.3.0           │     ✅ │
    │ 26  │ upcxx-extras/2020.3.8           │     ✅ │
    │ 27  │ upcxx-extras/2022.3.0           │     ✅ │
    │ 28  │ upcxx-extras/master             │     ✅ │
    └─────┴─────────────────────────────────┴────────┘
                Compilers Test Fail
    ┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
    ┃ No. ┃ Compiler Name            ┃ Status ┃
    ┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
    │ 1   │ upcxx-gpu/2021.9.0       │     ❌ │
    │ 2   │ upcxx-gpu/2022.3.0       │     ❌ │
    │ 3   │ upcxx-gpu/nightly        │     ❌ │
    │ 4   │ upcxx-gpu-1rail/2021.9.0 │     ❌ │
    │ 5   │ upcxx-gpu-1rail/nightly  │     ❌ │
    └─────┴──────────────────────────┴────────┘

If you want to test specific compilers instead of testing all compilers you can pass name of compiler as a positional argument
to `buildtest config compilers test` and buildtest will only test the selected compiler. Shown below is an example where we only test
compiler ``gcc/9.1.01``

.. code-block:: console

    $ buildtest config compilers test gcc/9.1.0
    Skipping test for compiler: builtin_gcc
    Skipping test for compiler: gcc/9.3.0
    Skipping test for compiler: gcc/11.1.0
    Skipping test for compiler: gcc/7.5.0
    Skipping test for compiler: gcc/12.1.0
    Skipping test for compiler: gcc/11.2.0
    Skipping test for compiler: gcc/10.2.0
          Compilers Test Pass
    ┏━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┓
    ┃ No. ┃ Compiler Name ┃ Status ┃
    ┡━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━┩
    │ 1   │ gcc/9.1.0     │     ✅ │
    └─────┴───────────────┴────────┘