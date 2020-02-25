import os
import pytest

from buildtest.tools.modules import (
    check_spack_module,
    check_easybuild_module,
    find_module_deps,
    list_all_parent_modules,
)
from buildtest.tools.modulesystem.module_difference import diff_trees
from buildtest.tools.modulesystem.tree import module_tree_add, module_tree_rm
from buildtest.tools.log import BuildTestError
from buildtest.module import Module, ModuleCollection, get_all_collections


@pytest.mark.skip("not working")
def test_spack_modules():
    module_tree_add(["/mxg-hpc/users/ssi29/spack/modules/linux-rhel7-x86_64/Core"])
    check_spack_module()
    module_tree_rm(["/mxg-hpc/users/ssi29/spack/modules/linux-rhel7-x86_64/Core"])


@pytest.mark.skip("not working")
def test_module_deps():
    module_tree_add(["/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core"])
    find_module_deps("GCCcore/8.1.0")
    module_tree_rm(["/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core"])


@pytest.mark.skip("not working")
def test_diff_trees():
    diff_trees(
        "/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core,/usr/share/lmod/lmod/modulefiles/Core/"
    )


@pytest.mark.skip("not working")
def test_easybuild_modules():
    module_tree_add(["/opt/easybuild/modules/all"])
    check_easybuild_module()
    module_tree_rm(["/opt/easybuild/modules/all"])


@pytest.mark.skip("not working")
def test_module_diff():
    """Testing module difference between two trees. First test is testing against same module tree, and the second
        test is against a different tree. """
    tree1 = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    tree2 = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    tree_list = f"{tree1},{tree2}"
    diff_trees(tree_list)

    tree_list = f"{tree1},/opt/easybuild/modules/all"
    diff_trees(tree_list)


@pytest.mark.xfail(
    reason="Test expected to fail because only one tree is passed",
    raises=BuildTestError,
)
def test_module_diff_invalid_args():
    """Testing when one moduletree is passed to ``buildtest module --diff-trees``"""
    tree = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    diff_trees(tree)


def test_list_all_parents():
    list_all_parent_modules()


class TestModule:
    def test_module(self):
        mod_names = ["lmod"]
        a = Module(mod_names)
        a.get_command()
        assert 0 == a.test_modules()

        b = Module(mod_names, force=True)
        assert 0 == b.test_modules()

        c = Module(mod_names, debug=True)
        assert 0 == c.test_modules()

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

    @pytest.mark.xfail(reason="Collection Name must be string when saving", raises=TypeError)
    def test_type_error_save_collection(self):
        cmd = Module(["settarg"])
        cmd.save(1)

    @pytest.mark.xfail(reason="Collection Name must be string when showing content of collection", raises=TypeError)
    def test_type_error_describe_collection(self):
        cmd = Module(["settarg"])
        cmd.describe(1)


class TestModuleCollection:
    def test_get_collection_string(self):
        a = ModuleCollection("settarg")
        assert "module restore settarg" == a.get_command()

    def test_collection_exists(self):
        assert "settarg" in get_all_collections()

    @pytest.mark.xfail(
        reason="Type error when a non-string argument to ModuleCollection class",
        raises=TypeError,
    )
    def test_type_error(self):
        a = ModuleCollection(1)
