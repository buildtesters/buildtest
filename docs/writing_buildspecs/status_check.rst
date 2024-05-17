.. _status:

Status Checks
================

buildtest will record state of each test which can be ``PASS`` or ``FAIL``. By default a 0 exit code is
**PASS** and anything else is a **FAIL**. The ``status`` property can be used to determine how test will report its state.
Currently, we can match state based on the following:

  - :ref:`Return Code Match <returncode>`
  - :ref:`Runtime <runtime>`
  - :ref:`Regular Expression on output/error file <regex>`
  - :ref:`Regular Expression on arbitrary file <file_regex>`
  - :ref:`Comparison Operators <comparison_operators>`
  - :ref:`Explicit Test Status <explicit_status>`
  - :ref:`File Checks <file_checks>`
  - :ref:`File Count <file_count>`


.. _returncode:

`returncode`: Return Code Matching
-----------------------------------

buildtest can report PASS/FAIL based on returncode, by default a 0 exit code is PASS
and everything else is FAIL. The returncode can be a list of exit codes to match.
In this example we have four tests called ``exit1_fail``, ``exit1_pass``,
``returncode_list_mismatch`` and ``returncode_int_match``.  We expect **exit1_fail** and
**returncode_mismatch** to ``FAIL`` while **exit1_pass** and **returncode_int_match**
will ``PASS``.

.. literalinclude:: ../tutorials/test_status/pass_returncode.yml
   :language: yaml
   :emphasize-lines: 17,26,35

Let's build this test and pay close attention to the **status**
column in output.

.. dropdown:: ``buildtest build -b tutorials/test_status/pass_returncode.yml``

   .. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml
      :shell:

The ``returncode`` field can be an integer or list of integers but it may not accept
duplicate values. If you specify a list of exit codes, buildtest will check actual returncode
with list of expected returncodes specified by `returncode` field.

Shown below are examples of invalid returncodes:

.. code-block:: yaml

      # empty list is not allowed
      returncode: []

      # floating point is not accepted in list
      returncode: [1, 1.5]

      # floating point not accepted
      returncode: 1.5

      # duplicates are not allowed
      returncode: [1, 2, 5, 5]

.. _regex:

`regex`: Regular Expression on stdout/stderr
--------------------------------------------

buildtest can configure PASS/FAIL of test based on regular expression on output or error file. This can be useful
if you are expecting a certain output from the test as pose to returncode check.

In this example we introduce, the ``regex`` field which is part of **status** that expects
a regular expression via ``exp``. The ``stream`` property must be  **stdout** or **stderr** which indicates
buildtest will read output or error file and apply regular expression. If there is a match, buildtest will record the
test state as **PASS** otherwise it will be a **FAIL**. In this example, we have four tests that will apply two regular expression
on output file and two regular expression on error file.

.. literalinclude:: ../tutorials/test_status/status_regex.yml
   :language: yaml
   :emphasize-lines: 9-11,20-22,31-33,42-44

Now if we run this test, we will see first test will pass while second one will fail even though the returncode is
a 0. Take a close look at the **status** property

.. dropdown:: ``buildtest build -b tutorials/test_status/status_regex.yml``

   .. command-output:: buildtest build -b tutorials/test_status/status_regex.yml

.. _file_regex:

`file_regex`: Regular Expression on files
-----------------------------------------

In the previous example, we applied :ref:`regular expression on output or error file <regex>`; however, you may want to apply
regular expression on arbitrary files. This can be done by specifying ``file_regex`` property. The ``file_regex`` property is
an array of assertions, where each assertion must have ``filename`` and ``exp`` property. The ``filename`` property is the path
to filename and ``exp`` is the regular expression you want to apply.

In this example, we have three tests that make use of ``file_regex`` property. The first test will perform a regular expression
on multiple file names. The second test will attempt to check on a directory name which is not supported since regular expression must
be applied to file name. The third test will show that variable expansion and environment variable expansion is supported.

.. literalinclude:: ../tutorials/test_status/regex_on_filename.yml
   :language: yaml
   :emphasize-lines: 9-14,23-26,35-40

We can build this test by running the following command:

.. dropdown:: ``buildtest build -b tutorials/test_status/regex_on_filename.yml``

   .. command-output:: buildtest build -b tutorials/test_status/regex_on_filename.yml


.. _runtime:

`runtime`: Passing Test based on runtime
-----------------------------------------

