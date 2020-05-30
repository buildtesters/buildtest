import json
import os

from buildtest.buildsystem.schemas.utils import (
    load_schema,
    get_schemas_available,
    get_schema_fullpath,
    here,
)
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA


def show_schema_layout(args):
    """This method implements command ``buildtest show schema`` which displays json schemas
       supported by buildtest. The input ``args`` is an instance of argparse class that contains
       user selection via command line. This method can do the following

       ``buildtest show schema --global`` - Display the global schema for Buildspec
       ``buildtest show schema --name <NAME>``. Display one of the supported buildtest schemas
       ``buildtest show schema --settings``. Display buildtest settings schema

       Parameters:

       :param args: instance of argparse class
       :type args: <class 'argparse.Namespace'>
       :result: output of json schema on console
    """

    # implements buildtest show schema --global
    if args._global:
        schema = os.path.join(here, "global.schema.json")
    # implements buildtest show schema --settings
    elif args.settings:
        schema = DEFAULT_SETTINGS_SCHEMA
    # implements buildtest show schema --name
    elif args.name:
        schema = get_schemas_available()[args.name]
        version = args.version or "latest"

        if version not in schema:
            print("Warning, %s is not a known version, showing latest." % version)

        schema = get_schema_fullpath(schema.get(version, schema.get("latest")))

    recipe = load_schema(schema)
    print(json.dumps(recipe, indent=2))
