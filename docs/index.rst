buildtest
==========

This documentation was last rebuild on |today| and is intended for version |version|.

Please refer to https://buildtest.readthedocs.io/en/latest/ for documentation
on latest release. If you are working off `devel` branch then please to *devel*
docs at https://buildtest.readthedocs.io/en/devel/.

Status
-----------

| |license| |docs| |codecov| |slack| |regressiontest|

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
    :target: http://hpcbuildtest.slack.com

.. |license| image:: https://img.shields.io/github/license/buildtesters/buildtest.svg

.. |codecov| image:: https://codecov.io/gh/buildtesters/buildtest/branch/devel/graph/badge.svg
    :target: https://codecov.io/gh/buildtesters/buildtest

.. |codefactor| image:: https://www.codefactor.io/repository/github/buildtesters/buildtest/badge
    :target: https://www.codefactor.io/repository/github/buildtesters/buildtest
    :alt: CodeFactor

.. |regressiontest| image:: https://github.com/buildtesters/buildtest/workflows/regressiontest/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions

Source Code
------------

- buildtest framework: https://github.com/buildtesters/buildtest

Test Repositories
------------------

- Cori @ NERSC: https://github.com/buildtesters/buildtest-cori
- Stampede2 @ TACC: https://github.com/buildtesters/buildtest-stampede2

Useful Links
-------------

- Documentation: http://buildtest.rtfd.io/

- Schema Docs: https://buildtesters.github.io/buildtest/

- ReadTheDocs: https://readthedocs.org/projects/buildtest/

- CodeCov: https://codecov.io/gh/buildtesters/buildtest

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
be useful when you are writting buildspecs.

A spin-off project called `lmodule <https://lmodule.readthedocs.io/en/latest/>`_
is a Python API for `Lmod <https://lmod.readthedocs.io/en/latest/>`_. The buildtest
module features were deprecated and moved to lmodule with the main objective is to
automate module load testing. For more details on lmodule see https://github.com/buildtesters/lmodule

To get started with buildtest, please review the :ref:`terminology`
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
   writing_buildspecs.rst
   builder.rst
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
