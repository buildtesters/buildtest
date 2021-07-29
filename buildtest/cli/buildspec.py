import json
import logging
import os

from buildtest.buildsystem.parser import BuildspecParser
from buildtest.cli.build import discover_buildspecs
from buildtest.defaults import (
    BUILDSPEC_CACHE_FILE,
    BUILDSPEC_DEFAULT_PATH,
    BUILDTEST_BUILDSPEC_DIR,
)
from buildtest.exceptions import BuildspecError, BuildTestError
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.file import (
    create_dir,
    is_dir,
    is_file,
    load_json,
    resolve_path,
    walk_tree,
)
from jsonschema.exceptions import ValidationError
from tabulate import tabulate
from termcolor import colored

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
    ):
        """The initializer method for BuildspecCache class is responsible for
        loading and finding buildspecs into buildspec cache. This method is called
        when using ``buildtest buildspec find`` command.

        :param rebuild: rebuild the buildspec cache by validating all buildspecs. The --rebuild is passed to this argument
        :type rebuild: bool, optional
        :param filterfields:  The --filter option contains list of key value pairs for filtering buildspecs
        :type filterfields: str, optional
        :param formatfields: The --format option contains list of key value pairs for formating buildspecs
        :type formatfields: str, optional
        :param roots:  List of directories to search for buildspecs. This argument contains value of --roots
        :type roots: list, optional
        :param header: Option to control whether header are printed in terse output. This argument contains value of --no-header
        :type header: bool, optional
        """

        if not is_dir(BUILDTEST_BUILDSPEC_DIR):
            create_dir(BUILDTEST_BUILDSPEC_DIR)

        self.configuration = configuration
        self.filter = filterfields
        self.format = formatfields
        self.header = header
        # if --root is not specified we set to empty list instead of None
        self.roots = roots or []

        # list of buildspec directories to search for .yml files
        self.paths = []

        # stores invalid buildspecs and the error messages
        self.invalid_buildspecs = {}

        self.terse = terse

        self.rebuild = rebuild
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
        In addition, we add the default buildspec path where we find tutorials
        and general tests.
        """

        buildspec_paths = self.configuration.target_config.get("buildspec_roots") or []

        if buildspec_paths:
            self.roots += buildspec_paths

        # only load default buildspecs if 'load_default_buildspecs' set to True
        if self.configuration.target_config.get("load_default_buildspecs"):
            self.paths += BUILDSPEC_DEFAULT_PATH

        # for every root buildspec defined in configuration or via --root option,
        # we resolve path and if path exist add to self.paths. The path must be a
        # directory. If its file, we ignore it
        if self.roots:

            for root in self.roots:
                path = resolve_path(root, exist=False)
                if not os.path.exists(path):
                    print(f"Path: {path} does not exist!")

                if is_file(path):
                    print(f"Path: {path} must be a directory not a file")

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
        """Given a list of buildspec files, validate each buildspec using BuildspecParser
        and return a list of valid buildspecs. Any invalid buildspecs are added to
        separate list
        """
        valid_buildspecs = []
        self.count = 0

        buildexecutor = BuildExecutor(self.configuration)

        for buildspec in buildspecs:
            self.count += 1

            try:
                parse = BuildspecParser(buildspec, buildexecutor)
            # any buildspec that raises SystemExit or ValidationError imply
            # buildspec is not valid, we add this to invalid list along with
            # error message and skip to next buildspec
            except (BuildTestError, BuildspecError, ValidationError) as err:
                self.invalid_buildspecs[buildspec] = err
                continue

            valid_buildspecs.append(parse)

            # if self.count % 5 == 0:
            #    print(f"Validated {self.count}/{len(buildspecs)} buildspecs")

        # print(f"Validated {self.count}/{len(buildspecs)} buildspecs")

        """
        # print invalid buildspecs if found
        if len(self.invalid_buildspecs) > 0:
            print("\n")
            print("Invalid buildspecs")
            print("{:_<80}".format(""))
            for file in self.invalid_buildspecs:
                print(file)

            print(f"Found {len(self.invalid_buildspecs)} invalid buildspecs")
            print("{:_<80}".format(""))

        print("\n")
        print(f"Adding {len(valid_buildspecs)} buildspec files to cache")
        """

        return valid_buildspecs

    def build_cache(self):
        """This method will rebuild the buildspec cache file by recursively searching
        all .yml files specified by input argument ``paths`` which is a list of directory
        roots. The buildspecs are validated and cache file is updated"

        :return: Rebuild cache file
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
        """
        print("Discovered Buildspecs")
        print("{:_<80}".format(""))
        for file in buildspecs:
            print(file)

        print(f"Found {len(buildspecs)} buildspecs ")
        print("{:_<80}".format(""))
        print("\n")
        """

        self.update_cache["invalids"] = {}

        # validate each buildspec and return a list of valid buildspec parsers that
        # is an instance of BuildspecParser class
        parsers = self._validate_buildspecs(buildspecs)

        if self.invalid_buildspecs:
            for buildspec in self.invalid_buildspecs.keys():
                self.update_cache["invalids"][buildspec] = str(
                    self.invalid_buildspecs[buildspec]
                )

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
        count = 0

        for file in self.update_cache["buildspecs"].keys():
            count += len(self.update_cache["buildspecs"][file].keys())

        # print(f"There are {count} tests in buildspec cache")
        self._write_buildspec_cache()

    def _check_filter_fields(self):
        """This method checks filter fields are valid. The filter fields are specified
        as ``buildtest buildspec find --filter <KEY1>=<VAL1>,<KEY2>=<VAL2>,...
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

        :param executor:  'executor; field from buildspec recipe
        :type executor: str, required
        :param tags: 'tags' field from buildspec recipe
        :type tags: str or list, required
        :param schema_type: 'type' field from buildspec recipe
        :type schema_type: str, required
        :return: boolean to determine if we need to skip buildspec
        :rtype: bool
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

                # filters buildspecs by executor, tags, type field. The return
                # is a boolean, if its True we skip the test
                if self._filter_buildspecs(executor, tags, schema_type):
                    continue

                # convert tags to string if its a list for printing purposes
                if isinstance(tags, list):
                    tags = " ".join(tags)

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

    def print_buildspecfiles(self, terse=None, header=None):
        """This method implements ``buildtest buildspec find --buildspec``
        which reports all buildspec files in cache.

        :param terse: This argument controls output of ``buildtest buildspec find --buildspec`` which is a boolean. If its ``True`` we print output in raw format otherwise we print in table format
        :type terse: bool
        """

        self.terse = terse or self.terse
        self.header = header or self.header
        if self.terse:

            if not self.header:
                print("buildspec")

            for buildspec in self.cache["buildspecs"].keys():
                print(buildspec)

            return

        table = {"buildspecs": self.cache["buildspecs"].keys()}
        if os.getenv("BUILDTEST_COLOR") == "True":
            print(
                tabulate(
                    table,
                    headers=[
                        colored(field, "blue", attrs=["bold"]) for field in table.keys()
                    ],
                    tablefmt="grid",
                )
            )
            return

        print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    def print_tags(self, terse=None, header=None):
        """This method implements ``buildtest buildspec find --tags`` which
        reports a list of unique tags from all buildspecs in cache file.

        :param terse: This argument controls output of ``buildtest buildspec find --tags`` which is a boolean. If its ``True`` we print output in raw format otherwise we print in table format
        :type terse: bool
        """

        self.terse = terse or self.terse
        self.header = header or self.header

        # if --terse option specified print list of all tags in machine readable format
        if self.terse:

            if not self.header:
                print("tag")

            for tag in self.cache["unique_tags"]:
                print(tag)

            return

        table = {"Tags": self.cache["unique_tags"]}
        headers = ["Tags"]
        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = [colored("Tags", "blue", attrs=["bold"])]

        print(tabulate(table, headers=headers, tablefmt="grid"))

    def print_executors(self, terse=None, header=None):
        """This method implements ``buildtest buildspec find --executors``
        which reports all executors from cache.

        :param terse: This argument controls output of ``buildtest buildspec find --executor`` which is a boolean. If its ``True`` we print output in raw format otherwise we print in table format
        :type terse: bool
        """

        self.terse = terse or self.terse
        self.header = header or self.header

        if self.terse:

            if not self.header:
                print("executor")

            for executor in self.cache["unique_executors"]:
                print(executor)

            return

        table = {"executors": self.cache["unique_executors"]}
        headers = ["executors"]
        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = [colored("executors", "blue", attrs=["bold"])]

        print(tabulate(table, headers=headers, tablefmt="grid"))

    def print_by_executors(self, terse=None, header=None):
        """This method prints executors by tests and implements
        ``buildtest buildspec find --group-by-executor`` command

        :param terse: Print output in machine readable format
        :type terse: bool
        """

        table = {"executor": [], "name": []}
        headers = table.keys()

        for executor_name in self.cache["executor"].keys():
            for test_name, description in self.cache["executor"][executor_name].items():
                table["executor"].append(executor_name)
                table["name"].append(test_name)

        self.terse = terse or self.terse
        self.header = header or self.header

        if self.terse:

            if not self.header:
                print("executor|name")

            for executor, name in zip(table["executor"], table["name"]):
                print(f"{executor}|{name}")
            return

        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = [colored(field, "blue", attrs=["bold"]) for field in table.keys()]

        print(tabulate(table, headers=headers, tablefmt="grid"))

    def print_by_tags(self, terse=None, header=None):
        """This method prints tags by tests and implements
        ``buildtest buildspec find --group-by-tags`` command

        :param terse: Print output in machine readable format
        :type terse: bool
        """

        table = {"tags": [], "name": []}
        headers = table.keys()

        for tagname in self.cache["tags"].keys():
            for test_name, description in self.cache["tags"][tagname].items():
                table["tags"].append(tagname)
                table["name"].append(test_name)

        self.terse = terse or self.terse
        self.header = header or self.header

        if self.terse:

            if not self.header:
                print("tags|name")

            for tags, name in zip(table["tags"], table["name"]):
                print(f"{tags}|{name}")
            return

        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = [colored(field, "blue", attrs=["bold"]) for field in table.keys()]

        print(tabulate(table, headers=headers, tablefmt="grid"))

    def print_buildspecs(self, terse=None, header=None):
        """Print buildspec table"""

        self.terse = terse or self.terse
        self.header = header or self.header

        # print terse output
        if self.terse:

            if not self.header:
                print("|".join(self.table.keys()))

            join_list = []

            for key in self.table.keys():

                join_list.append(self.table[key])

            t = [list(i) for i in zip(*join_list)]

            for i in t:
                print("|".join(i))

            return

        if os.getenv("BUILDTEST_COLOR") != "True":
            print(tabulate(self.table, headers=self.table.keys(), tablefmt="grid"))
            return

        print(
            tabulate(
                self.table,
                headers=[
                    colored(field, "blue", attrs=["bold"])
                    for field in self.table.keys()
                ],
                tablefmt="grid",
            )
        )

    def print_maintainer(self, terse=None, header=None):
        """This method prints maintainers from buildspec cache file which implements
        ``buildtest buildspec find --maintainers`` command.

        :param terse: This argument controls output of ``buildtest buildspec find --maintainers`` which is a boolean. If its ``True`` we print output in raw format otherwise we print in table format
        :type terse: bool

        """

        self.terse = terse or self.terse
        self.header = header or self.header

        if self.terse:

            if not self.header:
                print("maintainers")

            for maintainer in self.cache["maintainers"]:
                print(maintainer)

            return

        table = {"maintainers": []}
        headers = table.keys()

        for maintainer in self.cache["maintainers"].keys():
            table["maintainers"].append(maintainer)

        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = [colored(field, "blue", attrs=["bold"]) for field in table.keys()]

        print(tabulate(table, headers=headers, tablefmt="grid"))

    def print_maintainers_by_buildspecs(self, terse=None, header=None):
        """This method prints maintainers breakdown by buildspecs. This method
        implements ``buildtest buildspec find --maintainers-by-buildspecs``

        :param terse: Print output in machine readable format
        :type terse: bool
        """

        table = {"maintainers": [], "buildspec": []}
        headers = table.keys()
        for maintainer, buildspec in self.cache["maintainers"].items():
            table["maintainers"].append(maintainer)
            table["buildspec"].append(buildspec)

        self.terse = terse or self.terse
        self.header = header or self.header

        if self.terse:

            self.header = header or self.header
            if not self.header:
                print("maintainers|buildspec")

            for maintainer, buildspecs in zip(table["maintainers"], table["buildspec"]):

                print(f"{maintainer}|{':'.join(buildspecs)}")
            return

        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = [colored(field, "blue", attrs=["bold"]) for field in table.keys()]

        print(tabulate(table, headers=headers, tablefmt="grid"))

    def print_invalid_buildspecs(self, error=None):
        """Print invalid buildspecs from cache file. This method implements command ``buildtest buildspec find invalids``
        :param error: controls whether error message for each buildspec is printed. If set to `False`, the error messages will be omitted
        :type error: bool, optional
        """

        if not error:
            table = {"buildspecs": []}
            for key in self.cache["invalids"].keys():
                table["buildspecs"].append(key)

            headers = table.keys()

            if os.getenv("BUILDTEST_COLOR") == "True":
                headers = [
                    colored(field, "blue", attrs=["bold"]) for field in table.keys()
                ]

            print(tabulate(table, headers=headers, tablefmt="grid"))
            return

        for key in self.cache["invalids"].keys():
            print(key)
            print("{:_<80}".format(""))
            print(self.cache["invalids"][key])
            print("{:_<80}".format(""))
            print("\n\n")

    @staticmethod
    def print_filter_fields():
        """This method prints filter fields available for buildspec cache. This
        method implements command ``buildtest buildspec find --helpfilter``
        """

        filter_field_table = [
            ["buildspec", "Filter tests by buildspec", "FILE"],
            ["executor", "Filter by executor name", "STRING"],
            ["tags", "Filter by tag name ", "STRING"],
            ["type", "Filter by schema type ", "STRING"],
        ]

        if os.getenv("BUILDTEST_COLOR") != "True":
            print(
                tabulate(
                    filter_field_table,
                    headers=["Field", "Description", "Type"],
                    tablefmt="simple",
                )
            )
            return

        table = []

        for row in filter_field_table:
            table.append(
                [
                    colored(row[0], "green", attrs=["bold"]),
                    colored(row[1], "red"),
                    colored(row[2], "cyan"),
                ]
            )

        print(
            tabulate(
                table,
                headers=[
                    colored(field, "blue", attrs=["bold"])
                    for field in ["Field", "Description", "Type"]
                ],
                tablefmt="simple",
            )
        )

    @staticmethod
    def print_format_fields():
        """This method prints format fields available for buildspec cache. This
        method implements command ``buildtest buildspec find --helpformat``
        """
        headers = ["Field", "Description"]
        format_fields = [
            ["buildspec", "Display name of buildspec file"],
            ["description", "Show description of test"],
            ["executor", "Display 'executor' property in test"],
            ["name", "Display name of test"],
            ["tags", "Display 'tag' property in test "],
            ["type", "Display 'type' property in test"],
        ]

        if os.getenv("BUILDTEST_COLOR") != "True":
            print(tabulate(format_fields, headers=headers, tablefmt="simple"))
            return

        table = []
        for row in format_fields:
            table.append(
                [colored(row[0], "green", attrs=["bold"]), colored(row[1], "red")]
            )

        print(
            tabulate(
                table,
                headers=[colored(field, "blue", attrs=["bold"]) for field in headers],
                tablefmt="simple",
            )
        )

    def print_paths(self):
        """This method print buildspec paths, this implements command
        ``buildtest buildspec find --paths``
        """

        for path in self.paths:
            print(path)


def buildspec_validate(
    configuration, buildspecs=None, excluded_buildspecs=None, tags=None, executors=None
):
    """Entry point for ``buildtest buildspec validate``. This method is responsible for discovering buildspec
    with same options used for building buildspecs that includes ``--buildspec``, ``--exclude``, ``--tag``, and
    ``--executor``. Upon discovery we pass each buildspec to ``BuildspecParser`` class to validate buildspec and
    report any errors during validation which is raised as exceptions.

    :param configuration: An instance of SiteConfiguration class which is the loaded buildtest configuration used for validating the buildspecs.
    :type configuration: instance of SiteConfiguration
    :param buildspecs: List of paths to buildspec file which can be a file or directory
    :type buildspecs: List, optional
    :param excluded_buildspecs:
    :type excluded_buildspecs: List, optional
    :param tags: List of tag names to search for buildspec
    :type excluded_buildspecs: List, optional
    :param executors: List of executor names to search for buildspecs
    :type executors: List, optional
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
            BuildspecParser(buildspec=buildspec, buildexecutor=buildexecutor)
        except (BuildTestError, BuildspecError, ValidationError) as err:
            exception_counter += 1
            print("\nfile: ", buildspec)
            print("{:_<80}".format(""))
            print(err)
            print("\n")

        finally:
            print(f"Processing buildspec: {buildspec}")

    if exception_counter > 0:
        print(f"There were {exception_counter} buildspecs that failed validation")
    else:
        print("All buildspecs passed validation!!!")


