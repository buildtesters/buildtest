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
is already setup as described in :ref:`installing_buildtest` then  you can skip this step.

To install your python packages, you can run the following::

  pip install -r docs/requirements.txt

Building docs locally
-----------------------

To build your documentation, navigate to the `docs` directory and run the following::

  cd docs
  make clean
  make html

It is best practice to run ``make clean`` to ensure sphinx will remove old html
content from previous builds, but it is ok to skip this step if you are
making minor changes.

Running ``make html`` will build the sphinx project and generate all the html
files in ``docs/_build/html``. Once this process is complete you can view the html
pages by running the following::

    open _build/html/index.html

Please refer to the ``Makefile`` to see list of tags or run ``make`` for additional help.

Sphinx
-------

The documentation is built via `Sphinx <https://www.sphinx-doc.org/en/master/>`_ using
`reStructuredText (rST) <https://docutils.sourceforge.io/rst.html>`_ as its markup language. When
you run `make` you are running `sphinx-build <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_ command
which will generate the documentation.

Sphinx will read the configuration file `conf.py <https://github.com/buildtesters/buildtest/blob/devel/docs/conf.py>`_ used
for building the project. We have enabled a couple `sphinx extensions <https://www.sphinx-doc.org/en/master/usage/extensions/index.html>`_
in our project to customize our documentation

API Generation
---------------

We make use of `Sphinx AutoAPI <https://sphinx-autoapi.readthedocs.io/en/latest/>`_ to generate
buildtest API documentation that is hosted on https://buildtest.readthedocs.io/en/devel/api/index.html.
The Sphinx AutoAPI configuration is configured in sphinx configuration file `conf.py`. For more details
on configuration options see https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html

Command Line Documentation
----------------------------

We make use of `sphinx-argparse <https://sphinx-argparse.readthedocs.io/en/stable/index.html>`_ to generate
documentation for buildtest command line that is hosted at https://buildtest.readthedocs.io/en/devel/command.html.
In order to use this tool one must install this package and enable the extension in sphinx configuration.

DocStrings
-----------

We have enabled `napolean extension <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_ to support
Google style docstring. Please follow this format when you are writting docstring for buildtest codebase. For more details
on google style see: https://google.github.io/styleguide/pyguide.html

Generating Documentation Examples for Buildtest Tutorial
----------------------------------------------------------

The documentation examples for the buildtest tutorial are run inside the container image
ghcr.io/buildtesters/buildtest_spack:latest which means that some of the example output needs to be generated manually. There
is a script `doc-examples.py <https://github.com/buildtesters/buildtest/blob/devel/scripts/spack_container/doc-examples.py>`_ that
is responsible for auto-generating the documentation examples inside the container. To get the container running along with the buildtest codebase you will need to run the
following commands.

.. Note::

   You may need to `source /etc/profile` in your container if you see module command is not found.

.. code-block:: console

    docker run -it -v  $BUILDTEST_ROOT:/home/spack/buildtest ghcr.io/buildtesters/buildtest_spack:latest
    cd /home/spack/buildtest
    source scripts/spack_container/setup.sh

You will need to volume mount **$BUILDTEST_ROOT** into `/home/spack/buildtest` in-order to get buildtest code-base accessible inside
the container.

Once your setup is complete, you can auto-generate documentation examples by running the following ::

        buildtest tutorial-examples

Alternatively, the script can also be invoked via python as shown below :: 

        python scripts/spack_container/doc-examples.py

Please verify all the auto-generated examples that will be used in the documentation. Once you are content with all the changes please add all
the changes via ``git add``.
