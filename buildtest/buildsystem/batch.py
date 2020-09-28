class BatchScript:
    def get_headers(self):
        return self.headers


class LSFBatchScript(BatchScript):
    batch_translation = {
        "account": "-P",
        "begintime": "-b",
        "cpucount": "-n",
        "email-address": "-u",
        "exclusive": "-x",
        "memory": "-M",
        "nodecount": "-nnodes",
        "qos": None,
        "queue": "-q",
        "tasks-per-node": None,
        "timelimit": "-W",
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
                # if batch key is None that means scheduler doesn't support the option
                elif not self.batch[key]:
                    continue
                else:
                    self.headers += [
                        f"{self.directive} {self.batch_translation[key]} {value}"
                    ]


class SlurmBatchScript(BatchScript):
    batch_translation = {
        "account": "--account",
        "begintime": "--begin",
        "cpucount": "--ntasks",
        "email-address": "--mail-user",
        "exclusive": "--exclusive",
        "memory": "--mem",
        "nodecount": "--nodes",
        "qos": "--qos",
        "queue": "--partition",
        "tasks-per-node": "--ntasks-per-node",
        "timelimit": "--time",
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
                if key == "exclusive" and self.batch[key] == True:
                    self.headers += [
                        f"{self.directive} {self.batch_translation['exclusive']}=user"
                    ]
                # if batch key is None that means scheduler doesn't support the option
                elif not self.batch[key]:
                    continue
                else:
                    self.headers += [
                        f"{self.directive} {self.batch_translation[key]}={value}"
                    ]
