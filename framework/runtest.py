import os
import sys
import subprocess
import time
def systempkg_menu(systempkg):

	os.system("clear")

        dirs = [ d for d in os.listdir(systempkg) if os.path.isdir(os.path.join(systempkg,d)) ]
        print "System Package Tests: "
	print "-------------------------------------------"

        count = 0
        for i in dirs:
                print str(count)+".", i
                count = count + 1
        totalcount = count
        while True:
		text = """
Select Test # you want.
-3: Main Menu
-4: Exit Program
User Input: """
                userinput = input(text)
                if userinput >= 0 and userinput < totalcount:
                        break
		elif userinput == -3:
			runtest_menu()
		elif userinput == -4:
			sys.exit(0)
		else:
			print "Invalid entry, please try again"
		
        print "Selecting Package: " + dirs[userinput]
	systempkg_test_menu(systempkg, dirs[userinput])

def systempkg_test_menu(systempkgpath, pkg_name):

	os.system("clear")

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
		print 
		print " Available Tests for package: ", pkg_name
                print
                print "------------------------------------------------------"
                print " TEST ID                TEST NAME"
                print "------------------------------------------------------"

		for name in test_list:
			print str(count) + ".", name
			count = count + 1
		testcount = count

		userinput = userprompt()

		if userinput == -4:
			sys.exit(0)

		elif userinput == -3:
			runtest_menu()

		elif userinput == -1:
			passed_test = 0
			failed_test = 0

			for f in files_as_list:
				(output,passtest,failtest)=launch_test(f)
				passed_test = passed_test + passtest
				failed_test = failed_test + failtest

			total_tests = passed_test + failed_test
			passrate = float(passed_test) * 100.0 / float(total_tests) 
			failrate = float(failed_test) * 100.0 / float(total_tests) 

			print passrate, "% of tests passed -  ", passed_test, "/", total_tests
			print failrate, "% of tests failed - " , failed_test, "/", total_tests

			time.sleep(0.5)
			
		elif userinput >= 0 and userinput < testcount:
			output = launch_test(files_as_list[userinput])[0]
			print output

			time.sleep(0.5)
		elif userinput == -2:
			systempkg_menu(systempkgpath)
		else:
			print "Invalid Entry, please try again."
	

def eb_menu(ebpkg):

	os.system("clear")

	cmd = "find " + ebpkg + " -maxdepth 4 -mindepth 4 -type d"
	ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	(output,error) = ret.communicate()

	#dirs = [ d for d in os.listdir(ebpkg) if os.path.isdir(os.path.join(ebpkg,d)) ]
	output = output.split("\n")
        text =  """ 
Available EB Package Tests: 

ID      Application           Toolchain
========================================
"""
	print text


	toolchain = []
	# getting the toolchain name and version and adding to toolchain list
	for f in output:
		tcver = os.path.basename(f)
		tcname = os.path.basename(os.path.dirname(f))
		toolchain.append(os.path.join(tcname,tcver))


	app = []
	# getting the app name and version and add to app list
	for f in output:
		appver = os.path.basename(os.path.dirname(os.path.dirname(f)))
		appname = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(f))))
		app.append(os.path.join(appname,appver))

	# removing last element because its an empty token
	app = app[:-1]
	toolchain = toolchain[:-1]
	for i in xrange(len(app)):
		print i, "\t", app[i],"\t\t",toolchain[i]
	
	print 
	while True:
		
                text = """
Select Test # you want.
-3: Main Menu
-4: Exit Program
User Input: """
		userinput = input(text)

		if userinput >= 0 and userinput < len(app):
			break;
		elif userinput == -3:
			runtest_menu()
		elif userinput == -4:
			sys.exit(0)
		else:
			print "Invalid entry, please try again"

	print "Selected  APP: ", app[userinput], " TOOLCHAIN: ",  toolchain[userinput]
	
	os.system("clear")

	cmd = "find " + os.path.join(ebpkg,app[userinput],toolchain[userinput]) + """ -type f -name "*.sh" """
	ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	(outputmsg,errormsg) = ret.communicate()
	output_list = outputmsg.split("\n")
	# remove last element
	output_list = output_list[:-1]
	while True:
		print 
		print "Tests for Application: ", app[userinput], " Toolchain: ", toolchain[userinput]
		print 
		print "------------------------------------------------------"
		print " TEST ID                TEST NAME"
		print "------------------------------------------------------"
		for i in xrange(len(output_list)):
			print str(i) + ". \t", output_list[i] 
	
		userinput = userprompt()
	
		if userinput >= 0 and userinput < len(output_list):
			outputmsg = launch_test(output_list[userinput])[0]
			print outputmsg

			time.sleep(0.5)

		elif userinput == -1:
			total_pass = 0
			total_fail = 0
			for i in xrange(len(output_list)):
				(output,passtest,failtest) = launch_test(output_list[i])	
				total_pass = total_pass + passtest 
				total_fail = total_fail + failtest
			

			total_test = total_pass + total_fail

			passrate = float(total_pass) * 100.0 / float(total_test) 
			failrate = float(total_fail) * 100.0 / float(total_test) 
			print
			print "---------------------------------------------------------"
			print "Results:"
			print "---------------------------------------------------------"
			print "PASS RATE: ", passrate, "% with ", total_pass, "/", total_test
			print "FAIL RATE: ", failrate, "% with ", total_fail, "/", total_test
			
			time.sleep(0.5)
 
		elif userinput == -2: 
			eb_menu(ebpkg)
		elif userinput == -3:
			runtest_menu()
		elif userinput == -4:
			sys.exit(1)	
		else:
			print "Invalid entry, please try again"


def launch_test(test):
	 cmd = " cd " + os.path.dirname(test) + "; time sh " + test
         ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
         (output,errormsg) = ret.communicate()
         ec = ret.returncode
	 test_pass = 0
	 test_fail = 0
         if ec == 0:
		 test_pass = 1
	         print "TEST ", test, " PASSED"
         else:
		test_fail = 1
         	print "TEST ", test, " FAILED"
         return output, test_pass, test_fail


def userprompt():
	text = """
Select Test # you want.
-1: run all test
-2: Go back
-3: Main Menu
-4: Exit Program
User Input: """
	userinput = input(text)
	return userinput

def runtest_menu():

	os.system("clear")

	cwd = os.environ["BUILDTEST_ROOT"]
	testing = os.path.join(cwd,"testing")
	systempkg = os.path.join(testing,"system")
	ebpkg = os.path.join(testing,"ebapp")
	text = """ Select the type of tests to run
1) System Packages 
2) Easybuild
3) Exit Program
User Input:  """


	while True:
		userinput = input(text)
		if userinput == 1:
			systempkg_menu(systempkg)
		elif userinput == 2:
			eb_menu(ebpkg)
		elif userinput == 3:
			sys.exit(1)
		else:
			print "Invalid Entry, please try again"
			print
	



