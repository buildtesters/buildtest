import json
import subprocess
import sys

import yaml
from jsonschema import ValidationError
from rich.syntax import Syntax
from rich.table import Column, Table

from buildtest.defaults import console
from buildtest.exceptions import ConfigurationError
from buildtest.executors.setup import BuildExecutor


def config_cmd(args, configuration, editor, system):
    """Entry point for ``buildtest config`` command. This method will invoke other methods depending on input argument.

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        system (buildtest.system.BuildTestSystem): An instance of BuildTestSystem class
    """
    if args.config in ["view", "v"]:
        view_configuration(configuration, theme=args.theme, pager=args.pager)

    elif args.config in ["executors", "ex"]:
        buildexecutor = BuildExecutor(configuration)
        view_executors(
            configuration,
            buildexecutor,
            args.json,
            args.yaml,
            args.disabled,
            args.invalid,
        )

    elif args.config in ["validate", "val"]:
        validate_config(configuration, system.system["moduletool"])

    elif args.config == "systems":
        view_system(configuration)

    elif args.config in ["edit", "e"]:
        edit_configuration(configuration, editor)

    elif args.config in ["path", "p"]:
        view_path(configuration)


def edit_configuration(configuration, editor):
    """This method will open configuration file in editor. The preferred editor will be determined based on environment
    variable ``EDITOR`` if found otherwise will resort to ``vim``.

    Args:
        configuration (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class used for storing buildtest configuration
    """

    # subprocess.call([editor, configuration.file])
    cmd = subprocess.Popen([editor, configuration.file])
    cmd.communicate()

    print(f"Writing configuration file: {configuration.file}")


def view_system(configuration):
    """This method implements command ``buildtest config systems`` which displays
    system details from configuration file in table format.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
    """

    # table = {"system": [], "description": [], "hostnames": [], "moduletool": []}
    table = Table(
        "system",
        "description",
        "moduletool",
        Column("hostnames", overflow="fold"),
        title=f"System Summary (Configuration={configuration.file})",
        header_style="blue",
        min_width=120,
    )

    for name in configuration.config["system"].keys():
        desc = configuration.config["system"][name].get("description")
        moduletool = configuration.config["system"][name]["moduletool"]
        hosts = " ".join(configuration.config["system"][name]["hostnames"])

        table.add_row(name, desc, moduletool, hosts)
    console.print(table)


def validate_config(configuration, moduletool):
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
        moduletool (str): Name of moduletool for validating module system

    Raises:
        SystemExit: If exception is raised during validating configuration file.
    """

    try:
        configuration.validate(moduletool=moduletool)
    except (ValidationError, ConfigurationError) as err:
        print(err)
        raise sys.exit(f"{configuration.file} is not valid")

    console.print(f"{configuration.file} is valid")


def view_path(configuration):
    """Display the path to configuration file regardless if file is valid

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
    """
    console.print(configuration.file)


def view_configuration(configuration, theme=None, pager=None):
    """Display content of buildtest configuration file. This implements command ``buildtest config view``

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        theme (str, optional): Color theme to choose. This is the Pygments style (https://pygments.org/docs/styles/#getting-a-list-of-available-styles) which is specified by ``--theme`` option
    """

    theme = theme or "monokai"
    with open(configuration.file, "r") as bc:
        syntax = Syntax(bc.read(), "yaml", line_numbers=True, theme=theme)
    if pager:
        with console.pager():
            console.rule(configuration.file)
            console.print(syntax)
        return

    console.rule(configuration.file)
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

    executor_settings = {"executors": configuration.target_config["executors"]}

    # display output in JSON format
    if json_format:
        console.print(json.dumps(executor_settings, indent=2))
        return

    # display output in YAML format
    if yaml_format:
        console.print(yaml.dump(executor_settings, default_flow_style=False))
        return

    if disabled:
        if not configuration.disabled_executors:
            console.print("There are no disabled executors")
            return

        for executor in configuration.disabled_executors:
            console.print(executor)
        return

    if invalid:
        if not configuration.invalid_executors:
            console.print("There are no invalid executors")
            return

        for executor in configuration.invalid_executors:
            console.print(executor)
        return

    names = buildexecutor.names()
    for name in names:
        print(name)
