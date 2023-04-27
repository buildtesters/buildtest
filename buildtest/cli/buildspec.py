import json
import logging
import os
import random
import subprocess
import sys
import time

from buildtest.buildsystem.parser import BuildspecParser
from buildtest.cli.build import discover_buildspecs
from buildtest.cli.report import Report
from buildtest.defaults import (
    BUILDSPEC_CACHE_FILE,
    BUILDSPEC_DEFAULT_PATH,
    BUILDTEST_BUILDSPEC_DIR,
    console,
)
from buildtest.exceptions import BuildspecError, BuildTestError, ExecutorError
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.file import (
    create_dir,
    is_dir,
    is_file,
    load_json,
    resolve_path,
    walk_tree,
)
from buildtest.utils.tools import checkColor
from jsonschema.exceptions import ValidationError
from rich.layout import Layout
from rich.panel import Panel
from rich.pretty import pprint
from rich.syntax import Syntax
from rich.table import Column, Table

logger = logging.getLogger(__name__)


class BuildspecCache:
    table = {}
    filter_fields = ["type", "executor", "tags", "buildspec"]
    default_format_fields = ["name", "type", "executor", "tags", "description"]
    format_fields = default_format_fields + ["buildspec"]

    def __init__(
        self,
        configuration,
        rebuild=False,
        filterfields=None,
        formatfields=None,
        roots=None,
        header=None,
        terse=None,
        pager=None,
        color=None,
        count=None,
    ):
        """The initializer method for BuildspecCache class is responsible for loading and finding buildspecs into buildspec cache. First we
        resolve paths to directory where buildspecs will be searched. This can be specified via ``--roots`` option on command line or one can
        specify directory paths in the configuration file. Next we build the cache that contains metadata for each buildspec that will be
        written to file. If any filter or format options are specified we check if they are valid and finally display a content of the cache
        depending on the argument.

        This method is called when using ``buildtest buildspec find`` command.

        Args:
            configuration (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class that is loaded buildtest configuration.
            rebuild (bool, optional): rebuild the buildspec cache by validating all buildspecs when using ``buildtest buildspec find --rebuild``. Defaults to ``False`` if ``--rebuild`` is not specified
            filterfields (str, optional): The filter options specified via ``buildtest buildspec find --filter`` that contains list of key value pairs for filtering buildspecs
            formatfields (str, optional): The format options used for formating table. The format option is a comma separated list of format fields specified via ``buildtest buildspec find --format``
            roots (list, optional): List of directories to search for buildspecs. This argument contains value of ``buildtest buildspec find --roots``
            headers (bool, optional):  Option to control whether header are printed in terse output. This argument contains value of ``buildtest buildspec find --no-header``
            terse (bool, optional): Enable terse mode when printing output. In this mode we don't print output in table format instead output is printed in parseable format. This option can be specified via ``buildtest buildspec find --terse``
            color (str, optional): An instance of a string class that selects the color to use when printing table output
            count (int, optional): Number of entries to display in output. This argument contains value of ``buildtest buildspec find --count``
        """

        if not is_dir(BUILDTEST_BUILDSPEC_DIR):
            create_dir(BUILDTEST_BUILDSPEC_DIR)

        self.configuration = configuration
        self.filter = filterfields
        self.format = formatfields or self.configuration.target_config[
            "buildspecs"
        ].get("formatfields")
        self.header = header
        self.pager = pager or self.configuration.target_config["buildspecs"].get(
            "pager"
        )
        self.count = count or self.configuration.target_config["buildspecs"].get(
            "count"
        )
        # if --root is not specified we set to empty list instead of None
        self.roots = roots or []

        # list of buildspec directories to search for .yml files
        self.paths = []

        # stores invalid buildspecs and the error messages
        self.invalid_buildspecs = {}

        self.terse = terse or self.configuration.target_config["buildspecs"].get(
            "terse"
        )
        self.color = checkColor(color)

        self.rebuild = rebuild or self.configuration.target_config["buildspecs"].get(
            "rebuild"
        )
        self.cache = {}

        self.load_paths()
        self.build()

        self._check_filter_fields()
        self._check_format_fields()
        self.find_buildspecs()

    def get_cache(self):
        """Returns cache file as loaded dictionary"""

        return self.cache

    def load_paths(self):
        """Add all paths to search for buildspecs. We must read configuration file
        and check property ``buildspec_roots`` for list of directories to search.
        We check all directories exist, if any fail we don't add them to path.
        If no root directories are specified we load the default buildspec roots which are
        `tutorials <https://github.com/buildtesters/buildtest/tree/devel/tutorials>`_
        and `general_tests <https://github.com/buildtesters/buildtest/tree/devel/general_tests>`_ directory.
        """

        buildspec_paths = self.configuration.target_config.get("buildspec_roots") or []

        if buildspec_paths:
            self.roots += buildspec_paths

        # if no roots specified we load the default buildspec roots.
        if not self.roots:
            self.paths += BUILDSPEC_DEFAULT_PATH

        # for every root buildspec defined in configuration or via --root option,
        # we resolve path and if path exist add to self.paths. The path must be a
        # directory. If its file, we ignore it
        if self.roots:
            for root in self.roots:
                path = resolve_path(root, exist=False)
                if not os.path.exists(path):
                    console.print(f"[red]Path: {path} does not exist!")

                if is_file(path):
                    console.print(f"[red]Path: {path} must be a directory not a file")

                if is_dir(path):
                    self.paths.append(path)

    def build(self):
        """This method will build buildspec cache file. If user requests to
        rebuild cache we remove the file and recreate cache. If cache file
        exists, we simply load from cache
        """

        # implements buildtest buildspec find --rebuild which removes cache file
        # before finding all buildspecs. We only remove file if file exists
        if self.rebuild and is_file(BUILDSPEC_CACHE_FILE):
            try:
                os.remove(BUILDSPEC_CACHE_FILE)

                if not self.terse:
                    print(f"Clearing cache file: {BUILDSPEC_CACHE_FILE}")

            except OSError as msg:
                raise BuildTestError(msg)

        # if cache file is not found, then we will build cache by searching
        # all buildspecs paths and traverse directory to find all .yml files

        if not is_file(BUILDSPEC_CACHE_FILE):
            self.build_cache()

        self.cache = load_json(BUILDSPEC_CACHE_FILE)

    def _discover_buildspecs(self):
        """This method retrieves buildspecs based on ``self.paths`` which is a
        list of directory paths to search. If ``--root`` is specified
        we process each argument and recursively find all .yml files
        """

        buildspecs = []
        # add all buildspecs from each repo. walk_tree will find all .yml files
        # recursively and add them to list

        if not self.paths:
            raise BuildTestError(
                "Unable to search any buildspecs, please specify a directory"
            )

        if self.paths:
            for path in self.paths:
                buildspec = walk_tree(path, ".yml")
                buildspecs += buildspec

        if not self.terse:
            print(f"Buildspec Paths: {self.paths}")

        return buildspecs

    def _write_buildspec_cache(self):
        """This method is responsible for writing buildspec cache to file"""

        with open(BUILDSPEC_CACHE_FILE, "w") as fd:
            json.dump(self.update_cache, fd, indent=2)

        if not self.terse:
            print(f"Updating buildspec cache file: {BUILDSPEC_CACHE_FILE}")

    def _validate_buildspecs(self, buildspecs):
        """Given a list of buildspec files, validate each buildspec using :class:`buildtest.buildsystem.parser.BuildspecParser`
        class and return a list of valid buildspecs. Any invalid buildspecs are added to separate list

        Args:
            buildspecs: A list of buildspec to validate
        """
        valid_buildspecs = []

        buildexecutor = BuildExecutor(self.configuration)

        with console.status("Processing buildspecs", spinner="aesthetic"):
            for buildspec in buildspecs:
                try:
                    parse = BuildspecParser(
                        buildspec, buildexecutor, executor_match=True
                    )
                # any buildspec that raises SystemExit or ValidationError imply
                # buildspec is not valid, we add this to invalid list along with
                # error message and skip to next buildspec
                except (
                    BuildspecError,
                    ExecutorError,
                    ValidationError,
                ) as err:
                    if isinstance(err, BuildspecError):
                        self.invalid_buildspecs[buildspec] = {
                            "msg": err.get_exception()
                        }
                    else:
                        self.invalid_buildspecs[buildspec] = {"msg": repr(err)}

                    self.invalid_buildspecs[buildspec]["exception"] = repr(type(err))
                    continue

                valid_buildspecs.append(parse)
                time.sleep(0.05)

        return valid_buildspecs

    def get_names(self):
        """Return a list of test names found in buildspec cache. We only return test names for valid buildspecs"""

        valid_buildspecs = self.get_valid_buildspecs()

        test_names = []

        for buildspec in valid_buildspecs:
            for name in self.cache["buildspecs"][buildspec]:
                test_names.append(name)

        return test_names

    def get_random_tests(self, num_items=1):
        """Returns a list of random test names from the list of available test. The test are picked
        using `random.sample <https://docs.python.org/3/library/random.html#random.sample>`_

        Args:
            num_items (int, optional): Number of test items to retrieve
        """
        return random.sample(self.get_names(), num_items)

    def lookup_buildspec_by_name(self, name):
        """Given an input test name, return corresponding buildspec file found in the cache.

        Args:
            name (str): Name of test to query in cache

        Return:
            Return path to buildspec that contains name of test
        """
        valid_buildspecs = self.get_valid_buildspecs()

        for buildspec in valid_buildspecs:
            if name in self.cache["buildspecs"][buildspec].keys():
                return buildspec

    def build_cache(self):
        """This method will rebuild the buildspec cache file by recursively searching
        all .yml files specified by input argument ``paths`` which is a list of directory
        roots. The buildspecs are validated and cache file is updated
        """

        self.update_cache = {}
        self.update_cache["unique_tags"] = []
        self.update_cache["unique_executors"] = []
        self.update_cache["buildspecs"] = {}
        self.update_cache["executor"] = {}
        self.update_cache["tags"] = {}
        self.update_cache["maintainers"] = {}
        self.update_cache["paths"] = self.paths

        # for path in self.paths:
        #    self.update_cache[path] = {}

        buildspecs = self._discover_buildspecs()

        self.update_cache["invalids"] = {}

        # validate each buildspec and return a list of valid buildspec parsers that
        # is an instance of BuildspecParser class

        parsers = self._validate_buildspecs(buildspecs)

        if self.invalid_buildspecs:
            for buildspec in self.invalid_buildspecs.keys():
                self.update_cache["invalids"][buildspec] = self.invalid_buildspecs[
                    buildspec
                ]

        # for every parsers (valid buildspecs) we update cache to build an index
        for parser in parsers:
            recipe = parser.recipe["buildspecs"]

            # if maintainer field specified add all maintainers from buildspec to list
            if parser.recipe.get("maintainers"):
                for author in parser.recipe["maintainers"]:
                    if not self.update_cache["maintainers"].get(author):
                        self.update_cache["maintainers"][author] = []

                    self.update_cache["maintainers"][author].append(parser.buildspec)

            if not self.update_cache["buildspecs"].get(parser.buildspec):
                self.update_cache["buildspecs"][parser.buildspec] = {}

            for name in recipe.keys():
                self.update_cache["buildspecs"][parser.buildspec][name] = recipe[name]
                tags = recipe[name].get("tags")
                executor = recipe[name].get("executor")
                description = recipe[name].get("description")

                if tags:
                    # if tag is string, add to unique_tags list and associate name and description with tag name
                    if isinstance(tags, str):
                        self.update_cache["unique_tags"].append(tags)

                        if not self.update_cache["tags"].get(tags):
                            self.update_cache["tags"][tags] = {}

                        self.update_cache["tags"][tags][name] = description

                    elif isinstance(tags, list):
                        self.update_cache["unique_tags"] += tags

                        # for every tagname, build a tags to testname association
                        for tag in tags:
                            if not self.update_cache["tags"].get(tag):
                                self.update_cache["tags"][tag] = {}

                            self.update_cache["tags"][tag][name] = description

                if executor:
                    self.update_cache["unique_executors"].append(executor)

                    if not self.update_cache["executor"].get(executor):
                        self.update_cache["executor"][executor] = {}

                    self.update_cache["executor"][executor][name] = description

        self.update_cache["unique_tags"] = list(set(self.update_cache["unique_tags"]))
        self.update_cache["unique_executors"] = list(
            set(self.update_cache["unique_executors"])
        )

        self._write_buildspec_cache()

    def _check_filter_fields(self):
        """This method checks filter fields are valid. The filter fields are specified
        as ``buildtest buildspec find --filter <KEY1>=<VAL1>,<KEY2>=<VAL2>,...``

        Raises:
            BuildTestError: If there is an invalid filter field
        """

        self.executor_filter = None
        self.tags_filter = None
        self.type_filter = None

        if self.filter:
            filter_error = False
            # check if filter keys are accepted filter fields, if not we raise error
            for key in self.filter.keys():
                if key not in self.filter_fields:
                    print(f"Invalid filter key: {key}")
                    filter_error = True

            # raise error if any filter field is invalid
            if filter_error:
                raise BuildTestError(f"Invalid filter fields format {self.filter}")

            self.executor_filter = self.filter.get("executor")
            self.tags_filter = self.filter.get("tags")
            self.type_filter = self.filter.get("type")

    def _check_format_fields(self):
        """This method will check if all format fields are valid. Format fields
        are passed as comma separated fields: ``--format field1,field2,field3,...``

        Raises:
            BuildTestError: If there is an invalid format field
        """

        for field in self.default_format_fields:
            self.table[field] = []

        if self.format:
            format_error = False
            for key in self.format.split(","):
                if key not in self.format_fields:
                    print(f"Invalid format field: {key}")
                    format_error = True

                if format_error:
                    raise BuildTestError(f"Invalid format fields format {self.format}")

            # if --format option specified we setup cache dictionary based on format
            # fields that are added to list
            self.table = {}
            for field in self.format.split(","):
                self.table[field] = []

    def _filter_buildspecs(self, executor, tags, schema_type):
        """This method will return a boolean True/False that determines if
        buildspec test entry is skipped as part of filter process. The filter
        are done based on executor, tags, type field. ``True`` indicates test
        needs to be skipped.

        Args:
            executor (str): ``executor`` property in buildspec
            tags (list): `List of tagnames specified via `tags`` property in buildspec
            schema_type (str): ``type`` property in buildspec

        Returns:
            bool: Return True if there is **no** match otherwise returns False
        """

        # skip all entries that dont match filtered executor
        if self.executor_filter and self.executor_filter != executor:
            return True

        # if skip all entries that dont match filtered tag. We only search if --filter tag=value is set
        if self.tags_filter:
            # if tags is not set in buildspec cache we default to empty list which and this condition should always be true
            if self.tags_filter not in tags:
                return True

        if self.type_filter and self.type_filter != schema_type:
            return True

        return False

    def find_buildspecs(self):
        """This method will find buildspecs based on cache content. We skip any
        tests based on executor filter, tag filter or type filter and build
        a table of tests that will be printed using ``print_buildspecs`` method.

        Raises:
            BuildTestError: Raises exception if input buildspec for ``buildtest buildspec find --filter buildspec`` is invalid path or directory or buildspec not found in cache.
        """

        # by default we process all buildspecs
        filtered_buildspecs = self.cache["buildspecs"].keys()

        # handle logic for filtering tests by buildspec file.
        if self.filter:
            if self.filter.get("buildspec"):
                buildspec = resolve_path(self.filter["buildspec"])

                # raise exception if there is an issue resolving path
                if not buildspec:
                    raise BuildTestError(
                        f"Invalid file for filtered buildspec: {self.filter['buildspec']}"
                    )

                # if user specified a directory path we raise an exception
                if is_dir(buildspec):
                    raise BuildTestError(
                        f"{buildspec} must be a file not a directory path."
                    )

                # if user specified buildspec not found in buildspec cache we raise error
                if not buildspec in filtered_buildspecs:
                    raise BuildTestError(
                        f"{buildspec} is not found in buildspec cache. "
                    )

                filtered_buildspecs = [buildspec]

        for buildspecfile in filtered_buildspecs:
            for test in self.cache["buildspecs"][buildspecfile].keys():
                test_recipe = self.cache["buildspecs"][buildspecfile][test]
                schema_type = test_recipe.get("type")
                executor = test_recipe.get("executor")
                # if tags not defined in cache we set to empty list for comparison with tag_filter
                tags = test_recipe.get("tags") or []
                description = test_recipe.get("description")

                # convert tags to string if its a list for printing purposes
                if isinstance(tags, list):
                    tags = " ".join(tags)

                # filters buildspecs by executor, tags, type field. The return
                # is a boolean, if its True we skip the test
                if self._filter_buildspecs(executor, tags, schema_type):
                    continue

                if self.format:
                    for field in self.table.keys():
                        if field == "type":
                            self.table[field].append(schema_type)

                        elif field == "buildspec":
                            self.table[field].append(buildspecfile)
                        elif field == "name":
                            self.table[field].append(test)

                        # tags field must be stored as string for printing purposes
                        elif field == "tags":
                            self.table[field].append(tags)
                        else:
                            self.table[field].append(test_recipe.get(field))

                else:
                    self.table["name"].append(test)
                    self.table["type"].append(schema_type)
                    self.table["executor"].append(executor)
                    self.table["tags"].append(tags)
                    self.table["description"].append(description)

    def get_valid_buildspecs(self):
        """Return a list of valid buildspecs"""
        return self.cache["buildspecs"].keys()

    def get_invalid_buildspecs(self):
        """Return a list of invalid buildspecs"""
        return self.cache["invalids"].keys()

    def get_unique_tags(self):
        """Return a list of unique tags."""
        return self.cache["unique_tags"]

    def get_unique_executors(self):
        """Return a list of unique executors."""
        return self.cache["unique_executors"]

    def get_maintainers(self):
        """Return a list of maintainers."""
        return list(self.cache["maintainers"].keys())

    def get_paths(self):
        """Return a list of search paths"""
        return self.paths

    def tag_breakdown(self):
        """This method will return a breakdown of tags by test names."""
        tag_summary = {}
        for tagname in self.cache["tags"].keys():
            tag_summary[tagname] = self.cache["tags"][tagname].keys()

        return tag_summary

    def executor_breakdown(self):
        """This method will return a dictionary with breakdown of executors by test names."""
        executor_summary = {}
        for executor in self.cache["executor"].keys():
            executor_summary[executor] = self.cache["executor"][executor].keys()

        return executor_summary

    def test_breakdown_by_buildspec(self):
        """This method will return a dictionary with breakdown of buildspecs by test names."""

        buildspec_summary = {}
        for name in self.cache["buildspecs"].keys():
            buildspec_summary[name] = self.cache["buildspecs"][name].keys()

        return buildspec_summary

    def print_buildspecfiles(self, terse=None, header=None, row_count=None):
        """This method implements ``buildtest buildspec find --buildspec`` which reports all buildspec files in cache.

        Args:
            terse (bool, optional): This argument will print output in terse format if ``--terse`` option is specified otherwise will print output in table format
            header (bool, optional): This argument controls whether header will be printed in terse format. If ``--terse`` option is not specified this argument has no effect. This argument holds the value of ``--no-header`` option
            row_count (bool, optional): Print total number of records from the table
        """

        self.terse = terse or self.terse
        self.header = header or self.header
        if self.terse:
            if not self.header:
                console.print("buildspec", style=self.color)

            for buildspec in self.cache["buildspecs"].keys():
                console.print(f"[{self.color}]{buildspec}")

            return

        table = Table(
            Column("Buildspecs", overflow="fold"),
            title="List of Buildspecs",
            header_style="blue",
            row_styles=[self.color],
        )
        for buildspec in self.cache["buildspecs"].keys():
            table.add_row(buildspec)

        if self.pager:
            with console.pager():
                console.print(table)
            return

        if row_count:
            print(table.row_count)
            return

        console.print(table)

    def print_tags(self, row_count=None):
        """This method implements ``buildtest buildspec find --tags`` which
        reports a list of unique tags from all buildspecs in cache file.

        Args:
            row_count (bool, optional): Print total number of records from the table
        """

        # if --terse option specified print list of all tags in machine readable format
        if self.terse:
            if not self.header:
                console.print("tag", style=self.color)

            for tag in self.cache["unique_tags"]:
                console.print(f"[{self.color}]{tag}")

            return

        table = Table(
            Column("Tags", overflow="fold"),
            title="List of Tags",
            header_style="blue",
            row_styles=[self.color],
        )
        for tagname in self.cache["unique_tags"]:
            table.add_row(tagname)

        if self.pager:
            with console.pager():
                console.print(table)
            return

        if row_count:
            print(table.row_count)
            return

        console.print(table)

    def print_executors(self, row_count=None):
        """This method implements ``buildtest buildspec find --executors`` which reports all executors from cache.

        Args:
            row_count (bool, optional): Print total number of records from the table
        """

        if self.terse:
            if not self.header:
                console.print("executor", style=self.color)

            for executor in self.cache["unique_executors"]:
                console.print(f"[{self.color}]{executor}")

            return

        table = Table(
            Column("Executors", overflow="fold"),
            title="List of Executors",
            header_style="blue",
            row_styles=[self.color],
        )
        for executor in self.cache["unique_executors"]:
            table.add_row(executor)

        if self.pager:
            with console.pager():
                console.print(table)
            return

        if row_count:
            print(table.row_count)
            return

        console.print(table)

    def print_by_executors(self):
        """This method prints executors by tests and implements ``buildtest buildspec find --group-by-executor`` command"""

        if self.terse:
            if not self.header:
                console.print("executor|name|description", style=self.color)

            for executor_name in self.cache["executor"].keys():
                for test_name, description in self.cache["executor"][
                    executor_name
                ].items():
                    console.print(
                        f"[{self.color}]{executor_name}|{test_name}|{description}"
                    )
            return

        table = Table(title="Tests by Executors", header_style="blue", show_lines=True)
        table.add_column("Executors", style=self.color, overflow="fold")
        table.add_column("Name", style=self.color, overflow="fold")
        table.add_column("Description", style=self.color, overflow="fold")

        for executor_name in self.cache["executor"].keys():
            for test_name, description in self.cache["executor"][executor_name].items():
                table.add_row(executor_name, test_name, description)

        if self.pager:
            with console.pager():
                console.print(table)
            return

        console.print(table)

    def print_by_tags(self):
        """This method prints tags by tests and implements ``buildtest buildspec find --group-by-tags`` command"""

        if self.terse:
            if not self.header:
                console.print("tags|name|description", style=self.color)

            for tagname in self.cache["tags"].keys():
                for test_name, description in self.cache["tags"][tagname].items():
                    console.print(f"[{self.color}]{tagname}|{test_name}|{description}")
            return

        table = Table(title="Tests by Tags", header_style="blue", show_lines=True)
        table.add_column("Tags", style=self.color, overflow="fold")
        table.add_column("Name", style=self.color, overflow="fold")
        table.add_column("Description", style=self.color, overflow="fold")

        for tagname in self.cache["tags"].keys():
            for test_name, description in self.cache["tags"][tagname].items():
                table.add_row(tagname, test_name, description)

        if self.pager:
            with console.pager():
                console.print(table)
            return

        console.print(table)

    def print_buildspecs(self, terse=None, header=None, quiet=None, row_count=None):
        """Print buildspec table. This method is typically called when running ``buildtest buildspec find`` or options
        with ``--filter`` and ``--format``.

        Args:
            terse (bool, optional): This argument will print output in terse format if ``--terse`` option is specified otherwise will print output in table format
            header (bool, optional): This argument controls whether header will be printed in terse format. If ``--terse`` option is not specified this argument has no effect. This argument holds the value of ``--no-header`` option
            quiet (bool, optional): If this option is set we return immediately and don't anything. This is specified via ``buildtest buildspec find --quiet`` which can be useful when rebuilding cache without displaying output
            row_count (bool, optional): Print total number of records from the table
        """

        # Don't print anything if --quiet is set
        if quiet and self.rebuild:
            return

        self.terse = terse or self.terse
        self.header = header or self.header

        table = Table(
            title=f"Buildspec Cache: {BUILDSPEC_CACHE_FILE}",
            show_lines=True,
            row_styles=[self.color],
            title_justify="center",
            show_edge=False,
        )

        join_list = []

        for key in self.table.keys():
            join_list.append(self.table[key])

            table.add_column(key, overflow="fold", header_style="blue")

        t = [list(i) for i in zip(*join_list)]

        # if --count is specified then reduce list to length of self.count
        if self.count:
            t = t[: self.count]

        for i in t:
            table.add_row(*i)

        if self.terse:
            # print terse output

            if not self.header:
                console.print("|".join(self.table.keys()), style=self.color)

            for row in t:
                if not isinstance(row, list):
                    continue

                # if any entry contains None type we convert to empty string
                row = ["" if item is None else item for item in row]
                join_string = "|".join(row)
                console.print(f"[{self.color}]{join_string}")

            return

        if self.pager:
            with console.pager():
                console.print(table)
            return

        if row_count:
            console.print(table.row_count)
            return

        console.print(table)

    def list_maintainers(self):
        """Return a list of maintainers"""
        return self.cache["maintainers"]

    def print_maintainer(self):
        """This method prints maintainers from buildspec cache file which implements ``buildtest buildspec maintainers --list`` command."""

        if self.terse:
            if not self.header:
                console.print("maintainers", style=self.color)

            for maintainer in self.cache["maintainers"]:
                console.print(f"[{self.color}]{maintainer}")

            return

        table = Table(
            Column("Maintainers", overflow="fold"),
            header_style="blue",
            title_style="red",
            row_styles=[self.color],
        )

        for maintainer in self.cache["maintainers"].keys():
            table.add_row(maintainer)

        if self.pager:
            with console.pager():
                console.print(table)
            return

        console.print(table)

    def print_maintainers_find(self, name):
        """Display a list of buildspec files associated to a given maintainer. This command is used when running
        ``buildtest buildspec maintainers find``

        Args:
            name (str): Name of maintainer specified via ``buildtest buildspec maintainers find <name>``
        """

        maintainers = list(self.cache["maintainers"].keys())
        if name in maintainers:
            for file in self.cache["maintainers"][name]:
                console.print(file)

    def print_maintainers_by_buildspecs(self):
        """This method prints maintainers breakdown by buildspecs. This method implements ``buildtest buildspec maintainers --breakdown``."""

        if self.terse:
            if not self.header:
                console.print("maintainers|buildspec", style=self.color)

            for maintainer, buildspecs in self.cache["maintainers"].items():
                console.print(f"[{self.color}]{maintainer}|{':'.join(buildspecs)}")
            return

        table = Table(
            Column("Maintainers", overflow="fold"),
            Column("Buildspec", overflow="fold"),
            title="Breakdown of buildspecs by maintainers",
            header_style="blue",
            style="cyan",
            title_style="red",
            row_styles=[self.color],
            show_lines=True,
        )

        for maintainer, buildspecs in self.cache["maintainers"].items():
            table.add_row(maintainer, ":".join(buildspecs))

        if self.pager:
            with console.pager():
                console.print(table)
            return

        console.print(table)

    def print_invalid_buildspecs(self, error=None, terse=None, header=None):
        """Print invalid buildspecs from cache file. This method implements command ``buildtest buildspec find invalid``

        Args:
            error (bool, optional): Display error messages for invalid buildspecs. Default is ``False`` where we only print list of invalid buildspecs
            terse (bool, optional): Display output in machine readable format.
            header (bool, optional): Determine whether to print header column in machine readable format.
        """

        terse = terse or self.terse
        header = header or self.header

        if error and terse:
            console.print("The --terse flag can not be used with the --error option")
            sys.exit(1)

        if not self.get_invalid_buildspecs():
            console.print("There are no invalid buildspecs in cache")
            return

        # implementation for machine readable format specified via --terse
        if terse:
            if not header:
                print("buildspec")
            for buildspec in self.cache["invalids"].keys():
                print(buildspec)
            sys.exit(1)

        # if --error is not specified print list of invalid buildspecs in rich table
        if not error:
            table = Table(
                "Buildspec",
                "Exception",
                title="Invalid Buildspecs",
                header_style="blue",
                style="cyan",
                title_style="red",
                row_styles=[self.color],
            )
            for buildspec in self.cache["invalids"].keys():
                table.add_row(buildspec, self.cache["invalids"][buildspec]["exception"])
            console.print(table)
            sys.exit(1)

        # implementation for --error which displays buildspec file followed by error
        for buildspec, value in self.cache["invalids"].items():
            console.rule(buildspec)
            pprint(value)
        sys.exit(1)

    def print_filter_fields(self):
        """This method prints filter fields available for buildspec cache. This
        method implements command ``buildtest buildspec find --helpfilter``
        """

        table = Table(
            title="Filter Field Description", header_style="blue", show_lines=True
        )
        table.add_column("Field", style=self.color, overflow="fold")
        table.add_column("Type", style=self.color, overflow="fold")
        table.add_column("Description", style=self.color, overflow="fold")

        table.add_row("buildspecs", "Filter tests by buildspec", "FILE")
        table.add_row("executor", "Filter by executor name", "STRING")
        table.add_row("tags", "Filter by tag name ", "STRING")
        table.add_row("type", "Filter by schema type ", "STRING")
        console.print(table)

    def print_format_fields(self):
        """This method prints format fields available for buildspec cache. This
        method implements command ``buildtest buildspec find --helpformat``
        """
        table = Table(
            title="Format Field Description", header_style="blue", show_lines=True
        )
        table.add_column("Field", style=self.color, overflow="fold")
        table.add_column("Description", style=self.color, overflow="fold")

        table.add_row("buildspec", "Display name of buildspec file")
        table.add_row("description", "Show description of test")
        table.add_row("executor", "Display 'executor' property in test")
        table.add_row("name", "Display name of test")
        table.add_row("tags", "Display 'tag' property in test ")
        table.add_row("type", "Display 'type' property in test")
        console.print(table)

    def print_raw_filter_fields(self):
        """This method prints the raw filter fields available for buildspec cache. This
        method implements command ``buildtest buildspec find --filterfields``
        """
        for field in self.filter_fields:
            console.print(field, style=self.color)

    def print_raw_format_fields(self):
        """This method prints the raw format fields available for buildspec cache. This
        method implements command ``buildtest buildspec find --formatfields``
        """
        for field in self.format_fields:
            console.print(field, style=self.color)

    def print_paths(self):
        """This method print buildspec paths, this implements command ``buildtest buildspec find --paths``"""
        for path in self.paths:
            console.print(path)


