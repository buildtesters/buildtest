Building Documentation
=======================

ReadTheDocs
-------------
buildtest documentation (https://buildtest.readthedocs.io/en/latest) is hosted by ReadTheDocs (https://readthedocs.org)
which is a documentation platform for building and hosting your docs. buildtest project can be found at
https://readthedocs.org/projects/buildtest/ which will show the recent builds and project setting. If you are interested
in being a documentation maintainer, please contact **Shahzeb Siddiqui** (``shahzebmsiddiqui@gmail.com``) to enable
access to this project. buildtest documentation is using sphinx (http://www.sphinx-doc.org/en/master/) to build the
underlying documentation.

Setup
------
buildtest documentation is hosted in the ``docs`` directory found at the root of this repository. If you want to
build the documentation you will need to make sure your python environment has all the packages defined in
``docs/requirements.txt``. If your environment is already setup as described in :ref:`Setup` then  you can skip this step.

To install your python packages, you can run the following::

  pip install -r docs/requirements.txt

Building docs locally
-----------------------

To build your documentation simply run the following::

  cd docs
  make clean
  make html

It is best practice to run ``make clean`` to ensure sphinx will remove old html content from previous builds, but it is ok to
skip ``make clean`` if you are making minor changes.

Running ``make html`` will build the sphinx project and generate all the html files in ``docs/_build/html``. Once this process is
complete you may want to view the documentation. If you have ``firefox`` in your system you can simply run the following::

  make view

This will open a ``firefox`` session to the root of your documentation that was recently generated. You will want to
make sure you have X11 forwarding in order for firefox to work properly. Refer to the ``Makefile`` to see all of the
make tags and you may run ``make`` or ``make help`` for additional help.

When you run ``make html``, it will build API docs  which are located under ``docs/api``. Make sure the api docs
are committed if git reports any changes. Changes to api docs will happen only if new methods or classes
are added or any modification to docstrings.

If you want to rebuild API docs, it is best to remove all existing docs and regenerate them. This can be done as follows::

    git rm -rf docs/api/*
    make apidocs

Next you can add and commit the api docs.


Automate Documentation Examples
--------------------------------

buildtest has a script in ``$BUILDTEST_ROOT/buildtest/docgen/main.py`` to automate documentation examples. This
script can be run as follows::

  cd $BUILDTEST_ROOT
  python $BUILDTEST_ROOT/buildtest/docgen/main.py

This assumes your buildtest environment is setup, the script will write documentation test examples in ``docs/docgen``.
Consider running this script when **adding**, **modifying**, or **removing** documentation examples. Once the test are
complete, you will want to add the tests, commit and push as follows::

  git add docs/docgen
  git commit -m <MESSAGE>
  git push