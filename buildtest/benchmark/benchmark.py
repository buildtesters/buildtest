from buildtest.benchmark.osu import run_osu_microbenchmark, list_osu_tests, osu_info


def func_benchmark_osu_subcmd(args):
    """ OSU submenu entry point"""
    if args.run:
        run_osu_microbenchmark(args.config)
    if args.list:
        list_osu_tests()
    if args.info:
        osu_info()
