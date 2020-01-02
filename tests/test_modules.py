import os
import pytest

from buildtest.tools.modules import check_spack_module, check_easybuild_module, \
    find_module_deps, get_module_permutation_choices
from buildtest.tools.modulesystem.module_difference import diff_trees
from buildtest.tools.log import BuildTestError

"""
def test_spack_modules():
    module_tree_add(["/mxg-hpc/users/ssi29/spack/modules/linux-rhel7-x86_64/Core"])
    check_spack_module()
    module_tree_rm(["/mxg-hpc/users/ssi29/spack/modules/linux-rhel7-x86_64/Core"])


def test_easybuild_modules():
    module_tree_add(["/opt/easybuild/modules/all"])
    check_easybuild_module()
    module_tree_rm(["/opt/easybuild/modules/all"])


def test_module_deps():
    module_tree_add(["/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core"])
    find_module_deps("GCCcore/8.1.0")
    module_tree_rm(["/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core"])

def test_diff_trees():
    diff_trees("/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core,/usr/share/lmod/lmod/modulefiles/Core/")

"""



def test_module_diff():
    """Testing module difference between two trees. First test is testing against same module tree, and the second
        test is against a different tree. """
    tree1 = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    tree2 = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    tree_list = f"{tree1},{tree2}"
    diff_trees(tree_list)

    tree_list=f"{tree1},/opt/easybuild/modules/all"
    diff_trees(tree_list)

@pytest.mark.xfail(raises=BuildTestError)
def test_module_diff_invalid_args():
    """Testing when one moduletree is passed to ``buildtest module --diff-trees``"""
    tree = os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core")
    diff_trees(tree)

def test_module_permutation_choices():
    keys = get_module_permutation_choices()
    print (keys)