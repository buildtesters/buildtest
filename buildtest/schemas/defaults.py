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
    "compiler-v1.0.schema.json",
    "spack-v1.0.schema.json",
    "script-v1.0.schema.json",
]
schema_table["versions"] = {}
schema_table["versions"]["script"] = ["1.0"]
schema_table["versions"]["compiler"] = ["1.0"]
schema_table["versions"]["spack"] = ["1.0"]

schema_table["global.schema.json"] = {}
schema_table["global.schema.json"]["path"] = os.path.join(here, "global.schema.json")
schema_table["global.schema.json"]["recipe"] = load_schema(
    schema_table["global.schema.json"]["path"]
)
schema_table["script-v1.0.schema.json"] = {}
schema_table["script-v1.0.schema.json"]["path"] = os.path.join(
    here, "script-v1.0.schema.json"
)
schema_table["script-v1.0.schema.json"]["recipe"] = load_schema(
    schema_table["script-v1.0.schema.json"]["path"]
)
schema_table["compiler-v1.0.schema.json"] = {}
schema_table["compiler-v1.0.schema.json"]["path"] = os.path.join(
    here, "compiler-v1.0.schema.json"
)
schema_table["compiler-v1.0.schema.json"]["recipe"] = load_schema(
    schema_table["compiler-v1.0.schema.json"]["path"]
)


schema_table["spack-v1.0.schema.json"] = {}
schema_table["spack-v1.0.schema.json"]["path"] = os.path.join(
    here, "spack-v1.0.schema.json"
)
schema_table["spack-v1.0.schema.json"]["recipe"] = load_schema(
    schema_table["spack-v1.0.schema.json"]["path"]
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
    schema_table["compiler-v1.0.schema.json"]["recipe"]["$id"]: schema_table[
        "compiler-v1.0.schema.json"
    ]["recipe"],
    schema_table["script-v1.0.schema.json"]["recipe"]["$id"]: schema_table[
        "script-v1.0.schema.json"
    ]["recipe"],
    schema_table["spack-v1.0.schema.json"]["recipe"]["$id"]: schema_table[
        "spack-v1.0.schema.json"
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
