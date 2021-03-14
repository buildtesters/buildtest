Building Documentation
=======================

The buildtest documentation is written in `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ using sphinx.
You should be familiar with rst if you want to contribute to user documentation.

ReadTheDocs
-------------
buildtest `documentation <https://buildtest.readthedocs.io/en/latest>`_ is hosted
by ReadTheDocs at https://readthedocs.org which is a documentation platform for
building and hosting your docs.

buildtest project can be found at https://readthedocs.org/projects/buildtest/
which will show the recent builds and project setting. If you are interested
in becoming a maintainer, please contact **Shahzeb Siddiqui** (``shahzebmsiddiqui@gmail.com``)
to grant access to this project.

Setup
------

buildtest documentation is located in top-level `docs <https://github.com/buildtesters/buildtest/tree/devel/docs>`_ directory.
If you want to build the documentation you will need to make sure your python environment
has all the packages defined in ``docs/requirements.txt``. If your environment
is already setup as described in :ref:`Setup` then  you can skip this step.

To install your python packages, you can run the following::

  pip install -r docs/requirements.txt

Building docs locally
-----------------------

To build your documentation simply run the following::

  cd docs
  make clean
  make html

It is best practice to run ``make clean`` to ensure sphinx will remove old html
content from previous builds, but it is ok to skip this step if you are
making minor changes.

Running ``make html`` will build the sphinx project and generate all the html
files in ``docs/_build/html``. Once this process is complete you may want to view
the documentation. If you have ``firefox`` in your system you can simply run the
following::

  make view

This will open a ``firefox`` session to the root of your documentation that was
recently generated. Make sure you have X11 forwarding in order for firefox to
work properly. Refer to the ``Makefile`` to see all of the make tags or run
``make`` or ``make help`` for additional help.

Automate Documentation Examples
--------------------------------

buildtest has a script in top-level folder ``script/docgen.py`` to automate
documentation examples. This script can be run as follows::

  python script/docgen.py

This assumes your buildtest environment is setup, the script will write
documentation test examples in ``docs/docgen``. Consider running this script
when **adding**, **modifying**, or **removing** documentation examples. Once the
test are complete, you will want to add the tests, commit and push as follows::

  git add docs/docgen
  git commit -m <MESSAGE>
  git push