import json
import subprocess
import yaml
from lmod.module import Module
from lmod.spider import Spider


from buildtest.config import resolve_settings_file, load_settings
from buildtest.exceptions import BuildTestError
from buildtest.schemas.defaults import custom_validator, schema_table


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


def validate_modules(discovered_modules):
    """ This method will validate modules by running ``module load`` test for all
        discovered modules specified in parameter ``discovered_modules``. This method
        returns a list of modules that were valid, if all tests pass we return the same
        list. A module test pass if we get a returncode 0.

        :param discovered_modules:  A list of discovered modules specified as dictionary organized by compiler groups.
        :type discovered_modules: dict
        :return: Return a list of valid modules
        :rtype: dict
    """

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

    return valid_modules


def update_compiler_section(valid_modules, compilers):
    """ This method will update the compiler section by adding new compilers if
        neccessary and return a new compiler section that will be written back to
        disk as the new configuration file.

        :param valid_modules: A list of valid modules
        :param compilers: compiler section loaded as dictionary
        :return: Updated compiler section for buildtest configuration
        :rtype: dict
    """

    update_compilers = compilers
    if not update_compilers.get("compiler"):
        update_compilers["compiler"] = {}

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
            update_compilers["compiler"][name][new_compiler_entry]["module"] = {}
            update_compilers["compiler"][name][new_compiler_entry]["module"]["load"] = [
                module
            ]
            update_compilers["compiler"][name][new_compiler_entry]["module"][
                "purge"
            ] = False

    return update_compilers


def func_compiler_find(args=None):
    """This method implements ``buildtest config compilers find`` which detects
       new compilers based on module names defined in configuration. If system has
       Lmod we use Lmodule API to detect the compilers. For environment-modules we
       search for all modules in current ``$MODULEPATH``.
    """

    settings_file = resolve_settings_file()
    configuration = load_settings(settings_file)
    moduletool = configuration.get("moduletool")

    if moduletool == "N/A":
        raise BuildTestError(
            "You must have environment-modules or Lmod to use this tool. Please specify 'moduletool' in your configuration"
        )

    compilers = configuration.get("compilers")
    if not compilers:
        raise BuildTestError("Compiler section not detected")

    discovered_modules = find_compiler_modules(moduletool, compilers)

    if not discovered_modules:
        raise BuildTestError("No modules discovered")

    print("Discovered Modules:")
    print(json.dumps(discovered_modules, indent=2))
    print("\n\n")
    print("Testing Modules:")

    valid_modules = validate_modules(discovered_modules)

    update_compilers = update_compiler_section(valid_modules, compilers)

    configuration["compilers"] = update_compilers

    custom_validator(configuration, schema_table["settings.schema.json"]["recipe"])
    # validate(instance=configuration, schema=config_schema)
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
        raise BuildTestError("No compilers defined")

    bc = BuildtestCompilers()

    if args.json:
        bc.print_json()
    if args.yaml:
        bc.print_yaml()
    if args.list:
        names = bc.list()
        for name in names:
            print(name)


class BuildtestCompilers:
    def __init__(self):
        """
            :param compilers: compiler section from buildtest configuration.
            :type compilers: dict
        """

        configuration = load_settings()
        self.compilers = configuration["compilers"]["compiler"]

        self.names = []
        self.compiler_name_to_group = {}
        for name in self.compilers:
            if isinstance(self.compilers[name], dict):
                self.names += self.compilers[name].keys()
                for compiler in self.compilers[name].keys():
                    self.compiler_name_to_group[compiler] = name

    def print_json(self):
        """Prints compiler section in JSON, this implements ``buildtest config compilers --json``"""
        print(json.dumps(self.compilers, indent=2))

    def print_yaml(self):
        """Prints compiler section in YAML, this implements ``buildtest config compilers --yaml``"""
        print(yaml.dump(self.compilers, default_flow_style=False))

    def list(self):
        """Return all compilers defined in buildtest configuration"""
        return self.names
