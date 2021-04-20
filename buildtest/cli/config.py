import json
import getpass
import os
import shutil
import sys
import yaml
from jsonschema import ValidationError
from tabulate import tabulate
from termcolor import colored
from buildtest import BUILDTEST_VERSION

from buildtest.config import (
    check_settings,
    resolve_settings_file,
    buildtest_configuration,
)
from buildtest.defaults import BUILDSPEC_CACHE_FILE, supported_schemas
from buildtest.executors.setup import BuildExecutor
from buildtest.schemas.utils import load_recipe
from buildtest.system import system


def config_cmd(args, configuration):

    buildexecutor = BuildExecutor(configuration)

    if args.config == "view":
        view_configuration()

    elif args.config == "executors":
        view_executors(buildexecutor, args.json, args.yaml)

    elif args.config == "summary":
        view_summary()

    elif args.config == "validate":
        validate_config()

    elif args.config == "systems":
        view_system()


def view_system(settings_file=None):
    """This method implements command ``buildtest config systems`` which displays
    system details from configuration file in table format.
    """
    # settings_file = settings_file or resolve_settings_file()
    # print(settings_file)
    bc = check_settings(settings_path=settings_file, executor_check=False)
    table = {"system": [], "description": [], "hostnames": [], "moduletool": []}
    for name in bc.config["system"].keys():
        table["system"].append(name)
        table["description"].append(bc.config["system"][name].get("description"))
        table["moduletool"].append(bc.config["system"][name]["moduletool"])
        table["hostnames"].append(bc.config["system"][name]["hostnames"])

    if os.getenv("BUILDTEST_COLOR") == "True":
        print(
            tabulate(
                table,
                headers=[
                    colored(field, "blue", attrs=["bold"]) for field in table.keys()
                ],
                tablefmt="grid",
            )
        )
        return

    print(tabulate(table, headers=table.keys(), tablefmt="grid"))


def validate_config():
    """This method implements ``buildtest config validate`` which attempts to
    validate buildtest settings with schema. If it not validate an exception
    an exception of type SystemError is raised. We invoke ``check_settings``
    method which will validate the configuration, if it fails we except an exception
    of type ValidationError which we catch and print message.
    """

    settings_file = resolve_settings_file()
    try:
        check_settings(settings_path=settings_file, executor_check=True)
    except (ValidationError, SystemExit) as err:
        print(err)
        raise sys.exit(f"{settings_file} is not valid")

    print(f"{settings_file} is valid")


def view_configuration():
    """View buildtest configuration file. This implements ``buildtest config view``"""

    settings_file = resolve_settings_file()

    content = load_recipe(settings_file)

    print(yaml.dump(content, default_flow_style=False, sort_keys=False))

    print("{:_<80}".format(""))
    print(f"Settings File: {settings_file}")


def view_executors(buildexecutor, json_format=False, yaml_format=False):
    """Display executors from buildtest configuration. This implements ``buildtest config executors`` command.
    If no option is specified we display output in JSON format
    """

    d = {"executors": buildtest_configuration.target_config["executors"]}

    # display output in JSON format
    if json_format:
        print(json.dumps(d, indent=2))
        return

    # display output in YAML format
    if yaml_format:
        print(yaml.dump(d, default_flow_style=False))
        return

    names = buildexecutor.list_executors()
    for name in names:
        print(name)


def view_summary(buildtestsystem=None):
    """This method implements ``buildtest config summary`` option. In this method
    we will display a summary of System Details, Buildtest settings, Schemas,
    Repository details, Buildspecs files and test names.

    :parse buildtestsystem: instance of class BuildTestSystem, optional
    :type buildtestsystem: BuildTestSystem
    """

    system_details = buildtestsystem or system

    print("buildtest version: ", BUILDTEST_VERSION)
    print("buildtest Path:", shutil.which("buildtest"))

    print("\n")
    print("Machine Details")
    print("{:_<30}".format(""))
    print("Operating System: ", system_details.system["os"])
    print("Hostname: ", system_details.system["host"])
    print("Machine: ", system_details.system["machine"])
    print("Processor: ", system_details.system["processor"])
    print("Python Path", system_details.system["python"])
    print("Python Version:", system_details.system["pyver"])
    print("User:", getpass.getuser())

    print("\n")

    print("Buildtest Settings")
    print("{:_<80}".format(""))
    print(f"Buildtest Settings: {buildtest_configuration.file}")

    executors = []
    for executor_type in buildtest_configuration.target_config.get("executors").keys():
        for name in buildtest_configuration.target_config["executors"][
            executor_type
        ].keys():
            executors.append(f"{executor_type}.{name}")

    print("Executors: ", executors)

    print("Buildspec Cache File:", BUILDSPEC_CACHE_FILE)
    print("\n")

    print("Buildtest Schemas")
    print("{:_<80}".format(""))
    print("Available Schemas:", supported_schemas)
