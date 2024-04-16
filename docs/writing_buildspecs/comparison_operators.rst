.. _comparison_operators:

Comparison Operators
=====================

buildtest supports several comparison operators as part of status check such as **>**, **>=**, **<=**, **<**, **==**, **!=**. Each metric
is compared with a reference value that can be useful when running performance checks. In this section we will cover the following comparison:

- :ref:`assert_ge`
- :ref:`assert_gt`
- :ref:`assert_le`
- :ref:`assert_lt`
- :ref:`assert_eq`
- :ref:`assert_ne`
- :ref:`assert_range`

.. _assert_ge:

`assert_ge`: Greater Equal
---------------------------

buildtest can determine status check based on performance check. In this next example, we will run the
`STREAM <https://www.cs.virginia.edu/stream/>`_ memory benchmark and capture :ref:`metrics <metrics>` named ``copy``, ``scale``
``add`` and ``triad`` from the output and perform an Assertion Greater Equal (``assert_ge``) with a reference value.

The ``assert_ge`` contains a list of assertions in the ``comparisons`` property where each metric name is
referenced via ``name`` that is compared with the reference value defined by ``ref`` property. The comparison
is ``metric_value >= ref``, where **metric_value** is the value assigned to the metric name captured by the regular
expression. The ``type`` field in the metric section is used for the type conversion which can be **float**, **int**, or **string**.
The ``item`` is a numeric field used in `match.group <https://docs.python.org/3/library/re.html#re.Match.group>`_ to retrieve the output
from the regular expression search. The item must be non-negative number.

.. literalinclude:: ../tutorials/perf_checks/assert_ge.yml
    :language: yaml
    :emphasize-lines: 12-48
    :linenos:


buildtest will evaluate each assertion in the list and use a logical AND to determine the final
status of ``assert_ge``. The keyword ``mode`` is used to determine whether to perform a logical
**OR** / **AND** operation when evaluating the final expression. The ``mode`` can be any of the
values: [``AND``, ``OR``, ``and``, ``or``]. If ``mode`` is ommitted the default is logical **AND**.

Let's build this test, take a close look at the output of ``buildtest build`` and take note of the assertion
statement.


.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_ge.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_ge.yml

Let's run ``buildtest inspect query -o stream_test`` to retrieve the test details and output of STREAM test.

.. dropdown:: ``buildtest inspect query -o stream_test``

    .. command-output:: buildtest inspect query -o stream_test

.. _assert_gt:

`assert_gt`: Greater Than
-------------------------

In this example, we perform a **>** operation, this can be done via ``assert_gt`` property

.. literalinclude:: ../tutorials/perf_checks/assert_gt.yml
    :language: yaml
    :emphasize-lines: 37-47
    :linenos:

.. _assert_le:

`assert_le`: Less Than Equal
-----------------------------

In this example, we perform a **<=** operation, this can be done via ``assert_le`` property

.. literalinclude:: ../tutorials/perf_checks/assert_le.yml
    :language: yaml
    :emphasize-lines: 37-47
    :linenos:

.. _assert_lt:

`assert_lt`: Less Than
-----------------------

In this example, we perform a **<** operation, this can be done via ``assert_lt`` property

.. literalinclude:: ../tutorials/perf_checks/assert_lt.yml
    :language: yaml
    :emphasize-lines: 37-47
    :linenos:

.. _assert_eq:

`assert_eq`: Equal
--------------------------

buildtest can perform assert equality check with metrics to determine status of test. In this next example, we define
four metrics **x**, **y**, **first**, and **last** which will be compared with its reference value. We introduce a new
property ``assert_eq`` which is composed of list of assertions. Each reference is converted to its appropriate
type (``int``, ``float``, ``str``).

.. literalinclude:: ../tutorials/perf_checks/assert_eq.yml
    :language: yaml
    :emphasize-lines: 40-50
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
    :emphasize-lines: 22-23,28-29,33,42-43
    :linenos:

Let's build this test and see the output.

.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_eq_exceptions.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_eq_exceptions.yml

.. _assert_ne:

`assert_ne`: Not Equal
----------------------

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

`assert_range`: Upper and Lower Bound
--------------------------------------

The ``assert_range`` property can be used to test performance for a metric given a lower and upper bound. This property expects
one to specify ``lower`` and ``upper`` field which must be an integer or floating point number to perform comparison. buildtest will
perform an assertion, if metric value is in the range specified by **lower** and **upper**, then test will pass. Shown below
is an example using the ``assert_range`` property with stream benchmark.

.. literalinclude:: ../tutorials/perf_checks/assert_range.yml
    :language: yaml
    :emphasize-lines: 37-51
    :linenos:

Let's build this test and see the output


.. dropdown:: ``buildtest build -b tutorials/perf_checks/assert_range.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/assert_range.yml

Note that performance results may vary on your system and depending on the metric value you may want to adjust the
lower and upper bound to match your requirement.

`contains`, `not_contains`: Contains and Not Contains
------------------------------------------------------

Buildtest can perform status check with a list of reference values and check if metrics value is in the list. The
property ``contains`` and ``not_contains`` can be used to perform this type of check. The ``ref`` property is a list of
reference values that a metric must have to pass metrics check.

In example below we have two tests, the first test perform ``contains`` and ``not_contains`` on metrics **x**. We expect both
status check will pass. The second test is expected to fail because metric ``x`` will store integer value **1** but the list has
string equivalent **'1'**.

.. literalinclude:: ../tutorials/perf_checks/contains.yml
    :language: yaml
    :emphasize-lines: 17-25,41-45
    :linenos:

You can run this test, by running the following command

.. dropdown:: ``buildtest build -b tutorials/perf_checks/contains.yml``

    .. command-output:: buildtest build -b tutorials/perf_checks/contains.yml