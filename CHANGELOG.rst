CHANGELOG
=========

v0.8.0 (Mar xxx, 2020)
-----------------------

 - Add pre-commit hook to automate python format via ``black``. Add ``black --check`` as automated check see #172, #179
 - Remove CLI option ``buildtest build [run|log|test]`` see #163
 - Remove all module operations and cli menu ``buildtest module``. This is now moved to an API lmodule at https://github.com/HPC-buildtest/lmodule
 - removing extra dependencies argcomplete and termcolor
 - removing dependency of Lmod, only needed if modules specified in configs
 - replace ``toolkit/suite`` with ``site`` directory  in code and documentation examples
 - removing bash script and sourcing in favor of Python module install
 - build test "root" replaced with user home ``$HOME/.buildtest``
 - addition of ``buildtest get`` command to clone repository into toolkit/suite

v0.7.6 (Feb 4th, 2020)
-----------------------

- Add GitHub actions: ``greetings``, `trafico <https://github.com/marketplace/trafico-pull-request-labeler>`_, `URLs-checker <https://github.com/marketplace/actions/urls-checker>`_, `pull-request-size <https://github.com/marketplace/pull-request-size>`_ 
- Add `coveralls <https://github.com/marketplace/coveralls>`_ for coverage report 
- Use `Imgbot <https://github.com/marketplace/imgbot>`_ bot to convert all images via lossless compression to reduce image size
- Update ``.gitignore`` file to reflect file extension relevant to buildtest 
- Remove command option ``buildtest testconfigs maintainer`` and benchmark feature ``buildtest benchmark``
- Rename output style when showing buildtest configuration (``buildtest show --config``)
- Add option to list all parent modules ``buildtest module --list-all-parents``
- Move code base  from ``src/buildtest`` --> ``buildtest`` and move ``buildtest`` script --> ``bin/buildtest``
- Update contributing docs, and upload slides from 5th Easybuild User Meeting and FOSDEM20 

v0.7.5 (Dec 31st, 2019)
-----------------------

- Major improvement to Travis build. buildtest will now test for python ``3.6``, ``3.7``, ``3.8`` for Lmod version ``6.6.2`` and ``7.8.2``
- Travis will install easybuild and setup a mini software stack that is used for by regression test
- Port the regression test to comply with Travis build environment and ``coverage`` report automatically get pushed to CodeCov
- Removing subcommand ``buildtest benchmark [hpl | hpcg]``
- Add options to ``buildtest module loadtest`` to control behavior on module loadtest.
- buildtest can run module loadtest in a **login shell** via ``buildtest module loadtest --login`` and restrict number of
  test using ``--numtest`` flag. buildtest will automatically purge modules before loading test but this can be tweaked
  using ``--purge-modules`` flag
- Remove command ``buildtest list`` and remove implementation for retrieving easyconfigs ``buildtest list --easyconfigs``
- Option ``buildtest list --software`` is now ``buildtest module --software`` and ``buildtest list --modules`` is now ``buildtest module list``
- Add the following flags: ``--exclude-version-files``, ``--filter-include``, ``--querylimit`` to ``buildtest module list``
  to tweak behavior on module list
- Update buildtest configuration (``settings.yml``) with equivalent **key/value** to control behavior of ``buildtest module [list | loadtest]``.
  The configuration values are overridden by command line flags
- buildtest will ignore ``.version``, ``.modulerc`` and ``.modulerc.lua`` files when reporting modules in ``buildtest module list``. This
  is controlled by ``exclude-version-files`` in configuration or flag ``--exclude-version-files``
- Remove sanity check feature ``buildtest build --package`` and ``buildtest build --binary`` and remove configuration ``BUILDTEST_BINARY`` from configuration file
- Remove option ``buildtest build --parent-module-search`` and remove ``BUILDTEST_PARENT_MODULE_SEARCH`` from configuration file
- Update documentation procedure regarding **installation of buildtest** and remove **Concepts** page


v0.7.4 (Dec 11th, 2019)
-------------------------

- update documentation section **Background**, **Motivation**, **Inception**, and **Description**
- make use of ``$SRCDIR`` when setting variable ``SRCFILE`` in test script.
- add documentation issue template page
- add clang compiler support via ``compiler:clang``
- add contributing pages to buildtest documentation and add further clarification on release process, buildtest regression testing, and GitHub app integration
- add ``EDITOR`` key in buildtest configuration (**settings.yml**) to tweak editor when editing files
- change path to output/error files in ``buildtest module loadtest`` and print actual ``module load`` command
- adding github stalebot configuration see ``.github/stale.yml``
- adding github sponsor page ``.github/FUNDING.yml``
- add stream benchmark test see https://github.com/HPC-buildtest/buildtest-framework/commit/d2a2a4dc2e71c5921b211d4df4d68b7f52cbbf52
- adding github workflow ``black`` to format all python code base see ``.github/workflow/black.yml``
- install lmod and its dependency in travis build


