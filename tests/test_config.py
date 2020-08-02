from buildtest.config import (
    load_settings,
    check_settings,
)


def test_check_settings():
    settings = load_settings()
    check_settings(executor_check=False)
    assert "config" in settings.keys()
    assert "executors" in settings.keys()
