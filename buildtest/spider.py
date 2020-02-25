import json
import os
import subprocess

from buildtest.tools.defaults import BUILDTEST_SPIDER_FILE, BUILDTEST_CONFIG_FILE
from buildtest.tools.config import load_configuration


class Spider:
    """Class declaration of Spider class"""

    def __init__(self, tree=None):
        """Initialize method for Spider class.

        :param tree: User can specify a module tree to query from spider.
        :type tree: str
        """

        #  if user specifies a tree, then run spider command otherwise read from configuration file.
        if tree:
            self.tree = tree

            if not os.getenv("LMOD_DIR"):
                raise SystemError(
                    "Cannot find environment variable LMOD_DIR. Please fix your Lmod configuration!"
                )

            spider_cmd = f"{os.getenv('LMOD_DIR')}/spider -o spider-json {self.tree}"

            out = subprocess.check_output(spider_cmd, shell=True).decode("utf-8")
            self.spider_content = json.loads(out)

        else:
            with open(BUILDTEST_SPIDER_FILE, "r") as fd:
                self.spider_content = json.load(fd)

            content = load_configuration(BUILDTEST_CONFIG_FILE)
            self.tree = content.get("BUILDTEST_MODULEPATH", [])

    def get_trees(self):
        """" Return module trees used in spider command

        :return: return module trees used for querying from spider
        :rtype: str
        """
        return self.tree

    def get_unique_software(self):
        """Return all keys from spider. This is the unique software names.

        :return: return sorted list of all spider keys.
        :rtype: list
        """

        return sorted(list(self.spider_content.keys()))

    def get_modules(self):
        """Retrieve all module names from all module tree.

        :return: returns  a sorted list of all full canonical module name from all spider records.
        :rtype: list
        """

        module_names = []

        for module in self.get_unique_software():
            for mpath in self.spider_content[module].keys():

                module_names.append(self.spider_content[module][mpath]["fullName"])

        return sorted(module_names)

    def get_all_parents(self):
        """Return all parent modules from all spider trees. This will search all ``parentAA`` keys in spider
         content. The parent modules are used for setting MODULEPATH to other trees.

        :return: sorted list of all parent modules.
        :rtype: list
        """

        # we only care about unique modules. parentAA is bound to have duplicate modules.
        parent_set = set()

        for module in self.get_unique_software():
            for mpath in self.spider_content[module].keys():
                if "parentAA" in self.spider_content[module][mpath].keys():
                    for parent_comb in self.spider_content[module][mpath]["parentAA"]:
                        [parent_set.add(parent_module) for parent_module in parent_comb]

        return sorted(list(parent_set))

    def get_all_versions(self, key):
        """Get all versions of a particular software name.
        :param key: name of software
        :type key: str

        :return: list of module name as versions
        """

        # return empty list of key is not found
        if key not in self.get_unique_software():
            return []

        all_versions = []

        for modulefile in self.spider_content[key].keys():
            all_versions.append(self.spider_content[key][modulefile]["Version"])

        return all_versions
