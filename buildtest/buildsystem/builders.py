"""This file implements the Builder class that is responsible for getting builders
from a buildspec file. The Builder class is invoked once buildspec file has
parsed validation via BuildspecParser.
"""
import logging
import os
import re


from buildtest.buildsystem.scriptbuilder import ScriptBuilder
from buildtest.buildsystem.compilerbuilder import CompilerBuilder
from buildtest.menu.compilers import BuildtestCompilers
from buildtest.system import BuildTestSystem


class Builder:
    def __init__(self, bp, filters, testdir, rebuild=1):
        """ Based on a loaded Buildspec file, return the correct builder
            for each based on the type. Each type is associated with a known
            Builder class.

            :param bp: an instance of BuildspecParser class
            :type bp: BuildspecParser
            :param filter: A dictionary container filter fields for tags and executors passed from command line
            :type tag_filter: dict, required
            :param testdir: Test Destination directory, specified by --testdir
            :type testdir: str, required
            :param rebuild: Number of rebuilds for a tesst this is specified by ``buildtest build --rebuild``. Defaults to 1
            :type rebuild: int, optional
        """

        self.logger = logging.getLogger(__name__)
        self.testdir = testdir
        if not rebuild:
            self.rebuild = 1
        else:
            self.rebuild = rebuild or 1
            self.rebuild = int(rebuild)

        self.bp = bp
        self.filters = filters
        system = BuildTestSystem()
        self.builders = []

        for count in range(self.rebuild):
            for name in self.get_test_names():
                recipe = self.bp.recipe["buildspecs"][name]

                if recipe.get("skip"):
                    print(f"[{name}] test is skipped.")
                    continue

                if self._skip_tests_by_executor(recipe, name):
                    continue

                if self._skip_tests_by_tags(recipe, name):
                    continue

                if self._skip_tests_run_only(recipe, name, system):
                    continue

                # Add the builder based on the type
                if recipe["type"] == "script":
                    self.builders.append(
                        ScriptBuilder(
                            name, recipe, self.bp.buildspec, testdir=self.testdir
                        )
                    )
                elif recipe["type"] == "compiler":

                    self._build_compilers(name, recipe)

                else:
                    print(
                        "%s is not recognized by buildtest, skipping." % recipe["type"]
                    )

        for builder in self.builders:
            self.logger.debug(builder)

    def _build_compilers(self, name, recipe):
        """This method will perform regular expression with 'name' field in compilers
           section and retrieve one or more compiler that were defined in buildtest
           configuration. If any compilers were retrieved we return one or more
           builder objects that call CompilerBuilder

           :param name: name of test from buildspec file
           :type name: str
           :param recipe: loaded test recipe
           :type recipe: dict
        """
        self.compilers = {}
        bc = BuildtestCompilers()
        discovered_compilers = bc.list()
        # discovered_compilers = buildtest_compilers()

        # exclude compiler from search if 'exclude' specified in buildspec
        if recipe["compilers"].get("exclude"):
            for exclude in recipe["compilers"]["exclude"]:
                msg = f"Excluding compiler: {exclude} from test generation"
                print(msg)
                self.logger.debug(msg)
                discovered_compilers.remove(exclude)

        # apply regular expression specified by 'name' field against all discovered compilers
        for compiler_pattern in recipe["compilers"]["name"]:
            for bc_name in discovered_compilers:

                if re.match(compiler_pattern, bc_name):
                    builder = CompilerBuilder(
                        name,
                        recipe,
                        self.bp.buildspec,
                        compiler=bc_name,
                        testdir=self.testdir,
                    )
                    self.builders.append(builder)

    # Builders
    def _skip_tests_by_executor(self, recipe, testname):
        """This method returns a boolean if tests need to be skipped by executors. If
           executor in buildspec not found match in executor filter we skip test. This
           check is performed only if executor_filter is passed. The executor_filter
           is usually set if user runs ``buildtest build --executor``

           :param recipe: loaded buildspec recipe as dictionary
           :type recipe: dict
           :param testname: name of test instance in buildspec file
           :type testname: str
           :return: A boolean to determine if test is skipped
           :rtype: bool
        """

        # if input 'buildtest build --executor' is set we filter test by
        # executor name. For now we skip all test that don't belong in executor list.
        if (
            self.filters["executors"]
            and recipe.get("executor") not in self.filters["executors"]
        ):
            print(
                f"[{testname}] test is skipped because it is not in executor filter list: {self.filters['executors']}"
            )
            return True

        return False

    def _skip_tests_by_tags(self, recipe, name):
        """ This method determines if test should be skipped based on tag names specified
            in filter field that is specified on command line via ``buildtest build --tags``


            :param recipe: loaded buildspec recipe as dictionary
            :param name: An instance of test from buildspec file
            :return: Returns a boolean True/False which determines if test is skipped.
            :rtype: bool
        """

        if self.filters["tags"]:
            # if tags field in buildspec is empty, then we skip test only if user filters by tags
            if not recipe.get("tags"):
                return True

            found = False
            for tagname in self.filters["tags"]:
                if tagname in recipe.get("tags"):
                    found = True

            if not found:
                print(
                    f"[{name}] test is skipped because it is not in tag filter list: {self.filters['tags']}"
                )
                return True

        return False

    def _skip_tests_run_only(self, recipe, name, system):
        """ This method will skip tests based on ``run_only`` field from buildspec. Checks
            are performed based on conditionals and if any conditional is not met we skip test.

            :param recipe: loaded buildspec recipe as dictionary
            :param name: name of test from buildspec file
            :param system: An instance of ``BuildTestSystem`` class
            :return: Returns a boolean to see if test is skipped based on ``run_only`` property
            :rtype: bool
        """
        # if run_only field set, check if all conditions match before proceeding with test
        if recipe.get("run_only"):

            # skip test if host scheduler is not one specified via 'scheduler' field
            if recipe["run_only"].get("scheduler") and (
                recipe["run_only"].get("scheduler") not in system.system["scheduler"]
            ):
                msg = f"[{name}] test is skipped because ['run_only']['scheduler'] got value: {recipe['run_only']['scheduler']} but detected scheduler: {system.system['scheduler']}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if current user is not one specified in 'user' field
            if recipe["run_only"].get("user") and (
                recipe["run_only"].get("user") != os.getenv("USER")
            ):
                msg = f"[{name}] test is skipped because ['run_only']['user'] got value: {recipe['run_only']['user']} but detected user: {os.getenv('USER')}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if host platform is not equal to value specified by 'platform' field
            if recipe["run_only"].get("platform") and (
                recipe["run_only"].get("platform") != system.system["platform"]
            ):
                msg = f"[{name}] test is skipped because ['run_only']['platform'] got value: {recipe['run_only']['platform']} but detected platform: {system.system['platform']}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if host platform is not equal to value specified by 'platform' field
            if recipe["run_only"].get("linux_distro"):
                if system.system["os"] not in recipe["run_only"]["linux_distro"]:
                    msg = f"[{name}] test is skipped because ['run_only']['linux_distro'] got value: {recipe['run_only']['linux_distro']} but detected platform: {system.system['os']}."
                    print(msg)
                    self.logger.info(msg)
                    return True

        return False

    def get_builders(self):

        return self.builders

    def get_test_names(self):
        """ Return the list of test names for the loaded Buildspec recipe. This can
            be retrieved by returning a list of keys under 'buildspecs' property

            :return: A list of test names in buildspec file
            :rtype: list
        """

        keys = []
        if self.bp.recipe:
            keys = [x for x in self.bp.recipe["buildspecs"].keys()]
        return keys
