import os
import shutil
import yaml

from buildtest.tools.modulesystem.tree import module_tree_add, module_tree_list,\
    module_tree_rm, module_tree_set
from buildtest.tools.file import create_dir
from buildtest.tools.config import BUILDTEST_CONFIG_FILE

def test_module_tree_list():
    module_tree_list()

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
    """Testing if module tree can be set via command line ``buildtest module tree -s <tree>``. This will
        update the configuration."""
    module_tree_set(os.path.join(os.environ.get("LMOD_PKG"),"modulefiles/Core"))

    fd = open(BUILDTEST_CONFIG_FILE,"r")
    content = yaml.safe_load(fd)
    fd.close()

    assert os.path.join(os.environ.get("LMOD_PKG"), "modulefiles/Core") in content["BUILDTEST_MODULEPATH"]

    # undo set operation by removing tree
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