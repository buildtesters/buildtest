import json
import logging
import os
import sys

from tabulate import tabulate
from jsonschema.exceptions import ValidationError
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import load_settings
from buildtest.defaults import BUILDSPEC_CACHE_FILE, BUILDSPEC_DEFAULT_PATH
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_file, walk_tree, resolve_path

logger = logging.getLogger(__name__)


class BuildspecCache:

    table = {}
    filter_fields = ["type", "executor", "tags"]
    default_format_fields = ["name", "type", "executor", "tags", "description"]
    format_fields = default_format_fields + ["buildspecs"]

    def __init__(self, rebuild, filter, format, roots):
        self.filter = filter
        self.format = format
        self.roots = roots
        self.paths = []
        self.rebuild = rebuild
        self.cache = {}

        self.load_paths()
        self.build()

        self.check_filter_fields()
        self.check_format_fields()
        self.find_buildspecs()

    def get_paths(self):
        """Returns a list of root buildspec roots"""

        return self.paths

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

        config_opts = load_settings()
        buildspec_paths = config_opts.get("buildspec_roots") or []

        # self.file_roots will store files specified by --roots option
        self.file_roots = []

        if self.roots:
            buildspec_paths += self.roots

        # only load default buildspecs if 'load_default_buildspecs' set to True
        if config_opts.get("load_default_buildspecs"):
            self.paths += BUILDSPEC_DEFAULT_PATH

        # if buildspec_roots defined in configuration, resolve path and if path exist add
        # to list of paths to search for buildspecs
        if buildspec_paths:

            for root in buildspec_paths:
                path = resolve_path(root, exist=False)
                if not os.path.exists(path):
                    print(f"Path: {path} does not exist!")

                if is_file(path):
                    self.file_roots.append(path)

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
                print(f"Clearing cache file: {BUILDSPEC_CACHE_FILE}")
            except OSError as msg:
                raise BuildTestError(msg)

        # if cache file is not found, then we will build cache by searching
        # all buildspecs paths and traverse directory to find all .yml files

        if not is_file(BUILDSPEC_CACHE_FILE):
            self.build_cache()

        with open(BUILDSPEC_CACHE_FILE, "r") as fd:
            self.cache = json.loads(fd.read())

    def _discover_buildspecs(self):
        """This method retrieves buildspecs based on ``self.paths`` which is a
           list of directory paths to search. If --root is specified for specifying
           buildspec roots we process each argument, if its a file we add file,
           if its a directory we recursively find all .yml files
        """

        buildspecs = []
        # add all buildspecs from each repo. walk_tree will find all .yml files
        # recursively and add them to list
        for path in self.paths:
            buildspec = walk_tree(path, ".yml")
            buildspecs += buildspec

        # if --root specifies a file we add buildspecs only if they end in .yml extension
        if self.file_roots:
            for filename in self.file_roots:
                if filename.endswith(".yml"):
                    buildspecs += filename
                else:
                    print(
                        f"File: {filename} does not end in .yml extension, skipping file"
                    )

        print(f"\nBuildspec Paths: {self.paths} \n")

        # remove any files in .buildtest directory of root of repo.
        buildspecs = [
            buildspec
            for buildspec in buildspecs
            if os.path.basename(os.path.dirname(buildspec)) != ".buildtest"
        ]
        return buildspecs

    def _write_buildspec_cache(self):
        """This method is responsible for writing buildspec cache to file"""

        with open(BUILDSPEC_CACHE_FILE, "w") as fd:
            json.dump(self.update_cache, fd, indent=2)

        print(f"\nDetected {len(self.invalid_buildspecs)} invalid buildspecs \n")

        # write invalid buildspecs to file if any found
        if self.invalid_buildspecs:
            buildspec_error_file = os.path.join(
                os.path.dirname(BUILDSPEC_CACHE_FILE), "buildspec.error"
            )

            with open(buildspec_error_file, "w") as fd:
                for file, msg in self.invalid_buildspecs.items():
                    fd.write(f"buildspec:{file} \n\n")
                    fd.write(f"{msg} \n")

            print(f"Writing invalid buildspecs to file: {buildspec_error_file} ")
            print("\n\n")

    def _validate_buildspecs(self, buildspecs):
        """Given a list of buildspec files, validate each buildspec using BuildspecParser
           and return a list of valid buildspecs. Any invalid buildspecs are added to
           separate list
        """
        valid_buildspecs = []
        self.count = 0
        for buildspec in buildspecs:
            self.count += 1

            try:
                parse = BuildspecParser(buildspec)
            # any buildspec that raises SystemExit or ValidationError imply
            # buildspec is not valid, we add this to invalid list along with
            # error message and skip to next buildspec
            except (SystemExit, ValidationError) as err:
                self.invalid_buildspecs[buildspec] = err
                continue

            valid_buildspecs.append(parse)

            if self.count % 5 == 0:
                print(f"Validated {self.count}/{len(buildspecs)} buildspecs")

        print(f"Validated {self.count}/{len(buildspecs)} buildspecs")
        return valid_buildspecs

    def build_cache(self):
        """This method will rebuild the buildspec cache file by recursively searching
        all .yml files specified by input argument ``paths`` which is a list of directory
        roots. The buildspecs are validated and cache file is updated"

        :param paths: A list of directory roots to process buildspecs files.
        :type paths: list
        :return: Rebuild cache file
        """

        self.update_cache = {}
        self.update_cache["unique_tags"] = []
        self.update_cache["unique_executors"] = []
        self.update_cache["buildspecs"] = {}
        self.update_cache["executor"] = {}
        self.update_cache["tags"] = {}
        self.invalid_buildspecs = {}

        for path in self.paths:
            self.update_cache[path] = {}

        buildspecs = self._discover_buildspecs()
        print(f"Found {len(buildspecs)} buildspecs ")

        # validate each buildspec and return a list of valid buildspec parsers that
        # is an instance of BuildspecParser class
        parsers = self._validate_buildspecs(buildspecs)

        # for every parsers (valid buildspecs) we update cache to build an index
        for parser in parsers:

            recipe = parser.recipe["buildspecs"]

            path_root = [
                path
                for path in self.paths
                if os.path.commonprefix([parser.buildspec, path]) == path
            ]
            path_root = path_root[0]

            if not self.update_cache["buildspecs"].get(path_root):
                self.update_cache["buildspecs"][path_root] = {}

            if not self.update_cache["buildspecs"][path_root].get(parser.buildspec):
                self.update_cache["buildspecs"][path_root][parser.buildspec] = {}

            for name in recipe.keys():

                self.update_cache["buildspecs"][path_root][parser.buildspec][
                    name
                ] = recipe[name]
                tags = recipe[name].get("tags")
                executor = recipe[name].get("executor")
                description = recipe[name].get("description")

                if tags:

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

    def check_filter_fields(self):
        """ This method checks filter fields are valid. The filter fields are specified
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

    def check_format_fields(self):
        """ This method will check if all format fields are valid. Format fields
            are passed comma separated as --format field1,field2,field3,...
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
        """ This method will return a boolean True/False that determines if
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
        """ This method will find buildspecs based on cache content. We skip any
            tests based on executor filter, tag filter or type filter and build
            a table of tests that will be printed using print_buildspecs method.
        """

        for path in self.cache["buildspecs"].keys():
            for buildspecfile in self.cache["buildspecs"][path].keys():
                for test in self.cache["buildspecs"][path][buildspecfile].keys():

                    test_recipe = self.cache["buildspecs"][path][buildspecfile][test]
                    schema_type = test_recipe.get("type")
                    executor = test_recipe.get("executor")
                    # if tags not defined in cache we set to empty list for comparison with tag_filter
                    tags = test_recipe.get("tags") or []
                    description = test_recipe.get("description")

                    # filters buildspecs by executor, tags, type field. The return
                    # is a boolean, if its True we skip the test
                    if self._filter_buildspecs(executor, tags, schema_type):
                        continue

                    if self.format:
                        for field in self.table.keys():
                            if field == "type":
                                self.table[field].append(schema_type)

                            elif field == "buildspecs":
                                self.table[field].append(buildspecfile)
                            elif field == "name":
                                self.table[field].append(test)
                            # description, tags, executor have matching format fields with buildspec properties
                            else:
                                self.table[field].append(test_recipe.get(field))

                    else:
                        self.table["name"].append(test)
                        self.table["type"].append(schema_type)
                        self.table["executor"].append(executor)
                        self.table["tags"].append(tags)
                        self.table["description"].append(description)

    def get_buildspecfiles(self):
        """ This method implements ``buildtest buildspec find --buildspec-files``
            which reports all buildspec files in cache.

            :param cache: content of cache as dictionary
            :type cache: dict
        """

        table = {"buildspecs": []}
        files = []

        for path in self.cache["buildspecs"].keys():
            files += self.cache["buildspecs"][path].keys()

        table["buildspecs"] = files
        print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    def get_tags(self):
        """ This method implements ``buildtest buildspec find --tags`` which
            reports a list of unique tags from all buildspecs in cache file.

            :param cache: content of cache as dictionary
            :type cache: dict
        """

        table = {"Tags": []}

        table["Tags"] = self.cache["unique_tags"]
        print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    def get_executors(self):
        """ This method implements ``buildtest buildspec find --list-executors``
            which reports all executors from cache.

            :param cache: content of cache as dictionary
            :type cache: dict
        """

        table = {"executors": []}
        table["executors"] = self.cache["unique_executors"]
        print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    def print_by_executors(self):
        """ This method prints executors by tests and implements
            ``buildtest buildspec find --test-by-tags`` command
        """

        table = {"executor": [], "name": [], "description": []}

        for executor_name in self.cache["executor"].keys():
            for test_name, description in self.cache["executor"][executor_name].items():
                table["executor"].append(executor_name)
                table["name"].append(test_name)
                table["description"].append(description)

        print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    def print_by_tags(self):
        """ This method prints tags by tests and implements
            ``buildtest buildspec find --test-by-tags`` command
        """

        table = {"tags": [], "name": [], "description": []}

        for tagname in self.cache["tags"].keys():
            for test_name, description in self.cache["tags"][tagname].items():
                table["tags"].append(tagname)
                table["name"].append(test_name)
                table["description"].append(description)

        print(tabulate(table, headers=table.keys(), tablefmt="grid"))

    def print_buildspecs(self):
        """Print buildspec table"""

        print(tabulate(self.table, headers=self.table.keys(), tablefmt="grid"))

    @staticmethod
    def print_filter_fields():
        """This method prints filter fields available for buildspec cache. This
           method implements command ``buildtest buildspec find --helpfilter``"""

        filter_field_table = [
            ["executor", "Filter by executor name", "STRING"],
            ["tags", "Filter by tag name ", "STRING"],
            ["type", "Filter by schema type ", "STRING"],
        ]

        print(
            tabulate(
                filter_field_table,
                headers=["Field", "Description", "Type"],
                tablefmt="simple",
            )
        )

    @staticmethod
    def print_format_fields():
        """This method prints format fields available for buildspec cache. This
           method implements command ``buildtest buildspec find --helpformat``"""

        format_fields = [
            ["name", "Format by test name"],
            ["tags", "Format by tag name "],
            ["type", "Format by schema type"],
            ["executor", "Format by executor type"],
            ["description", "Format by description"],
            ["file", "Format by file"],
        ]

        print(
            tabulate(
                format_fields, headers=["Field", "Description"], tablefmt="simple",
            )
        )

    def print_paths(self):
        """ This method print buildspec paths, this implements command
            ``buildtest buildspec find --paths``
        """

        for path in self.get_paths():
            print(path)


def func_buildspec_find(args):
    """ Entry point for ``buildtest buildspec find``. This method
        will attempt to read for buildspec cache file (BUILDSPEC_CACHE_FILE)
        if found and print a list of all buildspecs. Otherwise, it will
        find and load all buildspecs and validate them using BuildspecParser class.
        BuildspecParser will raise SystemError or ValidationError if a buildspec
        is invalid which will be added to list of invalid buildspecs. Finally we
        print a list of all valid buildspecs and any invalid buildspecs are
        written to file along with error message.

        :param args: Input argument from command line passed from argparse
        :return: A list of valid buildspecs found in all repositories.
    """

    bp_cache = BuildspecCache(args.rebuild, args.filter, args.format, args.root)

    # implements buildtest buildspec find --tags
    if args.tags:
        bp_cache.get_tags()
        return

    # implements buildtest buildspec find --buildspec-files
    if args.buildspec_files:
        bp_cache.get_buildspecfiles()
        return

    if args.paths:
        bp_cache.print_paths()
        return

    # implements buildtest buildspec find --executors
    if args.executors:
        bp_cache.get_executors()
        return

    if args.group_by_executor:
        bp_cache.print_by_executors()
        return

    if args.group_by_tags:
        bp_cache.print_by_tags()
        return

    # implements buildtest buildspec find --helpfilter
    if args.helpfilter:
        bp_cache.print_filter_fields()
        return

    # implements buildtest buildspec find --helpformat
    if args.helpformat:
        bp_cache.print_format_fields()
        return

    bp_cache.print_buildspecs()


def parse_buildspecs(
    buildspecs, test_directory, rebuild, tags=None, executors=None, printTable=False
):
    """Parse all buildspecs by invoking class ``BuildspecParser``. If buildspec
    fails validation we add it to ``skipped_tests`` list and print all skipped
    tests at end. If buildspec passes validation we get all builders by invoking
    ``get_builders`` method in BuildspecParser class which gets all tests from
    buildspec file.

    :param buildspecs: A list of input buildspecs to parse
    :type buildspecs: list of filepaths
    :param test_directory: Test directory where buildspecs will be written
    :type test_directory: str (directory path)
    :param tags: A list of input tags to filter tests
    :type tags: list
    :param executors: A list of input executors to filter tests
    :type executors: list
    :param printTable: a boolean to control if parse table is printed
    :type printTable: bool, optional
    :return: A list of builder objects which are instances of ``BuilderBase`` class
    :rtype: list
    """

    builders = []
    table = {"schemafile": [], "validstate": [], "buildspec": []}
    invalid_buildspecs = []
    # build all the tests
    for buildspec in buildspecs:

        valid_state = True
        try:
            # Read in Buildspec file here, loading each will validate the buildspec file
            bp = BuildspecParser(buildspec)
        except (SystemExit, ValidationError) as err:
            invalid_buildspecs.append(
                f"Skipping {buildspec} since it failed to validate"
            )
            logger.error(err)
            continue

        table["schemafile"].append(bp.schema_file)
        table["validstate"].append(valid_state)
        table["buildspec"].append(buildspec)

        builders += bp.get_builders(
            testdir=test_directory,
            rebuild=rebuild,
            tag_filter=tags,
            executor_filter=executors,
        )

    # print any skipped buildspecs if they failed to validate during build stage
    if len(invalid_buildspecs) > 0:
        print("\n\n")
        print("Error Messages from Stage: Parse")
        print("{:_<80}".format(""))
        for test in invalid_buildspecs:
            print(test)

    if not builders:
        print("No buildspecs to process because there are no valid buildspecs")
        sys.exit(0)

    if printTable:
        print(
            """
+---------------------------+
| Stage: Parsing Buildspecs |
+---------------------------+ 
    """
        )
        print(tabulate(table, headers=table.keys(), tablefmt="presto"))

    return builders
