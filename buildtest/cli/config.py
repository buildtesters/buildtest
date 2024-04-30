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
from buildtest.schemas.defaults import custom_validator, schema_table


def config_cmd(command_args, configuration, editor, system):
    """Entry point for ``buildtest config`` command. This method will invoke other methods depending on input argument.

    Args:
        command_args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        system (buildtest.system.BuildTestSystem): An instance of BuildTestSystem class
    """

    handle_view_command(command_args, configuration)
    handle_profiles_command(command_args, configuration)
    handle_executors_command(command_args, configuration)
    handle_validate_command(command_args, configuration, system)
    handle_systems_command(command_args, configuration)
    handle_edit_command(command_args, configuration, editor)
    handle_path_command(command_args, configuration)


def handle_view_command(command_args, configuration):
    if command_args.config in ["view", "v"]:
        view_configuration(
            configuration, theme=command_args.theme, pager=command_args.pager
        )


def handle_profiles_command(command_args, configuration):
    if command_args.config in ["profiles", "prof"]:
        if command_args.profiles in ["list", "ls"]:
            list_profiles(
                configuration, theme=command_args.theme, print_yaml=command_args.yaml
            )

        if command_args.profiles in ["remove", "rm"]:
            remove_profiles(configuration, profile_name=command_args.profile_name)


def handle_executors_command(command_args, configuration):
    if command_args.config in ["executors", "ex"]:
        buildexecutor = BuildExecutor(configuration)
        if command_args.executors in ["list", "ls"]:
            view_executors(
                configuration=configuration,
                buildexecutor=buildexecutor,
                display_in_json_format=command_args.json,
                display_in_yaml_format=command_args.yaml,
                display_disabled=command_args.disabled,
                display_invalid=command_args.invalid,
                display_all=command_args.all,
            )
        if command_args.executors in ["remove", "rm"]:
            remove_executors(configuration, command_args.executor_names)


def handle_validate_command(command_args, configuration, system):
    if command_args.config in ["validate", "val"]:
        validate_config(configuration, system.system["moduletool"])


def handle_systems_command(command_args, configuration):
    if command_args.config == "systems":
        view_system(configuration)


def handle_edit_command(command_args, configuration, editor):
    if command_args.config in ["edit", "e"]:
        edit_configuration(configuration, editor)


def handle_path_command(command_args, configuration):
    if command_args.config in ["path", "p"]:
        view_path(configuration)


