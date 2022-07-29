import datetime
import json
import os
import re
import subprocess
from shutil import copyfile

import yaml
from buildtest.config import SiteConfiguration
from buildtest.defaults import console
from buildtest.exceptions import BuildTestError, ConfigurationError
from buildtest.schemas.defaults import custom_validator, schema_table
from buildtest.utils.tools import deep_get
from lmod.module import Module
from lmod.spider import Spider
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table


def compiler_cmd(args, configuration):

    if args.compilers == "find":
        compiler_find(args, configuration)
        return

    if args.compilers == "test":
        compiler_test(args, configuration)
        return

    bc = BuildtestCompilers(configuration)

    if args.json is False and args.yaml is False:
        bc.print_compilers()

    if args.json:
        bc.print_json()

    if args.yaml:
        bc.print_yaml()


def compiler_test(args, configuration):
    """This method implements ``buildtest config compilers test`` which tests
    the compilers with the corresponding modules if set. This command iterates
    over all compilers and perform the module load test and show an output of
    each compiler with a PASS or FAIL next to each compiler section.
    """
    bc = BuildtestCompilers(debug=args.debug, configuration=configuration)
    bc.find_compilers()
    console = Console()

    table = Table(title="Compilers Test Pass")
    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Compiler Name", style="green")
    table.add_column("Status", justify="right")
    count_id = 1
    for compiler_cat in bc.compiler_modules_lookup:
        for compiler in bc.compiler_modules_lookup[compiler_cat]:
            # table.add_row(str(count_id), compiler, "✅")
            count_id += 1

    if table.row_count:
        console.print(table)

    table = Table(title="Compilers Test Fail")
    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Compiler Name", style="red")
    table.add_column("Status", justify="right")

    count_id = 1
    for compiler_cat in bc.compiler_modules_lookup_fail:
        for compiler in bc.compiler_modules_lookup_fail[compiler_cat]:
            table.add_row(str(count_id), compiler, "❌")
            count_id += 1

    console.print(table)


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
    system = configuration.name()
    # delete system entry
    del configuration.config["system"][system]

    configuration.config["system"][system] = configuration.target_config

    custom_validator(
        configuration.config, schema_table["settings.schema.json"]["recipe"]
    )

    syntax = Syntax(
        yaml.safe_dump(configuration.config, default_flow_style=False, sort_keys=False),
        "yaml",
        theme="emacs",
    )
    console.print(syntax)
    # if --update is specified we update existing configuration file and write backup in same directory
    if args.update:
        fname = (
            "buildtest_"
            + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            + ".yml"
        )
        backup_file = os.path.join(os.path.dirname(configuration.file), fname)
        copyfile(configuration.file, backup_file)
        print("Writing backup configuration file to: ", backup_file)
        print(f"Updating configuration file: {configuration.file}")
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
        "nvhpc": {"cc": "nvc", "cxx": "nvcc", "fc": "nvfortran"},
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

        self._names = []
        self.compiler_name_to_group = {}
        for name in self.compilers:
            if isinstance(self.compilers[name], dict):
                self._names += self.compilers[name].keys()
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
        self.compiler_modules_lookup_fail = {}
        # test all modules via 'module load' and add only modules that passed (ret: 0)
        for name, module_list in module_dict.items():
            self.compiler_modules_lookup[name] = []
            self.compiler_modules_lookup_fail[name] = []
            for module in module_list:
                cmd = Module(module, debug=self.debug)
                ret = cmd.test_modules(login=True)
                # if module load test passed we add entry to list
                if ret == 0:
                    self.compiler_modules_lookup[name].append(module)
                else:
                    self.compiler_modules_lookup_fail[name].append(module)

        if self.debug:
            print("PASS Compilers: ", self.compiler_modules_lookup)
            print("FAIL Compilers: ", self.compiler_modules_lookup_fail)

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

    def names(self):
        """Return a list of compiler names defined in buildtest configuration"""
        return self._names

    def print_compilers(self):
        """This method implements ``buildtest config compilers`` which
        prints all compilers from buildtest configuration
        """
        for name in self._names:
            print(name)
