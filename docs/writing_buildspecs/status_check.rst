Status Checks
================

Buildtest has several mechanisms for determining how test will pass.
The status check is defined in the ``status`` field of a test. The status field is a list of
dictionaries where each dictionary is a status check.


linecount
----------

This check counts the number of lines in stdout or stderr and compares with reference count. This can be useful
if you want to make a test pass based on number of lines. buildtest will split lines by newline character and perform the comparison.

In the example below we will write 10 lines to standard output (stdout) and use the ``linecount`` status check to perform a comparison using the
reference count of 10. The ``linecount`` is an object which requires the fields: ``stream`` and ``count``. The ``stream`` can be **stdout** or **stderr**
and ``count`` is the reference count to compare against. This must be an integer value and greater than 0. In second test we will compare output
with standard error (``stream: stderr``) and compare with reference count of 5. Since the output is going to write 10 lines to error file we
should expect the second test to fail.

.. literalinclude:: ../tutorials/test_status/linecount.yml
   :language: yaml
   :emphasize-lines: 10-13, 23-26

Let's try building this test and you will see the test will pass based on line count comparison.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/test_status/linecount.yml``

    .. command-output:: buildtest build -b $BUILDTEST_ROOT/tutorials/test_status/linecount.yml

    We can inspect the output and error file for each corresponding test and we will notice that both tests will contain 10 lines of output.

    .. command-output:: buildtest inspect query -o linecount_stdout

    .. command-output:: buildtest inspect query -e linecount_stderr_mismatch
