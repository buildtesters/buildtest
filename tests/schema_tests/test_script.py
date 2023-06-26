import os

import pytest
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import SiteConfiguration
from buildtest.defaults import SCHEMA_ROOT
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.file import walk_tree
from jsonschema.exceptions import ValidationError

schema_name = "script"
schema_file = f"{schema_name}.schema.json"
schema_path = os.path.join(SCHEMA_ROOT, schema_file)
schema_examples = os.path.join(SCHEMA_ROOT, "examples", schema_file)


def check_invalid_recipes(buildspecs, buildexecutor):
    """This function is responsible for validating all invalid buildspecs

    Args:
        buildspecs (list): List of buildspecs to validate
        buildexecutor (BuildExecutor): BuildExecutor object

    """

    for buildspec in buildspecs:
        with pytest.raises(ValidationError) as excinfo:
            BuildspecParser(buildspec=buildspec, buildexecutor=buildexecutor)
        print(f"buildspec file: {buildspec} is invalid")
        print(excinfo.value)


def check_valid_recipes(buildspecs, buildexecutor):
    """This function is responsible for validating all valid buildspecs

    Args:
        buildspecs (list): List of buildspecs to validate
        buildexecutor (BuildExecutor): BuildExecutor object

    """

    for buildspec in buildspecs:
        BuildspecParser(buildspec=buildspec, buildexecutor=buildexecutor)
        print(f"buildspec file: {buildspec} is valid!")


@pytest.mark.schema
def test_script_examples(tmp_path):
    """the script test_organization is responsible for all the schemas
    in the root of the repository, under <schema>/examples.
    A schema specific test is intended to run tests that
    are specific to a schema. In this case, this is the "script"
    folder. Invalid examples should be under ./invalid/script.
    """

    configuration = SiteConfiguration()
    configuration.detect_system()
    configuration.validate()

    buildexecutor = BuildExecutor(configuration)

    print("Testing schema %s" % schema_file)

    invalids = os.path.join(schema_examples, "invalid")
    valids = os.path.join(schema_examples, "valid")

    invalid_buildspecs = walk_tree(invalids)
    valid_buildspecs = walk_tree(valids)

    check_valid_recipes(valid_buildspecs, buildexecutor)
    check_invalid_recipes(invalid_buildspecs, buildexecutor)
