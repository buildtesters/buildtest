import json
import getpass
import shutil
import sys
import yaml
from jsonschema import ValidationError
from buildtest import BUILDTEST_VERSION

from buildtest.config import (
    check_settings,
    resolve_settings_file,
    buildtest_configuration,
)
from buildtest.defaults import BUILDSPEC_CACHE_FILE, supported_schemas
from buildtest.schemas.utils import load_recipe
from buildtest.system import system


def func_config_validate(args=None):
    """This method implements ``buildtest config validate`` which attempts to
    validate buildtest settings with schema. If it not validate an exception
    an exception of type SystemError is raised. We invoke ``check_settings``
    method which will validate the configuration, if it fails we except an exception
    of type ValidationError which we catch and print message.
    """

    settings_file = resolve_settings_file()
    try:
        check_settings(settings_file)
    except (ValidationError, SystemExit) as err:
        print(err)
        raise sys.exit(f"{settings_file} is not valid")

    print(f"{settings_file} is valid")


def func_config_view(args=None):
    """View buildtest configuration file. This implements ``buildtest config view``"""

    settings_file = resolve_settings_file()
    print(f"Settings File: {settings_file}")
    print("{:_<80}".format(""))
    content = load_recipe(settings_file)

    print(yaml.dump(content, default_flow_style=False, sort_keys=False))


def func_config_executors(args=None):
    """Display executors from buildtest configuration. This implements ``buildtest config executors`` command.
    If no option is specified we display output in JSON format
    """

    # settings_file = resolve_settings_file()
    # content = load_recipe(settings_file)

    d = {"executors": buildtest_configuration.target_config["executors"]}

    # display output in JSON format
    if args.json:
        print(json.dumps(d, indent=2))
        return

    # display output in YAML format
    print(yaml.dump(d, default_flow_style=False))


def func_config_summary(args=None):
    """This method implements ``buildtest config summary`` option. In this method
    we will display a summary of System Details, Buildtest settings, Schemas,
    Repository details, Buildspecs files and test names.
    """

    print("buildtest version: ", BUILDTEST_VERSION)
    print("buildtest Path:", shutil.which("buildtest"))

    print("\n")
    print("Machine Details")
    print("{:_<30}".format(""))
    print("Operating System: ", system.system["os"])
    print("Hostname: ", system.system["host"])
    print("Machine: ", system.system["machine"])
    print("Processor: ", system.system["processor"])
    print("Python Path", system.system["python"])
    print("Python Version:", system.system["pyver"])
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
