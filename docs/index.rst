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

Terminology
-------------

As you go through the documentation, we wanted to define a few terminology often used through the docs so
its clear to the reader.

- **module:**  is a shell function to bash and csh/tcsh used for dynamically changing user environment (*PATH*, *LD_LIBRARY_PATH*, *MANPATH*)  by loading one or more module files.

- **Modulefile:** is a LUA or TCL file containing instructions on how to load an application environment.

- **User Collection:** is a list of one or more modules that can be referenced by a collection name. The collection name is not an actual module. Collections are found in ``$HOME/.lmod.d/<collection>``.

- **Module Tree:** is the root directory where **Modulefile** are found.

- **Subtree:** is a **Module Tree** but directory is not exposed to **MODULEPATH** which is typically set by some module (``parent module``). Often used in Hierarchical Module Naming Scheme.

- **Parent Module:** is a module that sets **MODULEPATH** to a **Module Tree** often called **Subtree**.

- **Spider:** is a tool provided by Lmod  to build the system spider cache and often used by System Administrator to keep cache up to date upon software install. This is not to be confused with ``module spider`` command that is typically used by users to find modules. See `spider <https://lmod.readthedocs.io/en/latest/136_spider.html>`_ for more details

- **Test Configuration:** - A YAML file that is complaint to one of the buildtest **Schema**. The configuration is used to describe how test is to be generated. The YAML file is passed to ``buildtest`` to generate the test-script.

- **Testscript:** This refers to the generated test script (shell-script) by buildtest

- **Schema:** This refers to the YAML schema defined for writing **Test Configuration** in buildtest.


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