def edit_buildspec_test(test_names, configuration, editor):
    """Open a list of test names in editor mode defined by ``EDITOR`` environment otherwise resort to ``vim``.
    This method will search for buildspec cache and find path to buildspec file corresponding to test name and open
    file in editor. If multiple test are specified via ``buildtest buildspec edit-test`` then each file will be open and
    upon closing file, the next file will be open for edit until all files are written.

    Args:
        test_names (list): A list of test names to open in editor
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        editor (str): Path to editor to use when opening file
    """
    cache = BuildspecCache(configuration=configuration)

    for name in test_names:
        if name not in cache.get_names():
            console.print(f"[red]Unable to find test {name} in cache")
            continue

        buildspec = cache.lookup_buildspec_by_name(name)

        # only used for regression testing to ensure test is not stuck for closing file
        if not editor:
            editor = "echo"  # Doesnt call the editor.

        subprocess.call([editor, buildspec])
        print(f"Writing file: {buildspec}")

        be = BuildExecutor(configuration)
        try:
            BuildspecParser(buildspec, be)
        except ValidationError:
            console.print(f"[red]{buildspec} is invalid")
            continue
        console.print(f"[green]{buildspec} is valid")


def edit_buildspec_file(buildspecs, configuration, editor):
    """Open buildspec in editor and validate buildspec with parser. This method is invoked by command ``buildtest buildspec edit-file``.

    Args:
        buildspec (str): Path to buildspec file to edit
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        editor (str): Path to editor to use when opening file
    """
    for file in buildspecs:
        buildspec = resolve_path(file, exist=False)
        if is_dir(buildspec):
            console.print(
                f"buildspec: {buildspec} is a directory, please specify a file type"
            )
            continue
        # only used for regression testing to ensure test is not stuck for closing file
        if not editor:
            editor = "cat"
        subprocess.call([editor, buildspec])

        print(f"Writing file: {buildspec}")

        be = BuildExecutor(configuration)
        try:
            BuildspecParser(buildspec, be)
        except ValidationError:
            console.print(f"[red]{buildspec} is invalid")
            continue
        console.print(f"[green]{buildspec} is valid")


