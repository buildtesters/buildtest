| |license| |docs| |codecov| |regressiontest|


buildtest
==========

This documentation was rebuilt on |today| and is intended for version |version|.

If you are working off the latest release please see  https://buildtest.readthedocs.io/en/latest/ for documentation.
If you are working off the `devel <https://github.com/buildtesters/buildtest/tree/devel>`_ branch then please refer to
https://buildtest.readthedocs.io/en/devel/
which references the `devel` branch.

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=devel
    :alt: Documentation Status
    :target: https://readthedocs.org/projects/buildtest/builds/

.. |license| image:: https://img.shields.io/github/license/buildtesters/buildtest.svg

.. |codecov| image:: https://codecov.io/gh/buildtesters/buildtest/branch/devel/graph/badge.svg
    :target: https://codecov.io/gh/buildtesters/buildtest

.. |codefactor| image:: https://www.codefactor.io/repository/github/buildtesters/buildtest/badge
    :target: https://www.codefactor.io/repository/github/buildtesters/buildtest
    :alt: CodeFactor

.. |regressiontest| image:: https://github.com/buildtesters/buildtest/workflows/regressiontest/badge.svg
    :target: https://github.com/buildtesters/buildtest/actions


Useful Links
-------------

- Source Code: https://github.com/buildtesters/buildtest
- Documentation: http://buildtest.rtfd.io/
- Schema Docs: https://buildtesters.github.io/buildtest/
- ReadTheDocs: https://readthedocs.org/projects/buildtest/
- CodeCov: https://codecov.io/gh/buildtesters/buildtest
- Slack Channel: http://hpcbuildtest.slack.com
- Slack Invite: https://communityinviter.com/apps/hpcbuildtest/buildtest-slack-invitation
- CodeFactor: https://www.codefactor.io/repository/github/buildtesters/buildtest
- Snyk: https://app.snyk.io/org/buildtesters/
- NERSC Test Repository: https://github.com/buildtesters/buildtest-nersc

Description
------------

`buildtest <https://github.com/buildtesters/buildtest>`_  is
a testing framework to help HPC sites write test for their system as part of their
routine acceptance and regression testing. Buildtest provides a YAML interface to write tests
which buildtest can validate and then use to generate shell scripts that run on your HPC system.
The test template (YAML) is called a **buildspec** which can define one or more test instances
and is validated by a `json schema <https://json-schema.org/>`_. Buildtest supports the following batch schedulers:
`IBM Spectrum LSF <https://www.ibm.com/support/knowledgecenter/SSWRJV_10.1.0/lsf_welcome/lsf_welcome.html>`_,
`Slurm <https://slurm.schedmd.com/>`_, `PBS <https://www.openpbs.org/>`_ and
`Cobalt <https://trac.mcs.anl.gov/projects/cobalt>`_. We publish the schema documentation, json schemas,
and schema examples at https://buildtesters.github.io/buildtest/ which is useful when you are
:ref:`writing buildspecs <writing_buildspecs>`.

To get started with buildtest, please see :ref:`Installing buildtest <installing_buildtest>` and
:ref:`Getting Started Guide <getting_started>`.

A spin-off project called `lmodule <https://lmodule.readthedocs.io/en/latest/>`_
is a Python API for `Lmod <https://lmod.readthedocs.io/en/latest/>`_. The buildtest
module features were deprecated and moved to lmodule with the main objective is to
automate module load testing. For more details on lmodule see https://github.com/buildtesters/lmodule

.. toctree::
   :maxdepth: 2
   :caption: Background

   what_is_buildtest

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installing_buildtest
   quick_start

.. toctree::
   :maxdepth: 2
   :caption: Tutorial

   command_line_tutorial
   buildspec_tutorial
   buildtest_perlmutter

.. toctree::
   :maxdepth: 2
   :caption: How-to-guides

   configuring_buildtest
   batch_support
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Explanation

   builder
   buildtest_site

.. toctree::
   :maxdepth: 2
   :caption: Reference

   getting_started
   writing_buildspecs
   features
   schema_examples
   facility_examples
   api
   command
   conferences

.. toctree::
   :maxdepth: 2
   :caption: Development Guide

   contributing

.. toctree::
    :caption: Useful Links

    Buildtest Github repo <https://github.com/buildtesters/buildtest>
    Buildtest Slack <https://hpcbuildtest.slack.com>
    buildtest at NERSC <https://github.com/buildtesters/buildtest-nersc>

License
--------

buildtest is released under the `MIT license <https://github.com/buildtesters/buildtest/blob/devel/LICENSE>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
