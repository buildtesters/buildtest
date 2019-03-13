.. _Setup:

Setup
=====


.. contents::
   :backlinks: none


Requirements
------------

buildtest is supported on Redhat or Centos

You need the following packages to get started.

- Python > 3.6 or higher

- Lmod ``yum install Lmod`` or environment-modules ``yum install environment-modules``

- CMake ``yum install cmake``

If you want to build Lmod or environment-modules see the following links

- http://lmod.readthedocs.io/en/latest/030_installing.html

- https://modules.readthedocs.io/en/stable/INSTALL.html


Installing buildtest
----------------------------

To get started clone the buildtest repos in your filesystem

.. program-output:: cat scripts/setup/clonerepo.txt

Once you clone the repos you will want to install the python dependencies for buildtest which can be done
by running

::

    pip install docs/requirements.txt

The `requirements.txt <https://github.com/HPC-buildtest/buildtest-framework/blob/master/docs/requirements.txt>`_ can
be installed in your pip, virtual environment, or conda environment.

Next you will want to create a directory ``.buildtest`` in your home directory and copy the ``settings.yml`` file
to this location

::

    mkdir $HOME/.buildtest
    cp settings.yml $HOME/.buildtest/settings.yml


.. Note:: Failure to copy settings.yml to ``$HOME/.buildtest/settings.yml`` will result in  an error

Next, edit the ``settings.yml`` file to specify buildtest configuration, see :ref:`configuring_buildtest` for details
on how to configure buildtest.

Each site will have to customize their buildtest configuration to reflect the root of the module trees.
You may specify multiple module trees  in ``settings.yml`` using variable ``BUILDTEST_MODULE_ROOT``.

You may specify any of the ``BUILDTEST_*`` variables as environment variables which will 
override values specified in  ``settings.yml``.

You may want to add buildtest to your path by running ``export PATH=$PWD:$PATH`` assuming buildtest is in the current
directory


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

.. Note:: It is highly recommended to setup auto-complete feature when using buildtest to make use of tab completion

buildtest version (``buildtest -V``)
-------------------------------------

You can check the current version of buildtest by running the following

::

    (siddis14-TgVBs13r) buildtest-framework[master !x?] $ buildtest -V
    buildtest version:  0.6.3
