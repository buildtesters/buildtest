buildtest
==========

`buildtest <https://github.com/HPC-buildtest/buildtest-framework>`_  is
a testing framework designed for HPC Software Stack Testing that is compatible with Lmod module system.
buildtest provides a set of YAML keys to write test configuration (YAML) that buildtest translates into complex test
scripts. This allows users to focus on writing test configuration with minimal knowledge of the
underlying system. Test configuration are reusable between HPC sites with the goal of sharing tests between the
HPC community.

For more details on buildtest check :ref:`summary_of_buildtest`

This documentation was last rebuild on |today| and is intended for version |version|.


.. toctree::
   :maxdepth: 2
   :caption: Background

   what_is_buildtest.rst
   feature_overview.rst


.. toctree::
   :maxdepth: 2
   :caption: Reference

   installing_buildtest.rst
   configuring_buildtest.rst
   building_test.rst
   introspection.rst
   spider.rst
   module_operation.rst
   managing_testconfigs.rst


.. toctree::
   :maxdepth: 2
   :caption: Development Guide

   contributing.rst
   references.rst


Slack
------

`Join <https://hpcbuildtest.herokuapp.com/>`_ the Slack Channel to get
connected. The slack channel can be accessed at http://hpcbuildtest.slack.com

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
