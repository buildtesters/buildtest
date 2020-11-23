from buildtest.config import check_settings


def test_check_settings():
    settings = check_settings(executor_check=False, retrieve_settings=True)
    assert isinstance(settings, dict)
    assert "executors" in settings.keys()
    assert "moduletool" in settings.keys()
    assert "load_default_buildspecs" in settings.keys()
