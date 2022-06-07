from statistics import mean, variance

from buildtest.cli.report import Report
from buildtest.defaults import console


def stats_cmd(args, report_file=None):

    results = Report(
        filter_args={"name": args.name},
        format_args="name,state,returncode,starttime,endtime,runtime",
        report_file=report_file,
    )

    first_result = Report(
        filter_args={"name": args.name},
        format_args="starttime",
        report_file=report_file,
        oldest=True,
    )
    last_result = Report(
        filter_args={"name": args.name},
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
    console.print(f"Mean Runtime {mean(runtimes):.6f}")
    console.print(f"Variance Runtime {variance(runtimes):0.6f}")

    results.print_report()
