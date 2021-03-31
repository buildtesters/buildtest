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
in root of buildtest that is read by **coverage** utility. The `regtest.py <https://github.com/buildtesters/buildtest/blob/devel/scripts/regtest.py>`_  script
will collect coverage details upon completion of regression test which is equivalent to running `coverage run -m pytest` but we make some additional checks when
running the script. Upon completion of tests you can run ``coverage report`` to show coverage results of your
regression test run locally. Shown below is an example output:

.. code-block:: console

    $ coverage report
    Name                                       Stmts   Miss Branch BrPart     Cover
    -------------------------------------------------------------------------------
    buildtest/__init__.py                          3      3      0      0     0.00%
    buildtest/defaults.py                         17     17      0      0     0.00%
    buildtest/executors/slurm.py                 110     93     28      0    12.32%
    buildtest/executors/cobalt.py                110     93     22      0    12.88%
    buildtest/executors/pbs.py                    96     81     14      0    13.64%
    buildtest/executors/lsf.py                   103     85     16      0    15.13%
    buildtest/utils/timer.py                      15      9      4      0    31.58%
    buildtest/menu/__init__.py                    29     16     10      0    33.33%
    buildtest/executors/setup.py                 108     60     60      8    35.71%
    buildtest/menu/compilers.py                  107     60     50      3    38.22%
    buildtest/config.py                          158     72     76     10    47.86%
    buildtest/system.py                          155     70     38     11    50.78%
    buildtest/docs.py                              5      2      0      0    60.00%
    buildtest/log.py                              19      7      0      0    63.16%
    buildtest/buildsystem/base.py                185     45     50      8    67.23%
    buildtest/menu/build.py                      421    117    208     22    70.59%
    buildtest/buildsystem/batch.py                75     17     44      7    71.43%
    buildtest/buildsystem/compilerbuilder.py     193     36     52     10    77.14%
    buildtest/buildsystem/builders.py            107     24     60      8    77.25%
    buildtest/utils/tools.py                      19      2     12      2    80.65%
    buildtest/exceptions.py                        7      2      4      0    81.82%
    buildtest/menu/buildspec.py                  356     46    188     22    83.82%
    buildtest/executors/local.py                  49      3     10      4    88.14%
    buildtest/buildsystem/scriptbuilder.py        41      3     10      3    88.24%
    buildtest/utils/file.py                       68     11     30      0    88.78%
    buildtest/menu/report.py                     193     16    114     14    89.58%
    buildtest/executors/base.py                   61      4     18      2    89.87%
    buildtest/utils/command.py                    68      3     20      5    90.91%
    buildtest/menu/config.py                      73      4     12      1    94.12%
    buildtest/buildsystem/parser.py               51      2     18      2    94.20%
    buildtest/menu/schema.py                      26      0     16      2    95.24%
    buildtest/menu/inspect.py                     63      2     46      3    95.41%
    buildtest/schemas/defaults.py                 32      0      0      0   100.00%
    buildtest/schemas/utils.py                    26      0      8      0   100.00%
    buildtest/utils/shell.py                      30      0      8      0   100.00%
    -------------------------------------------------------------------------------
    TOTAL                                       3179   1005   1246    147    66.19%

4 empty files skipped.

If you want to view the coverage details locally in a browser you can run: ``coverage html`` which will
write the results to directory **htmlcov**. You can open the file ``open htmlcov/index.html`` and it will show you
a summary of coverage results that you would see from codecov.

.. image:: coverage_locally.png


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
