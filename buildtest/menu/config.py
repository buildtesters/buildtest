import getpass
import json
import os
import shutil
import subprocess
import sys
import yaml
from jsonschema import ValidationError, validate
from buildtest import BUILDTEST_VERSION
from buildtest.schemas.utils import get_schema_fullpath, load_schema, load_recipe
from buildtest.config import check_settings, load_settings, resolve_settings_file
from buildtest.defaults import (
    BUILDTEST_SETTINGS_FILE,
    BUILDSPEC_CACHE_FILE,
    DEFAULT_SETTINGS_SCHEMA,
)
from buildtest.utils.file import is_file
from buildtest.defaults import supported_type_schemas, supported_schemas
from buildtest.system import BuildTestSystem
from lmod.module import Module
from lmod.spider import Spider


def func_compiler_find(args=None):
    """This method implements ``buildtest config compilers find`` which detects
       new compilers based on module names defined in configuration. If system has
       Lmod we use Lmodule API to detect the compilers. For environment-modules we
       search for all modules in current ``$MODULEPATH``.
    """
    pass

    settings_file = resolve_settings_file()
    configuration = load_settings(settings_file)
    moduletool = configuration.get("moduletool")

    if moduletool == "N/A":
        sys.exit(
            "You must have environment-modules or Lmod to use this tool. Please specify 'moduletool' in your configuration"
        )

    compilers = configuration.get("compilers")
    if not compilers:
        sys.exit("Compiler section not detected")

    # update_compilers will update compiler section in configuration file by detecting new compilers based on modules
    update_compilers = compilers

    if not update_compilers.get("compiler"):
        update_compilers["compiler"] = {}

    discovered_modules = {}
    if moduletool == "lmod":
        spider = Spider()

        # retrieve all modules from Lmod spider and add them to dictionary
        for name, module_list in compilers.get("find").items():
            spider_modules = spider.get_modules(module_list).values()
            discovered_modules[name] = list(spider_modules)

    elif moduletool == "environment-modules":
        modules = subprocess.getoutput("module av -t")
        modules = modules.split()

        # discover all modules based with list of module names specified in find field, we add all
        # modules that start with the key name
        for compiler, module_names in compilers.get("find").items():
            discovered_modules[compiler] = []
            for name in module_names:
                discovered_modules[compiler] += [
                    module.replace("(default)", "")
                    for module in modules
                    if module.startswith(name)
                ]
    print(discovered_modules)
    print("Discovered Modules:")
    print(json.dumps(discovered_modules, indent=2))

    # create a duplicate dictionary and delete all entry of empty list
    duplicate = discovered_modules.copy()

    for key, value in duplicate.items():
        if not duplicate[key]:
            del discovered_modules[key]

    print("\n\n")
    print("Testing Modules:")
    valid_modules = {}
    # test all modules via 'module load' and add only modules that passed (ret: 0)
    for name, module_list in discovered_modules.items():
        valid_modules[name] = []
        for module in module_list:
            cmd = Module(module, debug=True)
            ret = cmd.test_modules(login=True)
            # if module load test passed we add entry to list
            if ret == 0:
                valid_modules[name].append(module)

    for name, module_list in valid_modules.items():
        if not isinstance(update_compilers["compiler"].get(name), dict):
            update_compilers["compiler"][name] = {}

        for module in module_list:

            # replace first / with @ in format <compiler>@<version>
            new_compiler_entry = module.replace("/", "@", 1)
            # if its a new compiler entry let's add new entry to dict
            if new_compiler_entry not in compilers.get("compiler")[name].keys():
                update_compilers["compiler"][name][new_compiler_entry] = {}

                if name == "gcc":
                    update_compilers["compiler"][name][new_compiler_entry] = {
                        "cc": "gcc",
                        "cxx": "g++",
                        "fc": "gfortran",
                    }
                elif name == "intel":
                    update_compilers["compiler"][name][new_compiler_entry] = {
                        "cc": "icc",
                        "cxx": "icpc",
                        "fc": "ifort",
                    }
                elif name == "cray":
                    update_compilers["compiler"][name][new_compiler_entry] = {
                        "cc": "cc",
                        "cxx": "CC",
                        "fc": "ftn",
                    }
                elif name == "pgi":
                    update_compilers["compiler"][name][new_compiler_entry] = {
                        "cc": "pgcc",
                        "cxx": "pgc++",
                        "fc": "pgfortran",
                    }
                elif name == "clang":
                    update_compilers["compiler"][name][new_compiler_entry] = {
                        "cc": "clang",
                        "cxx": "clang++",
                    }
                elif name == "cuda":
                    update_compilers["compiler"][name][new_compiler_entry] = {
                        "cc": "nvcc",
                    }
            update_compilers["compiler"][name][new_compiler_entry]["modules"] = [module]

    configuration["compilers"] = update_compilers

    config_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)

    validate(instance=configuration, schema=config_schema)
    print(yaml.safe_dump(configuration, default_flow_style=False, sort_keys=False))
    print(f"Updating settings file:  {settings_file}")

    with open(settings_file, "w") as fd:
        yaml.safe_dump(configuration, fd, default_flow_style=False, sort_keys=False)


def func_config_compiler(args=None):
    """This method implements ``buildtest config compilers`` which shows compiler
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
