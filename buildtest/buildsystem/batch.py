class BatchScript:
    def get_headers(self):
        return self.headers


class LSFBatchScript(BatchScript):
    batch_translation = {
        "queue": "-q",
        "nodecount": "-nnodes",
        "cpucount": "-n",
        "timelimit": "-W",
        "memory": "-M",
        "account": "-P",
        "exclusive": "-x",
    }

    def __init__(self, batch=None, bsub=None):
        """
        :param batch: Input from  'batch' field that is scheduler agnostic configuration
        :param bsub: input from 'bsub' field in Buildspec inserted as #BSUB directive
        """

        self.headers = []
        self.directive = "#BSUB"

        self.batch = batch
        self.bsub = bsub

        self.build_header()

    def build_header(self):
        """Generate BSUB directive that will be part of the script"""

        # only process argument if bsub field is specified
        if self.bsub:
            for cmd in self.bsub:
                self.headers += [f"{self.directive} {cmd}"]

        # only process if batch field is specified
        if self.batch:

            for key, value in self.batch.items():

                if key == "exclusive" and self.batch[key] == True:
                    self.headers += [
                        f"{self.directive} {self.batch_translation['exclusive']}"
                    ]
                else:
                    self.headers += [
                        f"{self.directive} {self.batch_translation[key]} {value}"
                    ]


class SlurmBatchScript(BatchScript):
    batch_translation = {
        "queue": "--partition",
        "nodecount": "--nodes",
        "cpucount": "--ntasks",
        "timelimit": "--time",
        "memory": "--mem",
        "account": "--account",
        "exclusive": "--exclusive",
    }

    def __init__(self, batch=None, sbatch=None):
        """
        :param batch: The batch commands specified by batch field. These are scheduler agnostic fields
        :param sbatch: sbatch commands that are inserted with #SBATCH directive
        """
        self.headers = []
        self.directive = "#SBATCH"

        self.batch = batch
        self.sbatch = sbatch

        self.build_header()

    def build_header(self):
        """Generate SBATCH directive that will be part of the script"""

        # only process if sbatch field is specified
        if self.sbatch:
            for cmd in self.sbatch:
                self.headers += [f"{self.directive} {cmd}"]

        # only process if batch field is specified
        if self.batch:
            for key, value in self.batch.items():
                print(key, value)
                if key == "exclusive" and self.batch[key] == True:
                    self.headers += [
                        f"{self.directive} {self.batch_translation['exclusive']}=user"
                    ]
                else:
                    self.headers += [
                        f"{self.directive} {self.batch_translation[key]}={value}"
                    ]
