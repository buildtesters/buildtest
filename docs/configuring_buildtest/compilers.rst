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

.. dropdown:: ``buildtest config compilers --help``

    .. command-output:: buildtest config compilers --help

buildtest can represent compiler output in JSON, YAML using the ``--json`` and ``--yaml``.
Shown below is an example output with these options

.. dropdown:: ``buildtest config compilers --json``

    .. command-output:: buildtest config compilers --json

.. dropdown:: ``buildtest config compilers --yaml``

    .. command-output:: buildtest config compilers --yaml

If you want to see a flat listing of the compilers as names you can simply run ``buildtest config compilers`` as shown below

.. command-output:: buildtest config compilers

.. _detect_compilers:

Detect Compilers (Experimental Feature)
----------------------------------------

.. Note::

    This feature relies on module system (Lmod, environment-modules) to search modulefiles
    and one must specify **moduletool** property to indicate how buildtest will search modules.
    If ``moduletool: lmod`` is set, buildtest will rely on Lmod spider using `Lmodule  <http://lmodule.readthedocs.io/>`_
    API to detect and test all modules. If ``moduletool: environment-modules`` is set, buildtest
    will retrieve modules using output of ``module -t av``.

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
automatically add ``gcc/9.2.0-n7p74fd`` and ``gcc/10.2.0-37fmsw7`` modules as compiler
instance. Depending on the compiler group, buildtest will apply the compiler wrapper
``cc``, ``cxx``, ``fc`` however these can be updated manually. The module section
is generated with the module to load. One can further tweak the module behavior
along with purging or swap modules. In the output below buildtest will show the compilers detected in YAML format.

.. Note::

    ``buildtest config compilers find`` will not update the buildtest configuration with new compilers, you will need to use ``--update`` option
    to override the configuration file.


.. dropdown:: ``buildtest config compilers``

    .. code-block:: console

        $ buildtest config compilers find
        MODULEPATH: /Users/siddiq90/projects/spack/share/spack/lmod/darwin-catalina-x86_64/Core:/usr/local/Cellar/lmod/8.6.14/modulefiles/Darwin:/usr/local/Cellar/lmod/8.6.14/modulefiles/Core
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Detect Compilers ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran
          gcc/10.2.0-37fmsw7:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/10.2.0-37fmsw7
              purge: false
          gcc/9.3.0-n7p74fd:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/9.3.0-n7p74fd
              purge: false


You can use **--detailed** option to see how buildtest discovers compilers
by searching the modules in MODULEPATH and testing each one with a regular expression.
We can see in the output buildtest is applying a regular expression with each modulefile and if there is a match, we
add the compiler instance into the appropriate compiler group.

