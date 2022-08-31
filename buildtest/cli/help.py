from buildtest.defaults import console
from rich.table import Table


def print_build_help():
    """This method will print help message for command ``buildtest help build``"""

    table = Table(title="Building buildspecs", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest build -b <file>", "Build a single buildspec file")
    table.add_row(
        "buildtest build -b <dir>",
        "Build all buildspecs recursively in a given directory",
    )
    table.add_row(
        "buildtest build -b <file> -b <dir>", "Build buildspecs by file and directory"
    )
    table.add_row(
        "buildtest build -b <file> -b <dir> -x <file> -x <dir>",
        "Exclude files and directory when building buildspecs",
    )
    table.add_row(
        "buildtest build -t pass -t python",
        "Build buildspecs by tagname 'pass' and 'python'",
    )
    table.add_row(
        "buildtest build -e <executor1> -e <executor2>",
        "Building buildspecs by executor",
    )
    table.add_row(
        "buildtest build -b <file> -t <tagname1> -e <executor1>",
        "Building buildspecs with file, directory, tags, and executors",
    )
    table.add_row(
        "buildtest build -b tutorials  --filter type=script",
        "Build all tests in directory 'tutorials' and filter tests by type='script'",
    )
    table.add_row(
        "buildtest build -b tutorials  --filter tags=pass",
        "Build all tests in directory 'tutorials' and filter tests by tags='pass'",
    )
    table.add_row(
        "buildtest build -b tutorials  --filter maintainers=@bob",
        "Build all tests in directory 'tutorials' and filter tests by maintainers='@bob'",
    )
    table.add_row(
        "buildtest build --helpfilter",
        "Show list of filter fields used with --filter option",
    )
    table.add_row(
        "buildtest -c config.yml build -b <file>",
        "Use buildtest configuration file 'config.yml' ",
    )
    table.add_row("buildtest build -b <file> --rebuild 5", "Rebuild a test 5 times")
    table.add_row("buildtest build -b <file> --testdir /tmp", "Write tests in /tmp")

    table.add_row(
        "buildtest build --rerun", "Run last successful 'buildtest build' command"
    )
    table.add_row(
        "buildtest -r $HOME/python.json build -t python",
        "Write test to report file $HOME/python.json for all test run via 'python' tag",
    )
    table.add_row(
        "buildtest build -b <file> --module-purge --modules gcc,python",
        "For every test run 'module purge' and then load 'gcc' and 'python' module",
    )
    table.add_row(
        "buildtest build -b <file> --unload-modules gcc/9.3.0 --modules gcc/10.3.0",
        "For every test run 'module unload gcc/9.3.0' and then load 'gcc/10.3.0'",
    )
    table.add_row(
        "buildtest build -b /tmp/hostname.yml --maxpendtime 120 --pollinterval 10",
        "Poll jobs every 10 seconds and maximum pending time for jobs to 120 sec when submitting batch job. Job will be cancelled after 120sec if job is pending",
    )
    table.add_row(
        "buildtest build -b <file> --account dev",
        "Use project 'dev' when submitting batch jobs",
    )
    table.add_row(
        "buildtest build -b <file> --timeout 60",
        "Test will run till it reaches timeout of 60sec and then it will be cancelled if it exceeds the limit.",
    )

    console.print(table)


def print_buildspec_help():
    """This method will print help message for command ``buildtest help buildspec``"""

    table = Table(title="Finding Buildspecs", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest buildspec find",
        "Discover and validate all buildspecs and load all validated buildspecs in cache",
    )
    table.add_row("buildtest buildspec find --rebuild", "Rebuild cache file")
    table.add_row(
        "buildtest buildspec find --root /tmp --rebuild",
        "Discover buildspecs in /tmp and rebuild buildspec cache",
    )
    table.add_row(
        "buildtest buildspec find --quiet --rebuild",
        "Rebuild cache file but don't display output of cache",
    )
    table.add_row(
        "buildtest buildspec find --paths", "Print all root directories for buildspecs"
    )
    table.add_row(
        "buildtest buildspec find --buildspec",
        "List all available buildspecs from cache",
    )
    table.add_row(
        "buildtest buildspec find --executors", "List all unique executors from cache"
    )
    table.add_row(
        "buildtest buildspec find --filter type=script,tags=pass",
        "Filter buildspec cache based on type=script and  tags='pass'",
    )
    table.add_row(
        "buildtest buildspec find --filter buildspec=<path>",
        "Filter cache by buildspec file",
    )
    table.add_row(
        "buildtest buildspec find --format name,description",
        "Format table columns by field: 'name', and 'description'",
    )
    table.add_row("buildtest buildspec find --group-by-tags", "Group tests by tag name")
    table.add_row(
        "buildtest buildspec find --group-by-executor", "Group tests by executor name"
    )
    table.add_row("buildtest buildspec find --helpfilter", "Show all filter fields")
    table.add_row("buildtest buildspec find --helpformat", "Show all format fields")
    table.add_row("buildtest buildspec find --terse", "Display output in terse format")
    table.add_row("buildtest buildspec find invalid", "Show invalid buildspecs")
    table.add_row(
        "buildtest buildspec find invalid --error",
        "Show invalid buildspecs with error messages",
    )
    console.print(table)

    table = Table(title="Validating Buildspecs", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest buildspec validate -b <file>",
        "Validate a buildspec with JSON Schema",
    )
    table.add_row(
        "buildtest buildspec validate -b /tmp/ -x /tmp/network",
        "Validate all buildspecs in directory /tmp but exclude /tmp/network",
    )
    table.add_row(
        "buildtest buildspec validate -t python -t mac",
        "Validate all buildspecs for tagname 'python' and 'mac'",
    )
    table.add_row(
        "buildtest buildspec validate -e generic.local.bash",
        "Validate all buildspecs for executor 'generic.local.bash'",
    )

    console.print(table)

    table = Table(title="Additional Features of Buildspecs", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest buildspec summary", "Show summary of buildspec cache file")
    table.add_row(
        "buildtest buildspec summary --pager", "Pageants the output of summary"
    )
    table.add_row(
        "buildtest buildspec show python_hello",
        "Show content of buildspec based on test name 'python_hello'",
    )
    table.add_row(
        "buildtest buildspec show-fail",
        "Show content of buildspec on all failed tests",
    )
    table.add_row(
        "buildtest buildspec edit-test python_hello",
        "Open test 'python_hello' in editor and validate file upon closing",
    )
    table.add_row(
        "buildtest buildspec edit-file $BUILDTEST_ROOT/tutorials/sleep.yml",
        "Open file $BUILDTEST_ROOT/tutorials/sleep.yml in editor and validate file upon closing",
    )

    table.add_row(
        "buildtest buildspec maintainers find johndoe",
        "Find buildspec with maintainer name 'johndoe'",
    )
    table.add_row(
        "buildtest buildspec maintainers --list",
        "List all maintainers from buildspec cache",
    )
    table.add_row(
        "buildtest buildspec maintainers --list --terse --no-header",
        "List all maintainers in machine readable format without header",
    )
    table.add_row(
        "buildtest buildspec maintainers --breakdown",
        "Show breakdown of maintainers by buildspecs",
    )
    console.print(table)


def print_config_help():
    """This method will print help message for command ``buildtest help config``"""

    table = Table(title="Configuring Buildtest", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest config view", "View content of configuration file")
    table.add_row(
        "buildtest config validate", "Validate configuration file with JSON schema"
    )
    table.add_row(
        "buildtest config edit", "Edit configuration file in your preferred editor"
    )
    table.add_row(
        "buildtest config executors",
        "List all executors in flat listing from configuration file",
    )
    table.add_row(
        "buildtest config executors --yaml",
        "Show executor configuration in YAML format",
    )
    table.add_row(
        "buildtest config executors --json",
        "Show executor configuration in JSON format",
    )
    table.add_row(
        "buildtest config executors --disabled", "List all disabled executors"
    )
    table.add_row("buildtest config executors --json", "List all invalid executors")
    table.add_row("buildtest config path", "Show path to configuration file")
    table.add_row(
        "buildtest config systems",
        "List all available system entries in configuration file",
    )
    table.add_row(
        "buildtest -c /tmp/config.yml config validate",
        "Validate configuration file /tmp/config.yml",
    )
    table.add_row(
        "buildtest config compilers",
        "List all compilers from configuration file in flat listing",
    )
    table.add_row(
        "buildtest config compilers find",
        "Detect compilers and update configuration file",
    )
    table.add_row(
        "buildtest config compilers find --detailed --update",
        "Show detailed output when finding compiler and update configuration file with new compilers",
    )
    table.add_row(
        "buildtest config compilers test",
        "Test each compiler instance by performing module load test",
    )
    console.print(table)


def print_inspect_help():
    """This method will print help message for command ``buildtest help inspect``"""

    table = Table(title="Inspecting a test", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest inspect list",
        "Display all test names, ids, and corresponding buildspec file",
    )
    table.add_row("buildtest inspect list -t", "Show output in terse format")
    table.add_row(
        "buildtest inspect name hello", "Display last run for test name 'hello'"
    )
    table.add_row(
        "buildtest inspect name hello/9ac bar/ac9",
        "Display record for test 'hello/9ac' and 'bar/ac9'. Will find first match for each test ID",
    )
    table.add_row(
        "buildtest inspect buildspec tutorials/vars.yml",
        "Fetch latest runs for all tests in buildspec file 'tutorials/vars.yml'",
    )
    table.add_row(
        "buildtest inspect query -o exit1_fail",
        "Display content of output file for latest run for test name 'exit1_fail'",
    )
    table.add_row(
        "buildtest inspect query -e hello",
        "Display content of error file for test name 'hello'",
    )
    table.add_row(
        "buildtest inspect query exit1_fail/", "Display all runs for tests 'exit1_fail'"
    )
    table.add_row(
        "buildtest inspect query 'exit1_fail/(24|52)'",
        "Use regular expression when searching for test via 'buildtest inspect query'",
    )
    console.print(table)


def print_report_help():
    """This method will print help message for command ``buildtest help report``"""

    table = Table(title="Viewing Test Report", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest report", "Display all test results")
    table.add_row(
        "buildtest report --filter returncode=0", "Filter test results by returncode=0"
    )
    table.add_row(
        "buildtest report --filter state=PASS,tags=python",
        "Filter test by filter fields 'state', 'tags'.",
    )
    table.add_row(
        "buildtest report --filter buildspec=tutorials/vars.yml",
        "Filter report by buildspec file 'tutorials/vars.yml",
    )
    table.add_row(
        "buildtest report --format name,state,buildspec",
        "Format report table by field 'name', 'state', 'buildspec'",
    )
    table.add_row("buildtest report --helpfilter", "List all filter fields")
    table.add_row("buildtest report --helpformat", "List all format fields")
    table.add_row("buildtest report --latest", "Retrieve latest record for all tests")
    table.add_row("buildtest report --count", "Retrieve limited records for all tests")
    table.add_row(
        "buildtest -r /tmp/result.json report",
        "Read report file /tmp/result.json and display result",
    )
    table.add_row("buildtest report --failure", "Show all test failures")
    table.add_row("buildtest report --passed", "Show all test passed")
    table.add_row(
        "buildtest report --start 2022-01-01 --end 2022-01-05",
        "Show all test records in the date range from [2022-01-01, 2022-01-05]",
    )
    table.add_row("buildtest report --terse", "Print report in terse format")
    table.add_row("buildtest report list", "List all report files")
    table.add_row("buildtest report clear", "Remove content of default report file")
    table.add_row("buildtest report summary", "Show summary of test report")
    table.add_row(
        "buildtest report summary --detailed", "Show detailed summary of test report"
    )
    console.print(table)


def print_history_help():
    """This method will print help message for command ``buildtest help history``"""

    table = Table(title="Editing buildspec", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest history list", "List all build history files")
    table.add_row("buildtest history list --terse", "Print output in terse format")
    table.add_row(
        "buildtest history query 0", "Query content of history build identifier '0'"
    )
    table.add_row(
        "buildtest history query 0 --log", "Open logfile for build identifier '0'"
    )

    console.print(table)


def print_cdash_help():
    """This method will print help message for command ``buildtest help cdash``"""

    table = Table(title="Editing buildspec", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest cdash upload DEMO",
        "Upload all tests to cdash with build name 'DEMO'",
    )
    table.add_row(
        "buildtest cdash upload DEMO --open",
        "Upload test results to CDASH and open results in web browser",
    )
    table.add_row(
        "buildtest --report /tmp/result.json cdash upload DAILY_CHECK ",
        "Upload all tests from report file '/tmp/result.json' with build name DAILY_CHECK",
    )
    table.add_row(
        "buildtest cdash upload --site laptop DEMO",
        "Upload tests to CDASH with site named called 'laptop'",
    )

    table.add_row("buildtest cdash view", "Open CDASH project in web-browser")

    console.print(table)


def print_schema_help():
    """This method will print help message for command ``buildtest help schema``"""

    table = Table(title="Buildtest Schemas", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest schema", "Report all buildtest schema files")
    table.add_row(
        "buildtest schema -n script.schema.json -e ",
        "Show example for schema type script-v1.0-schema.json",
    )
    table.add_row(
        "buildtest schema -n script.schema.json -j",
        "Show content of JSON schema for script.schema.json",
    )
    console.print(table)


def print_stylecheck_help():
    """This method will print help message for command ``buildtest help stylecheck``"""

    table = Table(title="Buildtest stylecheck", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest stylecheck",
        "Run all style check without applying changes to codebase",
    )
    table.add_row(
        "buildtest stylecheck -a", "Run all style check and apply changes to codebase"
    )
    table.add_row("buildtest stylecheck --no-black", "Disable black style check")
    table.add_row("buildtest stylecheck --no-isort", "Disable isort check")
    table.add_row("buildtest stylecheck --no-pyflakes", "Disable pyflakes check")

    console.print(table)


def print_unittests_help():
    """This method will print help message for command ``buildtest help stylecheck``"""

    table = Table(title="Buildtest unittests", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest unittests", "Run all unittests, tests are executed via pytest"
    )
    table.add_row(
        "buildtest unittests --coverage",
        "Enable coverage reporting when running unittests",
    )
    table.add_row(
        "buildtest unittests --pytestopts '-vra'",
        "Pass pytest options '-vra' when running test",
    )
    table.add_row(
        "buildtest unittests --pytestopts '-m schema'",
        "Run all tests with marker name 'schema'. This is equivalent to 'pytest -m schema' ",
    )
    table.add_row(
        "buildtest unittests -s $BUILDTEST_ROOT/tests/cli/test_config.py",
        "Specify a list of files to run unittests instead of running all tests",
    )

    console.print(table)


def print_path_help():
    """This method will print help message for command ``buildtest help schema``"""

    table = Table(title="Get Path to Test", show_lines=False)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest path circle_area", "Get test root for test name 'circle_area'"
    )
    table.add_row(
        "buildtest path -t circle_area", "Get test script for test name 'circle_area'"
    )
    table.add_row(
        "buildtest path -o circle_area", "Get output file for test name 'circle_area'"
    )
    table.add_row(
        "buildtest path -e circle_area", "Get error file for test name 'circle_area'"
    )
    table.add_row(
        "buildtest path -b circle_area", "Get build script for test name 'circle area'"
    )
    table.add_row(
        "buildtest path --stagedir circle_area",
        "Get stage directory for test name 'circle_area'",
    )
    table.add_row(
        "buildtest path circle_area/abc",
        "Get test root for test name 'circle_area' starting with test ID 'abc'",
    )
    console.print(table)


def buildtest_help(command):
    """Entry point for ``buildtest help`` which display a summary of how to use buildtest commands

    Args:
        command (str): Name of buildtest command specified by ``buildtest help <command>``
    """

    if command in ["build", "bd"]:
        print_build_help()
    elif command in ["buildspec", "bc"]:
        print_buildspec_help()
    elif command in ["config", "cg"]:
        print_config_help()
    elif command in ["inspect", "it"]:
        print_inspect_help()
    elif command in ["report", "rt"]:
        print_report_help()
    elif command == "path":
        print_path_help()
    elif command in ["history", "hy"]:
        print_history_help()
    elif command == "cdash":
        print_cdash_help()
    elif command == "schema":
        print_schema_help()
    elif command in ["stylecheck", "style"]:
        print_stylecheck_help()
    elif command in ["unittests", "test"]:
        print_unittests_help()
