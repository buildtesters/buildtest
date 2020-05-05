.. _terminology:

Terminology
===========


.. csv-table:: Core Concepts
    :header: "Name", "Description"
    :widths: 30, 60

    **Buildspec**," is a YAML file that buildtest interprets when generating the test. A Buildspec may contain one or more test blocks that is validated by a ``Buildspec Schema``."
    **Buildspec Schema**," is a JSON file defining  valid/invalid key value pairs and formatting for the file"
    **Schema Library**," is a collection of one or more ``Buildspec Schema`` provided by buildtest."
    **Test Script**," is a generated shell script by buildtest as a result of processing one of the Buildspec."
    **Settings**," is a buildtest configuration file that can be in YAML/JSON that configures buildtest at your
    site. The Settings file must be compatible with the Settings Schema."
    **Settings Schema**," is a schema definition that dictates how to validate a ``Settings`` file."
    **Executor**," defines how a **TestScript** is to be executed. An executor can be of several types such as
    ``local``, ``slurm`` which defines if test is run locally of via scheduler. The executors are defined in the
    ``Settings`` file."




