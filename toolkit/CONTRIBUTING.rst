Contribution is not easy, so we created this document to describe how to get you setup
so you can contribute back and make everyone's life easier.

Preparation
=============

If you don't have a GitHub account please register your account at https://github.com/join

Fork the repo
--------------

First, you will need to fork https://github.com/HPC-buildtest/buildtest-configs

You might need to setup your SSH keys in your profile if you are using ssh
option for cloning. For more details on setting up SSH keys in your profile,
follow instruction found in
https://help.github.com/articles/connecting-to-github-with-ssh/

SSH key will help you pull and push to the repository without requesting your
credential for pull/push operation.

After creating your fork copy, clone your fork buildtest-framework repo

::

 git clone git@github.com:YOUR\_GITHUB\_LOGIN/buildtest-configs.git

Adding Upstream Remote
-----------------------

First you need to add the ``upstream`` repo, to do this you can issue the following

::

 git remote add upstream git@github.com/HPC-buildtest/buildtest-configs.git

 The ``upstream`` tag is used to sync changes from upstream repo to keep your
 repo in sync before you contribute back.

Sync your branch from upstream
-------------------------------

The ``devel`` from upstream will get Pull Requests from other contributors, inorder
to sync your forked repo with upstream, run the commands below:

::

 cd buildtest-configs
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
-----------------

Please make sure to create a new branch when adding and new feature. Do not push
to **master** or **devel** branch on your fork or upstream.

Create a new branch from ``devel`` branch as follows

::

 cd buildtest-configs
 git checkout devel
 git checkout -b featureX


Once you are ready to push to your fork repo do the following

::

 git push origin featureX


Once the branch is created in your fork, you can create a PR to the **devel** branch.

Test Contribution
------------------

buildtest will accept community contribution on test scripts. If you are new to buildtest
and just want to contribute your test scripts, then please add the test in
`contrib <https://github.com/HPC-buildtest/buildtest-configs/tree/master/contrib>`_ directory.

Each contribute will put their test in ``contrib/<GITUSER>`` directory which helps organize
test by individuals and keep track of contribution in case we need to reach out to individual
for further assistance.

Shown below is a directory structure for git user ``shahzebsiddiqui``

::

 contrib/
 └── shahzebsiddiqui
     └── helloworld
         ├── hello.sh
         ├── hello.yml
         └── src
             └── hello.c

Inside your directory ``contrib/<GITUSER>`` create a directory name that signifies name of
test. Any source code goes in ``src`` sub-directory and you may attach the yml configuration
and/or test script to run the source code.

You may add multiple sourcefiles, header files, and test scripts related to same test name but please
keep the volume of files to a minimum to avoid further complexity. The team will review your contribution
and add any changes to the core test toolkit if accepted.

Review
-------

Someone from the **buildtest team** will review the PR and get back to you with
the feedback. If the reviewer requests some changes, then the user is requested
to make changes and update the branch used for sending PR

If a PR is closed and you want to make slight adjustment, just open the PR and
make the change in your branch. If everything looks fine and PR is merged, you
can delete your local branch.
