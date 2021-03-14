from buildtest.config import check_settings, BuildtestConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_FILE


def test_check_settings():
    settings = check_settings(
        settings_path=DEFAULT_SETTINGS_FILE,
        executor_check=False,
    )

    assert settings
    assert isinstance(settings, BuildtestConfiguration)