def show_buildspecs(test_names, configuration, theme=None):
    """This is the entry point for ``buildtest buildspec show`` command which will print content of
    buildspec based on name of test.

    Args:
        test_names (list): List of test names to show content of file
        configuration (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class
        theme (str, optional): Color theme to choose. This is the Pygments style (https://pygments.org/docs/styles/#getting-a-list-of-available-styles) which is specified by ``--theme`` option
    """
    cache = BuildspecCache(configuration=configuration)
    theme = theme or "monokai"

    error_msg = []
    visited = set()
    for name in test_names:
        if name not in cache.get_names():
            error_msg.append(f"[red]Unable to find test {name} in cache")
            continue

        buildspec = cache.lookup_buildspec_by_name(name)
        if buildspec not in visited:
            visited.add(buildspec)

            console.rule(buildspec)
            with open(buildspec) as fd:
                syntax = Syntax(fd.read(), "yaml", theme=theme)
            console.print(syntax)

    if error_msg:
        for line in error_msg:
            console.print(line)


def show_failed_buildspecs(
    configuration, test_names=None, report_file=None, theme=None
):
    """This is the entry point for ``buildtest buildspec show-fail`` command which will print content of
    buildspec on name of all failed tests if a list of test names are not speficied

    Args:
        configuration (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class
        test_names (list, optional): List of test names to show content of file
        report_file (str, optional): Full path to report file to read
        theme (str, optional): Color theme to choose. This is the Pygments style (https://pygments.org/docs/styles/#getting-a-list-of-available-styles) which is specified by ``--theme`` option
    """
    results = Report(report_file=report_file)
    all_failed_tests = results.get_test_by_state(state="FAIL")

    if test_names:
        for test_name in test_names:
            if test_name not in all_failed_tests:
                console.print(
                    f"[red]{test_name} is not in one of the following failed test: {all_failed_tests}"
                )
        failed_tests = test_names
    else:
        failed_tests = all_failed_tests
    show_buildspecs(failed_tests, configuration, theme)


