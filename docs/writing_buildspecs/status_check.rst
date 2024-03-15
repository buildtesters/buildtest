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
   :emphasize-lines: 11

We will simply try validating this buildspec and you will see the error message from the JSON schema

.. dropdown:: ``buildtest buildspec validate -b tutorials/test_status/file_linecount_invalid.yml``
   :color: warning

    .. command-output:: buildtest buildspec validate -b tutorials/test_status/file_linecount_invalid.yml
       :returncode: 1


re
--

The ``re`` property can be used to select the type of regular expression to use with :ref:`regex <regex>` or :ref:`file_regex <file_regex>`
which can be `re.search <https://docs.python.org/3/library/re.html#re.search>`_, `re.match <https://docs.python.org/3/library/re.html#re.match>`_
or `re.fullmatch <https://docs.python.org/3/library/re.html#re.fullmatch>`_. The ``re`` property is a string type which is used to select the
regular expression function to use. In this next example, we will demonstrate the use of this feature with both ``regex`` and ``file_regex``.
The ``re`` property is optional and if not specified it defaults to **re.search**.

Since **re.search** will search for text at any position in the string, the first test ``re.search.stdout`` will match the
string **is** with the output. In the second test ``re.match.stdout`` we use **re.match** which matches from beginning of
string with input pattern **is** with output. We expect this match to **FAIL** since the output starts with **This is ...**.

In the third test ``re.fullmatch.stdout`` we set ``re: re.fullmatch`` which will match the entire string with the pattern.
We expect this match to **PASS** since the output and pattern are exactly the same. In the fourth test ``match_on_file_regex`` we have
have three regular expression, one for each type **re.search**, **re.match** and **re.fullmatch**. All of these expressions will find a match
and this test will **PASS**.

.. literalinclude:: ../tutorials/test_status/specify_regex_type.yml
   :language: yaml
   :emphasize-lines: 11,22,33,46,49,52

Let's try running this test example and see the generated output, all test should pass with exception of ``re.match.stdout``.

.. dropdown:: ``buildtest build -b tutorials/test_status/specify_regex_type.yml``

    .. command-output:: buildtest build -b tutorials/test_status/specify_regex_type.yml
