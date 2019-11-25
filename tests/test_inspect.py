from buildtest.tools.list import list_software, list_modules, find_easyconfigs
from buildtest.tools.config import show_configuration
from buildtest.tools.system import distro_short, get_binaries_from_rpm
from buildtest.tools.sysconfig.configuration import func_system_view, func_system_fetch

def test_list_software():
  list_software()

def test_list_modules():
  list_modules()

def test_find_easyconfigs():
  find_easyconfigs()

def test_show_config():
  show_configuration()

def test_distro_short():
  assert "rhel" == distro_short("Red Hat Enterprise Linux Server")
  assert "centos" == distro_short("CentOS")
  assert "suse" == distro_short("SUSE Linux Enterprise Server")

def test_get_system_package_binaries():
  bins = get_binaries_from_rpm("gcc")
  assert len(bins) > 0
  assert "/usr/bin/gcc" in bins

def test_system_fetch():
  func_system_fetch()

def test_system_view():
  func_system_view()
