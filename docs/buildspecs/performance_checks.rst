.. _perf_checks:

Performance Checks
====================

.. _metrics:

Defining Metrics
------------------

buildtest provides a method to define test metrics in the buildspecs which can be used to
store arbitrary content from the output/error file into named metric. A metric is
defined using the ``metrics`` property where each element under the **metrics** property
is the name of the metric which must be a unique name. A metric can apply regular expression
on stdout, stderr like in this example below. The metrics are captured in the test report which can
be queried via ``buildtest report`` or ``buildtest inspect``. Shown below is an example
where we define two metrics named ``hpcg_rating`` and ``hpcg_state``.

.. literalinclude:: ../tutorials/metrics_regex.yml
    :language: yaml
    :emphasize-lines: 8-19

The metrics will not impact behavior of test, it will only impact the test report. By default
a metric will be an empty dictionary if there is no ``metrics`` property. If we fail to match
a regular expression, the metric will be defined as an empty string.

.. Note::
   If your regular expression contains an escape character ``\`` you must surround your
   string in single quotes ``'`` as pose to double quotes ``"``

Let's build this test.

.. dropdown:: ``buildtest build -b tutorials/metrics_regex.yml``

   .. command-output:: buildtest build -b tutorials/metrics_regex.yml

We can query the metrics via ``buildtest report`` which will display all metrics as a comma separted
**Key/Value** pair. We can use ``buildtest report --format metrics`` to extract all metrics for a test.
Internally, we store the metrics as a dictionary but when we print them out via ``buildtest report`` we
join them together into a single string. Shown below is the metrics for the previous build.

.. dropdown:: ``buildtest report --filter buildspec=tutorials/metrics_regex.yml --format name,metrics``

   .. command-output:: buildtest report --filter buildspec=tutorials/metrics_regex.yml --format name,metrics

You can define a metric based on :ref:`variables <variables>` or :ref:`environment variables <environment_variables>`
which requires you have set ``vars`` or ``env`` property in the buildspec. The ``vars`` and
``env`` is a property under the metric name that can be used to reference name
of variable or environment variable. If you reference an invalid name, buildtest will assign the metric an empty string.
In this next example, we define two metrics ``gflop`` and ``foo`` that are assigned to variable ``GFLOPS`` and
environment variable ``FOO``.


Assert Greater Equal
----------------------

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

Assert Equal
---------------

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

Assert Range
-------------

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