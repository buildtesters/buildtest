.. _terminology:

Terminology
===========


.. csv-table:: Core Concepts
    :header: "name", "Description"
    :widths: 30, 150

    **SpecFile**,"A ``SpecFile`` is a YAML file that buildtest interprets when generating the test. The SpecFile may contain one or more specs."
    **Spec**,"A Spec is the basic building block for writing a test specification that is compatible with one of the Spec Schema.",
    **Spec Schema**,"A Spec Schema is a JSON file defining the schema with valid key/value pairs that are acceptable for the schema."
    **Schema Library**,"A Schema Library is a collection of one or more ``Spec Schema`` provided by buildtest."
    **TestScript**,"A TestScript is a generated shell script by buildtest as a result of processing one of the SpecFile."
    **Settings**,"Settings is a buildtest configuration file that can be in YAML/JSON that configures buildtest at your site. The Settings file must be compatible with the Settings Schema."
    **Settings Schema**,"A schema definition that dictates how to validate a ``Settings`` file."
    **Executor**,"An ``Executor`` defines how a **TestScript** is executed. An executor can be of several types such as ``local``, ``slurm`` which defines if test is run locally of via scheduler.  The executors are defined in the ``Settings`` file."




