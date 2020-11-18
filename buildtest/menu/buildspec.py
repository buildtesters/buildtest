import json
import logging
import os
import sys
import subprocess

from tabulate import tabulate
from jsonschema.exceptions import ValidationError
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import load_settings
from buildtest.defaults import BUILDSPEC_CACHE_FILE, BUILDSPEC_DEFAULT_PATH
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import is_file, walk_tree, resolve_path

logger = logging.getLogger(__name__)


class BuildspecCache:

    table = {"Name": [], "Type": [], "Executor": [], "Tags": [], "Description": []}
    filter_fields = ["type", "executor", "tags"]

    def __init__(self, rebuild, filter):
        self.filter = filter

        self.paths = []
        self.rebuild = rebuild
        self.cache = {}

        self.load_paths()
        self.build()

        self.check_filter_fields()
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
        buildspec_paths = config_opts.get("buildspec_roots")

        self.paths += BUILDSPEC_DEFAULT_PATH

        # if buildspec_roots defined in configuration, resolve path and if path exist add
        # to list of paths to search for buildspecs
        if buildspec_paths:

            for root in buildspec_paths:
                path = resolve_path(root, exist=False)
                if not os.path.exists(path):
                    print(f"Path: {path} does not exist!")

                self.paths.append(path)

    def build(self):
        """This method will build buildspec cache file. If user requests to
           rebuild cache we remove the file and recreate cache. If cache file
           exists, we simply load from cache
        """

        # implements buildtest buildspec find --clear which removes cache file
        # before finding all buildspecs
        if self.rebuild:
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

    def build_cache(self):
        """This method will rebuild the buildspec cache file by recursively searching
        all .yml files specified by input argument ``paths`` which is a list of directory
        roots. The buildspecs are validated and cache file is updated"

        :param paths: A list of directory roots to process buildspecs files.
        :type paths: list
        :return: Rebuild cache file
        """

        cache = {}
        cache["unique_tags"] = []
        cache["unique_executors"] = []
        cache["buildspecs"] = {}

        buildspecs = []
        invalid_buildspecs = {}
        parse = None
        # add all buildspecs from each repo. walk_tree will find all .yml files
        # recursively and add them to list
        for path in self.paths:
            cache["buildspecs"][path] = {}
            buildspec = walk_tree(path, ".yml")
            buildspecs += buildspec

        # remove any files in .buildtest directory of root of repo.
        buildspecs = [
            buildspec
            for buildspec in buildspecs
            if os.path.basename(os.path.dirname(buildspec)) != ".buildtest"
        ]
        print(f"Found {len(buildspecs)} buildspecs")

        # process each buildspec by invoking BuildspecParser which will validate
        # buildspec, if it fails it will raise SystemExit or ValidationError in
        # this case we skip to next buildspec
        count = 0
        for buildspec in buildspecs:
            count += 1

            try:
                parse = BuildspecParser(buildspec)
            # any buildspec that raises SystemExit or ValidationError imply
            # buildspec is not valid, we add this to invalid list along with
            # error message and skip to next buildspec
            except (SystemExit, ValidationError) as err:
                invalid_buildspecs[buildspec] = err
                continue

            if count % 5 == 0:
                print(f"Validated {count}/{len(buildspecs)} buildspecs")
            recipe = parse.recipe["buildspecs"]

            path_root = [
                path
                for path in self.paths
                if os.path.commonprefix([buildspec, path]) == path
            ]
            path_root = path_root[0]

            cache["buildspecs"][path_root][buildspec] = {}

            for name in recipe.keys():

                cache["buildspecs"][path_root][buildspec][name] = recipe[name]
                tags = recipe[name].get("tags")
                executor = recipe[name].get("executor")

                if tags:

                    if isinstance(tags, str):
                        cache["unique_tags"].append(tags)
                    elif isinstance(tags, list):
                        cache["unique_tags"] += tags

                if executor:
                    cache["unique_executors"].append(executor)

        cache["unique_tags"] = list(set(cache["unique_tags"]))
        cache["unique_executors"] = list(set(cache["unique_executors"]))

        print(f"Validated {count}/{len(buildspecs)} buildspecs")

        with open(BUILDSPEC_CACHE_FILE, "w") as fd:
            json.dump(cache, fd, indent=2)

        print(f"\nDetected {len(invalid_buildspecs)} invalid buildspecs \n")

        # write invalid buildspecs to file if any found
        if invalid_buildspecs:
            buildspec_error_file = os.path.join(
                os.path.dirname(BUILDSPEC_CACHE_FILE), "buildspec.error"
            )

            with open(buildspec_error_file, "w") as fd:
                for file, msg in invalid_buildspecs.items():
                    fd.write(f"buildspec:{file} \n\n")
                    fd.write(f"{msg} \n")

            print(f"Writing invalid buildspecs to file: {buildspec_error_file} ")
            print("\n\n")

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

    def find_buildspecs(self):
        """ This method will find buildspecs based on cache content. We skip any
            tests based on executor filter, tag filter or type filter and build
            a table of tests that will be printed using print_buildspecs method.
        """

        for path in self.cache["buildspecs"].keys():
            for buildspecfile in self.cache["buildspecs"][path].keys():
                for test in self.cache["buildspecs"][path][buildspecfile].keys():

                    schema_type = self.cache["buildspecs"][path][buildspecfile][
                        test
                    ].get("type")
                    executor = self.cache["buildspecs"][path][buildspecfile][test].get(
                        "executor"
                    )
                    # if tags not defined in cache we set to empty list for comparison with tag_filter
                    tags = (
                        self.cache["buildspecs"][path][buildspecfile][test].get("tags")
                        or []
                    )
                    description = self.cache["buildspecs"][path][buildspecfile][
                        test
                    ].get("description")

                    # skip all entries that dont match filtered executor
                    if self.executor_filter and self.executor_filter != executor:
                        continue

                    # if skip all entries that dont match filtered tag. We only search if --filter tag=value is set
                    if self.tags_filter:
                        # if tags is not set in buildspec cache we default to empty list which and this condition should always be true
                        if self.tags_filter not in tags:
                            continue

                    if self.type_filter and self.type_filter != schema_type:
                        continue

                    self.table["Name"].append(test)
                    self.table["Type"].append(schema_type)
                    self.table["Executor"].append(executor)
                    self.table["Tags"].append(tags)
                    self.table["Description"].append(description)

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

    def print_buildspecs(self):
        """Print buildspec table from """

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

    bp_cache = BuildspecCache(args.clear, args.filter)

    # implements buildtest buildspec find --tags
    if args.tags:
        bp_cache.get_tags()
        return

    # implements buildtest buildspec find --buildspec-files
    if args.buildspec_files:
        bp_cache.get_buildspecfiles()
        return

    # implements buildtest buildspec find --list-executors
    if args.list_executors:
        bp_cache.get_executors()
        return

    # implements buildtest buildspec find --helpfilter
    if args.helpfilter:
        bp_cache.print_filter_fields()
        return

    bp_cache.print_buildspecs()


