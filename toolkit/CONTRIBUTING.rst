Test Contribution
------------------

buildtest will accept community contribution on test scripts. If you are new to buildtest
and just want to contribute your test scripts, then please add the test in
`toolkit/contrib <https://github
.com/HPC-buildtest/buildtest-configs/tree/master/contrib>`_ directory.

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
