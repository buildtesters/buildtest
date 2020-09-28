from buildtest.buildsystem.batch import LSFBatchScript, SlurmBatchScript


def test_batchscript_example1():
    batch_cmds = {
        "account": "biology",
        "cpucount": "1",
        "memory": "500MB",
        "queue": "debug",
        "timelimit": "10",
    }
    expected_header = [
        "#BSUB -P biology",
        "#BSUB -n 1",
        "#BSUB -M 500MB",
        "#BSUB -q debug",
        "#BSUB -W 10",
    ]
    script = LSFBatchScript(batch_cmds)
    header = script.get_headers()
    assert expected_header == header
    print("actual header %s and expected header: %s" % (header, expected_header))

    script = SlurmBatchScript(batch_cmds)
    expected_header = [
        "#SBATCH --account=biology",
        "#SBATCH --ntasks=1",
        "#SBATCH --mem=500MB",
        "#SBATCH --partition=debug",
        "#SBATCH --time=10",
    ]
    header = script.get_headers()
    assert expected_header == header
    print("actual header %s and expected header: %s" % (header, expected_header))


def test_batchscript_example2():
    batch_cmds = {
        "tasks-per-node": "1",
        "cpucount": "2",
    }
    sbatch_cmd = ["-t 10", "-q normal"]
    script = SlurmBatchScript(batch_cmds, sbatch_cmd)
    header = script.get_headers()
    expected_header = [
        "#SBATCH -t 10",
        "#SBATCH -q normal",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --ntasks=2",
    ]
    assert expected_header == header

    bsub_cmds = ["-W 10", "-q normal"]
    script = LSFBatchScript(batch_cmds, bsub_cmds)
    header = script.get_headers()
    # tasks-per-node is not valid option in LSF so this option is skipped. bsub commands are processed first before batch
    expected_header = ["#BSUB -W 10", "#BSUB -q normal", "#BSUB -n 2"]
    assert expected_header == header
