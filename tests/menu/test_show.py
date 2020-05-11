from buildtest.menu.show import show_schema_layout


class script_schema:
    _global = False
    name = "script"
    version = "latest"


class script_mismatch_version_schema:
    _global = False
    name = "script"
    # invalid version for script schema this should resort to latest schema
    version = "99.99"


class global_schema:
    _global = True
    name = None
    version = None


def test_show_schema():

    show_schema_layout(script_schema)
    show_schema_layout(global_schema)
    show_schema_layout(script_mismatch_version_schema)
