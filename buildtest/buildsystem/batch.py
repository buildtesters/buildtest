class BatchScript:
    def get_headers(self):
        return self.headers


class LSFBatchScript(BatchScript):
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
    def __init__(self, pbs=None):
        """
        :param pbs: pbs commands that are inserted with #PBS directive
        """
        self.headers = []
        self.directive = "#PBS"

        self.pbs = pbs

        for cmd in self.pbs:
            self.headers += [f"{self.directive} {cmd}"]
