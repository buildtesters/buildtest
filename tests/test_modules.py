import yaml
import os
import shutil
from buildtest.tools.modules import check_spack_module, check_easybuild_module, \
    find_module_deps
from buildtest.tools.modulesystem.module_difference import diff_trees
from buildtest.tools.modulesystem.tree import module_tree_add, module_tree_list,\
    module_tree_rm, module_tree_set
from buildtest.tools.config import BUILDTEST_CONFIG_FILE
from buildtest.tools.file import create_dir

"""
def test_spack_modules():
    module_tree_add(["/mxg-hpc/users/ssi29/spack/modules/linux-rhel7-x86_64/Core"])
    check_spack_module()
    module_tree_rm(["/mxg-hpc/users/ssi29/spack/modules/linux-rhel7-x86_64/Core"])

def test_easybuild_modules():
    module_tree_add(["/mxg-hpc/users/ssi29/easybuild/modules/all"])
    check_easybuild_module()
    module_tree_rm(["/mxg-hpc/users/ssi29/easybuild/modules/all"])

def test_module_deps():
    module_tree_add(["/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core"])
    find_module_deps("GCCcore/8.1.0")
    module_tree_rm(["/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core"])

def test_diff_trees():
    diff_trees("/mxg-hpc/users/ssi29/easybuild-HMNS/modules/all/Core,/usr/share/lmod/lmod/modulefiles/Core/")

"""

def test_module_tree_add_and_remove():

    module_tree_add([os.path.join(os.environ.get("LMOD_PKG"),"modulefiles/Core")])


    fd = open(BUILDTEST_CONFIG_FILE,"r")
    content = yaml.safe_load(fd)
    fd.close()

    assert os.path.join(os.environ.get("LMOD_PKG"),"modulefiles/Core") in content["BUILDTEST_MODULEPATH"]

    module_tree_rm([os.path.join(os.environ.get("LMOD_PKG"),"modulefiles/Core")])

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()

    assert os.path.join(os.environ.get("LMOD_PKG"),"modulefiles/Core") not in content["BUILDTEST_MODULEPATH"]

def test_module_tree_set():
    module_tree_set(os.path.join(os.environ.get("LMOD_PKG"),"modulefiles/Core"))

    fd = open(BUILDTEST_CONFIG_FILE,"r")
    content = yaml.safe_load(fd)
    fd.close()

    assert os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core") in content["BUILDTEST_MODULEPATH"]

    module_tree_rm([os.path.join(os.environ.get("LMOD_PKG"),"modulefiles/Core")])

def test_module_tree_with_directory_expansion():

    dir1 = "$HOME/x1"
    dir2 = "~/x2"
    create_dir(dir1)
    create_dir(dir2)

    module_tree_add([dir1])

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()

    assert True is (os.path.expandvars(dir1) in content["BUILDTEST_MODULEPATH"])
    module_tree_rm([dir1])

    module_tree_add([dir2])

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()

    assert True is (os.path.expanduser(dir2) in content["BUILDTEST_MODULEPATH"])
    module_tree_rm([dir2])

    shutil.rmtree(os.path.expandvars(dir1))
    shutil.rmtree(os.path.expanduser(dir2))
