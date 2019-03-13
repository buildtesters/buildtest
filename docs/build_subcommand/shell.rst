Shell Types (``buildtest build --shell <shell>``)
====================================================



Currently, buildtest supports the following shell types

- sh (default)
- bash
- csh

To create tests for different shell types use ``buildtest build --shell <shell-type>``.
You may set the environment variable ``BUILDTEST_SHELL`` or set this in your
``settings.yml``


Let's build test for ``CMake/3.9.5-GCCcore-6.4.0`` with ``csh`` support by
running ``buildtest build -s CMake/3.9.5-GCCcore-6.4.0 --shell csh``


.. program-output:: cat scripts/build_subcommand/shell/CMake-3.9.5-GCCcore-6.4.0_csh.txt

Now let's check the test files

.. program-output:: cat scripts/build_subcommand/shell/CMake-3.9.5-GCCcore-6.4.0_csh_listing.txt


Let's rerun this with bash: ``buildtest build -s CMake/3.9.5-GCCcore-6.4.0 --shell bash``


.. program-output:: cat scripts/build_subcommand/shell/CMake-3.9.5-GCCcore-6.4.0_bash.txt

You will notice the test scripts for ``csh`` and ``bash`` are indicated with shell
extension to avoid name conflict.

.. program-output:: cat scripts/build_subcommand/shell/CMake-3.9.5-GCCcore-6.4.0_bash_listing.txt

Let's take a look at the ``CMakeList.txt`` file
which contains the test parameter required to run tests via ``ctest``. Everytime a
test is created it is added in CMakeList.txt if you check the file you will
notice the extension is also configured in CMakeList.txt

.. program-output:: cat scripts/build_subcommand/shell/CMake-3.9.5-GCCcore-6.4.0_CMakelists.txt
