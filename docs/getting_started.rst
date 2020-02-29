.. _Getting Started:

Getting Started with Buildtest
==============================

Interacting with the client
---------------------------

After you install buildtest, you should find the client on your path::


      $ which buildtest
      ~/.local/bin/buildtest


At this point you've also already configured build test, and are either working
on a cluster with Lmod or have it installed. As a reminder:

 - The test directory is where tests will be written, which defaults to ``$HOME/.buildtest/testdir``.
 - You can store tests (that can be referenced with relative paths) under ``$HOME/.buildtest/site``.


Cloning Tutorials
-----------------

To get started, let's clone a repository with tutorial tests. Since this is a group of tests,
we can put it in our tests directory by using the "get" command::

    $ buildtest get https://github.com/HPC-buildtest/tutorials.git
    Cloning into '/home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials'...

Which would be equivalent to doing this::

    $ mkdir -p $HOME/.buildtest/site/github.com/HPC-buildtest
    $ git clone https://github.com/HPC-buildtest/tutorials.git $HOME/.buildtest/site/github.com/HPC-buildtest/tutorials

You can also clone a specific branch::

    $ buildtest get -b add/hello-world-test https://github.com/HPC-buildtest/tutorials.git

And in either case, if the folder already exists, you'll be told::

    $ buildtest get https://github.com/HPC-buildtest/tutorials.git
    /home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials already exists. Remove and try again.

The tests are organized by their namespace, meaning that you'll find GitHub repos organized under
github.com, then the organization or username, and then the repository name.


Create a Test Configuration
---------------------------

We can refer to a config as a relative path to the test config root at ``$HOME/.buildtest/site`` or
we can provide a relative path to a config file anywhere on our system. Let's start
with the latter, and change directory to interact with our test configurations::

    $ cd /home/users/vsochat/.buildtest/site/github.com/HPC-buildtest/tutorials


Let's take a look at the simplest of examples - a "Hello Buildtest" example! This is
located in ``hello-world``::

    $ cd hello-world

Let's take a quick look at the structure of the folder here::


    $ tree
    .
    ├── hello.sh.yml
    └── src
        └── hello.sh

    1 directory, 2 files


The yaml (extension ``yml`` above) files in the root of the folder are test configurations.
This means that we write here the commands, environment, and other variables that are needed
for the test. Notice that the naming is in the format of ``[name][language].yml``. We know off
the bat that this is intended to test a bash script. Let's take a look at the file::


    testtype: singlesource
    scheduler: local
    description: Hello World Buildtest Example
    maintainer:
    - vsoch

    program:
      source: hello.sh
    

You'll see that most of the file is metadata. The testtype ``singlesource`` is exactly
what it sounds like - we are going to run a single script, the program ``hello.sh``.
There are no surprises here::


    $ cat src/hello.sh 
    #!/bin/bash

    printf "Hello Buildtest\n"


On a high level, the scripts you will run to test and other source files will
be located in the ``src`` folder of a test root, directly under one or more
configurations that reference them.


Run the Test Configuration
---------------------------

Let's run our test! We could be doing this from a relative path to the test configuration
file, **or** as a relative path from the root of our testdir at ``$HOME/.buildtest/site``
For example, either of the two would work in the case of this test::

    $ buildtest build -c github.com/HPC-buildtest/tutorials/hello-world/hello.sh.yml
    $ buildtest build -c hello.sh.yml


STOPPED HERE: compiler is required and we need a recipe type that doesn't require it.
