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

.. command-output:: buildtest config compilers test