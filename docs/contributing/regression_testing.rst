Regression Tests
=================

buildtest has a suite of regression tests to verify the state of buildtest. These
tests are located in the top-level directory `tests <https://github.com/buildtesters/buildtest/tree/devel/tests>`_.
buildtest is using `pytest <https://docs.pytest.org/en/latest/>`_ for running the regression tests.

Getting Started
----------------

In order to write regression tests, you should have ``pytest`` and ``coverage``
installed in your python environment. You can do this by installing all
dependencies found in requirements file::

    pip install -r docs/requirements.txt


Writing Regression Tests
-------------------------

If you want to write a new regression test, you should be familiar with
`coverage <https://coverage.readthedocs.io/>`_ report that is pushed to `codecov <https://codecov.io/gh/buildtesters/buildtest>`_.
The coverage report will give a detailed line-line coverage of source
code HIT/MISS when running the regression test. Increasing coverage report would
be great way to write a new regression test.

The `tests <https://github.com/buildtesters/buildtest/tree/devel/tests>`_ directory is structured in a way
that each source file has a corresponding test file that starts with ``test_``. For instance,
if you want to write a test for ``buildtest/utils/command.py``, there will be a corresponding
test under ``tests/utils/test_command.py``.

If you adding a new directory, make sure the name corresponds to one found under
``buildtest`` directory  and add a ``__init__.py`` in the new directory. This is
required by pytest for test discovery. All test methods must start
with **test_** in order for pytest to run your regression test.

Shown below is a simple test that always passes

.. code-block:: python

       def test_regression_example1():
            assert True

For more details on writing tests with pytest see
`Getting-Started <https://docs.pytest.org/en/latest/getting-started.html#installation-and-getting-started>`_.

Running Regression Test
------------------------

The recommended way to run regression test is via::

    $ python $BUILDTEST_ROOT/scripts/regtest.py

This script is a wrapper to `pytest` and `coverage`. We have a `pytest.ini <https://github.com/buildtesters/buildtest/blob/devel/pytest.ini>`_
found in top-level folder that defines pytest configuration. If you want to run tests
natively via `pytest` without using the script you can just run ``pytest`` and
it will run with options defined in `pytest.ini` file.

If you want to run all schema tests you can use the ``schema`` marker as follows::

   pytest -v -m schema

To see a list of pytest markers see `pytest.ini <https://github.com/buildtesters/buildtest/blob/devel/pytest.ini>`_
or run::

  pytest --markers

For a complete list of options refer to pytest `documentation <https://docs.pytest.org/en/latest/contents.html>`_
or run ``pytest --help``.

.. _coverage_test:

Running test via coverage
--------------------------

There is a coverage configuration file `.coveragerc <https://github.com/buildtesters/buildtest/blob/devel/.coveragerc>`_ located
in root of buildtest that is read by **coverage** utility. You can just run ``coverage run -m pytest``
to get line-line coverage of the source code. This action is done via `regtest.sh <https://github.com/buildtesters/buildtest/blob/devel/scripts/regtest.sh>`_ script if you
were to run it as is. Upon completion of tests you can run ``coverage report`` to show coverage results of your
regression test run locally. Shown below is an example output:

.. code-block:: console

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

If you want to view the coverage details locally in a browser you can run: ``coverage html`` which will
write the results to directory **htmlcov**. You can open the file ``open htmlcov/index.html`` and it will show you
a summary of coverage results that you would see from codecov.

For more details on coverage please refer to `coverage documentation <https://coverage.readthedocs.io/>`_.

Tox
----

buildtest provides a `tox.ini <https://github.com/buildtesters/buildtest/blob/devel/tox.ini>`_
configuration to allow user to test regression test in isolated virtual environment.
To get started install tox::

    pip install tox

Refer to `tox documentation <https://tox.readthedocs.io/en/latest/>`_ for more details.
To run tox for all envrionment you can run::

    tox

If your system has one python instance let's say python 3.7 you can
test for python 3.7 environment by running ``tox -e py37``.