buildtest can determine state of test based on `runtime` property which is part of
``status`` object. This can be used if you want to control how test `PASS` or `FAIL` based on
execution time of test. In example below we have five tests that make use of **runtime** property
for passing a test.  The runtime property support ``min`` and ``max`` property that can mark test
pass based on minimum and maximum runtime. A test will pass if it's execution time is greater than ``min``
time and less than ``max`` time. If `min` is specified without `max` property the upperbound is not set, likewise
`max` without `min` will pass if test is less than **max** time. The lower bound is not set, but test runtime
will be greater than 0 sec.

In test **timelimit_min**, we sleep for 2 seconds and it will pass because minimum runtime is 1.0 seconds. Similarly,
**timelimit_max** will pass because we sleep for 2 seconds with a max time of 5.0.

.. literalinclude:: ../tutorials/test_status/runtime_status_test.yml
   :language: yaml
   :emphasize-lines: 9-11,20-21,30-31,40-41,50-51

.. dropdown:: ``buildtest build -b tutorials/test_status/runtime_status_test.yml``

   .. command-output:: buildtest build -b tutorials/test_status/runtime_status_test.yml

If we look at the test results, we expect the first three tests **timelimit_min**, **timelimit_max**, **timelimit_min_max**
will pass while the last two tests fail because it fails to comply with runtime property.

.. dropdown:: ``buildtest report --filter buildspec=tutorials/test_status/runtime_status_test.yml --format name,id,state,runtime --latest``

   .. command-output:: buildtest report --filter buildspec=tutorials/test_status/runtime_status_test.yml --format name,id,state,runtime --latest

.. _explicit_status:

`state`: Explicitly Declare Status of Test
------------------------------------------

You can explicitly define status of test regardless of what buildtest does for checking status of test. This
can be useful if you want to explicitly mark a test as **PASS** or **FAIL** regardless of how test behaves. This can be done via
``state`` property which expects one of two types **PASS** or **FAIL**. If ``state`` property is specified, buildtest will ignore any checks
including returncode, regex, or runtime match.

In this next example we will demonstrate how one can use ``state`` property for marking test state. In this
example we have four tests. The first test ``always_pass`` will **PASS** even though we have a non-zero returncode. The
second test ``always_fail`` will **FAIL** even though it has a 0 returncode. The last two test demonstrate how one
can define state regardless of what is specified for returncode match. buildtest will honor the ``state`` property even if
their is a match on the returncode.

.. literalinclude:: ../tutorials/test_status/explicit_state.yml
   :language: yaml
   :emphasize-lines: 8,16,22-25,31-34

If we build this test, we expect buildtest to honor the value of ``state`` property

.. dropdown:: ``buildtest build -b tutorials/test_status/explicit_state.yml``

   .. command-output:: buildtest build -b tutorials/test_status/explicit_state.yml

.. _file_checks:

File Checks
------------

buildtest supports various file checks that can be used as means for passing test. This can include
checking for :ref:`file_existence`, :ref:`file_and_directory_check`, :ref:`symlink_check`, and :ref:`file_count`.

.. _file_existence:

`exists`: File Existence
~~~~~~~~~~~~~~~~~~~~~~~~~~

For instance, if you want to check for file existence, you can use  ``exists`` property
which expects a list of file or directory names to check. This can be useful if your test
will write some output file or directory and test will pass based on existence of file/directory.

In the example below we have two tests, first test will pass, where all files exist. We check for
files and directory path, note variable and shell expansion is supported.

In the second example, we expect this test to fail because filename **bar** does not exist.

.. literalinclude:: ../tutorials/test_status/exists.yml
   :language: yaml
   :emphasize-lines: 10-15,21-23

We can run this test by running the following, take note of the output.

.. dropdown:: ``buildtest build -b tutorials/test_status/exists.yml``

   .. command-output:: buildtest build -b tutorials/test_status/exists.yml

Each item in the ``exists`` field must be a string, which can lead to issue in example
below let's assume we want a test to pass based on a directory name **1**, if we specify
as follows, this test will fail validation.

.. literalinclude:: ../tutorials/test_status/file_exists_exception.yml
   :language: yaml
   :emphasize-lines: 7-8

We can validate this buildspec by running the following

.. dropdown:: ``buildtest bc validate -b tutorials/test_status/file_exists_exception.yml``
   :color: warning

    .. command-output:: buildtest bc validate -b tutorials/test_status/file_exists_exception.yml
       :returncode: 1

In order to run this test, we need to enclose each item in quotes. Shown below is the same test with quotations.

.. literalinclude:: ../tutorials/test_status/file_exists_with_number.yml
   :language: yaml
   :emphasize-lines: 7-8

Let's validate and build this test.


