def print_build_help():
    """This method will print help message for command ``buildtest help build``"""

    msg = """
Building Buildspecs
--------------------

Command                                                     Description

buildtest build -b <file>                                   Build a single buildspec file
buildtest build -b <dir>                                    Build all buildspecs recursively in a given directory
buildtest build -b <file> -b <dir>                          Build buildspecs by file and directory
buildtest build -b <file> -b <dir> -x <file> -x <dir>       Exclude files and directory when building buildspecs
buildtest build -t pass  -t python                          Build buildspecs by tagname 'pass' and 'python'
buildtest build -e <executor1> -e <executor2>               Building buildspecs by executor
buildtest build -b <file> -t <tagname1> -e <executor1>      Building buildspecs with file, directory, tags, and executors
buildtest build -b tutorials  --filter type=script          Build all tests in directory 'tutorials' and filter tests by type='script'
buildtest build -b tutorials  --filter tags=pass            Build all tests in directory 'tutorials' and filter tests by tags='pass'
buildtest build -b tutorials  --filter maintainers=@bob     Build all tests in directory 'tutorials' and filter tests by maintainers='@bob'
buildtest build --helpfilter                                Show list of filter fields used with --filter option
buildtest -c config.yml build -b <file>                     Use buildtest configuration file 'config.yml' 
buildtest build -b <file> --rebuild 5                       Rebuild a test 5 times
buildtest build -b <file> --testdir /tmp                    Write tests in /tmp
"""

    print(msg)


def print_buildspec_help():
    """This method will print help message for command ``buildtest help buildspec``"""

    msg = """ 
Finding Buildspecs
----------------------

Command                                                     Description

buildtest buildspec find                                    Discover and validate all buildspecs and load all validated buildspecs in cache
buildtest buildspec find --rebuild                          Rebuild cache file
buildtest buildspec find --root /tmp --rebuild              Discover buildspecs in /tmp and rebuild buildspec cache
buildtest buildspec find --paths                            Print all root directories for buildspecs
buildtest buildspec find --buildspec                        List all available buildspecs from cache
buildtest buildspec find --tags                             List all unique tags from cache
buildtest buildspec find --executors                        List all unique executors from cache
buildtest buildspec find --maintainers                      List all maintainers from cache
buildtest buildspec find --maintainers-by-buildspecs        Show breakdown of all buildspecs by maintainer names.
buildtest buildspec find --filter type=script,tags=pass     Filter buildspec cache based on type=script and  tags='pass'
buildtest buildspec find --filter buildspec=<path>          Filter cache by buildspec file    
buildtest buildspec find --format name,description          Format table columns by field: 'name' and 'description 
buildtest buildspec find --group-by-tags                    Group tests by tag name
buildtest buildspec find --group-by-executor                Group tests by executor name            
buildtest buildspec find --helpfilter                       Show all filter fields
buildtest buildspec find --helpformat                       Show all format fields
buildtest buildspec find --terse                            Display output in terse format
buildtest buildspec find invalid                            Show invalid buildspecs
buildtest buildspec find invalid --error                    Show invalid buildspecs with error messages

Validate buildspecs
---------------------
    
Command                                                     Description

buildtest buildspec validate -b <file>                      Validate a buildspec with JSON Schema 
buildtest buildspec validate -b /tmp/ -x /tmp/network       Validate all buildspecs in directory /tmp but exclude /tmp/network
buildtest buildspec validate -t python -t mac               Validate all buildspecs for tagname 'python' and 'mac'
buildtest buildspec validate -e generic.local.bash          Validate all buildspecs for executor 'generic.local.bash'

Buildspec Summary
-------------------

Command                                                     Description

buildtest buildspec summary                                 Show summary of buildspec cache file 
    
Show Content of buildspec
--------------------------

Command                                                     Description

buildtest buildspec show python_hello                       Show content of buildspec based on test name 'python_hello' 
"""

    print(msg)


def print_config_help():
    """This method will print help message for command ``buildtest help config``"""

    msg = """
Buildtest Configuration 
------------------------

Command                                                     Description

buildtest config view                                       View content of configuration file
buildtest config validate                                   Validate configuration file with JSON schema
buildtest config executors                                  List all executors in flat listing from configuration file
buildtest config executors --yaml                           Show executors configuration in YAML format
buildtest config executors --json                           Show executors configuration in JSON format
buildtest config executors --disabled                       List all disabled executors
buildtest config executors --invalid                        List all invalid executors
buildtest config systems                                    List all available system entries in configuration file
buildtest -c /tmp/config.yml config validate                Validate configuration file /tmp/config.yml
buildtest config compilers                                  List all compilers from configuration file in flat listing
buildtest config compilers find                             Detect compilers and update configuration file
"""
    print(msg)


