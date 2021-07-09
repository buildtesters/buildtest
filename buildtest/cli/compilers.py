import json
import os
import re
import subprocess

import yaml
from lmod.module import Module
from lmod.spider import Spider

from buildtest.config import SiteConfiguration
from buildtest.exceptions import BuildTestError, ConfigurationError
from buildtest.schemas.defaults import custom_validator, schema_table
from buildtest.utils.tools import deep_get


def compiler_cmd(args, configuration):

    if args.compilers == "find":
        compiler_find(args, configuration)
        return

    bc = BuildtestCompilers(configuration)

    if args.json is False and args.yaml is False:
        bc.print_compilers()

    if args.json:
        bc.print_json()

    if args.yaml:
        bc.print_yaml()


def compiler_find(args, configuration):
    """This method implements ``buildtest config compilers find`` which detects
    new compilers based on module names defined in configuration. If system has
    Lmod we use Lmodule API to detect the compilers. For environment-modules we
    search for all modules in current ``$MODULEPATH``.
    """

    bc = BuildtestCompilers(debug=args.debug, configuration=configuration)
    bc.find_compilers()
    # configuration["compilers"]["compiler"] = bc.compilers

    configuration.target_config["compilers"]["compiler"] = bc.compilers

    # delete system entry
    del configuration.config["system"][configuration.name]

    configuration.config["system"][configuration.name] = configuration.target_config

    custom_validator(
        configuration.config, schema_table["settings.schema.json"]["recipe"]
    )

    print(
        yaml.safe_dump(configuration.config, default_flow_style=False, sort_keys=False)
    )
    print("{:_<80}".format(""))
    print(f"Updating settings file: {configuration.file}")

    with open(configuration.file, "w") as fd:
        yaml.safe_dump(
            configuration.config,
            fd,
            default_flow_style=False,
            sort_keys=False,
        )


