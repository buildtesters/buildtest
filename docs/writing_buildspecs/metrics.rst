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


Metrics with Regex Type via 're'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Building on the previous example, we will use the ``re`` property specify the regular expression type to use. By default, buildtest will
use `re.search <https://docs.python.org/3/library/re.html#re.search>`_ if **re** is not specified; however you can specify **re** to use `re.match <https://docs.python.org/3/library/re.html#re.match>`_,
`re.fullmatch <https://docs.python.org/3/library/re.html#re.fullmatch>`_, or `re.search <https://docs.python.org/3/library/re.html#re.search>`_.

In this example, we will define 4 metrics **hpcg_text**, **hpcg_result**, **hpcg_file_text**, **hpcg_file_result**. The first two
metrics will capture from stdout using the ``regex`` property while the last two will capture from a file using the ``file_regex`` property.
The ``re.match`` will be used to capture the text **HPCG result is VALID** and **HPCG result is INVALID** from stdout and file, whereas
the ``re.search`` will be used to capture the test result **63.6515** and **28.1215** from stdout and file.

Finally, we will use the comparison operator :ref:`assert_eq` to compare the metrics with reference value.

.. literalinclude:: ../tutorials/metrics/metrics_with_regex_type.yml
    :language: yaml
    :emphasize-lines: 7-45

Let's attempt to build this test

.. dropdown:: ``buildtest build -b tutorials/metrics/metrics_with_regex_type.yml``

   .. command-output:: buildtest build -b tutorials/metrics/metrics_with_regex_type.yml

Upon completion, lets take a look at the metrics for this test, we can see this by running ``buildtest inspect query``
which shows the name of captured metrics and its corresponding values.

.. dropdown:: ``buildtest inspect query metric_regex_example_with_re``

   .. command-output:: buildtest inspect query metric_regex_example_with_re

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
