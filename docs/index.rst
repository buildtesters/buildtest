buildtest - Software Testing Framework
=========================================

Welcome to buildtest_ documentation. buildtest is a HPC Application Testing
Framework designed to build tests quickly and verify an entire HPC software stack

This documentation was last rebuild on |today| and is intended for version |version|.

Introduction to buildtest
-------------------------

.. toctree::
   :glob:
   :maxdepth: 2

   What_is_buildtest
   Architecture

Getting Started
---------------

.. toctree::
   :maxdepth: 2

   Setup.rst
   Buildtest_Variables.rst
   How_to_use_BuildTest.rst

Introspection Operations
-------------------------

.. toctree::
   :maxdepth: 1

   Show_Configuration.rst
   scan_test.rst
   List_Subcommand.rst
   Find_Operations.rst
   Module_Operations.rst

Building tests
-----------------

.. toctree::
   :maxdepth: 2

   Build_Operations.rst

Running tests
--------------

.. toctree::
   :maxdepth: 2

   Run_Subcommand


buildtest YAML Framework
------------------------

.. toctree::
   :maxdepth: 2

   Yaml_Subcommand.rst
   BinaryTest_Yaml_Application.rst
   BinaryTest_Yaml_SystemPackages.rst
   show_yaml_keys.rst
   Writing_Test_In_YAML.rst
   MPI_yaml.rst
   OpenMP_yaml.rst
   Jobscript_yaml_configuration.rst


Jobscript Features
------------------

.. toctree::
   :maxdepth: 2

   Job_Template
   Automate_BatchJobs

Additional Features
--------------------

.. toctree::
    :maxdepth: 2

    EasyBuild_Integration
    OHPC_Integration



Useful Links
-------------
* buildtest_ - The buildtest documentation
* buildtest-framework_ - The buildtest Testing framework
* buildtest-configs_ - buildtest YAML configs for generic apps
* R-buildtest-config_ - R test scripts repository
* Perl-buildtest-config_ - Perl test scripts repository
* Python-buildtest-config_ - Python test scripts repository
* Ruby-buildtest-config_ - Ruby test scripts repository

Join the buildtest slack channel (http://hpcbuildtest.slack.com) to get connected
with the community. To join this channel please email **shahzebmsiddiqui@gmail.com**

.. _buildtest: https://github.com/HPC-buildtest/buildtest
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
