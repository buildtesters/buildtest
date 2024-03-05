Status Checks
================

Buildtest has several mechanisms for determining how test will pass.
The status check is defined in the ``status`` field of a test. The status field is a list of
dictionaries where each dictionary is a status check.

.. _linecount:

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

.. dropdown:: ``buildtest build -b tutorials/test_status/linecount.yml``

    .. command-output:: buildtest build -b tutorials/test_status/linecount.yml

    We can inspect the output and error file for each corresponding test and we will notice that both tests will contain 10 lines of output.

    .. command-output:: buildtest inspect query -o linecount_stdout

    .. command-output:: buildtest inspect query -e linecount_stderr_mismatch

.. _file_linecount:

file_linecount
---------------

The ``file_linecount`` status check is similar to :ref:`linecount` but instead of comparing output from stdout or stderr,
it compares output from a file. This is useful if you want to compare output from a file with a reference count.
The ``file_linecount`` is an array of objects which requires the fields: ``file`` and ``count``.
The ``file`` is the path to file and ``count`` is the reference count to compare against.

To demonstrate this feature we will write 10 lines to a file named **count.txt** and write output of one echo statement to file **hello.txt**.
We will use ``file_linecount`` field to read both files and compare with reference count. We expect both checks to pass.

.. literalinclude:: ../tutorials/test_status/file_linecount.yml
   :language: yaml
   :emphasize-lines: 12-16

Let's try building this test and you will see in the build output comparison check is performed on both files. Buildtest will perform a logical
AND operation when comparing multiple files for linecount match.

.. dropdown:: ``buildtest build -b tutorials/test_status/file_linecount.yml``

    .. command-output:: buildtest build -b tutorials/test_status/file_linecount.yml

The ``file`` property must be a valid file that is readable, if you specify a directory name or non-existent file then buildtest will
be unable to read the file, hence test will fail to perform comparison. In this next example, we perform a comparison on ``file: /tmp`` and
``file: badfile.txt`` both of which are invalid for file comparison.

.. literalinclude:: ../tutorials/test_status/file_linecount_failure.yml
   :language: yaml
   :emphasize-lines: 12-16

Buildtest will be able to run the test; however, the test will fail because its unable to read the files to get actual line count for comparison.

.. dropdown:: ``buildtest build -b tutorials/test_status/file_linecount_failure.yml``

    .. command-output:: buildtest build -b tutorials/test_status/file_linecount_failure.yml

Finally, we must note that line count is expected to be **0 or greater**, if you specify a negative value for ``count``
then buildtest will raise an error according to the JSON schema.

.. literalinclude:: ../tutorials/test_status/file_linecount_invalid.yml
   :language: yaml
   :emphasize-lines: 12-16

We will simply try validating this buildspec and you will see the error message from the JSON schema

.. dropdown:: ``buildtest buildspec validate -b tutorials/test_status/file_linecount_invalid.yml``
   :color: warning

    .. command-output:: buildtest build -b tutorials/test_status/file_linecount_invalid.yml
       :returncode: 1
