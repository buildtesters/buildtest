Using buildtest at HPC sites
==============================

We assume you have read the :ref:`getting_started` and :ref:`configuring_buildtest` and now you
want to use buildtest at your site. This document will highlight some points to consider before you start.

To get started, you should consider standing up an empty repository where you will host your tests. This can
be GitHub, GitLab, bitbucket, etc...

Picking a version of buildtest
---------------------------------

If you are going to use buildtest, you should consider if you want
to use the bleeding edge (`devel <https://github.com/buildtesters/buildtest/tree/devel>`_), stable release (`master <https://github.com/buildtesters/buildtest/tree/master>`_) or a `tag release <https://github.com/buildtesters/buildtest/tags>`_.
Generally, we recommend you start off with stable release and then incrementally update your buildtest with new `releases <https://github.com/buildtesters/buildtest/releases>`_ as they
come out and check the `CHANGELOG.rst <https://github.com/buildtesters/buildtest/blob/devel/CHANGELOG.rst>`_ for updates between version release.

**Please make sure to read the appropriate version documentation based on the version of buildtest.**

- Devel Docs: https://buildtest.readthedocs.io/en/devel/index.html
- Stable Docs: https://buildtest.readthedocs.io/en/latest/

Configuring buildtest for your site
------------------------------------

Once you have picked a version of buildtest, you need to configure buildtest for your site, this
requires you see :ref:`configuring_buildtest`. We recommend you see `buildtest-nersc configuration <https://github.com/buildtesters/buildtest-nersc/blob/devel/config.yml>`_
that provides how buildtest is configured at NERSC. Once you have defined your configuration file you should make sure your configuration is valid by running::

    buildtest config validate

Writing Test
-------------

If you are going to write test, we assume you have read :ref:`buildspec_tutorial` section which covers
how to write buildspecs. You should consider reviewing the Schema Documentation: https://buildtesters.github.io/buildtest/
which goes in detail about each schema and buildspec attributes.

If you are writing tests, it's generally good practice to :ref:`define tags <define_tags>` in your
test so you can group tests by a tagname and run them via ``buildtest build --tags``. If you plan
to use tags to run your tests, you should document tags and how they are meant to be used.