import pytest
from buildtest.defaults import supported_schemas
from buildtest.menu.schema import func_schema


def test_func_schema():

    for schema in supported_schemas:

        class args:
            name = schema
            json = True
            example = True

        func_schema(args)

    class args:
        name = None
        json = False
        example = False

    func_schema(args)

    # passing --json or --example without --name will result in SystemExit exception
    class args:
        name = None
        json = True
        example = False

    with pytest.raises(SystemExit):
        func_schema(args)
