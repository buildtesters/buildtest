import json
import os
import subprocess
import sys

import yaml
from buildtest.defaults import console
from buildtest.exceptions import ConfigurationError
from buildtest.executors.setup import BuildExecutor
from jsonschema import ValidationError
from rich.syntax import Syntax
from rich.table import Column, Table


def config_cmd(args, configuration):
    """Entry point for ``buildtest config`` command. This method will invoke other methods depending on input argument.

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
    """
    if args.config == "view":
        view_configuration(configuration)

    elif args.config == "executors":
        buildexecutor = BuildExecutor(configuration)
        view_executors(
            configuration,
            buildexecutor,
            args.json,
            args.yaml,
            args.disabled,
            args.invalid,
        )

    elif args.config == "validate":
        validate_config(configuration)

    elif args.config == "systems":
        view_system(configuration)

    elif args.config == "edit":
        edit_configuration(configuration)


def edit_configuration(configuration):
    """This method will open configuration file in editor. The preferred editor will be determined based on environment
    variable ``EDITOR`` if found otherwise will resort to ``vim``.

    Args:
        configuration (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class used for storing buildtest configuration
    """

    EDITOR = os.environ.get("EDITOR", "vim")

    subprocess.call([EDITOR, configuration.file])

    print(f"Writing configuration file: {configuration.file}")


def view_system(configuration):
    """This method implements command ``buildtest config systems`` which displays
    system details from configuration file in table format.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
    """

    # table = {"system": [], "description": [], "hostnames": [], "moduletool": []}
    table = Table(
        "[blue]system",
        "[blue]description",
        "[blue]moduletool",
        Column("[blue]hostnames", overflow="fold"),
        title=f"System Summary (Configuration={configuration.file})",
        min_width=120,
    )

    for name in configuration.config["system"].keys():
        desc = configuration.config["system"][name].get("description")
        moduletool = configuration.config["system"][name]["moduletool"]
        hosts = " ".join(configuration.config["system"][name]["hostnames"])

        table.add_row(name, desc, moduletool, hosts)
    console.print(table)


def validate_config(configuration):
    """This method implements ``buildtest config validate`` which attempts to
    validate buildtest schema file `settings.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/settings.schema.json>`_.
    If it's not validate an exception is raised which could be
    `jsonschema.exceptions.ValidationError <https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError>`_
    or :class:`buildtest.exceptions.ConfigurationError`.

    If configuration is valid buildtest print something as follows.

    .. code-block:: console

        bash-3.2$ buildtest config validate
        /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/settings/config.yml is valid


    If there is an error validating configuration file, buildtest will print error message reported by exception

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class

    Raises:
        SystemExit: If exception is raised during validating configuration file.
    """

    try:
        configuration.validate()
    except (ValidationError, ConfigurationError) as err:
        print(err)
        raise sys.exit(f"{configuration.file} is not valid")

    print(f"{configuration.file} is valid")


def view_configuration(configuration):
    """Display content of buildtest configuration file. This implements command ``buildtest config view``"""

    console.rule(configuration.file)
    with open(configuration.file, "r") as bc:
        syntax = Syntax(bc.read(), "yaml", line_numbers=True, theme="emacs")
    console.print(syntax)


def view_executors(
    configuration,
    buildexecutor,
    json_format=False,
    yaml_format=False,
    disabled=False,
    invalid=False,
):
    """Display executors from buildtest configuration. This implements ``buildtest config executors`` command.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        buildexecutor (buildtest.executors.setup.BuildExecutor): An instance of BuildExecutor class
        json_format (bool): Display output in json format which is specified via ``buildtest config executors --json``
        yaml_format (bool): Display output in yaml format which is specified via ``buildtest config executors --yaml``
        disabled (bool): Display list of disabled executors which is specified via ``buildtest config executors --disabled``
        invalid (bool): Display list of invalid executors which is specified via ``buildtest config executors --invalid``
    """

    d = {"executors": configuration.target_config["executors"]}

    # display output in JSON format
    if json_format:
        console.print(json.dumps(d, indent=2))
        return

    # display output in YAML format
    if yaml_format:
        console.print(yaml.dump(d, default_flow_style=False))
        return

    if disabled:
        executors = configuration.disabled_executors
        if not executors:
            print("There are no disabled executors")
            return

        for executor in executors:
            print(executor)
        return

    if invalid:
        executors = configuration.invalid_executors
        if not executors:
            print("There are no invalid executors")
            return

        for executor in executors:
            print(executor)
        return

    names = buildexecutor.names()
    for name in names:
        print(name)
