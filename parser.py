from setup import *
import os,sys
field={
	'testblock':['generic','intel','java','python','cuda','R','mpi', 'intel-mpi'],
	'name':'',
	'source':'',
	'scheduler':['slurm','lsf','pbs'],
	'job':['True','False'],
	'buildopts':''
}
# read config file and verify its field
def parse_config(software,toolchain,filename,codedir):
        fd=open(filename,'r')

	# mapping of key,value pair from check_field
	configmap={}
		
	# read configuration and verify key,value pair from check_field and store result in list
	for line in fd.readlines():
		line=line.rstrip()
		key,value=check_field(line,filename,codedir)
		# if there is error in config file, return value from check_field will be False
		if [key,value] == [False,False]:
			print "Skipping File: ", filename, " due to error"
			return {}
		if key == "name":
			configmap["name"]=value
		elif  key == "source":
			configmap["source"]=value
		elif key == "scheduler":
			configmap["scheduler"]=value
		elif key == "job":
			configmap["job"]=value
		elif key == "buildopts":
			configmap["buildopts"]=value
		elif key == "testblock": 
			configmap["testblock"]=value
	fd.close()
	print configmap

	return configmap
# process configuration field in form <key>='<value>'		
def check_field(line,filename,codedir):
	key,value=['','']
	# if = found, split line by = and extract key,value
	if line.find(':') != -1:
		key,value=line.split(":")
		key=key.strip()
		value=value.strip()
		#key=key.replace("'","")
		#value=value.replace("'","")
		#key=key.replace("\n","")
		#value=value.rstrip('')
		#value=value.replace("\n","")
		
	else:
		print"Error processing: ", line

	#print "key,value=",key,value,field["job"],type(field["job"])
	# if key is name, check if filename matches field value of name
	#print key,len(key),"name",len("name")
	if key == "name":

		strip_ext=os.path.splitext(filename)[0]
		# get name of file only for comparison with key value "name"
		filename=os.path.basename(strip_ext)
		if value == filename:	
			#print "key=",key,"value=",value," Check OK!"
			# dont check for name, source, buildopts the check will be done outside this function
			return key,value
		else:	
			print "Invalid entry for ",key,"=",value,". Make sure it matches filename"
			return [False,False] 
	# check if source value is a valid file
	elif key == "source":
		codefile=codedir+value
		if not os.path.exists(codefile):
			print "Can't find file: ",codefile
			return [False,False] 
		else:
			#print "key=",key,"value=",value," OK!"
			return key,value
	# no check for buildopts, return as is
	elif key == "buildopts":
		#print "key=",key,"value=",value," OK!"
		return key,value
	
	# store list of valid values per key defined in field dictionary
	valuelist=[]

	# get value from dictionary if its scheduler or job to check if value field exist in list
	if key == "testblock":
		valuelist=field["testblock"]
		#print valuelist,type(valuelist)
	elif key == "scheduler":
		valuelist=field["scheduler"]
	elif key == "job":
		valuelist=field["job"]
	
	if value not in valuelist:
		print filename,"  Unable to process key=",key," value=", value
		return [False,False]
	else:
		#print "key=",key," value=", value,"  OK"
		return key,value

