import pytest
from buildtest.tools.tutorialexamples import generate_tutorial_examples


def test_buildtest_tutorial_examples():
    with pytest.raises(SystemExit):
        generate_tutorial_examples()
