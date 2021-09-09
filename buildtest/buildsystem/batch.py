class BatchScript:
    """Base class used for generating Batch directives for Schedulers"""

    def get_headers(self):
        return self.headers


class LSFBatchScript(BatchScript):
    """This class is responsible for building LSF batch script by taking ``bsub`` property and converting them into **#BSUB** directives"""

    def __init__(self, bsub):
        """This method will return a list of #BSUB directives used in job script

        Args:
            bsub (list): List of string items specified by ``bsub`` property in buildspec used for specified #BSUB directive

        Returns:
            list: A list of **#BSUB** directive that will be inserted for LSF Job Script
        """

        self.headers = []
        self.directive = "#BSUB"

        self.bsub = bsub

        for cmd in self.bsub:
            self.headers += [f"{self.directive} {cmd}"]


class SlurmBatchScript(BatchScript):
    """This class is responsible for building Slurm batch script by taking ``sbatch`` property and converting them into #SBATCH directives"""

    def __init__(self, sbatch):
        """This method will return a list of #Slurm directives used in job script

         Args:
             sbatch (list): List of string items specified by ``sbatch`` property in buildspec used for specified #SBATCH directive

        Returns:
            list: A list of **#SBATCH** directive that will be inserted for Slurm Job Script
        """
        self.headers = []
        self.directive = "#SBATCH"

        self.sbatch = sbatch

        for cmd in self.sbatch:
            self.headers += [f"{self.directive} {cmd}"]


class CobaltBatchScript(BatchScript):
    """This class is responsible for building Cobalt batch script by taking ``cobalt`` property and converting them into #COBALT directives"""

    def __init__(self, cobalt):
        """This method will return a list of #Cobalt directives used in job script

         Args:
             cobalt (list): List of string items specified by ``cobalt`` property in buildspec used for specified **#COBALT** directive

        Returns:
            list: A list of **#COBALT** directive that will be inserted for Cobalt Job Script
        """
        self.headers = []
        self.directive = "#COBALT"

        self.cobalt = cobalt

        for cmd in self.cobalt:
            self.headers += [f"{self.directive} {cmd}"]


class PBSBatchScript(BatchScript):
    """This class is responsible for building PBS batch script by taking ``pbs`` property and converting them into #PBS directives"""

    def __init__(self, pbs):
        """This method will return a list of #PBS directives used in job script

        Args:
            pbs (list): List of string items specified by ``pbs`` property in buildspec used for specified **#PBS** directive

        Returns:
            list: A list of **#PBS** directive that will be inserted for PBS Job Script
        """
        self.headers = []
        self.directive = "#PBS"

        self.pbs = pbs

        for cmd in self.pbs:
            self.headers += [f"{self.directive} {cmd}"]
