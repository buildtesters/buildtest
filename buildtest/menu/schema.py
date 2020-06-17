import json
import os
from jsonschema.exceptions import ValidationError
from buildtest.buildsystem.base import BuildspecParser
from buildtest.config import check_settings
from buildtest.buildsystem.schemas.utils import (
    load_schema,
    get_schema_fullpath,
    here,
)
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA, supported_schemas
from buildtest.utils.file import walk_tree, read_file


def func_schema(args):
    """This method implements command ``buildtest schema`` which shows a list
       of schemas, their json content and list of schema examples. The input
       ``args`` is an instance of argparse class that contains
       user selection via command line. This method can do the following

       ``buildtest schema`` - Show all schema names
       ``buildtest schema --name <NAME> -j ``. View json content of a specified schema
       ``buildtest schema --name <NAME> -e``. Show schema examples
       Parameters:

       :param args: instance of argparse class
       :type args: <class 'argparse.Namespace'>
       :result: output of json schema on console
    """

    # the default behavior when "buildtest schema" is executed is to show list of all
    # schemas
    if not args.json and not args.example:
        for schema in supported_schemas:
            print(schema)
        return

    # -n option is required when using -j or -e option
    if not args.name:
        raise SystemExit(
            "Please specify a schema name with -n option when using -j or -e option"
        )

    examples = None
    # implements buildtest show schema --global
    if args.name == "settings.schema.json":
        schema = DEFAULT_SETTINGS_SCHEMA
        examples = os.path.join(here, "settings", "examples")
    elif args.name == "global.schema.json":
        schema = os.path.join(here, "global.schema.json")
        examples = os.path.join(here, "global", "examples")
    elif args.name in ["script-v1.0.schema.json", "compiler-v1.0.schema.json"]:
        schema = get_schema_fullpath(args.name)
        # the examples directory is found same location where schema file is located
        examples = os.path.join(os.path.dirname(schema), "examples")

    recipe = load_schema(schema)
    if args.json:
        print(json.dumps(recipe, indent=2))

    # get all examples for specified schema. We validate all examples and
    # and print content of all examples. If there is an error during validation
    # we show the error message.
    if args.example:
        schema_examples = walk_tree(examples, ".yml")

        for example in schema_examples:
            valid_state = True
            err_msg = None
            # for settings.schema.json we validate each test by running check_settings
            if args.name == "settings.schema.json":
                try:
                    check_settings(example, run_init=False)
                except ValidationError as err:
                    valid_state = "FAIL"
                    err_msg = err
            # the rest of schemas are validated using BuildspecParser
            else:
                try:
                    BuildspecParser(example)
                except (SystemExit, ValidationError) as err:
                    valid_state = "FAIL"
                    err_msg = err

            content = read_file(example)
            print("\n")
            print(f"File: {example}")
            print(f"Valid State: {valid_state}")
            print("{:_<80}".format(""))
            print("\n")
            print(content)

            if err_msg:
                print("{:_<40} Validation Error {:_<40}".format("", ""))
                print(err_msg)
