from buildtest.config import load_settings
from buildtest.menu.build import discover_buildspecs, resolve_testdirectory, build_phase
from buildtest.menu.build import parse_buildspecs
from buildtest.executors.setup import BuildExecutor

tagname = ["pass"]
print(f"Searching by tagname: {tagname}")
included_bp, excluded_bp = discover_buildspecs(tags=tagname, debug=True)

configuration = load_settings()
testdir = resolve_testdirectory(configuration)

executor = BuildExecutor(configuration)
buildspec_filters = {"tags": None }
builders = parse_buildspecs(
    buildspecs=included_bp,
    executor=executor,
    test_directory=testdir,
    filters=buildspec_filters,
    rebuild=1,
    printTable=True,
)

build_phase(builders, printTable=True)
