"""This module implements the Builder class that is responsible for getting builders
from a buildspec file. The Builder class is invoked once buildspec file has
parsed validation via :class:`buildtest.buildsystem.parser.BuildspecParser`.
"""

import logging
import re

from buildtest.builders.compiler import CompilerBuilder
from buildtest.builders.script import ScriptBuilder
from buildtest.builders.spack import SpackBuilder
from buildtest.defaults import console
from buildtest.utils.tools import deep_get


class Builder:
    """The Builder class creates builder objects based on parsed buildspecs.

    The builder class is created based on the 'type' field in the test. If test contains
    ``type: script`` we will create builder by calling :class:`buildtest.builders.script.ScriptBuilder`.
    Likewise for ``type: compiler`` and ``type: spack`` we will call :class:`buildtest.builders.compiler.CompilerBuilder` and
    :class:`buildtest.builders.spack.SpackBuilder`.
    """

    def __init__(
        self,
        bp,
        buildtest_compilers,
        buildexecutor,
        filters,
        testdir,
        configuration,
        buildtest_system,
        rebuild=1,
        numprocs=None,
        numnodes=None,
        executor_type=None,
    ):
        """Based on a loaded Buildspec file, return the correct builder
        for each based on the type. Each type is associated with a known
        Builder class.

        Args:
            bp (buildtest.buildsystem.parser.BuildspecParser): Instance of BuildspecParser class
            buildexecutor (buildtest.executors.setup.BuildExecutor): Instance of BuildExecutor class
            filters (dict): List of filter fields specified via ``buildtest build --filter`` for filtering tests
            testdir (str): Test directory where tests will be written which could be specified via ``buildtest build --testdir`` or configuration file
            configuration (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class
            buildtest_system (buildtest.system.BuildTestSystem): Instance of BuildTestSystem class
            rebuild (int, option): Number of rebuild for test. This is specified via ``buildtest build --rebuild``. Defaults to 1
            numprocs (list, optional): List of processor values to create builder objects specified via ``buildtest build --procs``
            numnodes (list, optional): List of processor values to create builder objects specified via ``buildtest build --numnodes``
            executor_type (str, optional): Filter test by executor type (local, batch)
        """

        self.configuration = configuration
        self.system = buildtest_system
        self.logger = logging.getLogger(__name__)
        self.testdir = testdir
        self.buildexecutor = buildexecutor

        self.rebuild = rebuild or 1
        self.numprocs = numprocs
        self.numnodes = numnodes
        self.executor_type = executor_type

        self.bp = bp
        self.bc = buildtest_compilers
        self.filters = filters

        self.builders = []

        # skip property defined at top-level then skip test
        if self.bp.recipe.get("skip"):
            console.print(
                f"{self.bp.buildspec}: skipping all test since 'skip' is defined"
            )
            return

        if deep_get(self.filters, "maintainers"):
            if not self.bp.recipe.get("maintainers"):
                console.print(
                    f"{self.bp.buildspec}: skipping test because [italic]'maintainers'[/italic] field is not specified in buildspec."
                )
                return

            if self.filters["maintainers"] not in self.bp.recipe.get("maintainers"):
                console.print(
                    f"{self.bp.buildspec}: unable to find maintainer: {self.filters['maintainers']} in buildspec which contains the following maintainers: {self.bp.recipe.get('maintainers')} therefore we skip this test"
                )
                return

        for count in range(self.rebuild):
            for name in self.bp.get_test_names():
                recipe = self.bp.recipe["buildspecs"][name]

                if recipe.get("skip"):
                    msg = f"[red]{name}: skipping test due to [italic]'skip'[/italic] property."
                    self.logger.info(msg)
                    console.print(msg)
                    continue

                # apply filter by tags or type if --filter option is specified
                if self.filters:
                    if self._skip_tests_by_tags(recipe, name):
                        continue

                    if self._skip_tests_by_type(recipe, name):
                        continue

                # Add the builder for the script or spack schema

                if recipe["type"] in ["script", "compiler", "spack"]:
                    builders = self.build(name, recipe)
                    if builders:
                        self.builders += builders

        if self.executor_type:
            self.filter_by_executor_type()

    def filter_by_executor_type(self):
        """This method will filter test by executor type when using ``buildtest build --executor-type``. The filter can be made based on local or batch executors"""
        builders = []
        for builder in self.builders:
            if self.executor_type == "local" and not builder.is_local_executor():
                console.print(
                    f"[red]{builder} is excluded since its not using local executor"
                )
                continue

            elif self.executor_type == "batch" and builder.is_local_executor():
                console.print(
                    f"[red]{builder} is excluded since its not using batch executor"
                )
                continue

            builders.append(builder)

        self.builders = builders

    def create_script_builders(
        self, name, recipe, executor, nodes=None, procs=None, compiler_name=None
    ):
        """Create builder objects by calling :class:`buildtest.builders.script.ScriptBuilder` class.

        args:
            name (str): Name of test
            recipe (dict): Loaded test recipe from buildtest
            executor (str): Name of executor
            nodes (list, optional): A list of node configuration
            procs (list, optional): A list of process configuration
            compiler_name (str, optional): Name of resolved compiler instance
        """

        builders = []

        builder = ScriptBuilder(
            name=name,
            recipe=recipe,
            executor=executor,
            buildspec=self.bp.buildspec,
            buildexecutor=self.buildexecutor,
            configuration=self.configuration,
            testdir=self.testdir,
            compiler=compiler_name,
        )
        builders.append(builder)

        if nodes:
            for node in nodes:
                builder = ScriptBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    configuration=self.configuration,
                    testdir=self.testdir,
                    numnodes=node,
                    compiler=compiler_name,
                )
                builders.append(builder)
        if procs:
            for proc in procs:
                builder = ScriptBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    configuration=self.configuration,
                    testdir=self.testdir,
                    numprocs=proc,
                    compiler=compiler_name,
                )
                builders.append(builder)

        return builders

    def create_compiler_builders(
        self, name, recipe, executor, nodes=None, procs=None, compiler_name=None
    ):
        """Create builder objects by calling :class:`buildtest.builders.compiler.CompilerBuilder` class.

        args:
            name (str): Name of test
            recipe (dict): Loaded test recipe from buildtest
            executor (str): Name of executor
            nodes (list, optional): A list of node configuration
            procs (list, optional): A list of process configuration
            compiler_name (str, optional): Name of resolved compiler instance
        """
        builders = []

        builder = CompilerBuilder(
            name=name,
            recipe=recipe,
            executor=executor,
            buildspec=self.bp.buildspec,
            buildexecutor=self.buildexecutor,
            configuration=self.configuration,
            testdir=self.testdir,
            compiler=compiler_name,
        )
        builders.append(builder)

        if nodes:
            for node in nodes:
                builder = CompilerBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    configuration=self.configuration,
                    testdir=self.testdir,
                    numnodes=node,
                    compiler=compiler_name,
                )
                builders.append(builder)
        if procs:
            for proc in procs:
                builder = CompilerBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    configuration=self.configuration,
                    testdir=self.testdir,
                    numprocs=proc,
                    compiler=compiler_name,
                )
                builders.append(builder)

        return builders

    def create_spack_builders(self, name, recipe, executor, nodes=None, procs=None):
        """Create builder objects by calling :class:`buildtest.builders.spack.SpackBuilder` class.

        args:
            name (str): Name of test
            recipe (dict): Loaded test recipe from buildtest
            executor (str): Name of executor
            nodes (list, optional): A list of node configuration
            procs (list, optional): A list of process configuration
        """
        builders = []

        builder = SpackBuilder(
            name=name,
            recipe=recipe,
            executor=executor,
            buildspec=self.bp.buildspec,
            buildexecutor=self.buildexecutor,
            testdir=self.testdir,
        )
        builders.append(builder)

        if nodes:
            for node in nodes:
                builder = SpackBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    testdir=self.testdir,
                    numnodes=node,
                )
                builders.append(builder)
        if procs:
            for proc in procs:
                builder = SpackBuilder(
                    name=name,
                    recipe=recipe,
                    executor=executor,
                    buildspec=self.bp.buildspec,
                    buildexecutor=self.buildexecutor,
                    testdir=self.testdir,
                    numprocs=proc,
                )
                builders.append(builder)

        return builders

    def generate_builders(self, recipe, name, compiler_name=None):
        """This method is responsible for generating builders by applying regular expression specified by
        `executor` field in buildspec with list of executors. If their is a match we generate a builder.

        Args:
            name (str): Name of test in buildspec file
            recipe (dict): Loaded test recipe from buildspec file
            compiler_name (str, optional): Name of compiler

        Returns:
            List of builder objects
        """

        builders = []
        self.logger.debug(
            f"Searching for builders for test: {name} by applying regular expression with available builders: {self.buildexecutor.names()} "
        )
        for executor in self.buildexecutor.names():
            if (
                re.fullmatch(recipe["executor"], executor)
                and recipe["type"] == "script"
            ):
                self.logger.debug(
                    f"Found a match in buildspec with available executors via re.fullmatch({recipe['executor']},{executor})"
                )
                builders += self.create_script_builders(
                    name=name,
                    executor=executor,
                    recipe=recipe,
                    nodes=self.numnodes,
                    procs=self.numprocs,
                    compiler_name=compiler_name,
                )

            elif (
                re.fullmatch(recipe["executor"], executor)
                and recipe["type"] == "compiler"
            ):
                self.logger.debug(
                    f"Found a match in buildspec with available executors via re.fullmatch({recipe['executor']},{executor})"
                )
                builders += self.create_compiler_builders(
                    name=name,
                    executor=executor,
                    recipe=recipe,
                    nodes=self.numnodes,
                    procs=self.numprocs,
                    compiler_name=compiler_name,
                )

            elif (
                re.fullmatch(recipe["executor"], executor) and recipe["type"] == "spack"
            ):
                builders += self.create_spack_builders(
                    name=name,
                    executor=executor,
                    recipe=recipe,
                    nodes=self.numnodes,
                    procs=self.numprocs,
                )

        return builders

    def build(self, name, recipe):
        """This method will generate a list of builders by invoking method :func:`buildtest.buildsystem.builders.Builder.generate_builders`.
        If `compilers` is specified in buildspec we will perform regular expression to search for compilers based on `name`
        and retrieve one or more compiler that were defined in buildtest
        configuration. If any compilers were retrieved we return one or more
        builder objects based on compiler name.

        Args:
            name (str): name of test
            recipe (dict): Loaded test recipe from buildspec
        """
        discovered_compilers = self.bc.names()

        builders = []

        # compilers property in script schema is optional while in compiler schema its required. If 'compilers' is set with 'type: script' then return builders
        if not recipe.get("compilers"):
            builders = self.generate_builders(name=name, recipe=recipe)
            return builders

        # exclude compiler from search if 'exclude' specified in buildspec
        if recipe["compilers"].get("exclude"):
            for exclude in recipe["compilers"]["exclude"]:
                if exclude in discovered_compilers:
                    msg = f"[blue]{name}[/blue]: [red]Excluding compiler {exclude} during test generation"
                    console.print(msg)
                    self.logger.debug(msg)
                    discovered_compilers.remove(exclude)

        # apply regular expression specified by 'name' field against all discovered compilers
        for compiler_pattern in recipe["compilers"]["name"]:
            for bc_name in discovered_compilers:
                if re.match(compiler_pattern, bc_name):
                    builder = self.generate_builders(
                        name=name, recipe=recipe, compiler_name=bc_name
                    )

                    builders += builder

        if not builders:
            msg = f"[{name}][{self.bp.buildspec}]: Unable to find any compilers based on regular expression: {recipe['compilers']['name']} so no tests were created."
            print(msg)
            self.logger.debug(msg)
            return

        return builders

    def _skip_tests_by_tags(self, recipe, name):
        """This method determines if test should be skipped based on tag names specified
        in filter field that is specified on command line via ``buildtest build --filter tags=<TAGNAME>``

        Args:
            recipe (dict): Loaded test recipe from buildspec
            name (str): Name of test

        Returns:
            bool: False if ``buildtest build --filter tags`` is not specified. If specified we return ``True`` if ``tags`` field is not in test recipe or there is a matching tag.

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

        Args:
            recipe (dict): Loaded test recipe from buildspec
            name (str): Name of test

        Returns:
            bool: False if ``buildtest build --filter type`` is not specified. If there is a match with input filter and ``type`` field in test we return ``True``

        """

        if self.filters.get("type"):
            found = self.filters["type"] == recipe["type"]

            if not found:
                msg = f"[{name}][{self.bp.buildspec}]: test is skipped because it is not in type filter list: {self.filters['type']}"
                self.logger.info(msg)
                print(msg)
                return True

        return False

    def get_builders(self):
        """Return a list of builder objects"""
        return self.builders

    def get_filtered_buildspec(self):
        """Return a list of buildspec that were filtered out"""
        return self.filtered_buildspecs
