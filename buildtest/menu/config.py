import getpass
import json
import os
import shutil
import sys
import yaml
from jsonschema import ValidationError
from buildtest import BUILDTEST_VERSION
from buildtest.schemas.utils import get_schema_fullpath
from buildtest.config import check_settings, load_settings, resolve_settings_file
from buildtest.defaults import (
    BUILDTEST_SETTINGS_FILE,
    BUILDSPEC_CACHE_FILE,
)
from buildtest.utils.file import is_file
from buildtest.defaults import supported_type_schemas, supported_schemas
from buildtest.system import BuildTestSystem


def func_config_compiler(args=None):
    """This method implements ``buildtest config compiler`` which shows compiler
       section from buildtest configuration.
    """

    settings_file = resolve_settings_file()
    configuration = load_settings(settings_file)
    compilers = configuration.get("compilers") or {}
    compiler_dict = compilers.get("compiler")

    if not compiler_dict:
        sys.exit("No compilers defined")

    if args.json:
        print(json.dumps(compiler_dict, indent=2))
    if args.yaml:
        print(yaml.dump(compiler_dict, default_flow_style=False))
    if args.list:
        compiler_names = []
        for name in compiler_dict:
            if isinstance(compiler_dict[name], dict):
                compiler_names += compiler_dict[name].keys()

        [print(name) for name in compiler_names]


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

    os.system(f"cat {settings_file}")


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

    if is_file(BUILDSPEC_CACHE_FILE):
        with open(BUILDSPEC_CACHE_FILE, "r") as fd:
            buildspecs = json.loads(fd.read())

            tests = []
            count = 0
            for file in buildspecs:
                count += 1
                tests += buildspecs[file].keys()

            print("Number of buildspecs: ", count)
            print("Number of Tests:", len(tests))
            print("Tests: ", tests)

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
