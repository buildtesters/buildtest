from buildtest.tools.stylecheck import run_style_checks


def test_run_style_check():
    run_style_checks(
        no_black=False, no_isort=False, no_pyflakes=False, apply_stylechecks=False
    )
