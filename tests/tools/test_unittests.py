import os

import pytest

from buildtest.tools.unittests import resolve_unittest_config


def test_resolve_unittest_config_uses_explicit_file(tmp_path):
    config_file = tmp_path / "slurm.yml"
    config_file.write_text("testdir: /tmp/buildtest\n")

    assert resolve_unittest_config(str(config_file)) == str(config_file)


def test_resolve_unittest_config_uses_environment_file(tmp_path, monkeypatch):
    config_file = tmp_path / "custom.yml"
    config_file.write_text("testdir: /tmp/buildtest\n")
    monkeypatch.setenv("BUILDTEST_CONFIGFILE", str(config_file))

    assert resolve_unittest_config() == str(config_file)


def test_resolve_unittest_config_rejects_missing_file(tmp_path):
    with pytest.raises(SystemExit, match="Unable to find unittest configuration file"):
        resolve_unittest_config(os.fspath(tmp_path / "missing.yml"))