.. dropdown:: ``buildtest bc validate -b tutorials/test_status/file_exists_with_number.yml``

    .. command-output:: buildtest bc validate -b tutorials/test_status/file_exists_with_number.yml

.. dropdown:: ``buildtest build -b tutorials/test_status/file_exists_with_number.yml``

    .. command-output:: buildtest build -b tutorials/test_status/file_exists_with_number.yml

.. _file_and_directory_check:

`is_file`, `is_dir`: File and Directory Checks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the next example, we introduce checks for files and directory via ``is_file`` and
``is_dir`` property, which behaves similar to ``exists`` except they will check if each item
is a file or directory. We expect the first test to fail, because **$HOME/.bashrc** is
not a directory but a file. The second test will incorporate the same test and
use ``is_file`` for status check.

.. literalinclude:: ../tutorials/test_status/file_and_dir_check.yml
   :language: yaml
   :emphasize-lines: 7-11,17-22

Let's build the test and see the output.

.. dropdown:: ``buildtest build -b tutorials/test_status/file_and_dir_check.yml``

   .. command-output:: buildtest build -b tutorials/test_status/file_and_dir_check.yml

.. _symlink_check:

`is_symlink`: Symbolic Link Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can configure PASS/FAIL of test based on the status of symbolic link. This can be useful if your test will create a symbolic link to a file or directory and
test will pass if the symbolic link is present.

You can use the ``is_symlink`` property which expects a list of values that are checked for symbolic links. In the example below, the test will pass as all the values are valid symbolic links and are not broken. Note that variable and shell expansion
is supported.

.. literalinclude:: ../tutorials/test_status/is_symlink.yml
   :language: yaml
   :emphasize-lines: 9-13

We can run this test by running the following.

.. dropdown:: ``buildtest build -b tutorials/test_status/is_symlink.yml``

   .. command-output:: buildtest build -b tutorials/test_status/is_symlink.yml

.. _file_count:

`file_count`: File Count
-------------------------

buildtest can check for number of files in a directory. This can be useful if your test writes number of files and you
want to check if the number of files is as expected. You can use the ``file_count`` property to perform file count. This
property is a list of assertion, where each item is an object. The ``dir`` and ``count`` are required keys.

The ``dir`` is the path to directory to perform directory traversal, and ``count`` key is the number of expected files that will be
used for comparison. In the first test, we perform a directory walk and expect 5 files in the directory. We can perform directory
search based on file extension by using ``ext`` key. The ``ext`` property can be a string or a list. The second test will perform
directory walk on directory named **foo** and search for file extensions **.sh**, **.py**, **.txt**. The ``depth`` property controls
the maximum depth for directory traversal, this must be of an integer type. The ``depth`` property is optional and if not specified, we will
perform full directory traversal.

.. literalinclude:: ../tutorials/test_status/file_count.yml
   :language: yaml
   :emphasize-lines: 9-12,21-29


We can run this test by running the following.

.. dropdown:: ``buildtest build -b tutorials/test_status/file_count.yml``

   .. command-output:: buildtest build -b tutorials/test_status/file_count.yml

In the next example, we introduce ``filepattern`` property which allows you to check for files based on a pattern. The ``filepattern`` property
is a regular expression which is compiled via `re.compile <https://docs.python.org/3/library/re.html#re.compile>`_ and applied to a
directory path. Please note the regular expression must be valid, otherwise buildtest will not return any files during directory traversal.

You can use ``filepattern`` and ``ext`` property together to search for files. If both are specified, then we will search for files
with both methods and join the two list prior to performing comparison.

.. literalinclude:: ../tutorials/test_status/file_count_pattern.yml
   :language: yaml
   :emphasize-lines: 14-22,32-37


Let's build this test by running the following:

.. dropdown:: ``buildtest build -b tutorials/test_status/file_count_pattern.yml``

   .. command-output:: buildtest build -b tutorials/test_status/file_count_pattern.yml

In the next example, we will introduce ``filetype`` property that can be used to filter directory search based on file type.
The ``filetype`` property can one of the following values **file**, **dir**, **symlink**. Once set, the directory traversal will
seek out files based on the file type. Note that when ``filetype`` is set to ``dir`` we will return the parent directory and
all sub-directories. This test will create a few subdirectories and create symbolic link, next we will perform directory search
by directory and symbolic link. We expect this test to pass as we will find 3 directories and 2 symbolic links.

.. literalinclude:: ../tutorials/test_status/file_count_filetype.yml
   :language: yaml
   :emphasize-lines: 11-18

Let's build this test by running the following:

