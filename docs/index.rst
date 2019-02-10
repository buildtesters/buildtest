buildtest - Software Testing Framework
=========================================

.. Note:: This project is under development, the official release will be in 2020.

Welcome to buildtest! **buildtest** is a framework to automate software stack testing for
HPC facilities.

This documentation was last rebuild on |today| and is intended for version |version|.

Introduction to buildtest
-------------------------

.. toctree::
   :glob:
   :maxdepth: 2

   what_is_buildtest.rst
   architecture.rst

Getting Started
---------------

.. toctree::
   :maxdepth: 2

   setup.rst
   configuring_buildtest.rst
   how_to_use_buildtest.rst
   command_reference.rst

Introspection Operations
-------------------------

.. toctree::
   :maxdepth: 1

   show_configuration.rst
   scan_test.rst


Subcommands
-----------------

.. toctree::
   :maxdepth: 2

   list_subcommand.rst
   find_subcommand.rst
   module_subcommand.rst
   build_subcommand.rst
   run_subcommand.rst
   benchmark_subcommand.rst
   yaml_subcommand.rst


buildtest YAML Framework
------------------------

.. toctree::
   :maxdepth: 2


   show_yaml_keys.rst
   writing_test_in_yaml.rst
   mpi_yaml.rst
   openmp_yaml.rst
   jobscript_yaml_configuration.rst


Jobscript Features
------------------

.. toctree::
   :maxdepth: 2

   automate_batchjobs.rst

Miscellaneous
--------------------

.. toctree::
    :maxdepth: 2

    easybuild_integration.rst
    ohpc_integration.rst
    contributing.rst

Useful Links
-------------

* buildtest-framework_ - The buildtest Testing framework
* buildtest-configs_ - buildtest YAML configs for generic apps


Join the buildtest slack channel (http://hpcbuildtest.slack.com) to get connected
with the community. To join this channel please email **shahzebmsiddiqui@gmail.com**


.. _buildtest-framework: https://github.com/HPC-buildtest/buildtest-framework
.. _buildtest-configs: https://github.com/HPC-buildtest/buildtest-configs


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
