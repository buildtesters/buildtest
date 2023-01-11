Buildtest Tutorial on Perlmutter
===================================

This tutorial will be conducted on `Perlmutter <https://docs.nersc.gov/systems/perlmutter/>`_ system. If you need account access please
`Obtain a user account <https://docs.nersc.gov/accounts/>`_.

Setup
------

Once you have a NERSC account, you can `Connect to NERSC system <https://docs.nersc.gov/connect/>`_. You will need access to a
terminal client and ssh into perlmutter as follows::

    ssh <user>@perlmutter-p1.nersc.gov

To get started please load the `python` module since you will need python 3.7 or higher to use buildtest. This can be done by running::

    module load python

Next, you should `Install buildtest <installing_buildtest>`_ by cloning the repository in your $HOME directory.

Exercise 1: Running a Batch Job
--------------------------------

In this exercise, we will submit a batch job that will run `hostname` in the slurm cluster. Shown below is the example buildspec

.. literalinclude:: ../perlmutter_tutorial/ex1/hostname.yml
   :language: yaml

Let's run this test and poll interval for 10 secs::

   buildtest build -b perlmutter_tutorial/ex1/hostname.yml --pollinterval=10

Once test is complete, check the output of test by running::

    buildtest inspect query -o hostname_perlmutter

Next, let's update the test such that it runs on both `regular` and `debug` queue. You will need to update the `executor` property and
specify a regular expression. Please refer to :ref:`Multiple Executors <multiple_executors>`. You can retrieve a list of available executors
by running ``buildtest config executors``.

Once you have updated the test, please rerun the test, now you should expect to see two runs for same test.

Exercise 2: Performing Status Check
------------------------------------

In this exercise, we will check version of Lmod via environment **LMOD_VERSION** and specify the
the output using :ref:`regular expression <regex>`_.

.. literalinclude:: ../perlmutter_tutorial/ex2/module_version.yml
   :language: yaml

This buildspec is invalid, your first task is to make sure buildspec is valid. Once you have accomplished this task, try building
the test and check the output of test. If your test passes, try updating the regular expression and see if test fails. Revert the change
back and make the test pass.


