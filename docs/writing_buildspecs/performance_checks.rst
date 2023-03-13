.. _perf_checks:

Performance Checks
====================

.. _metrics:

Defining Metrics
------------------

buildtest provides a method to define test metrics in the buildspecs which can be used to
store arbitrary content from the output/error file or an arbitrary file into named metric. The
``metrics`` property is used to define a list of metric names using regular expression to assign a value
to the metric. In this example, we have two tests that define metrics ``hpcg_rate_stream``, ``hpcg_state_stream``
in the first test and ``hpcg_rate_file``, ``hpcg_state_file`` in the second test. The ``stream`` property is used
to read from stdout/stderr and apply the regular expression defined by ``exp``, whereas ``file_regex`` is used
to define metrics from an arbitrary file where ``file`` is the path to file.

.. literalinclude:: ../tutorials/metrics/metrics_regex.yml
    :language: yaml
    :emphasize-lines: 8-18,26-36

The metrics can be used with :ref:`comparison_operators` for performing more sophisticated status checks.
By default, a metric will be an empty dictionary if there is no ``metrics`` property. If we fail to match
a regular expression, the metric will be defined as an empty string (``''``).

.. Note::
   If your regular expression contains an escape character ``\`` you must surround your
   string in single quotes ``'`` as pose to double quotes ``"``

Let's build this test.

.. dropdown:: ``buildtest build -b tutorials/metrics/metrics_regex.yml``

   .. command-output:: buildtest build -b tutorials/metrics/metrics_regex.yml

The metrics are captured in the test report which can
be queried via ``buildtest report`` or ``buildtest inspect query``. Metrics can be seen in the test metadata,
for instance you can run ``buildtest inspect query`` and you will see metrics shown in table output.

.. dropdown:: ``buildtest inspect query metric_regex_example metric_file_regex``

    .. command-output:: buildtest inspect query metric_regex_example metric_file_regex

We can query the metrics via ``buildtest report`` which will display all metrics as a comma seperated
**Key/Value** pair. We can use ``buildtest report --format metrics`` to extract all metrics for a test.
Internally, we store the metrics as a dictionary but when we print them out via ``buildtest report`` we
join them together into a single string. Shown below is the metrics for the previous build.

.. dropdown:: ``buildtest report --filter buildspec=tutorials/metrics/metrics_regex.yml --format name,metrics``

   .. command-output:: buildtest report --filter buildspec=tutorials/metrics/metrics_regex.yml --format name,metrics


Invalid Metrics
~~~~~~~~~~~~~~~~~

We will discuss a few edge-cases when defining metrics that can lead to validation error. The `file_regex` and
`regex` property can't be declared at the same time when defining a metric. In example below
we have defined a metric named ``hello`` that uses both ``regex`` and ``file_regex``.

.. literalinclude:: ../tutorials/metrics/invalid_metrics.yml
    :language: yaml
    :emphasize-lines: 10-15

If we try to validate this buildspec, we will get an error message that ``regex`` and ``file_regex`` can't be specified
at the same time.

.. dropdown:: ``buildtest buildspec validate  -b tutorials/metrics/invalid_metrics.yml``
   :color: warning

   .. command-output:: buildtest buildspec validate  -b tutorials/metrics/invalid_metrics.yml
      :returncode: 1

When defining a metrics, you must specify ``regex`` or ``file_regex`` property in order to capture metric. If its not
specified, you will run into validation error. In this example, we define a metrics named ``foo``, but we don't
specify the ``regex`` or ``file_regex`` property therefore, this metric is invalid.

.. literalinclude:: ../tutorials/metrics/missing_required_in_metrics.yml
    :language: yaml
    :emphasize-lines: 7-9

The metrics must follow a pattern, this is typically alphanumeric characters including dot (``.``), hypen (``-``)
and underscore (``_``). In this example below, we have an invalid metric that doesn't conform to pattern.

.. literalinclude:: ../tutorials/metrics/invalid_metric_name.yml
    :language: yaml
    :emphasize-lines: 8

Let's try validating the buildspec to see the error message.

.. dropdown:: ``buildtest buildspec validate  -b tutorials/metrics/invalid_metric_name.yml``
   :color: warning

   .. command-output:: buildtest buildspec validate  -b tutorials/metrics/invalid_metric_name.yml
      :returncode: 1


.. _comparison_operators:

Comparison Operators
----------------------

buildtest supports several comparison operators as part of status check such as **>**, **>=**, **<=**, **<**, **==**, **!=**. Each metric
is compared with a reference value that can be useful when running performance checks. In this section we will cover the following comparison:

- :ref:`assert_ge`
- :ref:`assert_gt`
- :ref:`assert_le`
- :ref:`assert_eq`
- :ref:`assert_ne`
- :ref:`assert_range`

.. _assert_ge:

Greater Equal
~~~~~~~~~~~~~~

buildtest can determine status check based on performance check. In this next example, we will run the
`STREAM <https://www.cs.virginia.edu/stream/>`_ memory benchmark and capture :ref:`metrics <metrics>` named ``copy``, ``scale``
``add`` and ``triad`` from the output and perform an Assertion Greater Equal (``assert_ge``) with a reference value.

