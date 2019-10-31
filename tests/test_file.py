import pytest

from buildtest.tools.file  import is_dir, is_file
from buildtest.tools.log import BuildTestError

@pytest.mark.xfail(raises=BuildTestError)
def test_checking_directory():
  is_dir("/xyz123")

@pytest.mark.xfail(raises=BuildTestError)
def test_checking_file():
  is_file("$HOME/foo+boo.txt")

def test_directory_expansion():
  is_dir("$HOME")
  is_dir("~")

def test_check_file():
    is_file("~/.profile")
    is_file("$HOME/.profile")