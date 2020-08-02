.. _Setup:

Installing buildtest
=====================

Requirements
------------

You need the following packages to get started.

- Python >= 3.6

Cloning buildtest
------------------

To get started, clone the buildtest repository in your local machine as follows::

    $ git clone https://github.com/buildtesters/buildtest.git

If you prefer the SSH method, make sure your GitHub account is configured properly, for more details see
`Connecting to GitHub with SSH <https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>`_

Once your account is configured you can clone the repository as follows::

    $ git clone git@github.com:buildtesters/buildtest.git

If you prefer the latest code release, please pull the **devel** branch::

    $ git clone -b devel git@github.com:buildtesters/buildtest.git

Or you may switch to the **devel** branch if you already cloned it::

    $ git checkout devel

Installing buildtest
-----------------------

Depending on your python version, install buildtest as follows::

    # for site installed python
    $ pip install --user .

    # for virtual environment, local install
    $ pip install .

You may want to create an isolated python environment of choice depending on your preference you can use any of the following

- `virtualenv <https://virtualenv.pypa.io/en/latest/>`_

- `conda <https://conda.io/>`_

- `pipenv <https://pipenv.readthedocs.io/en/latest/>`_

Development Dependencies (Optional)
------------------------------------

If you plan to contribute back to buildtest, you will need to install additional dependencies found in the
requirements file in ``docs/requirements.txt`` as follows::

    $ pip install -r docs/requirements.txt

Usage (``buildtest --help``)
------------------------------

Once you are setup, you can run ``buildtest --help`` for more details on how to use buildtest. Shown below
is the output

.. program-output:: cat docgen/buildtest_--help.txt


buildtest commands make use of sub-commands (i.e ``buildtest <subcommand>``). For more details
on any subcommand run::

    $ buildtest <subcommand> --help

If you have got this far, please go to the next section on :ref:`configuring_buildtest`
