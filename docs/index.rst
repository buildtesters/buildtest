buildtest - Software Testing Framework
=========================================

Welcome to buildtest documentation. buildtest is a HPC Application Testing
Framework designed to build tests quickly and verify an entire HPC software stack

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
   list_subcommand.rst
   find_operations.rst
   module_operations.rst

Building tests
-----------------

.. toctree::
   :maxdepth: 2

   build_operations.rst

Running tests
--------------

.. toctree::
   :maxdepth: 2

   run_subcommand.rst


buildtest YAML Framework
------------------------

.. toctree::
   :maxdepth: 2

   yaml_subcommand.rst
   show_yaml_keys.rst
   writing_test_in_yaml.rst
   mpi_yaml.rst
   openmp_yaml.rst
   jobscript_yaml_configuration.rst


Jobscript Features
------------------

.. toctree::
   :maxdepth: 2

   job_template.rst
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
* R-buildtest-config_ - R test scripts repository
* Perl-buildtest-config_ - Perl test scripts repository
* Python-buildtest-config_ - Python test scripts repository
* Ruby-buildtest-config_ - Ruby test scripts repository

Join the buildtest slack channel (http://hpcbuildtest.slack.com) to get connected
with the community. To join this channel please email **shahzebmsiddiqui@gmail.com**


.. _buildtest-framework: https://github.com/HPC-buildtest/buildtest-framework
.. _buildtest-configs: https://github.com/HPC-buildtest/buildtest-configs
.. _R-buildtest-config: https://github.com/HPC-buildtest/R-buildtest-config
.. _Perl-buildtest-config: https://github.com/HPC-buildtest/Perl-buildtest-config
.. _Python-buildtest-config: https://github.com/HPC-buildtest/Python-buildtest-config
.. _Ruby-buildtest-config: https://github.com/HPC-buildtest/Ruby-buildtest-config



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