.. dropdown:: ``buildtest build -b tutorials/test_status/file_count_filetype.yml``

   .. command-output:: buildtest build -b tutorials/test_status/file_count_filetype.yml

Buildtest will perform a directory walk when using ``file_count``, which can run into performance issues if you have a large directory.
We have added a safety check during directory traversal to a maximum of **999999** files. You have the option to configure the directory
traversal limit using ``file_traversal_limit`` which is an integer, the default value is **10000** if not specified. The minimum value and
maximum value can be 1 and 999999 respectively.

In this next example, we will illustrate how this feature works. We will create 99 *.txt* files in directory **foo**. We will
perform two assertions with different values for ``file_traversal_limit``. In the first example, we will set this to 50 and
expect 50 files returned. We expect this check to be **True**. In the next example, we will set ``file_traversal_limit`` to 20 and
set ``count: 10`` where we should expect a failure. In principle, we should retrieve 20 files but this will mismatch the comparison check.

.. literalinclude:: ../tutorials/test_status/file_count_file_traverse_limit.yml
   :language: yaml
   :emphasize-lines: 9-16

We can try building this test by running the following:

.. dropdown:: ``buildtest build -b tutorials/test_status/file_count_file_traverse_limit.yml``

   .. command-output:: buildtest build -b tutorials/test_status/file_count_file_traverse_limit.yml

`mode`: Change Status Check Behavior to Logical AND/OR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the status check performed by buildtest is a logical OR, where if any of the status check is True, then the test will
PASS. However, if you want to change this behavior to logical AND, you can use the `mode` property. The valid values can be
[``AND``, ``and``, ``OR``, ``or``]. In the example below, we have two tests that illustrate the use of ``mode``.

.. literalinclude:: ../tutorials/test_status/mode.yml
   :language: yaml
   :emphasize-lines: 10,24,25-28

The first test uses ``mode: and`` which implies all status check are evaluated as logical **AND**, we expect this test to PASS.
In the second test, we use ``mode: or`` where status check are evaluated as logical **OR** which is the default behavior. Note if ``mode``
is not specified, it is equivalent to ``mode: or``. In second test, we expect this to pass because **regex** check will PASS however,
the **returncode** check will fail due to mismatch in returncode. If we changed this to ``mode: and`` then we would expect this test
to fail.

Shown below is the output of running this test.

.. dropdown:: ``buildtest build -b tutorials/test_status/mode.yml``

   .. command-output:: buildtest build -b tutorials/test_status/mode.yml


.. _linecount:

`linecount`: Line Count on Stdout/Stderr
-----------------------------------------

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

file_linecount: Line Count on File
-----------------------------------

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

.. _re:

`re`: Modify regular expression method
---------------------------------------

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
   :emphasize-lines: 6,8-11,17,19-22,28,30-33,39-41,43-52

Let's try running this test example and see the generated output, all test should pass with exception of ``re.match.stdout``.

.. dropdown:: ``buildtest build -b tutorials/test_status/specify_regex_type.yml``

    .. command-output:: buildtest build -b tutorials/test_status/specify_regex_type.yml

`post_run`: Specify Post Run Tests
-----------------------------------

Buildtest can run additional commands after test execution that can be specified via ``post_run`` property. This can be used to perform cleanup or additional
operations after test execution. To demonstrate this example we have the following buildspec. In this test we will create a directory named **demo** and create
a symbolic link named **$HOME/.bashrc_link**. You will notice that in ``status`` check we are comparing the existence of directory and symbolic link. This
is where ``post_run`` script comes into play where we want to remove the created directory and symbolic link. If we were to do this in ``run`` section, the test
will fail since **status** check will fail to find these files. The ``post_run`` property is a list of commands that will be executed in a bash shell.

.. literalinclude:: ../tutorials/post_run.yml
   :language: yaml
   :emphasize-lines: 6-16

Now we can build this test and see the output, note buildtest will run the post_run script after test execution and show the exit code of test. It won't affect the actual
test behavior even if the post run script fails to execute properly.

.. dropdown:: ``buildtest build -b tutorials/post_run.yml``

    .. command-output:: buildtest build -b tutorials/post_run.yml

We can confirm the files are not present by checking existence of these files by running the following commands

    .. command-output:: ls -l $HOME/.bashrc_link
        :returncode: 1

We can retrieve the full path to stage directory via ``buildtest path -s`` command given the name of test. The **demo** directory is created in stage directory
so if we run the following command we should see this directory is not present.

    .. command-output:: ls -l $(buildtest path -s post_run_example)/demo