class BuildtestCompilers:
    compiler_table = {
        "gcc": {"cc": "gcc", "cxx": "g++", "fc": "gfortran"},
        "intel": {"cc": "icc", "cxx": "icpc", "fc": "ifort"},
        "pgi": {"cc": "pgcc", "cxx": "pgc++", "fc": "pgfortran"},
        "cray": {"cc": "cc", "cxx": "CC", "fc": "ftn"},
        "clang": {"cc": "clang", "cxx": "clang++", "fc": "None"},
        "cuda": {"cc": "nvcc", "cxx": "nvcc", "fc": "None"},
        "upcxx": {"cc": "upcxx", "cxx": "upcxx", "fc": "None"},
    }

    def __init__(self, configuration, settings_file=None, debug=False):
        """
        :param settings_file: Specify an alternate settings file to use when finding compilers
        :param settings_file: str, optional
        :param compilers: compiler section from buildtest configuration.
        :type compilers: dict
        """

        self.configuration = configuration

        # if settings_file is provided, let's load settings into SiteConfiguration
        # and set self.configuration to loaded configuration
        if settings_file:
            bc = SiteConfiguration(settings_file)
            bc.detect_system()
            bc.validate()
            self.configuration = bc

        self.debug = debug

        if not deep_get(self.configuration.target_config, "compilers", "compiler"):
            raise BuildTestError("compiler section not defined")

        self.compilers = self.configuration.target_config["compilers"]["compiler"]

        self.names = []
        self.compiler_name_to_group = {}
        for name in self.compilers:
            if isinstance(self.compilers[name], dict):
                self.names += self.compilers[name].keys()
                for compiler in self.compilers[name].keys():
                    self.compiler_name_to_group[compiler] = name

    def find_compilers(self):
        """This method returns compiler modules discovered depending on your module system.
        If you have Lmod system we use spider utility to detect modules, this is leveraging
        Lmodule API. If you have environment-modules we parse output of ``module av -t``.


        :return: return a list of compiler modules detected based on module key name.
        :rtype: dict
        """

        self.moduletool = self.configuration.target_config.get("moduletool")

        if self.moduletool == "N/A" or not self.moduletool:
            raise ConfigurationError(
                self.configuration.config,
                self.configuration.file,
                "You must have environment-modules or lmod to use this tool. Please specify 'moduletool' in your configuration",
            )

        # The 'find' section is required for discovering new compilers
        if not self.configuration.target_config["compilers"].get("find"):
            raise ConfigurationError(
                self.configuration.config,
                self.configuration.file,
                "Compiler 'find' section not detected, we are unable to search for compilers.",
            )

        module_dict = {}
        print(f"MODULEPATH: {os.getenv('MODULEPATH')}")

        # First we discover modules, if its Lmod we use Lmodule API class Spider to retrieve modules
        if self.moduletool == "lmod":
            if self.debug:
                print("Searching modules via Lmod Spider")
            spider = Spider()

            spider_modules = list(spider.get_modules().values())
            for name, module_regex_patttern in self.configuration.target_config[
                "compilers"
            ]["find"].items():
                module_dict[name] = []
                raw_string = r"{}".format(module_regex_patttern)

                for module_fname in spider_modules:
                    if self.debug:
                        print(
                            f"Applying regex {raw_string} with module: {module_fname}"
                        )

                    if re.match(raw_string, module_fname):
                        module_dict[name].append(module_fname)

        # for environment-modules we retrieve modules by parsing output of 'module av -t'
        elif self.moduletool == "environment-modules":
            module_av = "module av -t"
            if self.debug:
                print(f"Searching modules by parsing content of command: {module_av}")

            cmd = subprocess.getoutput("module av -t")
            modules = cmd.split()

            # discover all modules based with list of module names specified in find field, we add all
            # modules that start with the key name
            for compiler, module_regex_pattern in self.configuration.target_config[
                "compilers"
            ]["find"].items():
                module_dict[compiler] = []

                raw_string = r"{}".format(module_regex_pattern)

                # apply regex against all modules, some modules have output with
                # (default) in that case we replace with empty string

                module_dict[compiler] += [
                    module.replace("(default)", "")
                    for module in modules
                    if re.match(raw_string, module)
                ]

        # ignore entry where value is empty list
        module_dict = {k: v for k, v in module_dict.items() if v}

        if not module_dict:
            raise BuildTestError("No modules discovered")

        self._validate_modules(module_dict)
        self._update_compiler_section()

    def _validate_modules(self, module_dict):
        """This method will validate modules by running ``module load`` test for all
        discovered modules specified in parameter ``discovered_modules``. This method
        returns a list of modules that were valid, if all tests pass we return the same
        list. A module test pass if we get a returncode 0.

        """

        if self.debug:
            print(f"Testing all discovered modules: {list(module_dict.values())}")

        self.compiler_modules_lookup = {}
        # test all modules via 'module load' and add only modules that passed (ret: 0)
        for name, module_list in module_dict.items():
            self.compiler_modules_lookup[name] = []
            for module in module_list:
                cmd = Module(module, debug=self.debug)
                ret = cmd.test_modules(login=True)
                # if module load test passed we add entry to list
                if ret == 0:
                    self.compiler_modules_lookup[name].append(module)

    def _update_compiler_section(self):
        """This method will update the compiler section by adding new compilers if
        found

        :return: Updated compiler section for buildtest configuration
        :rtype: dict
        """

        for name, module_list in self.compiler_modules_lookup.items():
            if not self.compilers.get(name):
                self.compilers[name] = {}

            for module in module_list:
                # if its a new compiler entry let's add new entry to dict
                if module not in self.compilers.get(name).keys():
                    self.compilers[name][module] = self.compiler_table[name].copy()

                # define module section for each compiler. This setting is automatically
                # set by buildtest but user may want to tweak this later.
                self.compilers[name][module]["module"] = {}
                self.compilers[name][module]["module"]["load"] = [module]
                self.compilers[name][module]["module"]["purge"] = False

    def print_json(self):
        """Prints compiler section in JSON, this implements ``buildtest config compilers --json``"""
        print(json.dumps(self.compilers, indent=2))

    def print_yaml(self):
        """Prints compiler section in YAML, this implements ``buildtest config compilers --yaml``"""
        print(yaml.dump(self.compilers, default_flow_style=False))

    def list(self):
        """Return all compilers defined in buildtest configuration"""
        return self.names

    def print_compilers(self):
        """This method implements ``buildtest config compilers`` which
        prints all compilers from buildtest configuration
        """
        for name in self.names:
            print(name)
