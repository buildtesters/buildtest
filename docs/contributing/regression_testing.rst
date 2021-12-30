Buildtest Unit Tests
=====================

buildtest has a suite of unit tests to verify the state of buildtest. These
tests are located in the top-level directory `tests <https://github.com/buildtesters/buildtest/tree/devel/tests>`_
and tests are run via `pytest <https://docs.pytest.org/en/latest/>`_

In order to run regression tests, you will need ``pytest`` and ``coverage``
installed in your python environment. This should be installed when installing buildtest.

Writing Unit Tests
-------------------

If you want to write a new test, you should be familiar with
`coverage <https://coverage.readthedocs.io/>`_ report that is pushed to `codecov <https://codecov.io/gh/buildtesters/buildtest>`_.
The coverage report will give a detailed line-line coverage of source
code HIT/MISS when running the unit test. We welcome user contribution that
will help increasing test coverage, in addition new features added to buildtest would require test to
ensure they are working properly.

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

Running Unit Test
------------------------

The **buildtest unittests** command can be used to run buildtest unit test. The script
is can be run as a standalone python script by running ``python $BUILDTEST_ROOT/tools/unittests.py``. Shown
below is the help option for ``buildtest unittests`` command.

.. command-output:: buildtest unittests --help

If you decide to run all regression test you can simply run ``buildtest unittests``. The ``--pytestopts`` can be used to
specify option to ``pytest`` when running unit test. The ``--sourcefiles`` option can be used to specify list of files or
directories to run unit test. The ``--coverage`` option can be used to enable coverage when running regression test,
by default this is disabled.

In example, we can specify options to pytest and specify arbitrary source files which can be useful if you want to run
a subset of regression test without running all of them.

.. command-output:: buildtest unittests -p "-vrP" --sourcefiles tests/utils/

The `pytest.ini <https://github.com/buildtesters/buildtest/blob/devel/pytest.ini>`_
found in top-level folder defines pytest configuration for running the unit tests. Some of the unit tests are
assigned a `marker <https://docs.pytest.org/en/6.2.x/example/markers.html>`_ which allows one to run a group of test together. You
can find all markers by running ``pytest --markers``.

If you want to run all tests with ``schema`` marker you can do the following::

   # run via buildtest unittests
   buildtest unittests -p "-m schema"

   # run via coverage
   coverage run -m pytest -m schema

For a complete list of options refer to pytest `documentation <https://docs.pytest.org/en/latest/contents.html>`_
or run ``pytest --help``.

.. _coverage_test:

Running test via coverage
--------------------------

There is a coverage configuration file `.coveragerc <https://github.com/buildtesters/buildtest/blob/devel/.coveragerc>`_ located
in root of buildtest that is read by **coverage** utility. The `buildtest/tools/unittests.py <https://github.com/buildtesters/buildtest/blob/devel/buildtest/tools/unittests.py>`_  script
will collect coverage details upon completion of regression test which is equivalent to running `coverage run -m pytest` but we make some additional checks when
running the script.

If you want to view the coverage details locally in a browser you can run: ``coverage html`` which will
write the coverage report to directory **htmlcov**. You can open the file ``open htmlcov/index.html`` and it will show you
a summary of coverage results that you would see from codecov. Shown below is a preview of coverage report that
you would see after running your regression test.

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
