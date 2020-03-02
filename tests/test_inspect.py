from buildtest.tools.config import show_configuration
from buildtest.tools.system import distro_short
from buildtest.tools.show import show_schema_layout


def test_show_config():
    show_configuration()

def test_distro_short():
    assert "rhel" == distro_short("Red Hat Enterprise Linux Server")
    assert "centos" == distro_short("CentOS")
    assert "suse" == distro_short("SUSE Linux Enterprise Server")


def test_show_schema():
    show_schema_layout()
