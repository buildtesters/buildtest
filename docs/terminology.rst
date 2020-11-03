.. _terminology:

Terminology
===========


.. csv-table::
    :header: "Name", "Description"
    :widths: 30, 60

    **Buildspec**,"is a YAML file that buildtest interprets when generating the test. A Buildspec may contain one or more test that is validated with a **global schema** and **sub schema**."
    **Schema**,"is a JSON Schema file (``.schema.json``) that defines structure of a buildspec file and it is used for validating a buildspec"
    **Global Schema**,"is a JSON schema that validates buildspec file. buildtest will validate all buildspecs with global schema"
    **Sub Schema**, "Each test section in a buildspec file is validated with one sub-schema defined by ``type`` field. The buildspec test section can only be validated with one sub-schema"
    **Test Script**,"is a generated shell script by buildtest as a result of processing one of the Buildspec."
    **Settings**,"is a buildtest configuration file in YAML that configures buildtest at your site. The Settings file must be compatible with the Settings Schema."
    **Settings Schema**,"is a special schema file that defines structure of buildtest settings."
    **Executor**,"is responsible for running a **TestScript**. An executor can be of several types such as ``local``, ``slurm``, ``lsf`` which defines if test is run locally or via a scheduler. The executors are defined in the ``Settings`` file."




