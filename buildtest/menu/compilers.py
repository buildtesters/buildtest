import json
import os
import re
import subprocess
import yaml
from lmod.module import Module
from lmod.spider import Spider

from buildtest.config import resolve_settings_file, load_settings
from buildtest.exceptions import BuildTestError
from buildtest.schemas.defaults import custom_validator, schema_table
from buildtest.utils.tools import Hasher


def find_compiler_modules(moduletool, compilers):
    """ This method returns compiler modules discovered depending on your module system.
        If you have Lmod system we use spider utility to detect modules, this is leveraging
        Lmodule API. If you have environment-modules we parse output of ``module av -t``.


        :param moduletool: moduletool defined in buildtest configuration, it must be 'lmod', 'environment-modules', or 'N/A'
        :param compilers: compiler section loaded as dictionary from buildtest configuration
        :return: return a list of compiler modules detected based on module key name.
        :rtype: dict
    """

    discovered = {}
    # First we discover modules, if its Lmod we use Lmodule API class Spider to retrieve modules
    if moduletool == "lmod":
        spider = Spider()

        # retrieve all modules from Lmod spider and add them to dictionary
        for name, module_list in compilers.get("find").items():
            spider_modules = spider.get_modules(module_list).values()
            discovered[name] = list(spider_modules)

    # for environment-modules we retrieve modules by parsing output of 'module av -t'
    elif moduletool == "environment-modules":
        modules = subprocess.getoutput("module av -t")
        modules = modules.split()

        # discover all modules based with list of module names specified in find field, we add all
        # modules that start with the key name
        for compiler, module_names in compilers.get("find").items():
            discovered[compiler] = []
            for name in module_names:
                discovered[compiler] += [
                    module.replace("(default)", "")
                    for module in modules
                    if module.startswith(name)
                ]

    # ignore entry where value is empty list
    discovered = {k: v for k, v in discovered.items() if v}

    return discovered


def func_compiler_find(args=None):
    """This method implements ``buildtest config compilers find`` which detects
       new compilers based on module names defined in configuration. If system has
       Lmod we use Lmodule API to detect the compilers. For environment-modules we
       search for all modules in current ``$MODULEPATH``.
    """

    settings_file = resolve_settings_file()
    configuration = load_settings(settings_file)

    bc = BuildtestCompilers(configuration, debug=args.debug)
    bc.find_compilers()
    configuration["compilers"]["compiler"] = bc.compilers

    # raise BuildTestError("ERROR")
    custom_validator(configuration, schema_table["settings.schema.json"]["recipe"])
    # validate(instance=configuration, schema=config_schema)
    print(f"Configuration File: {settings_file}")
    print("{:_<80}".format(""))
    print(yaml.safe_dump(configuration, default_flow_style=False, sort_keys=False))
    print("{:_<80}".format(""))
    print(f"Updating settings file:  {settings_file}")

    with open(settings_file, "w") as fd:
        yaml.safe_dump(configuration, fd, default_flow_style=False, sort_keys=False)


def func_config_compiler(args=None):
    """This method implements ``buildtest config compilers`` which shows compiler
       section from buildtest configuration.
    """

    settings_file = resolve_settings_file()
    configuration = load_settings(settings_file)

    bc = BuildtestCompilers(configuration)

    if args.json:
        bc.print_json()
    if args.yaml:
        bc.print_yaml()
    if args.list:
        bc.print_compilers()