def edit_configuration(configuration, editor):
    """This method will open configuration file in editor. The preferred editor will be determined based on environment
    variable ``EDITOR`` if found otherwise will resort to ``vim``.

    Args:
        configuration (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class used for storing buildtest configuration
    """

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
        Column("system", overflow="fold"),
        Column("description", overflow="fold"),
        Column("moduletool", overflow="fold"),
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
    """Display the path to configuration file regardless if file is valid. This implements command ``buildtest config path``

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
    with open(configuration.file, "r") as file_stream:
        syntax = Syntax(file_stream.read(), "yaml", line_numbers=True, theme=theme)
    if pager:
        with console.pager():
            console.rule(configuration.file)
            console.print(syntax)
        return

    console.rule(configuration.file)
    console.print(syntax)


def remove_profiles(configuration, profile_name):
    """This method will remove profile names from configuration file given a list of profile names. This method
    will be invoked when user runs ``buildtest config profiles remove`` command.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        profile_name (list): List of name of profile to remove
    """

    if not configuration.target_config.get("profiles"):
        console.print(
            f"Unable to remove any profiles because no profiles found in configuration file: {configuration.file}. Please create a profile using [red]buildtest build --save-profile[/red]"
        )
        return

    # variable to determine if file needs to be written back to disk
    write_back = False

    for name in profile_name:
        if name not in configuration.target_config["profiles"]:
            console.print(f"Unable to remove profile: {name} because it does not exist")
            continue

        del configuration.target_config["profiles"][name]
        console.print(f"Removing profile: {name}")
        write_back = True

    # if no profiles exist then delete top-level key 'profiles'
    if len(configuration.target_config["profiles"].keys()) == 0:
        del configuration.target_config["profiles"]

    custom_validator(
        configuration.config, schema_table["settings.schema.json"]["recipe"]
    )

    # only update the configuration file if we removed a profile
    if write_back:
        console.print(f"Updating configuration file: {configuration.file}")

        with open(configuration.file, "w") as file_descriptor:
            yaml.safe_dump(
                configuration.config,
                file_descriptor,
                default_flow_style=False,
                sort_keys=False,
            )


def list_profiles(configuration, theme=None, print_yaml=None):
    """Display the list of profile for buildtest configuration file. This implements command ``buildtest config profiles list``

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        theme (str, optional): Color theme to choose. This is the Pygments style (https://pygments.org/docs/styles/#getting-a-list-of-available-styles) which is specified by ``--theme`` option
        print_yaml (bool, optional): Display profiles in yaml format. This is specified by ``--yaml`` option
    """

    if not configuration.target_config.get("profiles"):
        console.print(
            f"Unable to list any profiles because no profiles found in configuration file: {configuration.file}. Please create a profile using `buildtest build --save-profile`"
        )
        return
    if print_yaml:
        profile_configuration = yaml.dump(
            configuration.target_config["profiles"], indent=2
        )
        syntax = Syntax(profile_configuration, "yaml", theme=theme or "monokai")
        console.print(syntax)
        return

    # print profiles as raw text
    for profile_name in configuration.target_config["profiles"].keys():
        print(profile_name)


def display_executors_in_json_format(executor_settings):
    console.print(json.dumps(executor_settings, indent=2))


def display_executors_in_yaml_format(executor_settings):
    console.print(yaml.dump(executor_settings, default_flow_style=False))


def display_disabled_executors(configuration):
    if not configuration.disabled_executors:
        console.print("There are no disabled executors")
        return

    for executor in configuration.disabled_executors:
        console.print(executor)


def display_invalid_executors(configuration):
    if not configuration.invalid_executors:
        console.print("There are no invalid executors")
        return

    for executor in configuration.invalid_executors:
        console.print(executor)


def display_all_executors(configuration):
    names = configuration.get_all_executors()
    for name in names:
        print(name)


def view_executors(
    configuration,
    buildexecutor,
    display_in_json_format=False,
    display_in_yaml_format=False,
    display_disabled=False,
    display_invalid=False,
    display_all=False,
):
    """Display executors from buildtest configuration. This implements ``buildtest config executors list`` command.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        buildexecutor (buildtest.executors.setup.BuildExecutor): An instance of BuildExecutor class
        display_in_json_format (bool): Display output in json format which is specified via ``buildtest config executors list --json``
        display_in_yaml_format (bool): Display output in yaml format which is specified via ``buildtest config executors list --yaml``
        display_disabled (bool): Display list of disabled executors which is specified via ``buildtest config executors list --disabled``
        display_invalid (bool): Display list of invalid executors which is specified via ``buildtest config executors list --invalid``
        display_all (bool): Display all executors which is specified via ``buildtest config executors list --all``

    """
    executor_settings = {"executors": configuration.target_config.get("executors", {})}

    if display_in_json_format:
        display_executors_in_json_format(executor_settings)
        return

    if display_in_yaml_format:
        display_executors_in_yaml_format(executor_settings)
        return

    if display_disabled:
        display_disabled_executors(configuration)
        return

    if display_invalid:
        display_invalid_executors(configuration)
        return

    if display_all:
        display_all_executors(configuration)
        return

    names = buildexecutor.names()
    for name in names:
        print(name)


def remove_executors(configuration, executor_names):
    """Remove executors from buildtest configuration. This implements ``buildtest config executors remove`` command.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        executor_names (list): List of executor names to remove
    """

    # variable to determine if file needs to be written back to disk
    write_back = False

    for name in executor_names:
        exec_type = name.split(".")[1]
        exec_name = name.split(".")[2]

        if not configuration.target_config["executors"].get(exec_type):
            console.print(
                f"Unable to remove executor: {name} because there are no executors of type: {exec_type}"
            )
            continue

        if exec_name not in configuration.target_config["executors"][exec_type].keys():
            console.print(
                f"Unable to remove executor: {name} because it does not exist"
            )
            continue

        del configuration.target_config["executors"][exec_type][exec_name]

        if len(configuration.target_config["executors"][exec_type].keys()) == 0:
            del configuration.target_config["executors"][exec_type]
        console.print(f"Removing executor: {name}")
        write_back = True

    custom_validator(
        configuration.config, schema_table["settings.schema.json"]["recipe"]
    )

    # only update the configuration file if we removed an executor
    if write_back:
        console.print(f"Updating configuration file: {configuration.file}")

        with open(configuration.file, "w") as file_descriptor:
            yaml.safe_dump(
                configuration.config,
                file_descriptor,
                default_flow_style=False,
                sort_keys=False,
            )
