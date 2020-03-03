import os
import pytest

from buildtest.tools.defaults import (
    BUILDTEST_MODULE_COLLECTION_FILE,
    BUILDTEST_SPIDER_FILE,
)
from buildtest.tools.configuration.config import func_config_view, func_config_restore
from buildtest.tools.log import BuildTestError
from buildtest.tools.modulesystem.module_difference import diff_trees
from buildtest.module import Module, get_all_collections


def test_module_diff():
    """Testing module difference between two trees. First test is testing against same module tree, and the second
        test is against a different tree. """
    tree1 = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    tree2 = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    tree_list = f"{tree1},{tree2}"
    diff_trees(tree_list)


@pytest.mark.xfail(
    reason="Test expected to fail because only one tree is passed",
    raises=BuildTestError,
)
def test_module_diff_invalid_args():
    """Testing when one moduletree is passed to ``buildtest module --diff-trees``"""
    tree = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    diff_trees(tree)


class TestModule:
    @pytest.mark.skip("not working")
    def test_module(self):
        mod_names = ["lmod"]
        a = Module(mod_names)
        print(a.get_command())
        assert 0 == a.test_modules()

        b = Module(mod_names, force=True)
        assert 0 == b.test_modules()

        c = Module(mod_names, debug=True)
        assert 0 == c.test_modules()

    @pytest.mark.skip("not working")
    def test_collection(self):
        cmd = Module(["settarg"])
        # save as collection name "settarg"
        cmd.save("settarg")
        # save as "default" collection
        cmd.save()
        # show "default" collection
        cmd.describe()
        # show "settarg" collection
        cmd.describe("settarg")

        assert 0 == cmd.test_collection("settarg")
        assert 0 == cmd.test_collection()

    @pytest.mark.skip("not working")
    def test_collection_exists(self):
        assert "settarg" in get_all_collections()

    @pytest.mark.xfail(
        reason="Collection Name must be string when saving", raises=TypeError
    )
    def test_type_error_save_collection(self):
        cmd = Module()
        cmd.save(1)

    @pytest.mark.xfail(
        reason="Collection Name must be string when showing content of collection",
        raises=TypeError,
    )
    def test_type_error_describe_collection(self):
        cmd = Module()
        cmd.describe(1)

    def test_get_collection(self):
        a = Module()
        assert "module restore settarg" == a.get_collection("settarg")
        assert "module restore default" == a.get_collection()

    @pytest.mark.xfail(
        reason="Type error when a non-string argument to ModuleCollection class",
        raises=TypeError,
    )
    def test_type_error(self):
        a = Module(1)
