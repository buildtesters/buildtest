import pytest
from buildtest.menu.schema import func_schema


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
            validate = False

        # run buildtest schema -n <schema> --json
        func_schema(args_json)

        class args_examples:
            name = schema
            json = False
            example = True
            validate = False

        class args_validate:
            name = schema
            json = False
            example = True
            validate = False

        # we dont run validate or examples for definitions.schema.json
        if schema == "definitions.schema.json":
            continue

        # run buildtest schema -n <schema> --examples
        func_schema(args_examples)

        # run buildtest schema -n <schema> --validate
        func_schema(args_validate)

    class args:
        name = None
        json = False
        example = False
        validate = False

    # run buildtest schema
    func_schema(args)

    class args:
        name = None
        json = True
        example = False
        validate = False

    # passing --json or --example without --name will result in SystemExit exception
    with pytest.raises(SystemExit):
        func_schema(args)

    class args:
        name = "definitions.schema.json"
        json = False
        example = True
        validate = False

    # passing --example  with defintions.schema.json will result in error
    with pytest.raises(SystemExit):
        func_schema(args)

    class args:
        name = "definitions.schema.json"
        json = False
        example = False
        validate = True

    # passing --validate  with defintions.schema.json will result in error
    with pytest.raises(SystemExit):
        func_schema(args)
