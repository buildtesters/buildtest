import os
import sys
import subprocess
import time
def systempkg_menu(systempkg):
        dirs = [ d for d in os.listdir(systempkg) if os.path.isdir(os.path.join(systempkg,d)) ]
        print "Available System Package Tests: "
        count = 0
        for i in dirs:
                print str(count)+".", i
                count = count + 1
        totalcount = count
        while True:
                userinput = input("Please make a selection (choose the number or type name of package): ")
                if userinput >= 0 and userinput < totalcount:
                        break
        print "Selecting Package: " + dirs[userinput]
	systempkg_test_menu(systempkg, dirs[userinput])
        return dirs[userinput]

def systempkg_test_menu(systempkgpath, pkg_name):
	print os.path.join(systempkgpath,pkg_name)
	cmd = "find " + os.path.join(systempkgpath,pkg_name) + """ -type f -name "*.sh" """
	files=os.popen(cmd).read()
	test_list = []
	count = 0
	# creating a list of files
	files_as_list = files.split("\n")
	# removing last element from list since its an empty token
	files_as_list = files_as_list[:-1]
	# string path and get test name

	# get top level test directory to cd into before running test
	test_directory = os.path.dirname(files_as_list[0])

	for f in files_as_list:
		test_list.append(os.path.basename(f))

	while True:
		count = 0
		for name in test_list:
			print str(count) + ".", name
			count = count + 1
		testcount = count
		text = """ 
Select Test # you want.
-1: run all test
-2: Go back
-3: Exit Program
Selection: """
		userinput = input(text)
		if userinput == -3:
			sys.exit(0)
		elif userinput == -1:
			passed_test = 0
			failed_test = 0

			for f in files_as_list:
				cmd = "cd " + test_directory + "; time sh " + f + " >/dev/null"
				ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
				ret.communicate()
				ec = ret.returncode
				if ec == 0: 
					print "TEST: ", f, " PASSED"
					passed_test = passed_test + 1
				else:
					print "TEST: ", f, " FAILED"
					failed_test = failed_test + 1

			total_tests = passed_test + failed_test
			passrate = float(passed_test) / float(total_tests) * 100
			failrate = float(failed_test) / float(total_tests) * 100

			print passrate, "% of tests passed -  ", passed_test, "/", total_tests
			print failrate, "% of tests failed - " , failed_test, "/", total_tests

			os.system("sleep 1")
	
		elif userinput >= 0 and userinput < testcount:
			cmd = "cd " + test_directory + "; time sh " + files_as_list[userinput] + " >/dev/null"
			ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			ret.communicate()
			ec = ret.returncode
			if ec == 0: 
				print "TEST: ", f, " PASSED"
			else:
				print "TEST: ", f, " FAILED"

			os.system("sleep 1")
		elif userinput == -2:
			systempkg_menu(systempkgpath)
		else:
			print "Invalid Entry, please try again."
	
	

cwd = os.getcwd()
testing = os.path.join(cwd,"testing")
systempkg = os.path.join(testing,"system")
ebpkg = os.path.join(testing,"ebapp")
text = """ Please select the type of tests to run
1) System Packages 
2) Easybuild 
"""
userinput = input(text)
if userinput == 1:
	pkg = systempkg_menu(systempkg)
	



