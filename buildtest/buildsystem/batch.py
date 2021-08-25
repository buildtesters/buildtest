class BatchScript:
    def get_headers(self):
        return self.headers


class LSFBatchScript(BatchScript):
    def __init__(self, bsub=None):
        """
        :param batch: Input from  'batch' field that is scheduler agnostic configuration
        :param bsub: input from 'bsub' field in Buildspec inserted as #BSUB directive
        """

        self.headers = []
        self.directive = "#BSUB"

        self.bsub = bsub

        self.build_header()

    def build_header(self):
        """Generate BSUB directive that will be part of the script"""

        # only process argument if bsub field is specified
        if self.bsub:
            for cmd in self.bsub:
                self.headers += [f"{self.directive} {cmd}"]


class SlurmBatchScript(BatchScript):
    def __init__(self, sbatch=None):
        """
        :param batch: The batch commands specified by batch field. These are scheduler agnostic fields
        :param sbatch: sbatch commands that are inserted with #SBATCH directive
        """
        self.headers = []
        self.directive = "#SBATCH"

        self.sbatch = sbatch

        self.build_header()

    def build_header(self):
        """Generate SBATCH directive that will be part of the script"""

        # only process if sbatch field is specified
        if self.sbatch:
            for cmd in self.sbatch:
                self.headers += [f"{self.directive} {cmd}"]


class CobaltBatchScript(BatchScript):
    def __init__(self, cobalt=None):
        """
        :param cobalt: cobalt commands that are inserted with #COBALT directive
        """
        self.headers = []
        self.directive = "#COBALT"

        self.cobalt = cobalt

        self.build_header()

    def build_header(self):
        # only process if sbatch field is specified
        if self.cobalt:
            for cmd in self.cobalt:
                self.headers += [f"{self.directive} {cmd}"]


class PBSBatchScript(BatchScript):
    def __init__(self, batch=None, pbs=None):
        """
        :param batch: The batch commands specified by batch field. These are scheduler agnostic fields
        :param pbs: pbs commands that are inserted with #PBS directive
        """
        self.headers = []
        self.directive = "#PBS"

        self.pbs = pbs

        self.build_header()

    def build_header(self):
        # only process if sbatch field is specified
        if self.pbs:
            for cmd in self.pbs:
                self.headers += [f"{self.directive} {cmd}"]
