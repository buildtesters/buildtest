buildtest
==========

Status
-----------


|license| |docs| |travis| |codecov| |coveralls| |slack| |codefactor| |core_infrastructure| |black|

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
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

Source Code
------------

- buildtest framework: https://github.com/buildtesters/buildtest
- buildtest schemas: https://github.com/buildtesters/schemas

Test Repositories
------------------

- Tutorials: https://github.com/buildtesters/tutorials
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
a testing framework designed to automate testing on any Linux systems including HPC clusters, workstation, or laptop.
buildtest provides several json-schemas that define how to write your test-configuration (YAML) also known as **Buildspecs**
that buildtest translates into a shell script.

For more details on buildtest check :ref:`summary_of_buildtest`

This documentation was last rebuild on |today| and is intended for version |version|.

.. toctree::
   :maxdepth: 2
   :caption: Background

   what_is_buildtest.rst
   terminology.rst

.. toctree::
   :maxdepth: 2
   :caption: Reference

   installing_buildtest.rst
   configuring_buildtest.rst
   getting_started.rst
   introspection.rst
   schemas.rst

.. toctree::
   :maxdepth: 2
   :caption: Development Guide

   contributing.rst
   references.rst

License
--------

buildtest is released under the `MIT license <https://github.com/buildtesters/buildtest/blob/devel/LICENSE>`_

Related Projects
-----------------

- `ReFrame: <https://reframe-hpc.readthedocs.io/en/stable/>`_ ``Re`` gression ``FRAME`` work for Software Testing

- `EasyBuild: <https://easybuild.readthedocs.io/en/latest/>`_ end-end software build framework with 1000+ software used for building tuned application for HPC clusters

- `Spack: <https://spack.readthedocs.io/en/latest/>`_  is ``S`` upercomputing ``PACK`` age Manager that supports 1000+ software packages and extremely efficient in combinatorial builds

- `Pavilion: <https://github.com/hpc/pavilion2>`_ is a framework for running and analyzing tests targeting HPC systems

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
