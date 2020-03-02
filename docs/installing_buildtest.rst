.. _Setup:

Installing Buildtest
=====================

Requirements
------------

You need the following packages to get started.

- Python >= 3.6


The following packages are required for using environment modules:

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

Next, we need to install buildtest dependencies from ``docs/requirements.txt`` by running ::

    $ pip install -r docs/requirements.txt


You may want to create an isolated python environment of choice depending on your preference you can use any of the following

- `virtualenv <https://virtualenv.pypa.io/en/latest/>`_

- `conda <https://conda.io/>`_

- `pipenv <https://pipenv.readthedocs.io/en/latest/>`_


Depending on your python version, install buildtest::

    # for site installed python
    $ python3 setup.py install --user

    # for virtual environment, local install
    $ python3 setup.py install


If you want auto-completion using ``argcomplete`` on buildtest options, you can
run this command::

    # for bash, shell
    eval "$(register-python-argcomplete buildtest)"

    # for csh, tsch
    eval `register-python-argcomplete --shell tcsh buildtest


You can add this to your bash ``.profile`` at ``$HOME/.profile`` to have it sourced
each time. After you do this, you can press **TAB** key on the keyboard to
fill in the arguments options::

    $ buildtest
    build        -h           module       --version
    config       --help       show         -V


For more details on argcomplete please see https://pypi.org/project/argcomplete/

Usage (``buildtest --help``)
------------------------------

Once you are setup, you can run ``buildtest --help`` for more details on how to use buildtest. Shown below
is the output

.. program-output:: cat docgen/buildtest_-h.txt


buildtest commands make use of sub-commands (i.e ``buildtest <subcommand>``). For more details
on any subcommand run::

    $ buildtest <subcommand> --help

If you have got this far, please go to the next section on :ref:`configuring_buildtest`
