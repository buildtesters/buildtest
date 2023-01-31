Buildtest Tutorial on Perlmutter
===================================

This tutorial will be conducted on the `Perlmutter <https://docs.nersc.gov/systems/perlmutter/>`_ system. If you need account access please
`obtain a user account <https://docs.nersc.gov/accounts/>`_.

Setup
------

Once you have a NERSC account, you can `connect to any NERSC system <https://docs.nersc.gov/connect/>`_.
terminal client and ssh into perlmutter as follows::

    ssh <user>@perlmutter-p1.nersc.gov

To get started please load the **python** module since you will need python 3.7 or higher to use buildtest. This can be done by running::

    module load python

Next, you should :ref:`Install buildtest <installing_buildtest>` by cloning the repository into your home directory::

    cd $HOME
    git clone https://github.com/buildtesters/buildtest.git

Once you have buildtest setup, please clone the following repository into your home directory as follows::

    git clone https://github.com/buildtesters/buildtest-nersc $HOME/buildtest-nersc
    export BUILDTEST_CONFIGFILE=$HOME/buildtest-nersc/config.yml

Once you are done, please navigate back to the root of buildtest::

    cd $BUILDTEST_ROOT

**If you get stuck on any exercise, you can see the solution to each exercise in file ".solution.txt"**

Exercise 1: Running a Batch Job
--------------------------------

In this exercise, we will submit a batch job that will run `hostname` in the slurm cluster. Shown below is the example buildspec

.. literalinclude:: ../perlmutter_tutorial/ex1/hostname.yml
   :language: yaml

Let's run this test with a poll interval of ten seconds::

   buildtest build -b $BUILDTEST_ROOT/perlmutter_tutorial/ex1/hostname.yml --pollinterval=10

Once test is complete, check the output of the test by running::

    buildtest inspect query -o hostname_perlmutter

Next, let's update the test such that it runs on both the **regular** and **debug** queue. You will need to update the **executor** property and
specify a regular expression. Please refer to :ref:`Multiple Executors <multiple_executors>` for reference. You can retrieve a list of available executors
by running ``buildtest config executors``.

Once you have updated and re-run the test, you should see two test runs for **hostname_perlmutter**, one for each executor. If you ran this successfully, in output of
``buildtest build`` you should see a test summary with two executors

.. code-block:: console

                                                                Test Summary
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ builder                               ┃ executor                    ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ hostname_perlmutter/80e317c1          │ perlmutter.slurm.regular    │ PASS   │ N/A N/A N/A                         │ 0          │ 45.324512│
├───────────────────────────────────────┼─────────────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
│ hostname_perlmutter/b1d7b318          │ perlmutter.slurm.debug      │ PASS   │ N/A N/A N/A                         │ 0          │ 75.54278 │
└───────────────────────────────────────┴─────────────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘


Exercise 2: Performing Status Check
------------------------------------

In this exercise, we will check the version of Lmod using the environment variable **LMOD_VERSION** and specifying the
the output using a :ref:`regular expression <regex>`. We will run the test with an invalid regular expression and see if test fails and
rerun example until it passes

.. literalinclude:: ../perlmutter_tutorial/ex2/module_version.yml
   :language: yaml

First let's try running this test, you will notice the test will fail validation::

    buildtest build -b perlmutter_tutorial/ex2/module_version.yml


**TODO:**

- Validate the buildspec using ``buildtest buildspec validate``
- Add a regular expression on ``stdout`` stream and make sure test fails
- Check output of test via ``buildtest inspect query``
- Update regular expression to match output with value of **$LMOD_VERSION** reported in test and rerun test until it passes.


Exercise 3: Querying Buildspec Cache
-------------------------------------

In this exercise you will learn how to use the :ref:`buildspec_interface`. Let's build the cache by running the following::

    buildtest buildspec find --root $HOME/buildtest-nersc/buildspecs --rebuild -q

In this task you will be required to do the following

**TODO:**

1. Find all tags
2. List all filters and format fields
3. Format tables via fields ``name``, ``description``
4. Filter buildspecs by tag ``e4s``
5. List all invalid buildspecs
6. Validate all buildspecs by tag ``e4s``
7. Show content of test ``hello_world_openmp``

Exercise 4: Querying Test Reports
----------------------------------

In this exercise you will learn how to :ref:`query test reports <test_reports>`. This can be done by
running ``buildtest report``. In this task please do the following

1. List all filters and format fields
2. Query all tests by returncode 0
3. Query all tests by tag ``e4s``
4. Print the total count of all failed tests

Let's upload the tests to CDASH by running the following::

    buildtest cdash upload $USER-buildtest-tutorial

If you were successful, you should see a link to https://my.cdash.org with link to test results, please click on the link
to view your test results and briefly analyze the test results.

.. code-block:: console

       buildtest cdash upload $USER-buildtest-tutorial
    Reading report file:  /Users/siddiq90/Documents/github/buildtest/var/report.json
    Uploading 110 tests
    Build Name:  siddiq90-buildtest-tutorial
    site:  generic
    MD5SUM: a589c72bcdabdab9038600a2789e429f
    You can view the results at: https://my.cdash.org//viewTest.php?buildid=2278337


Exercise 5: Specifying Performance Checks
--------------------------------------------

In this task, we will running the STREAM benchmark and use :ref:`performance checks <perf_checks>` to determine if
test will pass based on the performance results. Shown below is stream example that we will be using for this exercise

.. literalinclude:: ../perlmutter_tutorial/ex5/stream.yml
   :language: yaml

First, let's build this test and analyze the output::

  buildtest build -b perlmutter_tutorial/ex5/stream.yml
  buildtest inspect query -o stream_test

**TODO**

- Check the output of metrics ``copy`` and ``scale`` in the command **buildtest inspect query -o stream_test**
- Use the :ref:`assert_ge` check with metric ``copy`` and ``scale``. Specify a reference value (pick some high number) for metric **copy** and **scale*** that will cause test to **FAIL**.
- Next try different reference values and make sure test will **PASS**.
