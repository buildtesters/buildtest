Test Dependency
---------------

.. Note:: This feature is subject to change

Buildtest can support test dependencies which allows one to specify condition before running a test. Let's take a look
at this next example, we have a buildspec with three tests ``jobA``, ``jobB``, and ``jobC``. The test `jobA` will run immediately
but now we introduce a new keyword ``needs`` which is a list of test names as dependency. We want test `jobB` to run after jobA is
complete, and `jobC` to run once jobA and jobB is complete.

.. literalinclude:: ../tutorials/job_dependency/ex1.yml
   :language: yaml
   :emphasize-lines: 2,10,14,19,23

The ``needs`` property expects a list of strings, and values must match name of test.  If you specify an invalid
test name in `needs` property then buildtest will ignore the value. If multiple tests are specified in `needs` property then
all test must finish prior to running test.

Let's run this test, and take a note that buildtest will run test `jobA`, followed by `jobB` then `jobC`.

.. dropdown:: ``buildtest build -b tutorials/job_dependency/ex1.yml``

   .. command-output:: buildtest build -b tutorials/job_dependency/ex1.yml

Test Dependency by returncode
--------------------------------

In this next example, we can control behavior of job dependency based on returncode for a given test. This test has three
tests: ``test1``, ``test2`` and ``test3``. The first test will exit with returncode 1 but this test will pass because we have
set ``state: PASS`` to override the status check. The next test ``test2`` requires **test1** to have a returncode of 1 in order
to satisfy dependency. The ``returncode`` property expects a valid returncode and it can be a list of returncode similar to
how one specify ``returncode`` under the **status** property see :ref:`returncode`. The ``needs`` property can support multiple
test with returncode, in ``test3`` we require ``test1`` to have returncode 1 while ``test2`` has a returncode of 2. We expect `test2`
to return a returncode of 2 because of ``exit 2`` statement so we expect all three tests to run.

.. literalinclude:: ../tutorials/job_dependency/ex2.yml
   :language: yaml
   :emphasize-lines: 2,7-8,10,17-19,21,28-32

Let's build this test and take note of execution order of test.

.. dropdown:: ``buildtest build -b tutorials/job_dependency/ex2.yml``

   .. command-output:: buildtest build -b tutorials/job_dependency/ex2.yml

Test Dependency by state
---------------------------

You can specify ``state`` as a property to check for test state when specify test dependency. In this next example, we have
have four tests **pass_test**, **fail_test**, **pass_and_fail_test**, and **final_test**. The first test will be a PASS because
we have ``state: PASS``. The test ``fail_test`` depends on `pass_test` only if it has ``state: PASS``, if value is mismatch then test
will be skipped. Note that buildtest will skip test until next iteration if test is not executed, however if test is complete then buildtest
will cancel dependent test. We can specify multiple test dependencies with `state` property such as test **pass_and_fail_test** which expects
``pass_test`` to have `state: PASS` and ``fail_test`` to have `state: FAIL`. In test ``final_test``, shows how you can combine the format, the
``needs`` property is a list of object where each element is name of test. If no properties are associated with test name then buildtest will
wait until job is complete to execute test. In this example, the test expects both ``pass_test`` and ``fail_test`` to run while ``pass_and_fail_test``
must have returncode of 1.

.. literalinclude:: ../tutorials/job_dependency/ex3.yml
   :language: yaml
   :emphasize-lines: 2,6-7,12,18-20,25,29-33,40,44-48

Let's build this test and take note all tests are run.

.. dropdown:: ``buildtest build -b tutorials/job_dependency/ex3.yml``

   .. command-output:: buildtest build -b tutorials/job_dependency/ex3.yml

In this next example, we have three tests the first test will ``runtime_test`` will sleep for 5 seconds but it will fail due to runtime
requirement of 2sec. The next two tests ``runtime_test_pass`` and ``runtime_test_fail`` both depend on ``runtime_test`` however due to condition
only one of them can be run because ``runtime_test_pass`` expects `runtime_test` to have `state: PASS` while ``runtime_test_fail`` expects `runtime_test`
to have `state: FAIL`. This type of workflow can be used if you want to run a set of test based on one condition while running a different set of
test based on the negative condition.

.. literalinclude:: ../tutorials/job_dependency/ex4.yml
   :language: yaml
   :emphasize-lines: 2,6-8,11,15-17,20,24-26

Let's build this test and take note that we only run two tests and **runtime_test_fail** was skipped because test **runtime_test** has a
``state: PASS``.

.. dropdown:: ``buildtest build -b tutorials/job_dependency/ex4.yml``

   .. command-output:: buildtest build -b tutorials/job_dependency/ex4.yml