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

- Lmod ``yum install Lmod``

If you want to build Lmod see the following links

- http://lmod.readthedocs.io/en/latest/030_installing.html

Installing buildtest
----------------------------

To get started clone the buildtest repos in your filesystem::

    $ git clone git@github.com:HPC-buildtest/buildtest-framework.git


Once you clone the repos you will want to install the python dependencies for buildtest which can be done
by running

::

    $ pip install docs/requirements.txt

The `requirements.txt <https://github.com/HPC-buildtest/buildtest-framework/blob/master/docs/requirements.txt>`_ can
be installed via pip in your python environment (`virtualenv <https://virtualenv.pypa.io/en/latest/>`_,
`conda <https://conda.io/>`_ or `pipenv <https://pipenv.readthedocs.io/en/latest/>`_
.

To configure buildtest source the file ``sourceme.sh``::

    $ source sourceme.sh

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

You can check the current version of buildtest by running the following:

::

    $ buildtest -V
    buildtest version:  0.6.3
