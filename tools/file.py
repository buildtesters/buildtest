import os
from datetime import datetime

def stripHiddenFile(file): 
	"""  removes the leading "." character from file """
        file=file[1:]
        return file  

def create_file(filename,verbose):
        """ Create an empty file if it doesn't exist   """
        if not os.path.isfile(filename):
                fd=open(filename,'w')
                fd.close()
                if verbose >= 1:
                        print "Creating Empty File:", filename


def create_dir(dirname,verbose):
        """Create directory if it doesn't exist"""
        if not os.path.isdir(dirname):
                os.makedirs(dirname)
                if verbose >= 1:
                        print "Creating Directory: ",dirname

def string_in_file(string,filename):
	""" returns true/false to indicate if string is in file """
	if string in open(filename).read():
		return True
	else:
		return False

def isHiddenFile(inputfile):
	""" Return true/false to indicate if its a hidden file """
	if os.path.isdir(inputfile) == True:
		return False
	
        cmd = "basename " + inputfile
	filename=os.popen(cmd).read().strip()
	if filename[0] == ".":
                return True
        else:
                return False

def update_logfile(logdir,logcontent,verbose):
        create_dir(logdir,verbose)          
        logfilename = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")
        logfilepath = os.path.join(logdir,logfilename)

        print "Writing Log File: " + logfilepath

        fd = open(logfilepath,'w')
        fd.write(logcontent)
        fd.close()

