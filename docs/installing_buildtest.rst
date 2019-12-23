.. _Setup:

Installing Buildtest
=====================

Requirements
------------

You need the following packages to get started.

- Python >= 3.6

- Lmod


You can install Lmod in RedHat, Centos or Fedora as rpm (i.e ``yum install Lmod``). For Ubuntu you can install Lmod
by running ``apt-get install lmod``.

If you want to build Lmod from source see `Installing Lmod <https://lmod.readthedocs.io/en/latest/030_installing.html>`_


Cloning buildtest
------------------

To get started, clone the buildtest repository in your local machine as follows::

    $ git clone https://github.com/HPC-buildtest/buildtest-framework.git

If you prefer the SSH method, make sure your GitHub account is configured properly, for more details see
`Connecting to GitHub with SSH <https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>`_

Once your account is configured you can clone the repository as follows::

    $ git clone git@github.com:HPC-buildtest/buildtest-framework.git

If you prefer the latest code release, please pull the **devel** branch::

    $ git clone -b devel git@github.com:HPC-buildtest/buildtest-framework.git

Or you may switch to the **devel** branch if you already cloned it::

    $ git checkout devel

Buildtest Dependencies
-----------------------

Next, we need to install buildtest dependencies from ``requirements.txt`` by running ::

    $ pip install -r docs/requirements.txt

You may want to create an isolated python environment of choice depending on your preference you can use any of the following

- `virtualenv <https://virtualenv.pypa.io/en/latest/>`_

- `conda <https://conda.io/>`_

- `pipenv <https://pipenv.readthedocs.io/en/latest/>`_


Depending on your shell (``$SHELL``) source the appropriate file::

    # for bash,sh users
    $ source sourceme.sh

    # for tcsh,csh users
    $ source sourceme.csh

.. _autocomplete:

Setting up auto-complete on buildtest arguments
-----------------------------------------------

Before you start using buildtest you may want to setup autocomplete feature in your shell by running::

    # for bash,csh users
    eval "$(register-python-argcomplete buildtest)"

    # for tcsh,csh users
    eval `register-python-argcomplete --shell tcsh buildtest`

For more details on argcomplete please see https://pypi.org/project/argcomplete/

.. Note:: It is highly recommended to setup auto-complete feature when using buildtest to make use of tab completion

Usage (``buildtest --help``)
------------------------------

Once you are setup, you can run ``buildtest --help`` for more details on how to use buildtest. Shown below
is the output

.. program-output:: cat docgen/buildtest_-h.txt


buildtest commands make use of sub-commands (i.e ``buildtest <subcommand>``). For more details
on any subcommand run::

    $ buildtest <subcommand> --help

If you have got this far, please go to the next section on :ref:`configuring_buildtest`