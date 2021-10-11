from buildtest.defaults import console
from rich.panel import Panel
from rich.table import Table


def print_build_help():
    """This method will print help message for command ``buildtest help build``"""

    table = Table(title="Building buildspecs", show_lines=True)
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

    console.print(table)


def print_buildspec_help():
    """This method will print help message for command ``buildtest help buildspec``"""

    table = Table(title="Finding Buildspecs", show_lines=True)
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
        "buildtest buildspec find --maintainers", "List all maintainers from cache"
    )
    table.add_row(
        "buildtest buildspec find --maintainers-by-buildspecs",
        "Show breakdown of all buildspecs by maintainer names",
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

    table = Table(title="Validating Buildspecs", show_lines=True)
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

    table = Table(title="Additional Features of Buildspecs", show_lines=True)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest buildspec summary", "Show summary of buildspec cache file")
    table.add_row(
        "buildtest buildspec show python_hello",
        "Show content of buildspec based on test name 'python_hello'",
    )
    console.print(table)


def print_config_help():
    """This method will print help message for command ``buildtest help config``"""

    table = Table(title="Configuring Buildtest", show_lines=True)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest config view", "View content of configuration file")
    table.add_row(
        "buildtest config validate", "Validate configuration file with JSON schema"
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
    console.print(table)


def print_inspect_help():
    """This method will print help message for command ``buildtest help inspect``"""

    table = Table(title="Inspecting a test", show_lines=True)
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
        "buildtest inspect query -o hello",
        "Display content of output file for test name 'hello'",
    )
    table.add_row(
        "buildtest inspect query -e hello",
        "Display content of error file for test name 'hello'",
    )
    table.add_row(
        "buildtest inspect query -d first -o -e foo bar",
        "Display first record of tests 'foo', 'bar', and show output and error file",
    )
    table.add_row(
        "buildtest inspect query -o hello", "Display all runs for tests 'foo'"
    )
    console.print(table)


def print_report_help():
    """This method will print help message for command ``buildtest help report``"""

    table = Table(title="Viewing Test Report", show_lines=True)
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
    table.add_row(
        "buildtest report -r <report-file>",
        "Specify alternate report file to display test results",
    )
    table.add_row("buildtest report --terse", "Print report in terse format")
    table.add_row("buildtest report list", "List all report files")
    table.add_row("buildtest report clear", "Remove content of default report file")
    table.add_row("buildtest report summary", "Show summary of test report")
    console.print(table)


def print_edit_help():
    """This method will print help message for command ``buildtest help edit``"""

    table = Table(title="Editing buildspec", show_lines=True)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest edit tutorials/vars.yml",
        "Edit buildspec 'tutorials/vars.yml' in your preferred editor defined by environment $EDITOR. Upon closing file, buildtest will validate buildspec with jsonschema",
    )
    console.print(table)


def print_history_help():
    """This method will print help message for command ``buildtest help history``"""

    table = Table(title="Editing buildspec", show_lines=True)
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

    table = Table(title="Editing buildspec", show_lines=True)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row(
        "buildtest cdash upload DEMO",
        "Upload all tests to cdash with build name 'DEMO'",
    )
    table.add_row(
        "buildtest cdash upload 'DAILY_CHECK' --report result.json",
        "Upload all tests from report file 'result.json' with build name 'DAILY_CHECK'",
    )
    table.add_row(
        "buildtest cdash upload --site laptop DEMO",
        "Upload tests to CDASH with site named called 'laptop'",
    )
    table.add_row(
        "buildtest cdash upload -r /tmp/nightly.json nightly",
        "Upload tests from /tmp/nightly.json to CDASH with buildname 'nightly'",
    )
    table.add_row("buildtest cdash view", "Open CDASH project in web-browser")
    table.add_row(
        "buildtest cdash view --url <url>",
        "Open CDASH project in web-browser with a specified url",
    )

    console.print(table)


def print_schema_help():
    """This method will print help message for command ``buildtest help schema``"""

    table = Table(title="Buildtest Schemas", show_lines=True)
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="magenta")

    table.add_row("buildtest schema", "Report all buildtest schema files")
    table.add_row(
        "buildtest schema -n script-v1.0-schema.json -e ",
        "Show example for schema type script-v1.0-schema.json",
    )
    table.add_row(
        "buildtest schema -n script-v1.0-schema.json -j",
        "Show content of JSON schema for script-v1.0-schema.json",
    )
    console.print(table)


def print_path_help():
    """This method will print help message for command ``buildtest help schema``"""

    table = Table(title="Get Path to Test", show_lines=True)
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

    if command == "build":
        print_build_help()
    elif command == "buildspec":
        print_buildspec_help()
    elif command == "config":
        print_config_help()
    elif command == "inspect":
        print_inspect_help()
    elif command == "report":
        print_report_help()
    elif command == "path":
        print_path_help()
    elif command == "edit":
        print_edit_help()
    elif command == "history":
        print_history_help()
    elif command == "cdash":
        print_cdash_help()
    elif command == "schema":
        print_schema_help()
