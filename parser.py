from setup import *
import os,sys
import yaml
field={
	'testblock':['generic','intel','java','python','cuda','R','mpi', 'intel-mpi'],
	'name':'',
	'source':'',
	'scheduler':['slurm','lsf','pbs'],
	'buildopts':'',
	'buildcmd':'',
	'runcmd':'',
	'runextracmd':'',
	'mpi':'enabled',
	'cuda':'enabled'
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
	                codefile=codedir+content[key]
        	        if not os.path.exists(codefile):
                	        print "Can't find source file: ",codefile, ". Verify source file in directory:", codedir
				sys.exit(1)
		# checking for invalid scheduler option
		elif key == "scheduler":
			if content[key] not in field["scheduler"]:
				print "Invalid scheduler option: ", key, " Please select on of the following:" , field["scheduler"]
				sys.exit(1)
		# checking for invalid testblock option
		elif key == "testblock":
			# invalid testblock option
			if content[key] not in field["testblock"]:
				print "Invalid testblock option: ", key, " Please select on of the following:" , field["testblock"]
				sys.exit(1)
			
	fd.close()
	return content

