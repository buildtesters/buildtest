import textwrap

from buildtest.tools.config import show_configuration
from buildtest.tools.yaml import KEY_DESCRIPTION, SLURM_KEY_DESC, \
    LSF_KEY_DESC, MPI_KEY_DESC, ORTERUN_KEY_DESC, MPIEXEC_KEY_DESC


def func_show_subcmd(args):
    """Entry point to ``buildtest show`` sub command.

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    if args.config:
        show_configuration()

    if args.keys:
        show_yaml_keys()


def show_yaml_keys():
    """The method implements command ``buildtest show -k singlesource``.
    This method display the yaml keys for testblock:singlesource.
    """

    print ('{:>50}'.format("General Keys"))

    print ('{:20} | {:<30}'.format("Keys", "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(KEY_DESCRIPTION):
        print('{:20} | {:<30}'.format(k, textwrap.fill(KEY_DESCRIPTION[k], 120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("LSF Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "LSF Equivalents",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(LSF_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                        textwrap.fill(LSF_KEY_DESC[k][0],120),
                                        textwrap.fill(LSF_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("SLURM Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "Slurm Equivalents",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(SLURM_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                    textwrap.fill(SLURM_KEY_DESC[k][0],120),
                                    textwrap.fill(SLURM_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("MPI Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "MPI Launchers",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(MPI_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                    textwrap.fill(MPI_KEY_DESC[k][0],120),
                                    textwrap.fill(MPI_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("ORTERUN Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "ORTERUN Options",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(ORTERUN_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                    textwrap.fill(ORTERUN_KEY_DESC[k][0],120),
                                    textwrap.fill(ORTERUN_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("MPIEXEC.HYDRA Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "MPIEXEC.HYDRA Options",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(MPIEXEC_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                               textwrap.fill(
                                                   MPIEXEC_KEY_DESC[k][0], 120),
                                               textwrap.fill(
                                                   MPIEXEC_KEY_DESC[k][1],
                                                   120)))
