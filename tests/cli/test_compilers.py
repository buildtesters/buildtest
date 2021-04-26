import os
import pytest
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.exceptions import BuildTestError, ConfigurationError

here = os.path.dirname(os.path.abspath(__file__))


class TestBuildtestCompilers:
    configuration = SiteConfiguration()
    configuration.get_current_system()
    configuration.validate()
    bc = BuildtestCompilers(configuration)

    def test_init(self):

        assert hasattr(self.bc, "compilers")
        assert isinstance(self.bc.names, list)

    def test_print(self):
        self.bc.print_yaml()
        self.bc.print_json()
        self.bc.print_compilers()

    def test_invalid_moduletool(self):
        settings_file = os.path.join(here, "test_compilers", "invalid_moduletool.yml")
        print(f"Using settings file: {settings_file} for loading compilers")

        configuration = SiteConfiguration(settings_file)
        configuration.get_current_system()
        configuration.validate()

        bc = BuildtestCompilers(configuration=configuration)
        with pytest.raises(ConfigurationError):
            bc.find_compilers()

    def test_missing_compiler_find(self):
        settings_file = os.path.join(
            here, "test_compilers", "missing_compiler_find.yml"
        )
        print(f"Using settings file: {settings_file} for loading compilers")

        configuration = SiteConfiguration(settings_file)
        configuration.get_current_system()
        configuration.validate()

        bc = BuildtestCompilers(configuration=configuration)

        with pytest.raises(BuildTestError):
            bc.find_compilers()
