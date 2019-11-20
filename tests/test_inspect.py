
import os
import sys

#sys.path.insert(0, os.path.join(os.getenv("BUILDTEST_ROOT"), 'src'))
#sys.path.insert(0,"/u/users/ssi29/.local/share/virtualenvs/buildtest-framework-LDt8wyRf/lib/python3.7/site-packages")

from buildtest.tools.list import list_software, list_modules, find_easyconfigs
from buildtest.tools.config import show_configuration


def test_list_software():
  list_software()

def test_list_modules():
  list_modules()

def test_find_easyconfigs():
  find_easyconfigs()

def test_show_config():
  show_configuration()
