import json
import os
import subprocess

from tabulate import tabulate
from jsonschema.exceptions import ValidationError
from buildtest.defaults import BUILDSPEC_CACHE_FILE, BUILDSPEC_DEFAULT_PATH
from buildtest.config import load_settings
from buildtest.utils.file import is_file, walk_tree, resolve_path
from buildtest.buildsystem.parser import BuildspecParser


def func_buildspec_find(args):
    """Entry point for ``buildtest buildspec find``. This method
       will attempt to read for buildspec cache file (BUILDSPEC_CACHE_FILE)
       if found and print a list of all buildspecs. Otherwise, it will
       read the repo file (REPO_FILE) and find all buildspecs and validate
       them via BuildspecParser. BuildspecParser will raise SystemError or
       ValidationError if a buildspec is invalid which will be added to list
       of invalid buildspecs. Finally we print a list of all valid buildspecs
       and any invalid buildspecs are written to file along with error
       message.

       Parameters

       :param args: Input argument from command line passed from argparse
       :return: A list of valid buildspecs found in all repositories.
    """

    cache = {}
    config_opts = load_settings()

    buildspec_paths = (
        config_opts.get("config", {}).get("paths", {}).get("buildspec_roots")
    )
    paths = [BUILDSPEC_DEFAULT_PATH]

    if buildspec_paths:

        for root in buildspec_paths:
            path = resolve_path(root, exist=False)
            if os.path.exists(path):
                paths.append(path)

    print("Searching buildspec in following directories: ", ",".join(paths))
    # implements buildtest buildspec find --clear which removes cache file before finding all buildspecs
    if args.clear:
        try:
            os.remove(BUILDSPEC_CACHE_FILE)
            print(f"Clearing cache file: {BUILDSPEC_CACHE_FILE}")
        except OSError:
            pass

    # if cache file is not found, then we will build cache by searching
    # all buildspecs paths and traverse directory to find all .yml files
    if not is_file(BUILDSPEC_CACHE_FILE):

        buildspecs = []
        invalid_buildspecs = {}
        parse = None
        # add all buildspecs from each repo. walk_tree will find all .yml files
        # recursively and add them to list
        for path in paths:
            cache[path] = {}
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
                for path in paths
                if os.path.commonprefix([buildspec, path]) == path
            ]
            path_root = path_root[0]

            cache[path_root][buildspec] = {}

            for name in recipe.keys():

                if not isinstance(recipe[name], dict):
                    continue

                cache[path_root][buildspec][name] = recipe[name]

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

    with open(BUILDSPEC_CACHE_FILE, "r") as fd:
        cache = json.loads(fd.read())

    paths = cache.keys()

    table = {"Name": [], "Type": [], "Executor": [], "Tags": [], "Description": []}

    for path in paths:
        for buildspecfile in cache[path].keys():
            for test in cache[path][buildspecfile].keys():

                type = cache[path][buildspecfile][test]["type"]
                executor = cache[path][buildspecfile][test]["executor"]
                tags = cache[path][buildspecfile][test].get("tags")
                description = cache[path][buildspecfile][test].get("description")

                table["Name"].append(test)
                table["Type"].append(type)
                table["Executor"].append(executor)
                table["Tags"].append(tags)
                table["Description"].append(description)

    print(tabulate(table, headers=table.keys(), tablefmt="grid"))


def func_buildspec_view_edit(buildspec, view=False, edit=False):
    """This is a shared method for ``buildtest buildspec view`` and
       ``buildtest buildspec edit``.

       Parameters:
       :param buildspec: buildspec file section to view or edit.
       :param view: boolean to determine if we want to view buildspec file
       :param edit: boolean to control if we want to edit buildspec file in editor.
       :return: Shows the content of buildspec or let's user interactively edit buildspec. An exception can be raised if it's unable to find buildspec
    """

    with open(BUILDSPEC_CACHE_FILE, "r") as fd:
        cache = json.loads(fd.read())

    for path in cache.keys():
        for buildspecfile in cache[path].keys():
            if buildspec in list(cache[path][buildspecfile].keys()):
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
                        os.system(f"{config_opts['config']['editor']} {buildspecfile}")
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
