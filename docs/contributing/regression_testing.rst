Regression Tests
=================

buildtest has a suite of regression tests to verify the state of buildtest. These tests are located in
``$BUILDTEST_ROOT/tests`` and the tests can be executed using ``pytest``.


Running regression test locally
--------------------------------

To run all the tests you can run the following::

  pytest tests/

To print passed test with output consider running with option::

  pytest -rP tests/

If you are interested in failed tests run with option::

  pytest -rf tests/

Refer to pytest `documentation <https://docs.pytest.org/en/latest/contents.html>`_  for complete list of options.

Writing Regression Tests
-------------------------

If you want to write a new regression test, first you need to determine where the test will belong. If you decide to
create a new file, then file must start with **test_**. ``pytest`` will run all files and methods that start with **test_**
so this means your method names must comply with this format.  Shown below is a simple test that always passes

.. code-block:: python

       def test_regression_example1():
            assert True

For more details on writing tests with pytest see `Getting-Started <https://docs.pytest.org/en/latest/getting-started.html#installation-and-getting-started>`_
