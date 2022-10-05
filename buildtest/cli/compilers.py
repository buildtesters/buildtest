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
from rich.table import Table


def compiler_cmd(args, configuration):

    if args.compilers == "find":
        compiler_find(
            configuration,
            modulepath=args.modulepath,
            detailed=args.detailed,
            update=args.update,
        )
        return

    if args.compilers == "test":
        compiler_test(configuration, args.compiler_names)
        return

    bc = BuildtestCompilers(configuration)

    if args.json:
        bc.print_json()
        return

    if args.yaml:
        bc.print_yaml()
        return

    bc.print_compilers()


def compiler_test(configuration, compiler_names=None):
    """This method implements ``buildtest config compilers test`` which tests
    the compilers with the corresponding modules if set. This command iterates
    over all compilers and perform the module load test and show an output of
    each compiler.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        compiler_names (list, optional): A list of compiler names to test
    """
    pass_compilers = []
    fail_compilers = []

    compilers = configuration.target_config["compilers"]["compiler"]

    target_compilers = []

    if compiler_names:
        # catch input is not a list then we raise exception since we need to run 'set()' on a list otherwise we will get an error
        if not isinstance(compiler_names, list):
            raise BuildTestError(
                f"Compiler names must be specified as a list. We got type {type(compiler_names)}"
            )

        target_compilers = set(compiler_names)

    for name in compilers:
        for compiler_instance in compilers[name]:
            # skip compilers if one needs to test specific compiler instances via 'buildtest config compilers test <compiler>'
            if target_compilers and compiler_instance not in target_compilers:
                console.print(f"[red]Skipping test for compiler: {compiler_instance}")
                continue
            if compilers[name][compiler_instance].get("module"):
                module_test = compilers[name][compiler_instance]["module"]["load"]
                cmd = Module(module_test, debug=False)
                ret = cmd.test_modules(login=True)
                if ret == 0:
                    pass_compilers.append(compiler_instance)
                    continue
                fail_compilers.append(compiler_instance)
            else:
                pass_compilers.append(compiler_instance)

    compiler_pass = Table(title="Compilers Test Pass")
    compiler_fail = Table(title="Compilers Test Fail")

    compiler_pass.add_column("No.", style="cyan", no_wrap=True)
    compiler_pass.add_column("Compiler Name", style="green")
    compiler_pass.add_column("Status", justify="right")

    compiler_fail.add_column("No.", style="cyan", no_wrap=True)
    compiler_fail.add_column("Compiler Name", style="red")
    compiler_fail.add_column("Status", justify="right")

    for idx, pass_compiler in enumerate(pass_compilers):
        compiler_pass.add_row(str(idx + 1), pass_compiler, "✅")

    for idx, fail_compiler in enumerate(fail_compilers):
        compiler_fail.add_row(str(idx + 1), fail_compiler, "❌")

    if compiler_pass.row_count:
        console.print(compiler_pass)

    if compiler_fail.row_count:
        console.print(compiler_fail)


def compiler_find(configuration, modulepath=None, detailed=None, update=None):
    """This method implements ``buildtest config compilers find`` which detects
    new compilers based on module names defined in configuration. If system has
    Lmod we use Lmodule API to detect the compilers. For environment-modules we
    search for all modules in current ``$MODULEPATH``.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        modulepath (List, optional): An instance of List, a list of directories to search for modules via MODULEPATH to detect compilers
        detailed (bool, optional): An instance of bool, flag for printing a detailed report.
        update (bool, optional): An instance of bool, flag for updating configuration file with new compilers
    """

    bc = BuildtestCompilers(
        detailed=detailed, configuration=configuration, modulepath=modulepath
    )
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

    # print out all compilers from existing configuration file
    # run buildtest config compilers find --update to update existing configuration file
    bc.print_compilers()

    # if --update is specified we update existing configuration file and write backup in same directory
    if update:
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

    def __init__(
        self, configuration, settings_file=None, detailed=False, modulepath=None
    ):
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

        self.detailed = detailed

        # first read from config file for modulepath
        self.modulepath = deep_get(
            self.configuration.target_config, "compilers", "modulepath"
        )

        # override default modulepath if --modulepath is specified
        if modulepath:
            self.modulepath = ":".join(modulepath)

        # if not override then default
        self.modulepath = self.modulepath or os.getenv("MODULEPATH")

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
        console.print(f"MODULEPATH: {self.modulepath}")

        # First we discover modules, if its Lmod we use Lmodule API class Spider to retrieve modules
        if self.moduletool == "lmod":
            if self.detailed:
                print("Searching modules via Lmod Spider")
            spider = Spider(tree=self.modulepath)

            spider_modules = list(spider.get_modules().values())
            for name, module_regex_pattern in self.configuration.target_config[
                "compilers"
            ]["find"].items():
                module_dict[name] = []
                raw_string = r"{}".format(module_regex_pattern)

                for module_fname in spider_modules:
                    if self.detailed:
                        console.print(
                            f"Applying regex {raw_string} with module: {module_fname}"
                        )

                    if re.match(raw_string, module_fname):
                        module_dict[name].append(module_fname)

        # for environment-modules we retrieve modules by parsing output of 'module av -t'
        elif self.moduletool == "environment-modules":
            module_av = "module av -t"
            if self.detailed:
                print(f"Searching modules by parsing content of command: {module_av}")

            cmd = subprocess.getoutput("/bin/bash -c 'module -t av'")
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

        if self.detailed:

            table = Table(
                title="Discovered Modules", show_lines=True, header_style="blue"
            )
            table.add_column("Name")
            for modules in module_dict.values():
                for name in modules:
                    table.add_row(f"{name}")
            console.print(table)

        self.valid_compilers = {}
        self.invalid_compilers = {}
        # test all modules via 'module load' and add only modules that passed (ret: 0)
        for name, module_list in module_dict.items():
            self.valid_compilers[name] = []
            self.invalid_compilers[name] = []
            for module in module_list:
                cmd = Module(module, debug=self.detailed)
                ret = cmd.test_modules(login=True)
                # if module load test passed we add entry to list
                if ret == 0:
                    self.valid_compilers[name].append(module)
                else:
                    self.invalid_compilers[name].append(module)

        # if self.detailed:
        #    console.print("PASS Compilers: ", self.valid_compilers)
        #    console.print("FAIL Compilers: ", self.invalid_compilers)

    def _update_compiler_section(self):
        """This method will update the compiler section by adding new compilers if
        found

        :return: Updated compiler section for buildtest configuration
        :rtype: dict
        """

        for name, module_list in self.valid_compilers.items():
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
