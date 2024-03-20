Buildtest Tutorial on Perlmutter
===================================

This tutorial will be conducted on the `Perlmutter <https://docs.nersc.gov/systems/perlmutter/>`_ system. If you need account access please
`obtain a user account <https://docs.nersc.gov/accounts/>`_.

Setup
------

Once you have a NERSC account, you can `connect to any NERSC system <https://docs.nersc.gov/connect/>`_.
terminal client and ssh into perlmutter as follows::

    ssh <user>@perlmutter-p1.nersc.gov

To get started please load the **python** module since you will need python 3.8 or higher to use buildtest. This can be done by running::

    module load python

Next, you should :ref:`Install buildtest <installing_buildtest>` by cloning the repository into your HOME directory::

    git clone https://github.com/buildtesters/buildtest.git $HOME/buildtest

.. note::

    Please make sure you create a python virtual environment before you proceed with this tutorial.

Once you have buildtest setup, please clone the following repository into your home directory::

    git clone https://github.com/buildtesters/buildtest-nersc $HOME/buildtest-nersc

You will need to set the environment variable `BUILDTEST_CONFIGFILE` which will
point to the configuration file required to use buildtest on Perlmutter.

.. code-block:: console

    export BUILDTEST_CONFIGFILE=$HOME/buildtest-nersc/config.yml

Once you are done, please navigate back to the root of buildtest by running::

    cd $BUILDTEST_ROOT

The exercise can be found in directory `buildtest/perlmutter_tutorial <https://github.com/buildtesters/buildtest/tree/devel/perlmutter_tutorial>`_
where you will have several exercises to complete. You can navigate to this directory by running::

    cd $BUILDTEST_ROOT/perlmutter_tutorial

**If you get stuck on any exercise, you can see the solution to each exercise in file ".solution.txt"**

.. note::

    For exercise 2 and 3, you can check the solution by running the shell script ``bash .solution.sh``

Exercise 1: Performing Status Check
-------------------------------------

In this exercise, you will check the version of Lmod using the environment variable **LMOD_VERSION** and specify the
the output using a :ref:`regular expression <regex>`. We will run the test with an invalid regular expression and see if test **FAIL** and
rerun test until it **PASS**. Shown below is the example buildspec and please fix the highlighting lines in the test

.. literalinclude:: ../perlmutter_tutorial/ex1/module_version.yml
   :language: yaml
   :emphasize-lines: 3-4

.. todo::

    - Run the test by running ``buildtest build -b $BUILDTEST_ROOT/perlmutter_tutorial/ex1/module_version.yml`` and you will notice failure in validation
    - Validate the buildspec using ``buildtest buildspec validate`` to determine the error
    - Fix the buildspec and rerun ``buildtest buildspec validate`` until we have a valid buildspec.
    - Add a regular expression on ``stdout`` stream and make sure test fails
    - Check output of test via ``buildtest inspect query``
    - Update regular expression to match output with value of **$LMOD_VERSION** reported in test and rerun test until it passes.


Exercise 2: Querying Buildspec Cache
-------------------------------------

In this exercise you will learn how to use the :ref:`buildspec_interface`. Let's build the cache by running the following::

    buildtest buildspec find --root $HOME/buildtest-nersc/buildspecs --rebuild -q

.. todo::

    1. Find all tags
    2. List all filters and format fields
    3. Format tables via fields ``name``, ``description``
    4. Filter buildspecs by tag ``e4s``
    5. List all invalid buildspecs
    6. Validate all buildspecs by tag ``e4s``
    7. Show content of test ``hello_world_openmp``

Exercise 3: Query Test Report
-------------------------------

In this exercise you will learn how to :ref:`query test report <test_reports>`. This can be done by
running ``buildtest report``.

Before you start, please run the following command::

    buildtest bd -b $HOME/buildtest-nersc/buildspecs/apps/spack/

.. todo::

    1. List all filters and format fields
    2. Query all tests by returncode 0
    3. Query all tests by tag ``e4s``
    4. Print the total count of all failed tests

Let's upload the tests to CDASH by running the following::

    buildtest cdash upload $USER-buildtest-tutorial

Buildtest :ref:`cdash integration <cdash_integration>` via ``buildtest cdash upload`` allows buildtest to push test results to CDASH server. The test results
are captured in report file typically shown via ``buildtest report``. CDASH allows one to easily process the test results in web-interface.

If you were successful in running above command, you should see a link to CDASH server https://my.cdash.org with link to test results, please click on the link
to view your test results and briefly analyze the test results. Shown below is an example output

.. code-block:: console

       buildtest cdash upload $USER-buildtest-tutorial
    Reading report file:  /Users/siddiq90/Documents/github/buildtest/var/report.json
    Uploading 110 tests
    Build Name:  siddiq90-buildtest-tutorial
    site:  generic
    MD5SUM: a589c72bcdabdab9038600a2789e429f
    You can view the results at: https://my.cdash.org//viewTest.php?buildid=2278337


Exercise 4: Specifying Performance Checks
--------------------------------------------

In this exercise, you will be running the `STREAM benchmark <https://www.cs.virginia.edu/stream/>`_ and use :ref:`comparison operators <comparison_operators>`
to determine if test will pass based on the performance results. Shown below is the stream test that we will be using for this exercise

.. literalinclude:: ../perlmutter_tutorial/ex4/stream.yml
   :language: yaml

.. todo::

    - Run the stream test by running ``buildtest build -b $BUILDTEST_ROOT/perlmutter_tutorial/ex4/stream.yml``
    - Check the output of metrics ``copy`` and ``scale`` by running **buildtest inspect query -o stream_test**
    - Use the :ref:`assert_ge` check with metric ``copy`` and ``scale``. Specify a reference value `50000` for metric **copy** and **scale***
    - Run the same test and examine output
    - Next try different reference value such as ``5000`` and rerun test and see output

Exercise 5: Running a Batch Job
--------------------------------

In this exercise, you will submit a batch job that will run ``hostname`` in the slurm cluster. Shown below is the example buildspec

.. literalinclude:: ../perlmutter_tutorial/ex5/hostname.yml
   :language: yaml
   :emphasize-lines: 5,7,8

Take note that the test will run on executor ``perlmutter.slurm.debug`` which corresponds to the slurm ``debug`` queue on Perlmutter. The ``sbatch`` options
specify the :ref:`batch directives <batch_support>` for running the job.

In this exercise you are requested to do the following:

.. todo::

    - Run the test with poll interval for 10 sec ``$BUILDTEST_ROOT/perlmutter_tutorial/ex5/hostname.yml`` and take note of output, you should see job is submitted to batch scheduler. Refer to ``buildtest build --help`` for list of complete options
    - Check the output of test via ``buildtest inspect query``
    - Update the test to make use of :ref:`Multiple Executors <multiple_executors>` and run test on both **regular** and **debug** queue and rerun the test.
    - Rerun same test and you should see two test runs for **hostname_perlmutter** one for each executor.

    If you have completed this exercise, you should expect the following output from ``buildtest build``.

    .. code-block:: console

                                                                        Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                               ┃ executor                    ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime  ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ hostname_perlmutter/80e317c1          │ perlmutter.slurm.regular    │ PASS   │ N/A N/A N/A                         │ 0          │ 45.324512│
        ├───────────────────────────────────────┼─────────────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
        │ hostname_perlmutter/b1d7b318          │ perlmutter.slurm.debug      │ PASS   │ N/A N/A N/A                         │ 0          │ 75.54278 │
        └───────────────────────────────────────┴─────────────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘
