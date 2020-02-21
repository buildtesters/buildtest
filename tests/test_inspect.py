from buildtest.tools.modules import list_software, list_modules
from buildtest.tools.config import show_configuration
from buildtest.tools.system import distro_short
from buildtest.tools.sysconfig.configuration import func_system_view, func_system_fetch
from buildtest.tools.show import show_schema_layout


def test_list_software():
    list_software()


# def test_list_modules():
#  list_modules()


def test_show_config():
    show_configuration()


def test_distro_short():
    assert "rhel" == distro_short("Red Hat Enterprise Linux Server")
    assert "centos" == distro_short("CentOS")
    assert "suse" == distro_short("SUSE Linux Enterprise Server")


def test_system_fetch():
    func_system_fetch()


def test_system_view():
    func_system_view()


def test_show_schema():
    show_schema_layout()
