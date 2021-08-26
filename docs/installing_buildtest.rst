.. _Setup:

Installing buildtest
=====================

Requirements
------------

You need the following packages to install buildtest.

- `git <https://git-scm.com/downloads>`_
- `Python <https://www.python.org/downloads/>`_ >= 3.7

Cloning buildtest
------------------

To get started, clone the buildtest repository in your local machine as follows::

    # HTTPS
    $ git clone https://github.com/buildtesters/buildtest.git

    # SSH
    $ git clone git@github.com:buildtesters/buildtest.git

If you prefer the latest release use the **master** branch::

    $ git clone -b master git@github.com:buildtesters/buildtest.git

Installing buildtest
-----------------------

buildtest requires a python 3.7 or higher, we recommend you setup a python environment in order
to install buildtest. You can use `venv <https://docs.python.org/3/library/venv.html>`_, `conda <https://conda.io/>`_,
or `pipenv <https://pipenv.readthedocs.io/en/latest/>`_ to manage your python environment depending on your preference.

venv Setup
~~~~~~~~~~~

.. code-block::

    python3 -m venv $HOME/buildtest
    source $HOME/buildtest/activate

Conda Setup
~~~~~~~~~~~~~

.. code-block::

    conda create -n buildtest python=3.7
    source activate buildtest

Pipenv Setup
~~~~~~~~~~~~~

.. code-block::

    pipenv --python 3.7
    pipenv shell

Once you have your python environment setup, you can install buildtest, by sourcing the setup script
depending on your shell type::

    # BASH users
    $ source setup.sh

    # CSH users
    $ source setup.csh

This will add ``buildtest`` command in your $PATH and set environment variable
**$BUILDTEST_ROOT** which points to root of buildtest repo.

buildtest will provide tab completion for bash shell, this is managed by script `bash_completion.sh <https://github.com/buildtesters/buildtest/blob/devel/bash_completion.sh>`_,
if you encounter any issues with tab completion please raise an issue at https://github.com/buildtesters/buildtest/issues/.


Development Dependencies (Optional)
------------------------------------

If you plan to contribute back to buildtest, you will need to install additional
dependencies as follows::

    $ pip install -r docs/requirements.txt

Usage (``buildtest --help``)
------------------------------

Once you are setup, you can run ``buildtest --help`` for more details on how to
use buildtest. Shown below is the output

.. command-output:: buildtest --help

If you have got this far, please go to the next section on :ref:`getting_started`
