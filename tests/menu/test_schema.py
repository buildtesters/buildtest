import pytest
from buildtest.cli.schema import func_schema


@pytest.mark.schema
@pytest.mark.cli
def test_func_schema():

    supported_schemas = [
        "definitions.schema.json",
        "global.schema.json",
        "settings.schema.json",
        "compiler-v1.0.schema.json",
        "script-v1.0.schema.json",
    ]
    # for all schemas run --json, --examples, --validate option
    for schema in supported_schemas:

        class args_json:
            name = schema
            json = True
            example = False

        # run buildtest schema -n <schema> --json
        func_schema(args_json)

        class args_examples:
            name = schema
            json = False
            example = True

        # we dont run validate or examples for definitions.schema.json
        if schema == "definitions.schema.json":
            continue

        # run buildtest schema -n <schema> --example
        func_schema(args_examples)

    class args:
        name = None
        json = False
        example = False

    # run buildtest schema
    func_schema(args)

    class args:
        name = None
        json = True
        example = False

    # passing --json or --example without --name will result in SystemExit exception
    with pytest.raises(SystemExit):
        func_schema(args)

    class args:
        name = "definitions.schema.json"
        json = False
        example = True

    # passing --example  with definitions.schema.json will result in error
    with pytest.raises(SystemExit):
        func_schema(args)
