.. _Setup:

Installing buildtest
=====================

Requirements
------------

You need the following packages to install buildtest.

- `git <https://git-scm.com/downloads>`_
- `Python <https://www.python.org/downloads/>`_ >= 3.6

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

To install buildtest, navigate to buildtest repo and source the setup script as follows::

    # BASH users
    $ source setup.sh

    # CSH users
    $ source setup.csh

This will add ``buildtest`` command in your $PATH and set environment variable
**$BUILDTEST_ROOT** which points to root of buildtest repo.

You may want to create an isolated python environment of choice depending on your
preference you can use any of the following:

- `virtualenv <https://virtualenv.pypa.io/en/latest/>`_

- `conda <https://conda.io/>`_

- `pipenv <https://pipenv.readthedocs.io/en/latest/>`_

buildtest will provide tab completion for bash shell, this is managed by script `bash_completion.sh <https://github.com/buildtesters/buildtest/blob/devel/bash_completion.sh>`_,
if you encounter any issues with tab completion please raise an issue at https://github.com/buildtesters/buildtest/issues/new/choose.


Development Dependencies (Optional)
------------------------------------

If you plan to contribute back to buildtest, you will need to install additional
dependencies found in the requirements file in ``docs/requirements.txt`` as follows::

    $ pip install -r docs/requirements.txt

Usage (``buildtest --help``)
------------------------------

Once you are setup, you can run ``buildtest --help`` for more details on how to
use buildtest. Shown below is the output

.. command-output:: buildtest --help

If you have got this far, please go to the next section on :ref:`getting_started`
