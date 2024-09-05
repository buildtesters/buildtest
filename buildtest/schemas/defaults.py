import os

from jsonschema import Draft7Validator
from referencing import Registry, Resource

from buildtest.schemas.utils import load_schema

here = os.path.dirname(os.path.abspath(__file__))

schema_table = {}
schema_table["types"] = ["script", "spack"]
schema_table["names"] = [
    "global.schema.json",
    "definitions.schema.json",
    "settings.schema.json",
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

registry = Registry().with_resources(
    [(key, Resource.from_contents(recipe)) for key, recipe in schema_store.items()]
)


def custom_validator(recipe, schema):
    """
    Validate a JSON document against a given schema using a custom validator.

    This function utilizes `Registry` from the `referencing <https://python-jsonschema.readthedocs.io/en/latest/referencing/>`
    library to handle schema references locally and validate buildspecs with schema files on the
    local filesystem, ensuring that schema changes are synchronized with the code base updates.

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

    validator = Draft7Validator(schema, registry=registry)
    validator.validate(recipe)
