import json
import os

from buildtest.defaults import console
from buildtest.schemas.defaults import schema_table
from buildtest.schemas.utils import here
from buildtest.utils.file import read_file, walk_tree
from rich.syntax import Syntax


def schema_cmd(args):
    """This method implements command ``buildtest schema`` which shows a list
    of schemas, their json content and list of schema examples. The input
    ``args`` is an instance of argparse class that contains
    user selection via command line.

    Args:
        args (dict): Parsed arguments from `ArgumentParser.parse_args <https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args>`_
    """

    # the default behavior when "buildtest schema" is executed is to show list of all
    # schemas
    if not args.json and not args.example:
        for schema in schema_table["names"]:
            print(schema)
        return

    # -n option is required when using schema options
    if not args.name:
        raise SystemExit("Please specify a schema name with -n option")

    if args.json:
        console.print(json.dumps(schema_table[args.name]["recipe"], indent=2))
        return

    # There are no examples for definitions schema
    if args.name == "definitions.schema.json":
        if args.example or args.validate:
            raise SystemExit("There are no examples for definitions.schema.json")

    examples = os.path.join(here, "examples", args.name)

    # get all examples for specified schema. We validate all examples and
    # and print content of all examples. If there is an error during validation
    # we show the error message.

    schema_examples = walk_tree(examples, ".yml")
    for example in schema_examples:

        if args.example:
            content = read_file(example)
            console.rule(example)
            syntax = Syntax(content, "yaml", theme="emacs")
            console.print(syntax)
