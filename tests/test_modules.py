import yaml
import os
import shutil
from buildtest.tools.modules import check_spack_module, check_easybuild_module, \
    find_module_deps
from buildtest.tools.modulesystem.tree import module_tree_add, module_tree_list,\
    module_tree_rm, module_tree_set
from buildtest.tools.config import BUILDTEST_CONFIG_FILE
from buildtest.tools.file import create_dir

def test_spack_modules():
    check_spack_module()

def test_easybuild_modules():
    check_easybuild_module()

#def test_module_deps():
#    find_module_deps("GCCcore/8.1.0")


def test_module_tree_add_and_remove():
    #module_tree_list()
    module_tree_add(["/usr/share/lmod/lmod/modulefiles/Core/"])
    #module_tree_list()

    fd = open(BUILDTEST_CONFIG_FILE,"r")
    content = yaml.safe_load(fd)
    fd.close()

    assert True == ("/usr/share/lmod/lmod/modulefiles/Core/" in content["BUILDTEST_MODULEPATH"])

    module_tree_rm(["/usr/share/lmod/lmod/modulefiles/Core/"])

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()

    assert True == ("/usr/share/lmod/lmod/modulefiles/Core/" not in content["BUILDTEST_MODULEPATH"])

def test_module_tree_set():
    module_tree_set("/usr/share/lmod/lmod/modulefiles/Core/")

    fd = open(BUILDTEST_CONFIG_FILE,"r")
    content = yaml.safe_load(fd)
    fd.close()

    assert True == ("/usr/share/lmod/lmod/modulefiles/Core/" in content["BUILDTEST_MODULEPATH"])

    module_tree_rm(["/usr/share/lmod/lmod/modulefiles/Core/"])

def test_module_tree_with_directory_expansion():

    dir1 = "$HOME/x1"
    dir2 = "~/x2"
    create_dir(dir1)
    create_dir(dir2)

    module_tree_add([dir1])

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()

    assert True == (os.path.expandvars(dir1) in content["BUILDTEST_MODULEPATH"])
    module_tree_rm([dir1])

    module_tree_add([dir2])

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()

    assert True == (os.path.expanduser(dir2) in content["BUILDTEST_MODULEPATH"])
    module_tree_rm([dir2])

    shutil.rmtree(os.path.expandvars(dir1))
    shutil.rmtree(os.path.expanduser(dir2))
