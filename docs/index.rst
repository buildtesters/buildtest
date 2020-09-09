buildtest
==========

This documentation was last rebuild on |today| and is intended for version |version|.

Please refer to https://buildtest.readthedocs.io/en/latest/ for documentation
on latest release. If you are working of `devel` branch then please refer to
most up to date docs at https://buildtest.readthedocs.io/en/devel/.

Status
-----------

| |license| |docs| |travis| |codecov| |coveralls| |slack| |codefactor| |checkurls| |blackformat| |tutorials| |regressiontest| |buildtest_scripts| |core_infrastructure| |black|

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
    :target: http://hpcbuildtest.slack.com

.. |license| image:: https://img.shields.io/github/license/buildtesters/buildtest.svg

.. |core_infrastructure| image:: https://bestpractices.coreinfrastructure.org/projects/3469/badge

.. |codecov| image:: https://codecov.io/gh/buildtesters/buildtest/branch/devel/graph/badge.svg
    :target: https://codecov.io/gh/buildtesters/buildtest

.. |coveralls| image:: https://coveralls.io/repos/github/buildtesters/buildtest/badge.svg?branch=devel
    :target: https://coveralls.io/github/buildtesters/buildtest?branch=devel

.. |codefactor| image:: https://www.codefactor.io/repository/github/buildtesters/buildtest/badge
    :target: https://www.codefactor.io/repository/github/buildtesters/buildtest
    :alt: CodeFactor

.. |travis| image:: https://travis-ci.com/buildtesters/buildtest.svg?branch=devel
    :target: https://travis-ci.com/buildtesters/buildtest

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |checkurls| image:: https://github.com/buildtesters/buildtest/workflows/Check%20URLs/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |blackformat| image:: https://github.com/buildtesters/buildtest/workflows/Black%20Formatter/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |tutorials| image:: https://github.com/buildtesters/buildtest/workflows/TutorialsValidation/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |regressiontest| image:: https://github.com/buildtesters/buildtest/workflows/regressiontest/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

.. |buildtest_scripts| image:: https://github.com/buildtesters/buildtest/workflows/buildtest_scripts/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

Source Code
------------

- buildtest framework: https://github.com/buildtesters/buildtest
- buildtest schemas: https://github.com/buildtesters/schemas

Test Repositories
------------------

- Cori @ NERSC: https://github.com/buildtesters/buildtest-cori
- Stampede2 @ TACC: https://github.com/buildtesters/buildtest-stampede2

Useful Links
-------------

- Documentation: http://buildtest.rtfd.io/

- Schema Docs: https://buildtesters.github.io/schemas/

- ReadTheDocs: https://readthedocs.org/projects/buildtest/

- Travis: https://travis-ci.com/buildtesters/buildtest

- CodeCov: https://codecov.io/gh/buildtesters/buildtest

- Coveralls: https://coveralls.io/github/buildtesters/buildtest

- CodeFactor: https://www.codefactor.io/repository/github/buildtesters/buildtest

- Snyk: https://app.snyk.io/org/buildtesters/

- Slack Channel: http://hpcbuildtest.slack.com. Click `Here  <https://hpcbuildtest.herokuapp.com/>`_ to Join Slack 

Description
------------

`buildtest <https://github.com/buildtesters/buildtest>`_  is
a HPC testing framework to help sites perform acceptance & regression
testing of an HPC system. buildtest utilizes `json schema <https://json-schema.org/>`_
to define structure of test written in YAML called a  **Buildspec File**.
The `schema docs <https://buildtesters.github.io/schemas/>`_ is a resource that
hosts buildtest schemas and documents all field attributes for each schema, this will
be useful when you are :ref:`buildspec_overview`.

A spin-off project called `lmodule <https://lmodule.readthedocs.io/en/latest/>`_
which is a Python API for `Lmod <https://lmod.readthedocs.io/en/latest/>`_. The buildtest
module features were deprecated and moved to lmodule with the main object
of automating module load testing. For more details on lmodule see https://github.com/buildtesters/lmodule

To get started with buildtest, please review the :ref:`Terminology`
and proceed to :ref:`Setup`  followed by :ref:`Getting Started`.

For additional reference, you can read :ref:`summary_of_buildtest` and
:ref:`conferences`.


.. toctree::
   :maxdepth: 2
   :caption: Background

   what_is_buildtest.rst
   terminology.rst

.. toctree::
   :maxdepth: 2
   :caption: Reference

   installing_buildtest.rst
   getting_started.rst
   configuring_buildtest.rst
   builder.rst
   writing_buildspecs.rst
   scripting_buildtest.rst
   references.rst

.. toctree::
   :maxdepth: 2
   :caption: Development Guide

   contributing.rst
   api.rst

License
--------

buildtest is released under the `MIT license <https://github.com/buildtesters/buildtest/blob/devel/LICENSE>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