def summarize_buildspec_cache(configuration):

    cache = BuildspecCache(configuration=configuration)
    print("Reading Buildspec Cache File:", BUILDSPEC_CACHE_FILE)
    print("\n")
    print("Search Paths:", cache.get_paths())
    print("Total Valid Buildspecs: ", len(cache.get_valid_buildspecs()))
    print("Total Invalid Buildspecs: ", len(cache.get_invalid_buildspecs()))
    print("Total Unique Tags: ", len(cache.get_unique_tags()))
    print("Total Unique Executors: ", len(cache.get_unique_executors()))
    print("Total Maintainers:", len(cache.get_maintainers()))
    print("Unique Tags: ", cache.get_unique_tags())
    print("Unique Executors: ", cache.get_unique_executors())
    print("Unique Maintainers:", cache.get_maintainers())

    print("\n\nTag Breakdowns")
    print("{:_<30}".format(""))
    print("\n")

    table = {"name": [], "total": []}
    tag_summary = cache.tag_breakdown()
    for key in tag_summary.keys():
        table["name"].append(key)
        table["total"].append(len(tag_summary[key]))

    print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    print("\n\nExecutor Breakdowns")
    print("{:_<30}".format(""))
    print("\n")

    table = {"name": [], "total": []}
    executor_summary = cache.executor_breakdown()
    for key in executor_summary.keys():
        table["name"].append(key)
        table["total"].append(len(executor_summary[key]))

    print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    print("\n\nTest Breakdown by buildspecs")
    print("{:_<30}".format(""))
    print("\n")

    table = {"buildspec": [], "total": []}
    buildspec_summary = cache.test_breakdown_by_buildspec()
    for key in buildspec_summary.keys():
        table["buildspec"].append(key)
        table["total"].append(len(buildspec_summary[key]))

    print(tabulate(table, headers=table.keys(), tablefmt="grid"))


