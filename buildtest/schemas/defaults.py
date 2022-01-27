import os

from buildtest.schemas.utils import load_schema
from jsonschema import Draft7Validator, RefResolver

here = os.path.dirname(os.path.abspath(__file__))

schema_table = {}
schema_table["types"] = ["script", "compiler", "spack"]
schema_table["names"] = [
    "global.schema.json",
    "definitions.schema.json",
    "settings.schema.json",
    "compiler.schema.json",
    "spack.schema.json",
    "script.schema.json",
]

schema_table["global.schema.json"] = {}
schema_table["global.schema.json"]["path"] = os.path.join(here, "global.schema.json")
schema_table["global.schema.json"]["recipe"] = load_schema(
    schema_table["global.schema.json"]["path"]
)
schema_table["script.schema.json"] = {}
schema_table["script.schema.json"]["path"] = os.path.join(here, "script.schema.json")
schema_table["script.schema.json"]["recipe"] = load_schema(
    schema_table["script.schema.json"]["path"]
)
schema_table["compiler.schema.json"] = {}
schema_table["compiler.schema.json"]["path"] = os.path.join(
    here, "compiler.schema.json"
)
schema_table["compiler.schema.json"]["recipe"] = load_schema(
    schema_table["compiler.schema.json"]["path"]
)


schema_table["spack.schema.json"] = {}
schema_table["spack.schema.json"]["path"] = os.path.join(here, "spack.schema.json")
schema_table["spack.schema.json"]["recipe"] = load_schema(
    schema_table["spack.schema.json"]["path"]
)


schema_table["definitions.schema.json"] = {}
schema_table["definitions.schema.json"]["path"] = os.path.join(
    here, "definitions.schema.json"
)

schema_table["definitions.schema.json"]["recipe"] = load_schema(
    os.path.join(here, "definitions.schema.json")
)

schema_table["settings.schema.json"] = {}
schema_table["settings.schema.json"]["path"] = os.path.join(
    here, "settings.schema.json"
)
schema_table["settings.schema.json"]["recipe"] = load_schema(
    os.path.join(here, "settings.schema.json")
)


schema_store = {
    schema_table["global.schema.json"]["recipe"]["$id"]: schema_table[
        "global.schema.json"
    ]["recipe"],
    schema_table["compiler.schema.json"]["recipe"]["$id"]: schema_table[
        "compiler.schema.json"
    ]["recipe"],
    schema_table["script.schema.json"]["recipe"]["$id"]: schema_table[
        "script.schema.json"
    ]["recipe"],
    schema_table["spack.schema.json"]["recipe"]["$id"]: schema_table[
        "spack.schema.json"
    ]["recipe"],
    schema_table["definitions.schema.json"]["recipe"]["$id"]: schema_table[
        "definitions.schema.json"
    ]["recipe"],
    schema_table["settings.schema.json"]["recipe"]["$id"]: schema_table[
        "settings.schema.json"
    ]["recipe"],
}

resolver = RefResolver.from_schema(
    schema_table["definitions.schema.json"]["recipe"], store=schema_store
)


def custom_validator(recipe, schema):
    """This is a custom validator for validating JSON documents. We implement a
    custom resolver using `RefResolver <https://python-jsonschema.readthedocs.io/en/stable/references/#jsonschema.RefResolver>`_
    to find schemas locally in order to validate buildspecs with schema files on local filesystem. This ensures changes to
    schema can be done in sync with change to code base.

    This method uses `Draft7Validator <https://python-jsonschema.readthedocs.io/en/stable/validate/#jsonschema.Draft7Validator>`_
    for validating schemas. If there is an error during validation jsonschema will raise an exception of type
    `jsonschema.exceptions.ValidationError <https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError>`_

    Args:
        recipe (dict): Loaded test recipe as YAML document
        schema (dict): Schema document loaded in JSON format

    Raises:
        jsonschema.exceptions.ValidationError: if recipe fails to validate with schema
    """

    # making sure input recipe and schema are dictionary
    assert isinstance(recipe, dict)
    assert isinstance(schema, dict)

    validator = Draft7Validator(schema, resolver=resolver)
    validator.validate(recipe)
