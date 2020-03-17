from buildtest.menu.config import show_configuration
from buildtest.menu.show import show_schema_layout


def test_show_config():
    show_configuration()


def test_show_schema():
    class args:
        name = "script"
        version = "latest"

    show_schema_layout(args)