def buildspec_validate(
    configuration, buildspecs=None, excluded_buildspecs=None, tags=None, executors=None
):
    """Entry point for ``buildtest buildspec validate``. This method is responsible for discovering buildspec
    with same options used for building buildspecs that includes ``--buildspec``, ``--exclude``, ``--tag``, and
    ``--executor``. Upon discovery we pass each buildspec to ``BuildspecParser`` class to validate buildspec and
    report any errors during validation which is raised as exceptions.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class which is the loaded buildtest configuration used for validating the buildspecs.
        buildspecs (list, optional): List of paths to buildspec file which can be a file or directory. This option is specified via ``buildtest buildspec validate --buildspec``
        excluded_buildspecs (list, optional): List of excluded buildspecs which can be a file or directory. This option is specified via ``buildtest buildspec validate --exclude``
        tags (list, optional): List of tag names to search for buildspec to validate. This option is specified via ``buildtest buildspec validate --tag``
        executors (list, optional): List of executor names to search for buildspecs to validate. This option is specified via ``buildtest buildspec validate --executor``
    """

    buildspecs_dict = discover_buildspecs(
        buildspecs=buildspecs,
        exclude_buildspecs=excluded_buildspecs,
        tags=tags,
        executors=executors,
    )
    detected_buildspecs = buildspecs_dict["detected"]

    buildexecutor = BuildExecutor(site_config=configuration)

    # counter to keep track of number of exceptions raised during buildspec validation
    exception_counter = 0
    for buildspec in detected_buildspecs:
        try:
            BuildspecParser(
                buildspec=buildspec, buildexecutor=buildexecutor, executor_match=True
            )
        except (
            BuildspecError,
            ExecutorError,
            ValidationError,
        ) as err:
            exception_counter += 1
            console.rule(buildspec)
            if isinstance(err, BuildspecError):
                print(err.get_exception())
            else:
                print(err)
            print("\n")
        else:
            console.print(f"[green]buildspec: {buildspec} is valid")

    if exception_counter > 0:
        console.print(f"[red]{exception_counter} buildspecs failed to validate")
        sys.exit(1)

    console.print("[green]All buildspecs passed validation!!!")


