Contribution is not easy, so we created this document to describe how to get you setup
so you can contribute back and make everyone's life easier.

Preparation
=============

If you don't have a GitHub account please register your account at https://github.com/join

Fork the repo
--------------

First, you'll need to fork the repo https://github.com/HPC-buildtest/buildtest-framework

You might need to setup your SSH keys in your git profile if you are using ssh option for cloning. For more details on
setting up SSH keys in your profile, follow instruction found in
https://help.github.com/articles/connecting-to-github-with-ssh/

SSH key will help you pull and push to repository without requesting for password for every commit.

After creating your fork copy, clone your fork buildtest-framework repo

::

  git clone git@github.com:YOUR\_GITHUB\_LOGIN/buildtest-framework.git


Adding Upstream Remote
-----------------------

First you need to add the ``upstream`` repo, to do this you can issue the following

::

 git remote add upstream git@github.com/HPC-buildtest/buildtest-framework.git

 The ``upstream`` tag is used to sync changes from upstream repo to keep your
 repo in sync before you contribute back.


Sync your branch from upstream
-------------------------------

The ``devel`` from upstream will get Pull Requests from other contributors, inorder
to sync your forked repo with upstream, run the commands below:

::

 cd buildtest-framework
 git checkout devel
 git fetch upstream devel
 git pull upstream devel


Once the changes are pulled locally you can sync devel branch with your
fork as follows

::

 git checkout devel
 git push origin devel


Repeat this same operation with ``master`` branch if you want to sync it with upstream repo



Feature Branch
------------------

Please make sure to create a new branch when adding and new feature. Do not push to ``master`` or ``devel`` branch on
your fork or upstream.

Create a new branch from ``devel`` as follows

::

  cd buildtest-framework
  git checkout devel
  git checkout -b featureX


Once you are ready to push to your fork repo do the following

::

  git push origin featureX


Once the branch is created in your fork, you can create a PR for the ``devel`` branch for ``upstream`` repo
(https://github.com/HPC-buildtest/buildtest-framework)

Review
-------

Someone from the **buildtest team** will review the PR and get back to you with the feedback. If the reviewer requests
some changes, then the user is requested to make changes and update the branch used for sending PR


Documentation
----------------

buildtest documentation (https://buildtest.readthedocs.io/en/latest) is hosted by ReadTheDocs (https://readthedocs.org)
which is a documentation platform for building and hosting your docs. buildtest project can be found at
https://readthedocs.org/projects/buildtest/ which will show the recent builds and project setting. If you are interested
in being a documentation maintainer, please contact Shahzeb Siddiqui <shahzebmsiddiqui@gmail.com> to enable access to
this project. buildtest documentation is using sphinx (http://www.sphinx-doc.org/en/master/) to build the underlying
documentation.

buildtest documentation is hosted in ``docs`` found at the root of this repository. If you want to
build the documentation you will need to make sure your python environment has all the packages defined by
``requirements.txt``.

To install your python packages, you can run the following.

::

  pip install -r requirements.txt

The file ``requirements.txt`` can be found at https://github.com/HPC-buildtest/buildtest-framework/blob/master/docs/requirements.txt

To build your documentation simply run the following

::

  cd docs
  make html

This will build the sphinx project and generate all the html files. Once this process is complete you may want to view
the documentation. If you have ``firefox`` in your system you can simply run the following

::

  make view

This will open a ``firefox`` session to the root of your documentation that was recently generated. You will want to
make sure you have X11 forwarding in order for firefox to work properly. Refer to the ``Makefile`` to see all of the
make tags and you may run ``make`` or ``make help`` for additional help
