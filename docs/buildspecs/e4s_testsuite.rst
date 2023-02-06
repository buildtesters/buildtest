.. Note:: Please see :ref:`tutorial_setup` before you proceed with this section

.. _buildtest_e4s_testsuite:

Buildtest E4S Testsuite Integration
===================================

The `E4S Testsuite <https://github.com/E4S-Project/testsuite/>`_ is a collection of lightweight tests assembled for over 100 
software products provided by Extreme Scale Scientific Software Stack `(E4S) <https://e4s.io>`_ deployments. 
E4S is a spack based software stack but because not all spack packages provide internal testing functionality it 
is useful to have an alternative framework for testing deployed software.

The E4S Testsuite operates on a hierarchy of shell scripts with each test containing its own ``setup.sh``, ``clean.sh``, ``compile.sh`` 
and ``run.sh`` scripts. The `top level driver script <https://github.com/E4S-Project/testsuite/blob/master/test-all.sh>`_ sets up the test environment based on a configuration file which sets 
compilers, mpi run commands and other environment specific parameters. It then iterates through the selected tests 
and generates output consisting of log files for individual test runs and a summary listing of each test’s success or failure. The `README <https://github.com/E4S-Project/testsuite/blob/master/README.md>`_ provides more detail on its structure and usage.

The provided tests typically include source code, build, and input files for quick-running example applications. Some import test code from the spack install location or invoke spack internal tests directly.

Buildspecs using E4S Testsuite
------------------------------

E4S Testsuite provides and maintains pre-constructed tests for a number of products deployed at NERSC. It often 
makes sense to invoke these tests rather than develop new ones. Buildtest buildspecs that make use of the E4S Testsuite 
follow the pattern of loading the relevant spack modules, acquiring the testsuite and executing the test driver script on 
the selected test.

Shown below is an example buildspec running E4S Testsuite for testing the spack package ``mpich``. In order to test mpich, we need to install mpich into our container environment by running ``spack install mpich`` prior to testing the package. We will clone E4S Testsuite and invoke the driver script ``test-all.sh`` for running the test. 

.. literalinclude:: ../../examples/spack/e4s_testsuite_mpich.yml
    :language: yaml

We can see an example of the E4S Testsuite in action by running the following command.

.. dropdown:: ``buildtest build -b /home/spack/buildtest/examples/spack/e4s_testsuite_mpich.yml``

    .. program-output:: cat buildtest_tutorial_examples/spack/build/e4s_testsuite_mpich.txt

E4S Testsuite prints full test logs to the standard error instead of stdout so we must use ``buildtest inspect query -e`` to view the full test results. Let's view the test output by running the following:

.. dropdown:: ``buildtest inspect query -o -e -t mpich_e4s_testsuite``

    .. program-output:: cat buildtest_tutorial_examples/spack/inspect/e4s_testsuite_mpich.txt