def func_buildspec_view_edit(buildspec, view=False, edit=False):
    """This is a shared method for ``buildtest buildspec view`` and
       ``buildtest buildspec edit``.

       :param buildspec: buildspec file section to view or edit.
       :type buildspec: str (filepath)
       :param view: boolean to determine if we want to view buildspec file
       :type view: bool
       :param edit: boolean to control if we want to edit buildspec file in editor.
       :type edit: bool
       :return: Shows the content of buildspec or let's user interactively edit buildspec. An exception can be raised if it's unable to find buildspec
    """

    with open(BUILDSPEC_CACHE_FILE, "r") as fd:
        cache = json.loads(fd.read())

    for path in cache["buildspecs"].keys():
        for buildspecfile in cache["buildspecs"][path].keys():
            if buildspec in list(cache["buildspecs"][path][buildspecfile].keys()):
                if view:
                    cmd = f"cat {buildspecfile}"
                    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
                    print(output)
                if edit:
                    # this loop will terminate once user has edited file, and we parse
                    # the file for any errors. If one of the exceptions is raised, we
                    # print error message and set 'success' to False and user is requested
                    # to fix buildspec until it is valid.
                    while True:
                        success = True
                        config_opts = load_settings()
                        os.system(f"{config_opts['editor']} {buildspecfile}")
                        try:
                            BuildspecParser(buildspecfile)
                        except (SystemExit, ValidationError) as err:
                            print(err)
                            input("Press any key to continue")
                            success = False
                        # break out of while loop once user has successfully validated
                        # buildspec.
                        if success:
                            break

                return

    raise SystemExit(f"Unable to find buildspec {buildspec}")


def func_buildspec_view(args):
    """This method implements ``buildtest buildspec view`` which shows
    content of a buildspec file
    """
    func_buildspec_view_edit(args.buildspec, view=True, edit=False)


def func_buildspec_edit(args):
    """This method implement ``buildtest buildspec edit`` which
    allows one to edit a Buildspec file with one of the editors
    set in buildtest settings.
    """

    func_buildspec_view_edit(args.buildspec, view=False, edit=True)


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
