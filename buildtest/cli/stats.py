from statistics import StatisticsError, mean, variance

from buildtest.cli.report import Report
from buildtest.defaults import console
from buildtest.exceptions import BuildTestError


def stats_cmd(name, report_file=None):
    """Entry Point for ``buildtest stats``

    Args:
        name: Name of test specified command line via ``buildtest stats <name>``
        report_file (str, optional): Path to report file for querying results
    """
    results = Report(
        filter_args={"name": name},
        format_args="name,state,returncode,starttime,endtime,runtime",
        report_file=report_file,
    )

    first_result = Report(
        filter_args={"name": name},
        format_args="starttime",
        report_file=report_file,
        oldest=True,
    )
    last_result = Report(
        filter_args={"name": name},
        format_args="starttime",
        report_file=report_file,
        latest=True,
    )

    console.print("Total Test Runs: ", len(results.display_table["name"]))
    console.print("First Run:", first_result.display_table["starttime"][0])
    console.print("Last Run:", last_result.display_table["starttime"][0])

    console.print("Fastest Runtime: ", min(results.display_table["runtime"]))
    console.print("Slowest Runtime: ", max(results.display_table["runtime"]))

    # need to convert all items to float since each item is str
    runtimes = [float(runtime) for runtime in results.display_table["runtime"]]
    test_variance = variance(runtimes) if len(runtimes) > 1 else 0
    console.print(f"Mean Runtime {mean(runtimes):.6f}")
    console.print(f"Variance Runtime {test_variance:0.6f}")

    results.print_report()