The ``assert_ge`` contains a list of assertions where each metric name is
referenced via ``name`` that is compared with the reference value defined by ``ref`` property. The comparison
is ``metric_value >= ref``, where **metric_value** is the value assigned to the metric name captured by the regular
expression. The ``type`` field in the metric section is used for the type conversion which can be **float**, **int**, or **string**.
The ``item`` is a numeric field used in `match.group <https://docs.python.org/3/library/re.html#re.Match.group>`_ to retrieve the output
from the regular expression search. The item must be non-negative number.

.. literalinclude:: ../tutorials/perf_checks/assert_ge.yml
    :language: yaml
    :emphasize-lines: 12-46
    :linenos:


buildtest will evaluate each assertion in the list and use a logical AND to determine the final
status of ``assert_ge``.

Let's build this test, take a close look at the output of ``buildtest build`` and take note of the assertion
statement.


.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_ge.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_ge.yml

Let's run ``buildtest inspect query -o stream_test`` to retrieve the test details and output of STREAM test.

.. dropdown:: ``buildtest inspect query -o stream_test``

    .. command-output:: buildtest inspect query -o stream_test

.. _assert_gt:

Greater Than
~~~~~~~~~~~~~~

In this example, we perform a **>** operation, this can be done via ``assert_gt`` property

.. literalinclude:: ../tutorials/perf_checks/assert_gt.yml
    :language: yaml
    :emphasize-lines: 37-46
    :linenos:

.. _assert_le:

Less Than Equal
~~~~~~~~~~~~~~~~~

In this example, we perform a **<=** operation, this can be done via ``assert_le`` property

.. literalinclude:: ../tutorials/perf_checks/assert_le.yml
    :language: yaml
    :emphasize-lines: 37-46
    :linenos:

.. _assert_eq:

Assert Equal
~~~~~~~~~~~~~~

buildtest can perform assert equality check with metrics to determine status of test. In this next example, we define
four metrics **x**, **y**, **first**, and **last** which will be compared with its reference value. We introduce a new
property ``assert_eq`` which is composed of list of assertions. Each reference is converted to its appropriate
type (``int``, ``float``, ``str``).

.. literalinclude:: ../tutorials/perf_checks/assert_eq.yml
    :language: yaml
    :emphasize-lines: 40-49
    :linenos:

This test is expected to pass where all assertions are **True**. Let's build the test and see the output

.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_eq.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_eq.yml

.. dropdown:: ``buildtest inspect query -o assert_eq_example``

    .. command-output:: buildtest inspect query -o assert_eq_example

In the next example, we have two tests to highlight some exceptions. In the first test, we define an invalid metric name **invalid_metric**
in ``assert_eq`` since this metric was not defined in ``metrics`` field, therefore this test will fail. The second test will fail because we have
a mismatch in value captured by metric ``x`` which is **1** however the reference value is **2**.

.. literalinclude:: ../tutorials/perf_checks/assert_eq_exceptions.yml
    :language: yaml
    :emphasize-lines: 21-22,27-28,33,40,41
    :linenos:

Let's build this test and see the output.

.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_eq_exceptions.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_eq_exceptions.yml

.. _assert_ne:

Assert Not Equal
~~~~~~~~~~~~~~~~~~

In this section, we will discuss the inverse equality operation **Not Equal** check (**!=**) with reference value.

We can use ``assert_ne`` property to perform **!=** check, it works similar to **assert_eq** with data types **int**,
**float** and **str**. In this example, we check the metrics ``x``, ``y``, ``first`` and ``last`` and each metric
should pass. The reference value is converted to the data-type (``type`` field) for each metrics

.. literalinclude:: ../tutorials/perf_checks/assert_ne.yml
    :language: yaml
    :emphasize-lines: 17,23,29,35,41-49
    :linenos:

We expect this test to pass. In order to run this test, you can do the following

.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_ne.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_ne.yml

.. _assert_range:

Assert Range
~~~~~~~~~~~~~

The ``assert_range`` property can be used to test performance for a metric given a lower and upper bound. This property expects
one to specify ``lower`` and ``upper`` field which must be an integer or floating point number to perform comparison. buildtest will
perform an assertion, if metric value is in the range specified by **lower** and **upper**, then test will pass. Shown below
is an example using the ``assert_range`` property with stream benchmark.

.. literalinclude:: ../tutorials/perf_checks/assert_range.yml
    :language: yaml
    :emphasize-lines: 37-50
    :linenos:

Let's build this test and see the output


.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_range.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_range.yml

Note that performance results may vary on your system and depending on the metric value you may want to adjust the
lower and upper bound to match your requirement.

Contains and Not Contains
--------------------------

Buildtest can perform status check with a list of reference values and check if metrics value is in the list. The
property ``contains`` and ``not_contains`` can be used to perform this type of check. The ``ref`` property is a list of
reference values that a metric must have to pass metrics check.

In example below we have two tests, the first test perform ``contains`` and ``not_contains`` on metrics **x**. We expect both
status check will pass. The second test is expected to fail because metric ``x`` will store integer value **1** but the list has
string equivalent **'1'**.

.. literalinclude:: ../tutorials/perf_checks/contains.yml
    :language: yaml
    :emphasize-lines: 17-23,39-42
    :linenos:

You can run this test, by running the following command

.. dropdown:: ``buildtest build -b tutorials/perf_checks/contains.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/contains.yml