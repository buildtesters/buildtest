import json
import os

from buildtest.buildsystem.schemas.utils import (
    load_schema,
    get_schemas_available,
    get_schema_fullpath,
    here,
)


def show_schema_layout(args):
    """This method implements command ``buildtest show schema`` which displays json schemas
       supported by buildtest. The input ``args`` is an instance of argparse class that contains
       user selection via command line. The method can display the global schema when
       ``buildtest show schema --global`` is specified or any name schema via
       ``buildtest show schema --name <NAME>``. The result is an output of the json schema on the console.

       Parameters:

       :param args: instance of argparse class
       :type args: <class 'argparse.Namespace'>
       :result: output of json schema on console
    """

    # implements ``buildtest show schema --global``. Since we can't use args.global we set this to main
    if args.main:
        global_schema = os.path.join(here, "global.schema.json")
        # check if file exists
        assert global_schema
        recipe = load_schema(global_schema)
        print(json.dumps(recipe, indent=2))
        return

    # section below implements ``buildtest show schema --name``
    schema = get_schemas_available()[args.name]
    version = args.version or "latest"

    if version not in schema:
        print("Warning, %s is not a known version, showing latest." % version)

    schema = get_schema_fullpath(schema.get(version, schema.get("latest")))
    schema = load_schema(schema)
    print(json.dumps(schema, indent=2))
