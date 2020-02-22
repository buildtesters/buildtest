import subprocess

def get_all_collections():
    """Return all module collection """
    collections = "module -t savelist"
    ret = subprocess.Popen(collections,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out  = ret.communicate()[1]
    tmp = out.decode("utf-8").split()

    return (tmp)

class ModuleCollection:
    def __init__(self,collection):
        self.collection = collection
        self.module_cmd = f"module restore {self.collection}"
    def test_collection(self):
        ret = subprocess.Popen(self.module_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret.communicate()
        return ret.returncode
    def get_command(self):
        return self.module_cmd


class Module:
    def __init__(self,modules):
        self.modules = modules
        self.module_load_cmd = [f"module load {x}; " for x in self.modules]
    def get_command(self):
        return " ".join(self.module_load_cmd)
    def test_modules(self):
        ret = subprocess.Popen(self.module_load_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        ret.communicate()
        return ret.returncode
