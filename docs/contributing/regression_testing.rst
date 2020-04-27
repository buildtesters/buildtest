Regression Tests
=================

buildtest has a suite of regression tests to verify the state of buildtest. These tests are located in
the top-level directory ``tests``. buildtest is using `pytest <https://docs.pytest.org/en/latest/>`_ for running
the regression tests.

Getting Started
----------------

In order to write regression tests, you should have ``pytest`` and ``coverage`` installed in your python environment.
You can do this by installing the requirements file::

    pip install -r docs/requirements.txt


Writing Regression Tests
-------------------------

If you want to write a new regression test, you would want to get familiar with the coverage report gather in codecov and
coveralls. The coverage report for codecov (https://codecov.io/gh/buildtesters/buildtest) or coveralls
(https://coveralls.io/github/buildtesters/buildtest) will give a detailed line-line coverage detail of source
code HIT/MISS when running the regression test. Increasing coverage report would be great way to write a new regression test.

The ``tests`` directory is structured in a way that each source file has a corresponding test file that starts with ``test_``.
For instance, if you want to write a test for ``buildtest/utils/command.py``, there will be a corresponding test under
``tests/utils/test_command.py``.

If you adding a new directory, make sure the name corresponds to one found under ``buildtest`` directory  and add a
``__init__.py`` in the new directory. This is required by pytest for test discovery. All test methods must start
with **test_** in order for pytest to run your regression test.

Shown below is a simple test that always passes

.. code-block:: python

       def test_regression_example1():
            assert True

For more details on writing tests with pytest see `Getting-Started <https://docs.pytest.org/en/latest/getting-started.html#installation-and-getting-started>`_

Running Test with pytest
------------------------

To run all the tests you can run the following::

  pytest tests/

Some other options can be useful for troubleshooting such as::

    # print passed test with output
    pytest -rP tests

    # print all failed tests
    pytest -rf tests

    # print all test with verbose
    pytests -v tests

    # print all except Pass tests
    pytest -ra tests

For a complete list of options refer to pytest `documentation <https://docs.pytest.org/en/latest/contents.html>`_
or run ``pytest --help``.

You may want to run coverage against your test, this can be done by running::

    coverage run -m pytest tests

This can be used with ``coverage report`` to show coverage results of your regression test run locally. Shown below
is an example output::

    $ coverage report
    Name                                        Stmts   Miss Branch BrPart  Cover
    -----------------------------------------------------------------------------
    buildtest/__init__.py                           2      0      0      0   100%
    buildtest/buildsystem/__init__.py               0      0      0      0   100%
    buildtest/buildsystem/base.py                 222     19     76     19    85%
    buildtest/buildsystem/schemas/__init__.py       0      0      0      0   100%
    buildtest/buildsystem/schemas/utils.py         53      8     26      8    77%
    buildtest/config.py                            65     29     28      5    48%
    buildtest/defaults.py                          18      0      0      0   100%
    buildtest/exceptions.py                         5      1      2      1    71%
    buildtest/log.py                               18      0      0      0   100%
    buildtest/main.py                              11     11      0      0     0%
    buildtest/menu/__init__.py                     62     47      4      0    23%
    buildtest/menu/build.py                        62     52     28      0    11%
    buildtest/menu/config.py                       35      1     18      0    98%
    buildtest/menu/get.py                          31     23     10      0    20%
    buildtest/menu/show.py                         17      3      6      3    74%
    buildtest/menu/status.py                       11      8      2      0    23%
    buildtest/system.py                            37     37     10      0     0%
    buildtest/utils/__init__.py                     0      0      0      0   100%
    buildtest/utils/command.py                     49      2     12      3    92%
    buildtest/utils/file.py                        46      0     14      2    97%
    -----------------------------------------------------------------------------
    TOTAL                                         744    241    236     41    63%


You may want to run ``coverage report -m`` which will show missing line numbers in report. For more details on coverage
refer to `coverage documentation <https://coverage.readthedocs.io/>`_.


