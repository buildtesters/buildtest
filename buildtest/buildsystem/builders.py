"""This file implements the Builder class that is responsible for getting builders
from a buildspec file. The Builder class is invoked once buildspec file has
parsed validation via BuildspecParser.
"""
import logging
import os
import re

from buildtest.buildsystem.compilerbuilder import CompilerBuilder
from buildtest.buildsystem.scriptbuilder import ScriptBuilder
from buildtest.buildsystem.spack import SpackBuilder
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.exceptions import BuildTestError
from buildtest.system import system
from buildtest.utils.tools import deep_get


class Builder:
    def __init__(
        self,
        bp,
        buildexecutor,
        filters,
        testdir,
        configuration,
        buildtest_system=None,
        rebuild=1,
    ):
        """Based on a loaded Buildspec file, return the correct builder
        for each based on the type. Each type is associated with a known
        Builder class.

        :param bp: an instance of BuildspecParser class
        :type bp: BuildspecParser, required
        :param buildexecutor: an instance of BuildExecutor class defines Executors from configuration file
        :type buildexecutor: BuildExecutor, required
        :param filters: A filter fields for filtering tests.
        :type filters: dict, required
        :param testdir: Test Destination directory, specified by --testdir
        :type testdir: str, required
        :param configuration: Instance of SiteConfiguration class
        :type configuration: SiteConfiguration
        :param buildtest_system: Instance of BuildTestSystem
        :type buildtest_system: BuildTestSystem
        :param rebuild: Number of rebuilds for a tesst this is specified by ``buildtest build --rebuild``. Defaults to 1
        :type rebuild: int, optional
        """

        self.configuration = configuration
        self.system = buildtest_system or system
        self.logger = logging.getLogger(__name__)
        self.testdir = testdir
        self.buildexecutor = buildexecutor

        if not rebuild:
            self.rebuild = 1
        else:
            # FIX LINE BELOW
            self.rebuild = rebuild or 1
            self.rebuild = int(rebuild)

        self.bp = bp
        self.filters = filters

        if deep_get(self.filters, "maintainers"):
            if not self.bp.recipe.get("maintainers"):
                raise BuildTestError(
                    f"[{self.bp.buildspec}]: skipping test because maintainers field is not specified when using buildtest build --filter maintainers={self.filters['maintainers'] }"
                )

            if self.filters["maintainers"] not in self.bp.recipe.get("maintainers"):
                raise BuildTestError(
                    f"[{self.bp.buildspec}]: skipping buildspec due to filter by maintainers: {self.filters['maintainers']}"
                )

        self.builders = []

        for count in range(self.rebuild):
            for name in self.get_test_names():
                recipe = self.bp.recipe["buildspecs"][name]

                if recipe.get("skip"):
                    msg = f"[{name}]({self.bp.buildspec}): test is skipped."
                    self.logger.info(msg)
                    print(msg)
                    continue

                # apply filter by tags or type if --filter option is specified
                if self.filters:
                    if self._skip_tests_by_tags(recipe, name):
                        continue

                    if self._skip_tests_by_type(recipe, name):
                        continue

                if self._skip_tests_run_only(recipe, name):
                    continue

                # Add the builder for the script or spack schema
                if recipe["type"] in ["script", "spack"]:
                    self.builders += self._generate_builders(recipe, name)

                elif recipe["type"] == "compiler":

                    self._build_compilers(name, recipe)
                else:
                    print(
                        "%s is not recognized by buildtest, skipping." % recipe["type"]
                    )

        for builder in self.builders:
            self.logger.debug(builder)

    def _generate_builders(self, recipe, name, compiler_name=None):
        """This method is responsible for generating builders by applying regular expression specified by
        `executor` field in buildspec with list of executors. If their is a match we generate a builder.

        :param name: Name of test in buildspec file
        :type name: str
        :param recipe: Loaded test recipe from a test section.
        :type recipe: dict
        :param compiler_name: Name of compiler
        :type compiler_name: str, optional
        :return: A list of builder objects
        :type recipe: object


        """
        builders = []
        self.logger.debug(
            f"Searching for builders for test: {name} by applying regular expression with available builders: {self.buildexecutor.list_executors()} "
        )
        for executor in self.buildexecutor.list_executors():
            builder = None

            if (
                re.fullmatch(recipe.get("executor"), executor)
                and recipe["type"] == "script"
            ):
                self.logger.debug(
                    f"Found a match in buildspec with available executors via re.fullmatch({recipe.get('executor')},{executor})"
                )
                builder = ScriptBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    testdir=self.testdir,
                )

            elif (
                re.fullmatch(recipe.get("executor"), executor)
                and recipe["type"] == "compiler"
            ):
                self.logger.debug(
                    f"Found a match in buildspec with available executors via re.fullmatch({recipe.get('executor')},{executor})"
                )
                builder = CompilerBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    compiler=compiler_name,
                    buildspec=self.bp.buildspec,
                    configuration=self.configuration,
                    buildexecutor=self.buildexecutor,
                    testdir=self.testdir,
                )

            elif (
                re.fullmatch(recipe.get("executor"), executor)
                and recipe["type"] == "spack"
            ):
                builder = SpackBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    testdir=self.testdir,
                )

            if builder:
                self.logger.debug(builder)
                builders.append(builder)

        return builders

    def _build_compilers(self, name, recipe):
        """This method will perform regular expression with 'name' field in compilers
        section and retrieve one or more compiler that were defined in buildtest
        configuration. If any compilers were retrieved we return one or more
        builder objects that call CompilerBuilder

        :param bp: an instance of BuilderspecParser class
        :type bp: BuildspecParser
        :param recipe: loaded test recipe
        :type recipe: dict
        """
        self.compilers = {}

        bc = BuildtestCompilers(configuration=self.configuration)
        discovered_compilers = bc.list()

        builders = []
        # exclude compiler from search if 'exclude' specified in buildspec
        if recipe["compilers"].get("exclude"):
            for exclude in recipe["compilers"]["exclude"]:
                if exclude in discovered_compilers:
                    msg = f"Excluding compiler: {exclude} from test generation"
                    print(msg)
                    self.logger.debug(msg)
                    discovered_compilers.remove(exclude)

        # apply regular expression specified by 'name' field against all discovered compilers
        for compiler_pattern in recipe["compilers"]["name"]:
            for bc_name in discovered_compilers:
                if re.match(compiler_pattern, bc_name):

                    builder = self._generate_builders(
                        name=name, recipe=recipe, compiler_name=bc_name
                    )

                    builders += builder

        if not builders:
            msg = f"[{name}][{self.bp.buildspec}]: Unable to find any compilers based on regular expression: {recipe['compilers']['name']} so no tests were created."
            print(msg)
            self.logger.debug(msg)
            return

        for builder in builders:
            self.builders.append(builder)

    def _skip_tests_by_tags(self, recipe, name):
        """This method determines if test should be skipped based on tag names specified
        in filter field that is specified on command line via ``buildtest build --filter tags=<TAGNAME>``


        :param recipe: loaded buildspec recipe as dictionary
        :type recipe: dict
        :param name: An instance of test from buildspec file
        :type name: str
        :return: Returns a boolean True/False which determines if test is skipped.
        :rtype: bool
        """

        if self.filters.get("tags"):
            # if tags field in buildspec is empty, then we skip test only if user filters by tags
            if not recipe.get("tags"):
                return True

            found = False
            # for tagname in self.filters:
            if self.filters["tags"] in recipe.get("tags"):
                found = True

            if not found:
                msg = f"[{name}][{self.bp.buildspec}]: test is skipped because it is not in tag filter list: {self.filters}"
                self.logger.info(msg)
                print(msg)
                return True

        return False

    def _skip_tests_by_type(self, recipe, name):
        """This method determines if test should be skipped based on type field specified
        in filter field that is specified on command line via ``buildtest build --filter type=<SCHEMATYPE>``


        :param recipe: loaded buildspec recipe as dictionary
        :type recipe: dict
        :param name: An instance of test from buildspec file
        :type name: str
        :return: Returns a boolean True/False which determines if test is skipped.
        :rtype: bool
        """

        if self.filters.get("type"):

            found = self.filters["type"] == recipe["type"]

            if not found:
                msg = f"[{name}][{self.bp.buildspec}]: test is skipped because it is not in type filter list: {self.filters['type']}"
                self.logger.info(msg)
                print(msg)
                return True

        return False

    def _skip_tests_run_only(self, recipe, name):
        """This method will skip tests based on ``run_only`` field from buildspec. Checks
        are performed based on conditionals and if any conditional is not met we skip test.

        :param recipe: loaded buildspec recipe as dictionary
        :type recipe: dict, required
        :param name: name of test from buildspec file
        :type name: str, required
        :return: Returns a boolean to see if test is skipped based on ``run_only`` property
        :rtype: bool
        """
        # if run_only field set, check if all conditions match before proceeding with test
        if recipe.get("run_only"):

            # skip test if host scheduler is not one specified via 'scheduler' field
            if recipe["run_only"].get("scheduler") and (
                recipe["run_only"].get("scheduler")
                not in self.system.system["scheduler"]
            ):
                msg = f"[{name}][{self.bp.buildspec}]: test is skipped because ['run_only']['scheduler'] got value: {recipe['run_only']['scheduler']} but detected scheduler: {self.system.system['scheduler']}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if current user is not one specified in 'user' field
            if recipe["run_only"].get("user") and (
                recipe["run_only"].get("user") != os.getenv("USER")
            ):
                msg = f"[{name}][{self.bp.buildspec}]: test is skipped because this test is expected to run as user: {recipe['run_only']['user']} but detected user: {os.getenv('USER')}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if host platform is not equal to value specified by 'platform' field
            if recipe["run_only"].get("platform") and (
                recipe["run_only"].get("platform") != self.system.system["platform"]
            ):
                msg = f"[{name}][{self.bp.buildspec}]: test is skipped because this test is expected to run on platform: {recipe['run_only']['platform']} but detected platform: {self.system.system['platform']}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if host platform is not equal to value specified by 'platform' field
            if recipe["run_only"].get("linux_distro"):
                if self.system.system["os"] not in recipe["run_only"]["linux_distro"]:
                    msg = f"[{name}][{self.bp.buildspec}]: test is skipped because this test is expected to run on linux distro: {recipe['run_only']['linux_distro']} but detected linux distro: {self.system.system['os']}."
                    print(msg)
                    self.logger.info(msg)
                    return True

        return False

    def get_builders(self):

        return self.builders

    def get_test_names(self):
        """Return the list of test names for the loaded Buildspec recipe. This can
        be retrieved by returning a list of keys under 'buildspecs' property

        :return: A list of test names in buildspec file
        :rtype: list
        """

        keys = []
        if self.bp.recipe:
            keys = [x for x in self.bp.recipe["buildspecs"].keys()]
        return keys