def summarize_buildspec_cache(pager, configuration, color=None):
    """entry point for ``buildtest buildspec summary``

    Args:
        configuration (buildtest.config.SiteConfiguration): instance of type SiteConfiguration
        pager (bool): Boolean control output of summary with paging
        color (str, optional): An instance of str, color that the summary should be printed in
    """
    if pager:
        with console.pager():
            summary_print(configuration)
            return
    summary_print(configuration, color)


def summary_print(configuration, color=None):
    """Prints summary of buildspec cache which is run via command ``buildtest buildspec summary``

    Args:
        configuration (buildtest.config.SiteConfiguration): instance of type SiteConfiguration
        color (str, optional): An instance of str, color that the summary should be printed in
    """
    cache = BuildspecCache(configuration=configuration)
    consoleColor = checkColor(color)
    msg = f"""
    [yellow]Reading Buildspec Cache File:[/yellow]  [cyan]{BUILDSPEC_CACHE_FILE}[/cyan] 
    [yellow]Total Valid Buildspecs:[/yellow]        [cyan]{len(cache.get_valid_buildspecs())}[/cyan] 
    [yellow]Total Invalid Buildspecs:[/yellow]      [cyan]{len(cache.get_invalid_buildspecs())}[/cyan] 
    [yellow]Total Unique Tags:[/yellow]             [cyan]{len(cache.get_unique_tags())}[/cyan] 
    [yellow]Total Maintainers:[/yellow]             [cyan]{len(cache.get_maintainers())}[/cyan] 
"""

    console.print(Panel.fit(msg))
    layout = Layout()
    layout.split_column(Layout(name="top"), Layout(name="bottom"))

    layout["top"].split_row(
        Layout(name="top-left"), Layout(name="top-center"), Layout(name="top-right")
    )
    layout["top"].ratio = 2

    # layout['bottom'].split_row(Layout(name="bottom-left"))
    ################ Tag Breakdown #################
    tag_table = Table(title="Tag Breakdown", header_style="blue")
    # tag_table.overflow="fold"

    tag_table.add_column("tag", style=consoleColor, overflow="fold")
    tag_table.add_column("total tests", style=consoleColor, overflow="fold")

    tag_summary = cache.tag_breakdown()
    for tag, tag_count in tag_summary.items():
        tag_table.add_row(tag, str(len(tag_count)))

    ################ Executor Breakdown #################
    executor_table = Table(title="Executor Breakdown")
    executor_table.add_column(
        "executor", style=consoleColor, header_style="blue", overflow="fold"
    )
    executor_table.add_column(
        "total tests", style=consoleColor, header_style="blue", overflow="fold"
    )

    executor_summary = cache.executor_breakdown()
    for executor, executor_count in executor_summary.items():
        executor_table.add_row(executor, str(len(executor_count)))

    ################ Maintainers #################
    maintainer_table = Table(title="Maintainers Breakdown")
    maintainer_table.add_column(
        "maintainers", style=consoleColor, header_style="blue", overflow="fold"
    )
    maintainer_table.add_column(
        "total buildspecs", style=consoleColor, header_style="blue", overflow="fold"
    )

    for maintainer in cache.list_maintainers():
        num_buildspecs = len(cache.cache["maintainers"][maintainer])
        maintainer_table.add_row(maintainer, str(num_buildspecs))

    buildspec_table = Table(
        title="Test Breakdown by buildspec", show_lines=True, header_style="blue"
    )
    buildspec_table.add_column("Tests", style=consoleColor, overflow="fold")
    buildspec_table.add_column("Total", style=consoleColor, overflow="fold")
    buildspec_table.add_column("Buildspec", style=consoleColor, overflow="fold")

    ################ Test Breakdown by Buildspec #################
    buildspec_summary = cache.test_breakdown_by_buildspec()
    for buildspec, tests in buildspec_summary.items():
        buildspec_table.add_row("\n".join(tests), str(len(tests)), buildspec)

    invalid_buildspecs_table = Table(
        title="Invalid Buildspecs", show_lines=True, header_style="blue"
    )
    invalid_buildspecs_table.add_column(
        "Buildspecs", style=consoleColor, overflow="fold"
    )

    for buildspec in cache.get_invalid_buildspecs():
        invalid_buildspecs_table.add_row(buildspec)

    layout["top-left"].update(tag_table)
    layout["top-center"].update(executor_table)
    layout["top-right"].update(maintainer_table)
    layout["bottom"].update(invalid_buildspecs_table)

    console.print(layout)
    console.print(buildspec_table)


