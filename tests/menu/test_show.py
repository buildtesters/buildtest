from buildtest.menu.show import show_schema_layout

def test_show_schema():
    class args:
        name = "script"
        version = "latest"

    show_schema_layout(args)
