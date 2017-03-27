import os
# creates a relationship between software-version to a toolchain to show. This will show how a module file relates to a particular toolchain
def isHiddenFile(inputfile):
	if os.path.isdir(inputfile) == True:
		return False
	
        cmd = "basename " + inputfile
	filename=os.popen(cmd).read().strip()
	if filename[0] == ".":
                return True
        else:
                return False
def stripHiddenFile(file): 
        file=file[1:]
        return file  

def print_dictionary(dictionary):
        for key in dictionary:
                print key, sset(dictionary[key])

def print_set(setcollection):
	for item in setcollection:
		print item
class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