class BuildtestCompilers:
    compiler_table = {
        "gcc": {"cc": "gcc", "cxx": "g++", "fc": "gfortran",},
        "intel": {"cc": "icc", "cxx": "icpc", "fc": "ifort",},
        "pgi": {"cc": "pgcc", "cxx": "pgc++", "fc": "pgfortran",},
        "cray": {"cc": "cc", "cxx": "CC", "fc": "ftn",},
        "clang": {"cc": "clang", "cxx": "clang++", "fc": None},
        "cuda": {"cc": "nvcc", "cxx": "nvcc", "fc": None,},
    }

    def __init__(self, configuration, debug=False):
        """
            :param compilers: compiler section from buildtest configuration.
            :type compilers: dict
        """
        self.configuration = Hasher(configuration)
        self.debug = debug

        self.moduletool = self.configuration["moduletool"]

        if self.moduletool == "N/A" or not self.moduletool:
            raise BuildTestError(
                "You must have environment-modules or Lmod to use this tool. Please specify 'moduletool' in your configuration"
            )

        # The 'find' section is required for discovering new compilers
        if (
            not self.configuration["compilers"]
            or not self.configuration["compilers"]["find"]
        ):
            raise BuildTestError("Compiler section not detected")

        self.compilers = self.configuration["compilers"]["compiler"]

        self.names = []
        self.compiler_name_to_group = {}
        for name in self.compilers:
            if isinstance(self.compilers[name], dict):
                self.names += self.compilers[name].keys()
                for compiler in self.compilers[name].keys():
                    self.compiler_name_to_group[compiler] = name

    def find_compilers(self):
        """ This method returns compiler modules discovered depending on your module system.
            If you have Lmod system we use spider utility to detect modules, this is leveraging
            Lmodule API. If you have environment-modules we parse output of ``module av -t``.


            :return: return a list of compiler modules detected based on module key name.
            :rtype: dict
        """

        module_dict = {}
        print(f"MODULEPATH: {os.getenv('MODULEPATH')}")

        # First we discover modules, if its Lmod we use Lmodule API class Spider to retrieve modules
        if self.moduletool == "lmod":
            if self.debug:
                print("Searching modules via Lmod Spider")
            spider = Spider()

            spider_modules = list(spider.get_modules().values())
            for name, module_regex_patttern in self.configuration["compilers"][
                "find"
            ].items():
                module_dict[name] = []
                for module_fname in spider_modules:
                    if re.match(module_regex_patttern, module_fname):
                        module_dict[name].append(module_fname)

        # for environment-modules we retrieve modules by parsing output of 'module av -t'
        elif self.moduletool == "environment-modules":
            module_av = "module av -t"
            if self.debug:
                print(f"Searching modules by parsing content of command: {module_av}")

            modules = subprocess.getoutput("module av -t")
            modules = modules.split()

            # discover all modules based with list of module names specified in find field, we add all
            # modules that start with the key name
            for compiler, module_names in self.compilers.get("find").items():
                module_dict[compiler] = []
                for name in module_names:
                    # apply regex against all modules, some modules have output with
                    # (default) in that case we replace with empty string
                    module_dict[compiler] += [
                        module.replace("(default)", "")
                        for module in modules
                        if re.match(name, module)
                    ]

        # ignore entry where value is empty list
        module_dict = {k: v for k, v in module_dict.items() if v}

        if not module_dict:
            raise BuildTestError("No modules discovered")

        # print (json.dumps(self.discovered, indent=2))
        self._validate_modules(module_dict)
        self.update_compiler_section()

    def _validate_modules(self, module_dict):
        """ This method will validate modules by running ``module load`` test for all
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

    def update_compiler_section(self):
        """ This method will update the compiler section by adding new compilers if
            neccessary and return a new compiler section that will be written back to
            disk as the new configuration file.

            :return: Updated compiler section for buildtest configuration
            :rtype: dict
        """

        for name, module_list in self.compiler_modules_lookup.items():
            if not isinstance(self.compilers[name], dict):
                self.compilers[name] = {}

            for module in module_list:

                # replace first / with @ in format <compiler>@<version>
                # new_compiler_entry = module.replace("/", "@", 1)
                # if its a new compiler entry let's add new entry to dict
                if module not in self.compilers.get(name).keys():

                    self.compilers[name][module] = self.compiler_table[name]

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
        """This method print detected compilers from buildtest setting. This method is invoked by
           command ``buidltest config compilers --list
        """
        print(self.names)
        for name in self.names:
            print(name)
