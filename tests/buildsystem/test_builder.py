import os
import pytest

here = os.path.dirname(os.path.abspath(__file__))

from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import walk_tree

"""
def test_Builder(tmp_path):
    directory = os.path.join(here, "invalid_builds")
    filters = {"tags": None, "executors": None}
    print(os.listdir(directory))
    for buildspec in walk_tree(directory, ".yml"):
        buildspecfile = os.path.join(directory, buildspec)
        print("file:", buildspecfile)
        bp = BuildspecParser(buildspecfile)
        builder = Builder(bp=bp, testdir=tmp_path, filters=filters)
        builders = builder.get_builders()
        for builder in builders:
            with pytest.raises(BuildTestError):
                builder.build()

    directory = os.path.join(here, "valid_builds")
    filters = {"tags": None, "executors": None}
    for buildspec in os.listdir(directory):
        buildspec = os.path.join(directory, buildspec)
        bp = BuildspecParser(buildspec)
        builder = Builder(bp=bp, testdir=tmp_path, filters=filters)
        builders = builder.get_builders()
        for builder in builders:
            builder.build()
"""