def print_inspect_help():
    """This method will print help message for command ``buildtest help inspect``"""
    msg = """
    
Inspecting a Test
------------------

Command                                                     Description

buildtest inspect list                                      Display all test names, ids and corresponding buildspec file
buildtest inspect list -t                                   Show output in terse format
buildtest inspect name hello                                Display all tests results
buildtest inspect name foo bar                              Display record of test name 'foo' and 'bar'
buildtest inspect buildspec tutorials/vars.yml              Fetch latest runs for all tests in buildspec file 'tutorials/vars.yml'      
buildtest inspect id <ID>                                   Display record of test by unique identifer
buildtest inspect query -o hello                            Display content of output file for test name 'hello'
buildtest inspect query -e hello                            Display content of error file for test name 'hello'
buildtest inspect query -d first -o -e foo  bar             Display first record of tests 'foo', 'bar', and show output and error file
buildtest inspect query -d all foo                          Display all runs for tests 'foo'
    """

    print(msg)


def print_report_help():
    """This method will print help message for command ``buildtest help report``"""
    msg = """    
View Test Report 
----------------

Command                                                     Description

buildtest report                                            Display all tests results
buildtest report --filter returncode=0                      Filter test results by returncode=0
buildtest report --filter state=PASS,tags=python            Filter test by multiple filter fields.
buildtest report --filter buildspec=tutorials/vars.yml      Filter report by buildspec file 'tutorials/vars.yml
buildtest report --format name,state,buildspec              Format report table by field 'name', 'state', 'buildspec'
buildtest report --helpfilter                               List all filter fields
buildtest report --helpformat                               List all format fields
buildtest report --oldest                                   Retrieve oldest record for all tests 
buildtest report --latest                                   Retrieve latest record for all tests 
buildtest report -r <report-file>                           Specify alternate report file to display test results
buildtest report --terse                                    Print report in terse format
buildtest report list                                       List all report files
buildtest report clear                                      Remove content of report file
buildtest report summary                                    Show summary of test report
    """
    print(msg)


def print_edit_help():
    """This method will print help message for command ``buildtest help edit``"""
    msg = """
Edit Buildspec
---------------

Command                                                     Description

buildtest edit tutorials/vars.yml                           Edit buildspec in your preferred editor defined by environment $EDITOR. Upon closing file, buildtest will validate buildspec with jsonschema 
"""
    print(msg)


def print_history_help():
    """This method will print help message for command ``buildtest help history``"""
    msg = """    
Build History
---------------
    

Command                                                     Description

buildtest history list                                      List all build history files 
buildtest history query 0                                   Query content of history build identifier '0' 
buildtest history query 0 --log                             Open logfile for build identifier '0'
"""
    print(msg)


def print_cdash_help():
    """This method will print help message for command ``buildtest help cdash``"""

    msg = """   
CDASH Support
---------------------

Command                                                     Description

buildtest cdash upload DEMO                                 Upload all tests to cdash with build name 'DEMO' 
buildtest cdash upload 'DAILY_CHECK' --report result.json   Upload all tests from report file result.json with build name 'DAILY_CHECK'
buildtest cdash upload --site laptop DEMO                   Upload tests to CDASH with site named called 'laptop' 
buildtest cdash upload -r /tmp/nightly.json nightly         Upload tests from /tmp/nightly.json to CDASH with buildname 'nightly'
buildtest cdash view                                        Open CDASH project in web-browser
buildtest cdash view --url <url>                            Open CDASH project in web-browser with a specified url
    """
    print(msg)


def print_schema_help():
    """This method will print help message for command ``buildtest help schema``"""
    msg = """
Schema Support
----------------------

Command                                                     Description

buildtest schema                                            Report all buildtest schema files 
buildtest schema -n script-v1.0-schema.json -e              Show example for schema type script-v1.0-schema.json
buildtest schema -n script-v1.0-schema.json -j              Show content of JSON schema for script-v1.0-schema.json 
"""
    print(msg)


def print_path_help():
    """This method will print help message for command ``buildtest help schema``"""
    msg = """

Get Test Path
-------------

Command                                                     Description

buildtest path circle_area                                  Get test root for test name 'circle_area'
buildtest path -t circle_area                               Get test script for test name 'circle_area'
buildtest path -o circle_area                               Get output file for test name 'circle_area'
buildtest path -e circle_area                               Get error file for test name 'circle_area'
buildtest path -b circle_area                               Get build script for test name 'circle_area'
buildtest path --stagedir circle_area                       Get stage directory for test name 'circle_area'
buildtest path circle_area/abc                              Get test root for test name 'circle_area' starting with test ID 'abc'
"""
    print(msg)


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
