.. Note:: Please see :ref:`tutorial_setup` before you proceed with this section

.. _buildtest_e4s_testsuite:

Buildtest E4S Testsuite Integration
===================================

The `E4S Testsuite <https://github.com/E4S-Project/testsuite/>`_ is a collection of lightweight tests assembled for over 100 
software products provided by `E4S <https://e4s.io>`_ deployments. 
E4S is a spack based software stack but because not all spack packages provide internal testing functionality it 
is useful to have an alternative framework for testing deployed software.

The E4S Testsuite operates on a hierarchy of shell scripts with each test containing its own setup, clean, compile 
and run scripts. The `top level driver script <https://github.com/E4S-Project/testsuite/blob/master/test-all.sh>`_ sets up the test environment based on a configuration file which sets 
compilers, mpi run commands and other environment specific parameters. It then iterates through the selected tests 
and generates output consisting of log files for individual test runs and a summary listing of each test’s success or failure. The `README <https://github.com/E4S-Project/testsuite/blob/master/README.md>`_ provides more detail on its structure and usage.

Tests in the testsuite typically include source code and build files needed to build a small test application against 
libraries provided by the spack install along with any input files required for the subsequent run test. These are 
often extracted from test functionality included in the product’s source 
tree that is not included in the final install. An application may have multiple test definitions to support different 
configurations such as the use of different hardware accelerators.  Products with spack packages that include spack test 
functionality are trivial to add to the E4S Testsuite, as opposed to fully implementing a distinct test.

Buildspecs using E4S Testsuite
------------------------------

Because the E4S Testsuite provides and maintains pre-constructed tests for a number of products deployed at NERSC it often 
makes sense to invoke these tests rather than develop new ones. Buildtest buildspecs that make use of the E4S Testsuite 
follow the pattern of loading the relevant spack modules, acquiring the testsuite and executing the test driver script on 
the selected test. Buildtest ascertains and reports success or failure based on the return code provided by the E4S Testsuite driver script. 

This buildspec presents a typical e4s-testsuite invocation for a spack install of mpich. Before launching buildtest with this spec make sure mpich is available
in your spack environment by doing ``spack install mpich``. The example buildspec below should work in a generic linux environment where a spack provided mpich is installed. Fields needed to run in the perlmutter test environment are commented out for reference.

.. literalinclude:: ../../examples/spack/e4s_testsuite_mpich.yml
    :language: yaml

We can see an example of the E4S Testsuite in action by running the following command.

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/e4s_testuite_mpich.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/e4s_testuite_mpich.txt

View the test output by running this command. Note that the E4S Testsuite typically prints its results to the standard error output so we included the ``-e`` flag.

.. dropdown:: ``buildtest inspect query -o -e -t mpich_e4s_testsuite``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/e4s_testuite_mpich.yml
