from buildtest.buildsystem.batch import (
    CobaltBatchScript,
    LSFBatchScript,
    PBSBatchScript,
    SlurmBatchScript,
)


def test_batchscript_example1():

    expected_header = [
        "#BSUB -P biology",
        "#BSUB -n 1",
        "#BSUB -M 500MB",
        "#BSUB -q debug",
        "#BSUB -W 10",
    ]
    script = LSFBatchScript(["-P biology", "-n 1", "-M 500MB", "-q debug", "-W 10"])
    header = script.get_headers()
    assert expected_header == header
    print("actual header %s and expected header: %s" % (header, expected_header))

    script = SlurmBatchScript(
        [
            "--account=biology",
            "--ntasks=1",
            "--mem=500MB",
            "--partition=debug",
            "--time=10",
        ]
    )
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

    script = CobaltBatchScript(
        ["--project biology", "--proccount 1", "--queue debug", "--time 10"]
    )
    header = script.get_headers()

    expected_header = [
        "#COBALT --project biology",
        "#COBALT --proccount 1",
        "#COBALT --queue debug",
        "#COBALT --time 10",
    ]

    assert header == expected_header

    script = PBSBatchScript(["-A biology", "-q debug", "-l nodes=1", "-l walltime=10"])
    headers = script.get_headers()
    expected_header = [
        "#PBS -A biology",
        "#PBS -q debug",
        "#PBS -l nodes=1",
        "#PBS -l walltime=10",
    ]
    expected_header == headers
