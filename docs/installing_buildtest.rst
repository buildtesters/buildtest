.. _Setup:

Installing buildtest
=====================

Requirements
------------

You need the following packages to get started.

- git
- Python >= 3.6
- pip

Cloning buildtest
------------------

To get started, clone the buildtest repository in your local machine as follows::

    $ git clone https://github.com/buildtesters/buildtest.git

If you prefer the SSH method, make sure your GitHub account is configured properly, for more details see
`Connecting to GitHub with SSH <https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>`_

Once your account is configured you can clone the repository as follows::

    $ git clone git@github.com:buildtesters/buildtest.git

If you prefer the latest release use the **master** branch::

    $ git clone -b master git@github.com:buildtesters/buildtest.git

Installing buildtest
-----------------------

To install buildtest you need to source the setup script as follows::

    # BASH users
    $ source setup.sh

    # CSH users
    $ source setup.csh

We have enabled tab completion of buildtest arguments using `argcomplete <https://kislyuk.github.io/argcomplete/>`_
library. Upon sourcing the setup script you can use the tab completion with any buildtest
arguments.

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

If you have got this far, please go to the next section on :ref:`Getting_Started`
