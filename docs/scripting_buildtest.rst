Scripting in buildtest
========================

This guide will walk you through on how to script with buildtest.


Let's take this first example where we discover all buildspecs found in top-level
``tutorials`` directory.

.. literalinclude:: scripting_examples/ex1.py

The variable ``BUILDTEST_ROOT`` is the root of buildtest and typically setup once
you install buildtest. The ``discover_buildspec`` method can be invoked to retrieve
a list of buildspecs discovered. The method will return two list, one for discovered
and excluded buildspecs.

Now let's run this example and note we see all buildspecs in **tutorials** directory
were retrieved. This is equivalent to running ``buildtest build --buildspec tutorials``.

.. program-output:: python scripting_examples/ex1.py

We can also discover buildspecs by tags, in next example we discover all buildspecs
by **tutorials** tag. This can be done by passing a tagname for argument **tags**
in *discover_buildspecs* method.

This is equivalent to running ``buildtest build --tags tutorials``.

.. literalinclude:: scripting_examples/ex2.py

.. Note:: You must have a buildspec cache in order to discover tags (``buildtest buildspec find``)

Now let's run this test

.. program-output:: python scripting_examples/ex2.py


You can combine tags and buildspecs with *discover_buildspecs* method and buildtest
will combine the results.

Now that we can find buildspecs, let's try to parse and build the tests. In next
example we will *discover*, *parse*, and *build* all tests with tag name **tutorials**.

.. literalinclude:: scripting_examples/ex3.py

We retrieve all buildspecs by tag *tutorials* as mentioned in previous example. Next
we load buildtest configuration using **load_settings** which returns a dictionary
containing buildtest configuration. During this process, we validate the buildtest
configuration.

Next, we need to figure out our test directory in order to write tests. This
can be achieved by passing the loaded configuration to method **resolve_testdirectory**.
The return will be path to test directory. The test directory can be specified
on command line ``buildtest build --testdir`` or path in configuration. If its not
set in configuration we default to ``$BUILDTEST_ROOT/var/tests``

Next we invoke ``parse_buildspecs`` which expects a list of buildspecs, test directory
and executor. The ``printTable=True`` will print parse table of buildspecs that are validated. The
*parse_buildspecs* will validate each buildspec, and skip any buildspecs that fail validation.
The parser is implemented in class ``BuildspecParser``. For all valid buildspecs
we return a list of builders that is a list of tests for each buildspec that
is an instance of ``BuilderBase`` class that is responsible for building the test.

Next we pass all builders to ``build_phase`` method which will generate testscript
for each builder. The ``printTable=True`` will print table for builder phase.

.. Note:: Each builder corresponds to a single test name.

Now let's run this script and notice the output resembles similar to running
``buildtest build --tags tutorials`` but we stop right after build. In otherwords
this is equivalent to ``buildtest build --tags tutorials --stage=build``.

.. program-output:: python scripting_examples/ex3.py

Now you may have guessed it, ``--stage=parse`` will stop right after the parse stage, in this
case we won't invoke `build_phase` method.

