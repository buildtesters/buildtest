buildtest
==========

This documentation was last rebuild on |today| and is intended for version |version|.

If you are working off a latest release please see  https://buildtest.readthedocs.io/en/latest/ for documentation.
If you are working off `devel <https://github.com/buildtesters/buildtest/tree/devel>`_ branch then please refer to
https://buildtest.readthedocs.io/en/devel/
which references the `devel` branch.

Status
-----------

| |license| |docs| |codecov| |slack| |regressiontest|

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |license| image:: https://img.shields.io/github/license/buildtesters/buildtest.svg

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
    :target: http://hpcbuildtest.slack.com

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

Useful Links
-------------

- Documentation: http://buildtest.rtfd.io/

- Schema Docs: https://buildtesters.github.io/buildtest/

- ReadTheDocs: https://readthedocs.org/projects/buildtest/

- CodeCov: https://codecov.io/gh/buildtesters/buildtest

- CodeFactor: https://www.codefactor.io/repository/github/buildtesters/buildtest

- Snyk: https://app.snyk.io/org/buildtesters/

- Slack Channel: http://hpcbuildtest.slack.com

- Slack Invite: https://hpcbuildtest.herokuapp.com

Description
------------

`buildtest <https://github.com/buildtesters/buildtest>`_  is
a testing framework to help HPC sites write test for their system as part of their
routine acceptance & regression test. buildtest provides a YAML interface to write tests
which buildtest can validate and generate shell scripts that can run on your HPC system.
The test template (YAML) is called **buildspec** which can define one or more test instance
that is validated by a `json schema <https://json-schema.org/>`_. buildtest supports the following batch schedulers
for job submission: `IBM Spectrum LSF <https://www.ibm.com/support/knowledgecenter/SSWRJV_10.1.0/lsf_welcome/lsf_welcome.html>`_,
`Slurm <https://slurm.schedmd.com/>`_, and `Cobalt <https://trac.mcs.anl.gov/projects/cobalt/>`_. We
publish the schema documentation, json schemas, and schema examples at https://buildtesters.github.io/buildtest/
which is useful when you are :ref:`writing buildspecs <writing_buildspecs>`.

To get started with buildtest, please see :ref:`installing buildtest <Setup>`  and
:ref:`getting started guide <getting_started>`.

A spin-off project called `lmodule <https://lmodule.readthedocs.io/en/latest/>`_
is a Python API for `Lmod <https://lmod.readthedocs.io/en/latest/>`_. The buildtest
module features were deprecated and moved to lmodule with the main objective is to
automate module load testing. For more details on lmodule see https://github.com/buildtesters/lmodule

.. toctree::
   :maxdepth: 2
   :caption: Background

   what_is_buildtest
   terminology

.. toctree::
   :maxdepth: 2
   :caption: Reference

   installing_buildtest
   getting_started
   configuring_buildtest
   writing_buildspecs
   builder
   buildtest_site
   references

.. toctree::
   :maxdepth: 2
   :caption: Development Guide

   contributing
   api

License
--------

buildtest is released under the `MIT license <https://github.com/buildtesters/buildtest/blob/devel/LICENSE>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
