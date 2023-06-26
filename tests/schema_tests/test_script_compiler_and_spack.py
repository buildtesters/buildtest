import os

import pytest
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import SiteConfiguration
from buildtest.defaults import SCHEMA_ROOT
from buildtest.exceptions import InvalidBuildspecSchemaType
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.file import walk_tree
from jsonschema.exceptions import ValidationError

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()

buildexecutor = BuildExecutor(configuration)


def check_invalid_buildspecs(buildspecs):
    """This function is responsible for validating all invalid buildspecs

    Args:
        buildspecs (list): List of buildspecs to validate
    """

    for buildspec in buildspecs:
        with pytest.raises(ValidationError) as excinfo:
            BuildspecParser(buildspec=buildspec, buildexecutor=buildexecutor)
        print(f"buildspec file: {buildspec} is invalid")
        print(excinfo.value)


def check_valid_buildspecs(buildspecs):
    """This function is responsible for validating all valid buildspecs

    Args:
        buildspecs (list): List of buildspecs to validate
    """

    for buildspec in buildspecs:
        BuildspecParser(buildspec=buildspec, buildexecutor=buildexecutor)
        print(f"buildspec file: {buildspec} is valid!")


def validate_examples(schema_file):
    """This method will validate all example buildspecs for a given schema file. Each schema has valid and invalid buildspecs.
    This method will find all buildspecs and validate them against the schema file.

    Args:
        schema_file (str): Name of schema file
    """

    schema_examples = os.path.join(SCHEMA_ROOT, "examples", schema_file)

    print("Testing schema %s" % schema_file)

    invalid_buildspecs = walk_tree(os.path.join(schema_examples, "invalid"))
    valid_buildspecs = walk_tree(os.path.join(schema_examples, "valid"))

    check_valid_buildspecs(valid_buildspecs)
    check_invalid_buildspecs(invalid_buildspecs)


@pytest.mark.schema
def test_script_examples():
    validate_examples(schema_file="script.schema.json")


@pytest.mark.schema
def test_compiler_examples():
    validate_examples(schema_file="compiler.schema.json")


@pytest.mark.schema
def test_spack_examples():
    validate_examples(schema_file="spack.schema.json")


def test_missing_type():
    """Test that exception is raised when schema type is missing"""
    buildspec = os.path.join(
        SCHEMA_ROOT, "examples", "special_invalid_buildspecs", "missing_type.yml"
    )
    try:
        BuildspecParser(buildspec=buildspec, buildexecutor=buildexecutor)
    except InvalidBuildspecSchemaType as err:
        print(err)
