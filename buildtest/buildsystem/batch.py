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
        "network": "-network",
        "nodecount": "-nnodes",
        "qos": None,
        "queue": "-q",
        "tasks-per-core": None,
        "tasks-per-node": None,
        "tasks-per-socket": None,
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
                elif not self.batch_translation.get(key):
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
        "network": "--network",
        "nodecount": "--nodes",
        "qos": "--qos",
        "queue": "--partition",
        "tasks-per-core": "--ntasks-per-core",
        "tasks-per-node": "--ntasks-per-node",
        "tasks-per-socket": "--ntasks-per-socket",
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
                elif not self.batch_translation.get(key):
                    continue
                else:
                    self.headers += [
                        f"{self.directive} {self.batch_translation[key]}={value}"
                    ]


class CobaltBatchScript(BatchScript):
    batch_translation = {
        "account": "--project",
        "begintime": None,
        "cpucount": "--proccount",
        "email-address": "--notify",
        "exclusive": None,
        "memory": None,
        "network": None,
        "nodecount": "--nodecount",
        "qos": None,
        "queue": "--queue",
        "tasks-per-core": None,
        "tasks-per-node": None,
        "tasks-per-socket": None,
        "timelimit": "--time",
    }

    def __init__(self, batch=None, cobalt=None):
        """
        :param batch: The batch commands specified by batch field. These are scheduler agnostic fields
        :param sbatch: sbatch commands that are inserted with #SBATCH directive
        """
        self.headers = []
        self.directive = "#COBALT"

        self.batch = batch
        self.cobalt = cobalt

        self.build_header()

    def build_header(self):
        # only process if sbatch field is specified
        if self.cobalt:
            for cmd in self.cobalt:
                self.headers += [f"{self.directive} {cmd}"]

        # only process if batch field is specified
        if self.batch:
            for key, value in self.batch.items():

                # if batch key is None that means scheduler doesn't support the option
                if self.batch_translation.get(key):
                    self.headers += [
                        f"{self.directive} {self.batch_translation[key]} {value}"
                    ]
                else:
                    continue


class PBSBatchScript(BatchScript):
    batch_translation = {
        "account": "project",
        "begintime": None,
        "cpucount": "-l ncpus",
        "email-address": "-WMail_Users",
        "exclusive": None,
        "memory": "-l mem",
        "network": None,
        "nodecount": "-l nodes",
        "qos": None,
        "queue": "-q",
        "tasks-per-core": None,
        "tasks-per-node": None,
        "tasks-per-socket": None,
        "timelimit": "-l walltime",
    }

    def __init__(self, batch=None, pbs=None):
        """
        :param batch: The batch commands specified by batch field. These are scheduler agnostic fields
        :param pbs: pbs commands that are inserted with #PBS directive
        """
        self.headers = []
        self.directive = "#PBS"

        self.batch = batch
        self.pbs = pbs

        self.build_header()

    def build_header(self):
        # only process if sbatch field is specified
        if self.pbs:
            for cmd in self.pbs:
                self.headers += [f"{self.directive} {cmd}"]

        # only process if batch field is specified
        if self.batch:
            for key, value in self.batch.items():

                # if batch key is None that means scheduler doesn't support the option
                if self.batch_translation.get(key):
                    self.headers += [
                        f"{self.directive} {self.batch_translation[key]}={value}"
                    ]
                else:
                    continue


def get_sbatch_lines(name, sbatch, batch):
    """This method will return a list of lines with #SBATCH directive given an input ``sbatch`` and ``batch`` key.
    :param name: The name of the Slurm job, output and error file.
    :type name: str
    :param sbatch: ``bsub`` key from buildspec that defines #BSUB directives
    :type sbatch: list
    :param batch: ``batch`` key from buildspec that defines a key/value pair of scheduler configuration
    :type: dict
    """

    lines = []
    script = SlurmBatchScript(batch=batch, sbatch=sbatch)
    lines += script.get_headers()
    lines += [f"#SBATCH --job-name={name}"]
    lines += [f"#SBATCH --output={name}.out"]
    lines += [f"#SBATCH --error={name}.err"]

    return lines


def get_bsub_lines(name, bsub, batch):
    """This method will return a list of lines with #BSUB directive given an input ``bsub`` and ``batch`` key.
    :param name: The name of the LSF job, output and error file.
    :type name: str
    :param bsub: ``bsub`` key from buildspec that defines #BSUB directives
    :type bsub: list
    :param batch: ``batch`` key from buildspec that defines a key/value pair of scheduler configuration
    :type: dict
    """

    lines = []
    script = LSFBatchScript(batch=batch, bsub=bsub)

    lines += script.get_headers()
    lines += [f"#BSUB -J {name}"]
    lines += [f"#BSUB -o {name}.out"]
    lines += [f"#BSUB -e {name}.err"]

    return lines


def get_pbs_lines(name, pbs, batch):
    """This method will return a list of lines with #PBS directive given an input ``pbs`` and ``batch`` key.
    :param name: The name of the PBS job, output and error file.
    :type name: str
    :param bsub: ``bsub`` key from buildspec that defines #BSUB directives
    :type bsub: list
    :param batch: ``batch`` key from buildspec that defines a key/value pair of scheduler configuration
    :type: dict
    """

    lines = []
    script = PBSBatchScript(batch=batch, pbs=pbs)

    lines += script.get_headers()
    lines += [f"#PBS -N {name}"]

    return lines


def get_cobalt_lines(name, cobalt, batch):
    """This method will return a list of lines with #COBALT directive given an input ``cobalt`` and ``batch`` key.
    :param name: The name of the Cobalt job, output and error file.
    :type name: str
    :param cobalt: ``bsub`` key from buildspec that defines #BSUB directives
    :type cobalt: list
    :param batch: ``batch`` key from buildspec that defines a key/value pair of scheduler configuration
    :type: dict
    """

    lines = []
    script = CobaltBatchScript(batch=batch, cobalt=cobalt)

    lines += script.get_headers()
    lines += [f"#COBALT --jobname {name}"]

    return lines
