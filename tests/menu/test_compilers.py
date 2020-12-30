import os
import pytest
from buildtest.menu.compilers import BuildtestCompilers
from buildtest.exceptions import BuildTestError

here = os.path.dirname(os.path.abspath(__file__))


class TestBuildtestCompilers:

    bc = BuildtestCompilers()

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
        bc = BuildtestCompilers(settings_file=settings_file)
        with pytest.raises(BuildTestError):
            bc.find_compilers()

    def test_missing_compiler_find(self):
        settings_file = os.path.join(
            here, "test_compilers", "missing_compiler_find.yml"
        )
        print(f"Using settings file: {settings_file} for loading compilers")
        bc = BuildtestCompilers(settings_file=settings_file)
        with pytest.raises(BuildTestError):
            bc.find_compilers()
