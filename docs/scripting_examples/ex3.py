from buildtest.config import load_settings
from buildtest.menu.build import discover_buildspecs, resolve_testdirectory, build_phase
from buildtest.menu.buildspec import parse_buildspecs

tagname = ["tutorials"]
print(f"Searching by tagname: {tagname}")
included_bp, excluded_bp = discover_buildspecs(tags=tagname, debug=True)

configuration = load_settings()
testdir = resolve_testdirectory(configuration)
buildspec_filters = {"tags": None, "executors": ["local.bash"]}
builders = parse_buildspecs(
    buildspecs=included_bp,
    test_directory=testdir,
    filters=buildspec_filters,
    rebuild=1,
    printTable=True,
)

build_phase(builders, printTable=True)
