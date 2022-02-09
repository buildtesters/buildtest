.. _installing_buildtest:

Installing buildtest
=====================

Requirements
------------

You need the following packages to install buildtest.

- `git <https://git-scm.com/downloads>`_
- `Python <https://www.python.org/downloads/>`_ >= 3.7

Cloning buildtest
------------------

To get started, clone the buildtest repository in your local machine as follows

.. tabs::

    .. code-tab:: bash HTTPS

        git clone https://github.com/buildtesters/buildtest.git

    .. code-tab:: bash SSH

        git clone git@github.com:buildtesters/buildtest.git

If you prefer the latest release, you can clone the **master** branch::

    $ git clone -b master git@github.com:buildtesters/buildtest.git

Installing buildtest
-----------------------

buildtest requires a python 3.7 or higher, we recommend you setup a python environment in order
to install buildtest. You can use `venv <https://docs.python.org/3/library/venv.html>`_, `conda <https://conda.io/>`_,
or `pipenv <https://pipenv.readthedocs.io/en/latest/>`_ to manage your python environment depending on your preference.
Assuming you have cloned buildtest in your HOME directory you will need to follow these instructions to install buildtest.

.. tabs::

    .. code-tab:: bash Virtual Environment (bash)

       python3 -m venv $HOME/.pyenv/buildtest
       source $HOME/.pyenv/buildtest/bin/activate
       source $HOME/buildtest/setup.sh

    .. code-tab:: bash Virtual Environment (csh)

       python3 -m venv $HOME/.pyenv/buildtest
       source $HOME/.pyenv/buildtest/bin/activate.csh
       source $HOME/buildtest/setup.csh

    .. code-tab:: bash Conda

       conda create -n buildtest python=3.7
       source activate buildtest
       source $HOME/buildtest/setup.sh

    .. code-tab:: bash pipenv

       pipenv --python 3.7
       pipenv shell
       source $HOME/buildtest/setup.sh

For csh users you will need to ``source setup.csh`` in order to install buildtest.

Upon installation, you should see ``buildtest`` in your $PATH and environment variable
**$BUILDTEST_ROOT** will point to root of buildtest repo.

buildtest will provide tab completion for bash shell, this is managed by script `bash_completion.sh <https://github.com/buildtesters/buildtest/blob/devel/bash_completion.sh>`_,
if you encounter any issues with tab completion please raise an issue at https://github.com/buildtesters/buildtest/issues/.

Specify Python Wrapper via BUILDTEST_PYTHON
-------------------------------------------

The `buildtest <https://github.com/buildtesters/buildtest/blob/devel/bin/buildtest>`_ program will search for
a python wrapper (`python`, `python3`) to run buildtest, however you can specify an alternate python wrapper by
setting environment variable ``BUILDTEST_PYTHON`` wrapper. This variable will be set during execution of buildtest,
please note the python wrapper must be 3.7 or higher in-order for buildtest to function properly.

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