def buildspec_find(args, configuration):
    """Entry point for ``buildtest buildspec find`` command"""

    cache = BuildspecCache(
        rebuild=args.rebuild,
        filterfields=args.filter,
        formatfields=args.format,
        roots=args.root,
        configuration=configuration,
        header=args.no_header,
        terse=args.terse,
    )

    if args.buildspec_find_subcommand == "invalid":
        cache.print_invalid_buildspecs(error=args.error)
        return

    # buildtest buildspec find --tags
    if args.tags:
        cache.print_tags()
        return

    # buildtest buildspec find --buildspec
    if args.buildspec:
        cache.print_buildspecfiles()
        return

    # buildtest buildspec find --paths
    if args.paths:
        cache.print_paths()
        return

    # buildtest buildspec find --executors
    if args.executors:
        cache.print_executors()
        return

    # buildtest buildspec find --group-by-executors
    if args.group_by_executor:
        cache.print_by_executors()
        return

    # buildtest buildspec find --group-by-tags
    if args.group_by_tags:
        cache.print_by_tags()
        return

    # buildtest buildspec find --maintainers
    if args.maintainers:
        cache.print_maintainer()
        return

    #  buildtest buildspec find --maintainers-by-buildspecs
    if args.maintainers_by_buildspecs:
        cache.print_maintainers_by_buildspecs()
        return

    # buildtest buildspec find --helpfilter
    if args.helpfilter:
        cache.print_filter_fields()
        return

    # buildtest buildspec find --helpformat
    if args.helpformat:
        cache.print_format_fields()
        return

    cache.print_buildspecs()
