import getpass
import json
import os
import shutil
import subprocess
import sys
import yaml
from jsonschema import ValidationError, validate
from buildtest import BUILDTEST_VERSION
from buildtest.exceptions import BuildTestError
from buildtest.schemas.utils import get_schema_fullpath, load_schema, load_recipe
from buildtest.config import check_settings, load_settings, resolve_settings_file
from buildtest.defaults import (
    BUILDTEST_SETTINGS_FILE,
    BUILDSPEC_CACHE_FILE,
    DEFAULT_SETTINGS_SCHEMA,
)
from buildtest.defaults import supported_type_schemas, supported_schemas
from buildtest.system import BuildTestSystem


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
    content = load_recipe(settings_file)

    print(yaml.safe_dump(content, sys.stdout, sort_keys=False))


def func_config_summary(args=None):
    """This method implements ``buildtest config summary`` option. In this method
    we will display a summary of System Details, Buildtest settings, Schemas,
    Repository details, Buildspecs files and test names.
    """

    system = BuildTestSystem()
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
    print(f"Buildtest Settings: {BUILDTEST_SETTINGS_FILE}")

    validstate = "VALID"
    try:
        check_settings()
    except ValidationError:
        validstate = "INVALID"

    print("Buildtest Settings is ", validstate)

    settings_file = resolve_settings_file()
    settings = load_settings(settings_file)

    executors = []
    for executor_type in settings.get("executors").keys():
        for name in settings["executors"][executor_type].keys():
            executors.append(f"{executor_type}.{name}")

    print("Executors: ", executors)

    print("Buildspec Cache File:", BUILDSPEC_CACHE_FILE)
    print("\n")

    print("Buildtest Schemas")
    print("{:_<80}".format(""))
    print("Available Schemas:", supported_schemas)
    print("Supported Sub-Schemas")
    print("{:_<80}".format(""))
    for schema in supported_type_schemas:
        path = get_schema_fullpath(schema)
        print(schema, ":", path)
        examples_dir = os.path.join(os.path.dirname(path), "examples")
        print("Examples Directory for schema: ", examples_dir)