def buildspec_maintainers(
    configuration,
    list_maintainers=None,
    breakdown=None,
    terse=None,
    header=None,
    color=None,
    name=None,
):
    """Entry point for ``buildtest buildspec maintainers`` command.

    Args:
        configuration (buildtest.config.SiteConfiguration): instance of type SiteConfiguration
        list_maintainers (bool, optional): List all maintainers
        terse (bool, optional): Print in terse mode
        header (bool, optional): If True disable printing of headers
        color (bool, optional): Print output of table with selected color
        name (str, optional): List all buildspecs corresponding to maintainer name. This command is specified via ``buildtest buildspec maintainers find <name>``
    """

    cache = BuildspecCache(
        configuration=configuration, terse=terse, header=header, color=color
    )

    if list_maintainers:
        cache.print_maintainer()

    if breakdown:
        cache.print_maintainers_by_buildspecs()

    if name:
        cache.print_maintainers_find(name=name)


def buildspec_find(args, configuration):
    """Entry point for ``buildtest buildspec find`` command

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
        configuration (buildtest.config.SiteConfiguration): instance of type SiteConfiguration
    """

    cache = BuildspecCache(
        rebuild=args.rebuild,
        filterfields=args.filter,
        formatfields=args.format,
        roots=args.root,
        configuration=configuration,
        header=args.no_header,
        terse=args.terse,
        pager=args.pager,
        color=args.color,
        count=args.count,
    )

    if args.buildspec_find_subcommand == "invalid":
        cache.print_invalid_buildspecs(error=args.error)
        return

    # buildtest buildspec find --tags
    if args.tags:
        cache.print_tags(row_count=args.row_count)
        return

    # buildtest buildspec find --buildspec
    if args.buildspec:
        cache.print_buildspecfiles(row_count=args.row_count)
        return

    # buildtest buildspec find --paths
    if args.paths:
        cache.print_paths()
        return

    # buildtest buildspec find --executors
    if args.executors:
        cache.print_executors(row_count=args.row_count)
        return

    # buildtest buildspec find --group-by-executors
    if args.group_by_executor:
        cache.print_by_executors()
        return

    # buildtest buildspec find --group-by-tags
    if args.group_by_tags:
        cache.print_by_tags()
        return

    # buildtest buildspec find --helpfilter
    if args.helpfilter:
        cache.print_filter_fields()
        return

    # buildtest buildspec find --helpformat
    if args.helpformat:
        cache.print_format_fields()
        return

    # buildtest buildspec find --filterfields
    if args.filterfields:
        cache.print_raw_filter_fields()
        return

    # buildtest buildspec find --formatfields
    if args.formatfields:
        cache.print_raw_format_fields()
        return

    cache.print_buildspecs(quiet=args.quiet, row_count=args.row_count)
