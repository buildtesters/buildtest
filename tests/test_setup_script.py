from pathlib import Path


def test_setup_script_avoids_unconditional_coverage_config_export():
    script = (Path(__file__).resolve().parents[1] / "setup.sh").read_text()

    assert "COVERAGE_PROCESS_START" in script
    assert 'if [ -f "$buildtest_root/.coveragerc" ]; then' in script


def test_sitecustomize_checks_for_coveragerc_before_startup():
    script = (Path(__file__).resolve().parent / "sitecustomize.py").read_text()

    assert "coverage.process_startup()" in script
    assert "os.path.exists(config_path)" in script
