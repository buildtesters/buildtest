Contributing Guide
==================

This guide is geared for developers and maintainers of buildtest who want to contribute
back to buildtest project. There are many ways you can help contribute to buildtest that may include:

- Improve user documentation
- Increase test coverage of buildtest regression tests.
- Work on an `existing issue <https://github.com/buildtesters/buildtest/issues>`_
- Report a bug or new feature requests at https://github.com/buildtesters/buildtest/issues

Overview
---------

buildtest codebase is written in Python 3, so if you are new to Python you will want to
check out the python 3 tutorial: https://docs.python.org/3/tutorial/. This is a good
starting point to understand python basics. If you are familiar with Python 2 you may want to review
the `Python 2-3 cheat sheet <http://python-future.org/compatible_idioms.html>`_.

buildtest relies on `YAML <https://yaml.org/>`_ and `JSON Schema <https://json-schema.org/>`_,
you should review `Understanding JSON Schema <https://json-schema.org/understanding-json-schema/>`_ article
as it provides a thorough overview of JSON Schema. There are several resources
to help you learn YAML for instance you can check out:

- https://www.tutorialspoint.com/yaml/index.htm
- https://learnxinyminutes.com/docs/yaml/

buildtest has a regression test that is run via `pytest <https://docs.pytest.org/en/stable/>`_. You
should be familiar with pytest and it's usage and documentation as it will help you write
regression test. The regression test makes use of `coverage <https://coverage.readthedocs.io/>`_
to measure code coverage of buildtest source code. This is configured using `.coveragerc <https://github.com/buildtesters/buildtest/blob/devel/.coveragerc>`_ file located
in top of repo. The coverage data is pushed to `codecov <https://docs.codecov.io/docs>`_ at https://codecov.io/gh/buildtesters/buildtest/.

buildtest has several CI checks written in GitHub workflows. These are found in `.github/workflows <https://github.com/buildtesters/buildtest/tree/devel/.github/workflows>`_
directory of buildtest. You should familiarize yourself with `github worflow syntax <https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions>`_
if you want to contribute back to github workflows.

Git is essential to code contribution so we recommend you get comfortable using `git`
as it will be discussed in :ref:`code contributing guide <code_contribution_guide>`.
We recommend you review one the following guides to help you learn `git`:

- https://guides.github.com/introduction/git-handbook/
- https://git-scm.com/docs/gittutorial
- https://guides.github.com/
- https://lab.github.com/

buildtest documentation is built on `sphinx <https://www.sphinx-doc.org/en/master/>`_
and hosted via `readthedocs <https://readthedocs.org/>`_. Be sure to check out
`documentation on readthedocs  <https://docs.readthedocs.io/en/stable/>`_ to understand
how it works. The buildtest project is hosted at https://readthedocs.org/projects/buildtest/ which
hosts the public documentation at https://buildtest.readthedocs.io/. The documentation
pages are written in `reStructured Text (rST) <https://docutils.sourceforge.io/rst.html>`_
which is Sphinx's markup language when hosting the docs.

Contributing Topics
--------------------

.. toctree::

   contributing/code_contribution_guide
   contributing/github_integration
   contributing/build_documentation
   contributing/regression_testing
   contributing/schema
   contributing/maintainer_guide
   contributing/new_maintainer_checklist
