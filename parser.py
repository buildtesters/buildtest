from setup import *
import os,sys
import yaml
field={
	'name':'',
	'source':'',
	'scheduler':['slurm','lsf','pbs'],
	'buildopts':'',
	'buildcmd':'',
	'runcmd':'',
	'runextracmd':'',
	'mpi':'enabled',
	'cuda':'enabled',
	'nproc': ''
}
# read config file and verify the key-value content with dictionary field
def parse_config(software,toolchain,filename,codedir):
        fd=open(filename,'r')
	content=yaml.load(fd)
	# iterate over dictionary to seek any invalid keys 
	for key in content:
		if key not in field:
			print "ERROR: invalid key", key 
			sys.exit(1)
		# key-value name must match the yaml file name, but strip out .yaml extension for comparison
		if key == "name":
			strip_ext=os.path.splitext(filename)[0]
        	        # get name of file only for comparison with key value "name"
                	filename=os.path.basename(strip_ext)
                	if content[key] != filename:   
                        	print "Invalid value for key: ",key,":",content[key],". Value should be:", filename
				sys.exit(1)
		# source must match a valid file name
		elif key == "source":
	                codefile=os.path.join(codedir,content[key])
        	        if not os.path.exists(codefile):
                	        print "Can't find source file: ",codefile, ". Verify source file in directory:", codedir
				sys.exit(1)
		# checking for invalid scheduler option
		elif key == "scheduler":
			if content[key] not in field["scheduler"]:
				print "Invalid scheduler option: ", key, " Please select on of the following:" , field["scheduler"]
				sys.exit(1)
		elif key == "nproc":
			if not str(content[key]).isdigit(): 
				print "nproc key must be an integer value"
				sys.exit(1)
			
	fd.close()
	return content