v0.7.3 (Nov 25th, 2019)
-----------------------

- enable ``cuda``, ``intel``, ``pgi`` compilation, this can be set via ``compilers`` key
- Define shell variables ``CC``, ``FC``, ``CXX`` to be used to reference builds
- Define shell variable ``EXECUTABLE`` to reference generated executable
- Fix Code Style issues reported by CodeFactor (https://www.codefactor.io/repository/github/hpc-buildtest/buildtest-framework)
- Add , hust-19 slides, buildtest architecture and workflow diagram in documentation
- Simplify output of ``buildtest module --easybuild`` and ``buildtest module --spack``
- Add ``module purge`` or ``module --force purge`` in test (#122)
- automate documentation examples for building test examples
- move all documentation examples to ``toolkit/suite/tutorial``
- update CONTRIBUTING.rst guide to include section on building buildtest API docs, automating documentation examples and running regression test via pytest


v0.7.2 (Nov 8th, 2019)
----------------------
- automate documentation test generation using python script
- add support for coverage see https://codecov.io/gh/HPC-buildtest/buildtest-framework
- adding dry option when building tests (short: ``-d`` or long option:``--dry``)
- automate buildtest testing process via pytest. Add initial support with 25+ regression tests
- adding directory expansion support when files or directory are references such as $HOME or tilde (~) operation
- adding several badges to README.rst

v0.7.1 (Aug 30, 2019)
---------------------
- Re-implement core mechanics of the build framework by using new YAML schema.
- Release buildtest under MIT license
- Yaml schema can be printed via ``buildtest show -k singlesource``. The schema provides building
  C, C++, Fortran code along with MPI test. Provides keys such as ``cflags``, ``cxxflags``, ``fflags``
  ``cppflags``, ``ldflags`` for passing compiler options. The schema provides a dictionary to
  insert **#BSUB** and **#SBATCH** directives into job scripts via ``bsub:`` and ``sbatch:`` keys.
- Add documentation example on C, C++, Fortran, MPI, and OpenACC code.
- Add options **buildtest build bsub** (bsub wrapper) such as ``-n``, ``-W``, ``-M``,``-J``,``--dry-run``.
- Add key TESTDIR in **build.json** to identify test directory, this makes it easier when running test


v0.7.0 (Aug 22, 2019)
----------------------
- autodetect slurm configuration from system and write to json file
- add option ``buildtest module --module-deps`` that prints modules dependent on parent modules
- add subparser ``buildtest module tree`` that provides operation for managing module trees (**BUILDTEST_MODULEPATH**)
- remove subparser ``buildtest find``
- add option ``buildtest build --collection`` for building test with Lmod user collection
- remove option ``buildtest build --software``
- add option ``buildtest build --modules`` which allows test to be build with multiple module versions
- add option ``buildtest module collection`` for managing module collection using buildtest. Alternative to Lmod user collection
- remove option ``buildtest --clean-logs``
- Color output of Lua and non-lua modules in ``buildtest list --modules``.
-  Remove option ``--python-package``, ``--perl-package``, ``--ruby-package``, ``--r-package`` from **build** menu. Also delete all reference in documentation and delete repository
- ``--buildtest-software`` option is removed
- ``--format`` option in list submenu only supports **json**. Previously it also supported **csv**
- Rename all test scripts for documentation and rst files to be lower case
- Convert CONTRIBUTING guide from Markdown to Restructured Text (RsT) and add Contributing section in documentation
- Change buildtest config file path to be $HOME/.buildtest/settings.yml
- Use sphinx-argparse to automate argparse documentation
- Rename main program **_buildtest** to **buildtest** and changed source code directory layout
- Add option ``-b`` or ``--binary`` for native support for sanity check on binary commands in framework without using yaml files
- Update requirements.txt
- Migrate documentation to buildtest-framework
- Create subcommand **find** and move option ``-ft`` and ``-fc`` to this menu
- Add logo for license, version, download, status to README.rst
- Type checking support for buildtest configuration file
- Remove option ``--output`` from **run** submenu
- Add support for OSU Benchmark  and add this to benchmark submenu and document this page
- Add threshold value for running test. This can be configured using BUILDTEST_SUCCESS_THRESHOLD
- Create submenu ``module`` and move option ``--diff-trees`` and ``--module-load-test`` to this menu

v0.6.3 (Oct 26, 2018)
----------------------------
- OpenHPC yaml files are moved from $BUILDTEST_CONFIGS_REPO/ohpc to  $BUILDTEST_CONFIGS_REPO/buildtest/ohpc
- This led to minor fix on how buildtest will write yaml files via ``_buildtest yaml --ohpc`` and build tests via ``_buildtest build --ohpc``

v0.6.2 (Oct 26, 2018)
----------------------------
- Add OpenHPC integration with buildtest with option ``--ophc``. This is available for ``build`` and ``yaml`` subcommand
- Rename option ``--ignore-easybuild`` to ``--easybuild``. When this is set, buildtest will check if software is easybuild software.
- BUILDTEST_EASYBUILD and BUILDTEST_OHPC can be defined in configuration file or environment variable
- Fix sorting issue with output for ``_buidltest list -svr`` and ``_buildtest list -bs``
- Add option ``--prepend-modules`` that can prepend modules to test script before loading application module.
- buildtest will now ignore all .version* files as pose to .version file, this is due to Lmod 7 and how OpenHPC module files have hidden modules with format .versionX.Y.Z
-

v0.6.1 (Oct 18, 2018)
---------------------------
- Fix issue with pypi package dependency in version 0.6.0

v0.6.0 (Oct 18, 2018)
---------------------------
- **New Feature:** option to build all software and system packages using ``--all-software`` and ``--all-package``
- **New Feature:** option to build all yaml configuration for software and system package using ``--all-software`` and ``--all-package``
- **New Feature:** option to run all tests for software and system package using ``--all-software`` and ``--all-package``
- **New Feature:** add option ``--output`` to control output  for test execution. Output can be redirected to /dev/null or /dev/stdout
- rename option ``--system`` to ``--package``
- option ``--software`` and ``--package`` is consistent across build, yaml, and run subcommand
- Add test count, passed and failed test after each test run when using ``_buildtest run``.
- option ``--rebuild`` and ``--overwrite`` will work with ``--all-software`` and ``--all-package`` in yaml subcommand to automate rebuilding of yaml files
-  Move option `--module-naming-scheme`  to build subcommand
- **bug fix:** directory issue for running buildtest first time https://github.com/HPC-buildtest/buildtest-framework/issues/81
- **bug fix:** print error https://github.com/HPC-buildtest/buildtest-framework/issues/80

v0.5.0 (Oct 8, 2018)
-----------------------

- **New Feature:** Add new sub-commands ``build`` ``list`` ``run`` to buildtest
- Move the following options to ``build`` sub command
   - ``-s``
   - ``-t``
   - ``--enable-job``
   - ``--job-template``
   - ``--system``
   - ``--r-package-test``
   - ``--python-package-test``
   - ``--perl-package-test``
   - ``--ruby-package-test``
   - ``--shell``
   - ``--ignore-easybuild``
   - ``--clean-tests``
   - ``--testdir``
   - ``--clean-build``
- Move the following option to ``list`` sub command
  - ``-ls``
  - ``-lt``
  - ``-svr``
- Add option ``--format`` in ``list`` sub command to view output in ``csv``, ``json``. Default is ``stdout``
- Add the following option to ``run`` sub command
   - ``--app``
   - ``--systempkg``
   - ``--interactive`` (originally ``--runtest``)
   - ``--testname``
- Added basic error handling support
- Add ``description`` key in all yaml files
-  Tests have permission ``755`` so they can run automatically as any user see https://github.com/HPC-buildtest/buildtest-framework/pull/79/commits/6a2570e9d547b0fb3ab81a14770583a192092224
- Options for ``--ebyaml`` now generates date-time stamp for ``command.yaml`` see https://github.com/HPC-buildtest/buildtest-framework/pull/79/commits/a5968263e4faeac0b65386b22d9b1d5cff604185
- Add script ``check.sh`` to automate testing of buildtest features and package building for verification
- **bug fix:** https://github.com/HPC-buildtest/buildtest-framework/pull/79/commits/8017d48c10cee706669ae5b56077640722442571
- **bug fix:** https://github.com/HPC-buildtest/buildtest-framework/pull/79/commits/8dfe78bce930e23eb2242e4e4666f926bf60131f

v0.4.0 (Sep 11, 2018)
--------------------------

- Must use Python 3.6 or higher to use this version. All versions < 0.4.0 are supported by Python 2.6 or higher

v0.3.0 () (Aug 7, 2018)
----------------------------------

- Package buildtest as pypi package, now it can be installed via ``pip install buildtest-framework``
- Rename ``buildtest`` to ``_buildtest`` and all code is now under ``buildtest``
- All buildtest repos are now packaged as pypi package and test are moved under `buildtest` directory
- The option `--ebyaml` is now working with auto-complete feature and ability to create yaml files for software packages
- Binary test are now created based on unique sha256sum see https://github.com/HPC-buildtest/buildtest-framework/commit/92c012431000ff338532a899e3b5f465f18786dd
- Output of `--scantest` has been fixed and added to documentation
- Add singularity CDASH script, need some more work on getting server setup properly

New options
~~~~~~~~~~~~~
- `--r-package`: build test for r packages
- `--python-package`: build test for python packages
- `--perl-package:` build test for perl packages
- `--ruby-package`: build test for ruby packages
- `--show-keys` : Display description of yaml keys

- The option `--testset` is removed and will be replaced by individual option for r, perl, python, ruby package options


Bug Fixes
~~~~~~~~~~~~~

- Fix issue with `--runtest` option, it was broken at some point now it is working as expected
- Add extra configuration option in `config_opts` to reuse variable that were needed throughout code and fix bug with `--sysyaml` see https://github.com/HPC-buildtest/buildtest-framework/commit/493b53e4cfdb5710b384409edc7c85ceb05395ba
- Fix bug with directory not found in menu,py by moving function `check_configuration` and `override_configuration` from main.py to menu,py see https://github.com/HPC-buildtest/buildtest-framework/commit/d2c78076eb551683bf81a3a7d12ae10971460971

v0.2.0 (May 18, 2018)
---------------------------

This is a major release update on buildtest with additional options and most importantly
ability to test software stack without easybuild. buildtest can be used to test multiple
software trees, with ability to disable easybuild check for software stack built without
easybuild. The easybuild verification in buildtest has been simplified and it can easily
report which software is built by easybuild.

buildtest can report difference between 2 module trees and multiple module trees can be
specified at same time for building test, and listing software, and software-version.
There has been some improvement on how buildtest operates with ``Flat-Naming-Scheme (FNS)``
module naming scheme for module tree. Basically you don't need to use ``--toolchain``
option with buildtest if you are using ``FNS`` naming scheme but for ``HMNS``
module tree you will need to use ``--toolchain`` option

- Add short option ``-mns`` for ``--module-naming-scheme`` and report total count for software, toolchain and software-version for options ``-ls``, ``-lt``, ``-svr``
- Adding options ``--clean-logs``, ``--clean-tests`` for removing directories via command line
- The file ``config.yaml`` is used to modify buildtest configuration and users can modify this to get buildtest working.
- Environment variables can override configuration in ``config.yaml`` to allow further flexibility
- add option ``--logdir`` to specify alternate path from the command line
- remove option ``--check-setup``
- buildtest can operate on multiple module trees for option ``-ls`` and ``-svr``
- rename option ``--modules-to-easyconfigs`` to ``--easyconfigs-to-moduletrees`` with a short option ``-ecmt``
- add option to show difference between module trees using ``--diff-tree``
- Fixed a bug where ``.version`` files were reported in method ``get_module_list``
- Add option ``--ignore-easybuild`` to disable easybuild check for a module tree
- rename buildtest variables in source code
- add option ``--show`` to display buildtest configuration
- add option ``--enable-job`` to enable Job integration with buildtest this is used with options ``--job-template``
- rename all sub-directories in repo ``BUILDTEST_CONFIGS_REPO`` to lowercase to allow buildtest to generate tests if software is lower case such as ``gcc`` and ``GCC`` in the module file. This enables buildtest to operate with module trees that dont follow easybuild convention
- buildtest will only generate tests for packages in python, R, ruby, perl when using ``--testset`` option if software has these packages installed. This avoids having to create excess test when they are bound to fail
- ``--testset`` option now works properly for both ``HMNS`` and ``FNS`` module naming scheme and is able to operate on modules that don't follow easybuild module naming convention

v0.1.8 (Feb 27, 2018)
------------------------

- Automate batch job submission from buildtest via **--submitjob**
- Fix shell magic (#!/bin/sh, #!/bin/bash, #!/bin/csh) for binary test
- Tab completion for buildtest argument using ``argcomplete`` module. See https://github.com/HPC-buildtest/buildtest-framework/pull/52/commits/ddb9e426f1b466d3e9b1957a009f0955c236f7a2
- autopopulate choice for ``--system``, ``--sysyaml``, and ``--software``
- Fix output of ``-svr`` and resolve bug when 2 modules with same app/version found in different trees. Only in HMNS. See https://github.com/HPC-buildtest/buildtest-framework/pull/52/commits/7ddf91b761f88ddacf0548c7f259b2badd93bdfd for more details
- Group buildtest commands for ease of use.
- Support for yaml keys **scheduler** and **jobslot** to enable jobscript creation from yaml files. See https://github.com/HPC-buildtest/buildtest-framework/pull/52/commits/0fe4189df0694bef586e9d8e4565ec4cc3e169c9
- Further support for scheduler and automatic detection. Currently supports LSF and SLURM.

v0.1.7 (Feb 27, 2018)
------------------------

- Add support for creating LSF Job scripts via templates. Use **buildtest --job-template** see https://github.com/HPC-buildtest/buildtest-framework/commit/927dc09e347fdafa7020d7cfd3016fd8f430ac10
- Add support for creating YAML config for system package binary testing  via **buildtest --sysyaml** see https://github.com/HPC-buildtest/buildtest-framework/commit/4ab8870eddb9da5177b6c414e98f1231d14b35ab
- adding keys envvar, procrange, threadrange in YAML https://github.com/HPC-buildtest/buildtest-framework/commit/9a2152307dbf88943618a0b7ee8f6984de3a5340 https://github.com/HPC-buildtest/buildtest-framework/commit/1524238919be638edc831df6395425f92e46bc2c   https://github.com/HPC-buildtest/buildtest-framework/commit/3d43b8a68946c4a376e1645c4ad204c7498ae6c3
-  Add support for multiple shell (csh, bash, sh) see https://github.com/HPC-buildtest/buildtest-framework/commit/aea9d6ff06dcc207e84ba0953c53e2cbd67a49fe https://github.com/HPC-buildtest/buildtest-framework/commit/c154db87f876251cc6b2985e8bfb8c2265843216
- remove verbose option from buildtest
- major code refactor see https://github.com/HPC-buildtest/buildtest-framework/commit/fd8d466dc1f009f5822d2161eaf73e85f42a985e https://github.com/HPC-buildtest/buildtest-framework/commit/9d112c0e2e8c6800013eeda7968f568a749f2586
- Fixed a bug during compiler detection when building GCC see https://github.com/HPC-buildtest/buildtest-framework/commit/f139756213a280301771214894c8f48e8bcee4e8
- create a pretty menu for Interactive Testing via **buildtest --runtest** see https://github.com/HPC-buildtest/buildtest-framework/commit/231cfeb0cf88cbc70826a9e76697947d06f0a6e1
- replace shell commands **subprocess.Popen()** with python library equivalents
- Add support for **--testset Tcl** see https://github.com/HPC-buildtest/buildtest-framework/commit/373cc1ea2fb2c5aedcf9ddadf105a94232cc1fa4
- Add support for **--testset Ruby** see https://github.com/HPC-buildtest/buildtest-framework/commit/c6b7133b5fc4b0690b8040d0e437784567cc1963
- Print software in alphabetical order for -svr option see https://github.com/HPC-buildtest/buildtest-framework/commit/fcf61019c644cd305e459234a85c5d39df06433f

v0.1.6 (Feb 27, 2018)
-------------------------

- Add support for FlatNamingScheme in buildtest, added flag ``--module-naming-scheme`` to control setting
- Add prototype functions
    - get_appname()
    - get_appversion()
    - get_toolchain_name()
    - get_toolchain_version()

- Add support for logging via Python Logger module
- Fix buildtest version, in 0.1.5 release buildtest was reporting version 1.0.1
- Provide clean termination when no easyconfig is found
- Fix issue when no toolchain is provided in CMakeList.txt
- Optimize nested loop when performing --software-version-relationship

v0.1.5 (Feb 27, 2018)
------------------------------

The buildtest repo has been moved from http://github.com/shahzebsiddiqui to http://github.com/HPC-buildtest

- Report what tests can be generated from buildtest through YAML files by using **--scantest**
- Fixed a bug with flag **-svr** that was related to structure of easybuild repo, now no dependency on easybuild repo. Also added pretty output
- Adding CONTRIBUTION page
- Fix out software, toolchain, and easyconfig check is done. Arguments to --software and --toolchain must go through module check, then toolchain check, and then finally easyconfig check
- Add support for **--check-setup** which can be used to determine if buildtest framework is setup properly
- Add interactive testing via **buildtest --runtest** which is menu-driven with ability to run all tests, or run individual test directory in menu and see output
- Fix some issues with --testset and now buildtest reports number of tests generated not the path for each test to limit output. For --testset like R, Python, Perl buildtest will report generated test for each package
- buildtest will now use **eb --list-toolchains** to get list of all toolchains for toolchain check
- Can properly generate tests via --testset when R, Python, and Perl repos were created and moved out of buildtest-configs
- Add **buildtest -V** for version display

There has been lots of restructuring of code. There still needs some improvement for organizing scripts by functions


v0.1.4 (Feb 27, 2018)
---------------------------

- Major code restructure around processing binary test and support for logging environment variable
    - BUILDTEST_LOGCONTENT
    - BUILDTEST_LOGDIR
    - BUILDTEST_LOGFILE

- Provide get functions to retrieve value from arg.parser
- Add support for Perl with ``--testset``
- Add for more logging support in module and eb verification

v0.1.3 (Feb 27, 2018)
--------------------------

There have been several changes in the buildtest framework to allow for more capabilities.

The following changes have been done in this release
- buildtest can generate binary test for same executable with multiple parameters. See
- Adding support for R, Perl and Python with more tests.
- R, Python, Perl (soon to come), and MPI tests are organized in testset using **--testset** flag
this allows for multiple packages to reuse tests across different apps. For instance OpenMPI, MPICH, MVAPICH and intel can now reference the mpi testset.
- Add support for **inputfile** YAML key to allow input redirection into program.
- Add support for **outputfile** YAML key to allow output redirection.
- Add support for argument passing using **arg** key word
- Add support for **iter** YAML key to allow N tests to be created.
- Switching BUILDTEST_MODULEROOT to BUILDTEST_MODULE_EBROOT to emphasize module tree should be coming from what easybuild generates.
- Fixed some bugs pertaining to CMakeLists.txt

v0.1.2 (Feb 27, 2018)
----------------------------

The current release add supports for logging by default.

buildtest will now report useful operations for each function call that can be used for troubleshooting. The logs work with options like --verbose to report extra details in log file.

- The logs display output on the following
    - Verification of software and toolchain with module file and easyconfig parameters
    - Display output of each test generated
    - Display changes to any CMakeLists.txt
    - Output key values from YAML configs
    - Output log from ancillary features like (**--list-toolchain**, **--list-unique-software**, **--software-version-relation**)

- buildtest can now search YAML configs and buildtest generated test scripts using the command **-fc** and **-ft**
- Now all buildtest-config files are removed and migrated to

v0.1.1 (Feb 27, 2018)
------------------------


In this release, we have restructured the source directory. Now there are two sub directories
 * ebapps
 * system

buildtest can now support binary tests for system packages. There is a command.yaml file for each system package in its own directory. Each system package is in its own subdirectory where the name of the directory is the name of the system package. buildtest is using RHEL7 package names as reference.

The following system package tests have been added

* binutils
* chrony
* git
* hwloc
* ncurses
* pinfo
* procps-ng
* sed
* time
* wget

Compile from source YAML scripts can now be stored in subdirectories. buildtest can now generate tests in sub directory, this would be essential for building tests for R, Python, Ruby, Perl, etc...

Tests for the following EB apps have been added:
* Python
    1. blist
    2. cryptography
    3. Cython
    4. dateutil
    5. deap
    6. funcsigs
    7. mpi4py
    8. netaddr
    9. netifaces
    10. nose
    11. numpy
    12. os
    13. paramiko
    14. paycheck
    15. pytz
    16. scipy
    17. setuptools


Added python documentation header for each function and GPL license section in all the files

v0.1.0 (Feb 26, 2017)
------------------------

buildtest generates test scripts from YAML files. The following apps have tests:

EasyBuild Applications
-------------------------
* Anaconda2
* binutils
* Bowtie
* Bowtie2
* CMake
* CUDA
* GCC
* git
* HDF5
* hwloc
* intel
* Java
* netCDF
* numactl
* OpenMPI
* Python

System Packages
-------------------

* acl
* coreutils
* curl
* diffstat
* gcc
* gcc-c++
* gcc-gfortran
* iptables
* ltrace
* perl
* powertop
* python
* ruby
