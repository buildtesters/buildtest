.. _Setup:

Setup
=====


.. contents::
   :backlinks: none


Requirements
------------

buildtest is compatible with RHEL/Centos

You need the following packages to get started.

- Python > 3.6 or higher

- Lmod ``yum install Lmod`` or environment-modules ``yum install environment-modules``

- CMake ``yum install cmake``

If you want to build Lmod or environment-modules manually please see http://lmod.readthedocs.io/en/latest/030_installing.html
or https://modules.readthedocs.io/en/stable/INSTALL.html for more details

Installing buildtest via pip
----------------------------

If you want to install buildtest you can use ``pip`` to install all the buildtest
packages.

Run the following assuming you have pip

.. code::

    pip install buildtest-framework --user

Make sure your $PATH has ``$HOME/.local/bin`` in its path to pick up buildtest
automatically

Installing buildtest via conda
------------------------------

If you have Anaconda you may install buildtest via ``conda`` to ensure your
python environment is setup properly.

First install python > 3.6 or higher in your conda environment

.. code::

    conda create -n buildtest python>=3.6

Next, get in to your conda environment

.. code::

    source activate buildtest

Next you will  install ``buildtest`` inside your conda environment via ``pip install buildtest-framework --user``

Installing buildtest via git
----------------------------

To get started just clone all the repos related to buildtest in your filesystem

.. program-output:: cat scripts/setup/clonerepo.txt

Once you clone the repos you will want to edit your ``settings.yml`` file to specify
buildtest configuration


Take a look at file ``$BUILDTEST_ROOT/settings.yml`` and copy this file to
``$HOME/.buildtest/settings.yml`` and edit the file accordingly. You can refer
to ``settings.example.yml`` for more details

.. Note:: Failure to copy settings.yml to $HOME/.buildtest/settings.yml will result in  an error

Each site will have to customize their buildtest configuration to reflect the root of the module trees.
You may specify multiple module trees  in ``settings.yml`` for variable ``BUILDTEST_MODULE_ROOT``.

You may specify any of the ``BUILDTEST_*`` variables with exception of ``BUILDTEST_ROOT``
using environment variables which will override values specified in  ``settings.yml``.

The environment variables are used by buildtest to determine the path where to retrieve
module files, yaml configs and write test scripts. You can also reference
these variables in yaml configs to write custom build and run commands. The testscript can
reference source directory via **BUILDTEST_CONFIGS_REPO** to find files of interest

Setting up auto-complete on buildtest arguments
-----------------------------------------------

Before you start using buildtest you may want to setup autocomplete feature in your shell by running

::

    eval "$(register-python-argcomplete buildtest)"

This command works for ``bash`` or  ``sh`` shell, if you are using ``tcsh`` you
can run

::

    eval `register-python-argcomplete --shell tcsh buildtest`

For more details on argcomplete please visit https://pypi.org/project/argcomplete/

This will setup auto-complete on buildtest arguments which will be useful when
building tests.

buildtest version (``buildtest -V``)
-------------------------------------

You can check the current version of buildtest by running the following

::

    (siddis14-TgVBs13r) buildtest-framework[master !x?] $ buildtest -V
    buildtest version:  0.6.3
