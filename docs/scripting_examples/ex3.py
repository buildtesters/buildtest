from buildtest.config import load_settings
from buildtest.menu.build import discover_buildspecs, resolve_testdirectory, build_phase
from buildtest.menu.buildspec import parse_buildspecs

tagname = ["tutorials"]
print(f"Searching by tagname: {tagname}")
included_bp, excluded_bp = discover_buildspecs(tags=tagname, debug=True)

configuration = load_settings()
testdir = resolve_testdirectory(configuration)
builders = parse_buildspecs(included_bp, testdir, rebuild=1, printTable=True)

build_phase(builders, printTable=True)