.. dropdown:: ``buildtest config compilers --detailed``

    .. code-block:: console

        $ buildtest config compilers find --detailed
        MODULEPATH: /Users/siddiq90/projects/spack/share/spack/lmod/darwin-catalina-x86_64/Core:/usr/local/Cellar/lmod/8.6.14/modulefiles/Darwin:/usr/local/Cellar/lmod/8.6.14/modulefiles/Core
        Searching modules via Lmod Spider
        Applying regex ^(gcc) with module: autoconf/2.69-3yrvwbu
        Applying regex ^(gcc) with module: autoconf-archive/2019.01.06-qoeupni
        Applying regex ^(gcc) with module: automake/1.16.2-vjjvnh7
        Applying regex ^(gcc) with module: berkeley-db/18.1.40-zixsuu6
        Applying regex ^(gcc) with module: bzip2/1.0.8-uem3fk5
        Applying regex ^(gcc) with module: diffutils/3.7-67w5vu5
        Applying regex ^(gcc) with module: gcc/9.3.0-n7p74fd
        Applying regex ^(gcc) with module: gcc/10.2.0-37fmsw7
        Applying regex ^(gcc) with module: gdbm/1.18.1-qcqdlzf
        Applying regex ^(gcc) with module: gmp/6.1.2-pstkmss
        Applying regex ^(gcc) with module: isl/0.21-v6cpwya
        Applying regex ^(gcc) with module: isl/0.20-ypts4jg
        Applying regex ^(gcc) with module: libiconv/1.16-3kkozjq
        Applying regex ^(gcc) with module: libsigsegv/2.12-dg5wkck
        Applying regex ^(gcc) with module: libtool/2.4.6-sp423u5
        Applying regex ^(gcc) with module: lmod
        Applying regex ^(gcc) with module: m4/1.4.18-wctmckj
        Applying regex ^(gcc) with module: mpc/1.1.0-xid3nuo
        Applying regex ^(gcc) with module: mpc/1.1.0-sqfmp67
        Applying regex ^(gcc) with module: mpfr/3.1.6-nm4h2fx
        Applying regex ^(gcc) with module: mpfr/4.0.2-6in3dph
        Applying regex ^(gcc) with module: ncurses/6.2-g5wyknv
        Applying regex ^(gcc) with module: perl/5.32.0-hlmfvxi
        Applying regex ^(gcc) with module: pkgconf/1.7.3-pxfp6qy
        Applying regex ^(gcc) with module: readline/8.0-d4acjhu
        Applying regex ^(gcc) with module: settarg
        Applying regex ^(gcc) with module: zlib/1.2.11-id3vwmq
        Applying regex ^(gcc) with module: zstd/1.4.5-2tk5glw
          Discovered Modules
        ┏━━━━━━━━━━━━━━━━━━━━┓
        ┃ Name               ┃
        ┡━━━━━━━━━━━━━━━━━━━━┩
        │ gcc/9.3.0-n7p74fd  │
        ├────────────────────┤
        │ gcc/10.2.0-37fmsw7 │
        └────────────────────┘
        [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/9.3.0-n7p74fd  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/10.2.0-37fmsw7  "
        [DEBUG] Return Code: 0
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Detect Compilers ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran
          gcc/10.2.0-37fmsw7:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/10.2.0-37fmsw7
              purge: false
          gcc/9.3.0-n7p74fd:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/9.3.0-n7p74fd
              purge: false

Enable Programming Environments
--------------------------------

If you have a Cray based system, you would be familiar with Programming Environments (``PrgEnv-*``) modulefiles that will be present on your system. We can configure
buildtest to enable programming environment support which will detect for Programming Environment and test ``PrgEnv-*`` modules, if they are present buildtest will automatically
add the modules into the corresponding compiler instance.

To demonstrate this let's take a look at the following configuration that is available on Cori. To enable programming environment
support you need to set ``enable_prgenv`` which is a boolean that determines whether to detect for programming environments. The
property ``prgenv_modules`` is a mapping of compiler groups to the corresponding ``PrgEnv-*`` modulefile. For instance **PrgEnv-gnu**
is the programming environment modulefile that will load the GNU compiler on Cray systems.

.. literalinclude:: ../tests/settings/cori.yml
    :emphasize-lines: 6-10

Now let's run **buildtest config compilers find --detailed** and take note of the generated compilers, you will see that ``PrgEnv-*`` modules for each compiler group
that has the programming environment. Furthermore, we see the cray wrappers **cc**, **CC**, and **ftn** are used instead of the compiler wrappers.

.. dropdown:: ``buildtest config compilers find --detailed``

    .. code-block:: console

        (buildtest)  ~/gitrepos/buildtest/tests/settings/ [prgenv_support] buildtest config compilers find --detailed
        MODULEPATH: /opt/cray/pe/perftools/21.12.0/modulefiles:/opt/cray/pe/craype-targets/default/modulefiles:/opt/cray/ari/modulefiles:/opt/cray/pe/modulefiles:/opt/cray/modulefiles:/opt/modulefiles:/global/common/software/nersc/cle7up03/modulefiles:/global/common/software/nersc/cle7up03/extra_modulefiles:/global/common/cori_cle7up03/ftg/modulefiles
        Searching modules by parsing content of command: module av -t
          Discovered Modules
        ┏━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Name                ┃
        ┡━━━━━━━━━━━━━━━━━━━━━┩
        │ gcc/7.3.0           │
        ├─────────────────────┤
        │ gcc/8.1.0           │
        ├─────────────────────┤
        │ gcc/8.3.0           │
        ├─────────────────────┤
        │ gcc/10.3.0          │
        ├─────────────────────┤
        │ gcc/11.2.0          │
        ├─────────────────────┤
        │ craype/2.6.2        │
        ├─────────────────────┤
        │ craype/2.7.10       │
        ├─────────────────────┤
        │ intel/19.0.3.199    │
        ├─────────────────────┤
        │ intel/19.1.2.254    │
        ├─────────────────────┤
        │ intel/19.1.0.166    │
        ├─────────────────────┤
        │ intel/19.1.1.217    │
        ├─────────────────────┤
        │ intel/19.1.2.275    │
        ├─────────────────────┤
        │ intel/19.1.3.304    │
        ├─────────────────────┤
        │ upcxx/2021.9.0      │
        ├─────────────────────┤
        │ upcxx/2022.3.0      │
        ├─────────────────────┤
        │ upcxx/2022.9.0      │
        ├─────────────────────┤
        │ upcxx/bleeding-edge │
        ├─────────────────────┤
        │ upcxx/nightly       │
        └─────────────────────┘
        [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/7.3.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/8.1.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/8.3.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/10.3.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load gcc/11.2.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load craype/2.6.2  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load craype/2.7.10  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load intel/19.0.3.199  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load intel/19.1.2.254  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load intel/19.1.0.166  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load intel/19.1.1.217  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load intel/19.1.2.275  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load intel/19.1.3.304  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load upcxx/2021.9.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load upcxx/2022.3.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load upcxx/2022.9.0  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load upcxx/bleeding-edge  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load upcxx/nightly  "
        [DEBUG] Return Code: 0
        Testing Programming Environment Modules
        [DEBUG] Executing module command: bash -l -c "module purge && module load PrgEnv-gnu  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load PrgEnv-cray  "
        [DEBUG] Return Code: 0
        [DEBUG] Executing module command: bash -l -c "module purge && module load PrgEnv-intel  "
        [DEBUG] Return Code: 0
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Detect Compilers ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        cray:
          craype/2.6.2:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-cray
              - craype/2.6.2
              purge: false
          craype/2.7.10:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-cray
              - craype/2.7.10
              purge: false
        gcc:
          builtin_gcc:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            fc: /usr/bin/gfortran
          gcc/10.3.0:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-gnu
              - gcc/10.3.0
              purge: false
          gcc/11.2.0:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-gnu
              - gcc/11.2.0
              purge: false
          gcc/7.3.0:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-gnu
              - gcc/7.3.0
              purge: false
          gcc/8.1.0:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-gnu
              - gcc/8.1.0
              purge: false
          gcc/8.3.0:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-gnu
              - gcc/8.3.0
              purge: false
        intel:
          intel/19.0.3.199:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-intel
              - intel/19.0.3.199
              purge: false
          intel/19.1.0.166:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-intel
              - intel/19.1.0.166
              purge: false
          intel/19.1.1.217:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-intel
              - intel/19.1.1.217
              purge: false
          intel/19.1.2.254:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-intel
              - intel/19.1.2.254
              purge: false
          intel/19.1.2.275:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-intel
              - intel/19.1.2.275
              purge: false
          intel/19.1.3.304:
            cc: cc
            cxx: CC
            fc: ftn
            module:
              load:
              - PrgEnv-intel
              - intel/19.1.3.304
              purge: false
        upcxx:
          upcxx/2021.9.0:
            cc: upcxx
            cxx: upcxx
            fc: None
            module:
              load:
              - upcxx/2021.9.0
              purge: false
          upcxx/2022.3.0:
            cc: upcxx
            cxx: upcxx
            fc: None
            module:
              load:
              - upcxx/2022.3.0
              purge: false
          upcxx/2022.9.0:
            cc: upcxx
            cxx: upcxx
            fc: None
            module:
              load:
              - upcxx/2022.9.0
              purge: false
          upcxx/bleeding-edge:
            cc: upcxx
            cxx: upcxx
            fc: None
            module:
              load:
              - upcxx/bleeding-edge
              purge: false
          upcxx/nightly:
            cc: upcxx
            cxx: upcxx
            fc: None
            module:
              load:
              - upcxx/nightly
              purge: false

Test Compilers (Experimental Feature)
--------------------------------------

Next we run ``buildtest config compilers test`` which test each compiler instance by performing 
module load test and show an output of each compiler.

.. dropdown:: ``buildtest config compilers test``

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
to **buildtest config compilers test** and buildtest will only test the selected compiler. Shown below is an example where we only test
compiler ``gcc/9.1.01``

.. dropdown:: ``buildtest config compilers test gcc/9.1.0``

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