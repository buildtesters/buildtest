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
    custom resolver for finding json schemas locally by implementing a schema store.
    The input arguments ``recipe`` and ``schema`` is your input JSON recipe and schema
    content for validating the recipe. This method uses Draft7Validator for validating
    schemas.

    :param recipe: Input recipe as JSON document
    :type recipe: dict
    :param schema: Input JSON Schema content to validate JSON document
    :type schema: dict
    """

    # making sure input recipe and schema are dictionary
    assert isinstance(recipe, dict)
    assert isinstance(schema, dict)

    validator = Draft7Validator(schema, resolver=resolver)
    validator.validate(recipe)
