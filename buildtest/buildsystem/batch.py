class BatchScript:
    def get_headers(self):
        return self.headers


class LSFBatchScript(BatchScript):
    """This class is responsible for building LSF batch script by taking ``bsub`` property and converting them
    into #BSUB directives
    """

    def __init__(self, bsub):
        """
        :param batch: Input from  'batch' field that is scheduler agnostic configuration
        :param bsub: input from 'bsub' field in Buildspec inserted as #BSUB directive
        """

        self.headers = []
        self.directive = "#BSUB"

        self.bsub = bsub

        for cmd in self.bsub:
            self.headers += [f"{self.directive} {cmd}"]


class SlurmBatchScript(BatchScript):
    """This class is responsible for building Slurm batch script by taking ``sbatch`` property and converting them
    into #SBATCH directives
    """

    def __init__(self, sbatch):
        """
        :param batch: The batch commands specified by batch field. These are scheduler agnostic fields
        :param sbatch: sbatch commands that are inserted with #SBATCH directive
        """
        self.headers = []
        self.directive = "#SBATCH"

        self.sbatch = sbatch

        for cmd in self.sbatch:
            self.headers += [f"{self.directive} {cmd}"]


class CobaltBatchScript(BatchScript):
    """This class is responsible for building Cobalt batch script by taking ``cobalt`` property and converting them
    into #COBALT directives
    """

    def __init__(self, cobalt):
        """
        :param cobalt: cobalt commands that are inserted with #COBALT directive
        """
        self.headers = []
        self.directive = "#COBALT"

        self.cobalt = cobalt

        for cmd in self.cobalt:
            self.headers += [f"{self.directive} {cmd}"]


class PBSBatchScript(BatchScript):
    """This class is responsible for building PBS batch script by taking ``pbs`` property and converting them
    into #PBS directives
    """

    def __init__(self, pbs):
        """
        :param pbs: pbs commands that are inserted with #PBS directive
        """
        self.headers = []
        self.directive = "#PBS"

        self.pbs = pbs

        for cmd in self.pbs:
            self.headers += [f"{self.directive} {cmd}"]
