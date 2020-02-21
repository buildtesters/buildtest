import os
import sys

from buildtest.tools.buildsystem.status import show_status_report, get_total_build_ids
from buildtest.tools.build import clear_builds

"""
def test_build_report():
    show_status_report()


def test_get_build_ids():
    build_ids = get_build_ids()
    assert isinstance(build_ids, range)

    total_build_ids = get_total_build_ids()
    # total build ids must be an integer
    assert isinstance(total_build_ids, int)
    # total build ids must be number greater than 0
    assert total_build_ids >= 0


def test_clear_build():
    clear_builds()
"""
