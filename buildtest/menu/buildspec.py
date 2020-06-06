import json
import os
import subprocess
import yaml

from buildtest.defaults import REPO_FILE, BUILDSPEC_CACHE_FILE
from buildtest.config import get_default_settings
from buildtest.utils.file import is_file, walk_tree

from buildtest.buildsystem.schemas.utils import load_recipe


def func_buildspec_find(args):

    # if is_file(BUILDSPEC_CACHE_FILE):
    #    return

    # if repo file not found then terminate with message since we can't find
    # any buildspecs
    if not is_file(REPO_FILE):
        raise SystemExit("Unable to find any buildspecs because no repositories found.")

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    paths = []
    for repo in repo_dict.keys():
        paths.append(repo_dict[repo]["dest"])

    buildspecs = []
    for path in paths:
        buildspec = walk_tree(path, ".yml")
        buildspecs += buildspec

    cache = {}
    for buildspec in buildspecs:
        recipe = load_recipe(buildspec)
        cache[buildspec] = {}
        cache[buildspec]["sections"] = []
        cache[buildspec]["section_summary"] = {}
        # print (recipe.keys())
        for name in recipe.keys():

            if not isinstance(recipe[name], dict):
                continue

            cache[buildspec]["sections"].append(name)
            cache[buildspec]["section_summary"][name] = {}
            cache[buildspec]["section_summary"][name]["type"] = recipe[name].get("type")
            cache[buildspec]["section_summary"][name]["description"] = recipe[name].get(
                "description"
            )

    with open(BUILDSPEC_CACHE_FILE, "w") as fd:
        json.dump(cache, fd, indent=2)

    print("{:<30} {:<30} {:<30}".format("Name", "Type", "Description", "Buildspec"))
    print("{:_<80}".format(""))
    for buildspec in cache.keys():
        for name in cache[buildspec]["section_summary"].keys():
            description = cache[buildspec]["section_summary"][name]["description"]
            type = cache[buildspec]["section_summary"][name]["type"]

            description = str(description)
            type = str(type)
            print("{:<30} {:<30} {:<30}".format(name, type, description))

            # print(name, type, description)


def func_buildspec_view_edit(args, view=False, edit=False):
    with open(BUILDSPEC_CACHE_FILE, "r") as fd:
        cache = json.loads(fd.read())

    for key in cache.keys():
        if args.buildspec in cache[key]["sections"]:
            if view:
                cmd = f"cat {key}"
                output = subprocess.check_output(cmd, shell=True).decode("utf-8")
                print(output)
            if edit:
                config_opts = get_default_settings()
                os.system(f"{config_opts['config']['editor']} {key}")
            return

    raise SystemExit(f"Unable to find buildspec {args.buildspec}")


def func_buildspec_view(args):
    func_buildspec_view_edit(args, view=True, edit=False)


def func_buildspec_edit(args):
    func_buildspec_view_edit(args, view=False, edit=True)


def func_buildspec_check(args):
    pass
