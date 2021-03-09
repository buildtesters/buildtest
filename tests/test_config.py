from buildtest.config import check_settings
from buildtest.defaults import DEFAULT_SETTINGS_FILE


def test_check_settings():
    settings = check_settings(
        settings_path=DEFAULT_SETTINGS_FILE,
        executor_check=False,
        retrieve_settings=True,
    )
    print(settings)
    assert isinstance(settings, dict)
    # check required keys provided for all system name in configuration file
    for key in ["executors", "moduletool", "load_default_buildspecs", "hostnames"]:
        assert key in settings.keys()
