from buildtest.cli.stats import stats_cmd


def test_stats():
    name = "exit1_fail"
    stats_cmd(name)
