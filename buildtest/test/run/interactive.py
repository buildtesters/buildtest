############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""
This module implements the --runtest feature of buildtest. This is an interactive
menu for running tests and gives user another alternative other than ctest

:author: Shahzeb Siddiqui (Pfizer)
"""
import os
import sys
import subprocess
import time
import glob

from buildtest.tools.config import config_opts

def systempkg_menu(systempkg):

    try:
        dirs = [ d for d in os.listdir(systempkg) if os.path.isdir(os.path.join(systempkg,d)) ]
    except OSError as err_msg:
        print(f"{err_msg}")
        raise

    while True:
        os.system("clear")

        text = """

        =========================================
        ||  ID    ||    System Package         ||
        =========================================   """

        print (text)
        count = 0
        for i in dirs:
            print (("\t||").expandtabs(8) +  ("\t" + str(count)+"\t||").expandtabs(3), "\t".expandtabs(4) + (i + "\t||").expandtabs(24))
            count = count + 1

        print ("\
            ========================================== \
            ")


        text = """

		Select Test # you want to run
                 _____________________________
                |  m  |  Main Menu            |
                |_____|_______________________|
                |  e  |   Exit Program        |
                |_____|_______________________|

		User Input: """

        userinput = input(text)

        if userinput.lower() == "m":
            runtest_menu()
        elif userinput.lower() == "e":
            sys.exit(0)

        # check if user prompt is not integer, report error
        if not userinput.isdigit():
            print ("Invalid format for user input, please type a number")
            time.sleep(1)
            continue

        userinput = int(userinput)
        if userinput >= 0 and userinput < count:
            break
        else:
            print ("Invalid entry, please try again")
            time.sleep(1.0)

    print ("Selecting Package: %s", dirs[userinput])
    systempkg_test_menu(systempkg, dirs[userinput])

def systempkg_test_menu(systempkgpath, pkg_name):

    os.system("clear")

    files_as_list = []
    # get all files with .sh extension for system package tests
    for dirpath, dirs, files in os.walk(os.path.join(systempkgpath,pkg_name)):
    	for file in files:
    		if file.endswith(".sh") or file.endswith(".csh") or file.endswith(".bash"):
    			files_as_list.append(os.path.join(dirpath,file))


    # if no test found then go back to previous menu
    if len(files_as_list) == 0:
        print(f"No Test found for system package: {pkg_name}")
        time.sleep(1)
        systempkg_menu(systempkgpath)
    test_list = []
    count = 0


    # get top level test directory to cd into before running test
    test_directory = os.path.dirname(files_as_list[0])

    for f in files_as_list:
    	test_list.append(os.path.basename(f))

    while True:
        os.system("clear")
        count = 0
        print
        print (("\t" + "System Package: ").expandtabs(40), pkg_name)
        print
        print ("""
        ------------------------------------------------------------------------------
        |    ID   |                          TEST NAME			                      |
        ------------------------------------------------------------------------------	""")

        for name in test_list:
        	print ("\t|".expandtabs(16),(str(count)+"\t|").expandtabs(8), (name + "\t| ").expandtabs(65))
        	count = count + 1
        testcount = count
        print ("\
        ------------------------------------------------------------------------------ ")

        userinput = userprompt()

        if userinput.lower() == "e":
        	sys.exit(0)

        elif userinput.lower() == "m":
        	runtest_menu()

        elif userinput.lower() == "b":
        	systempkg_menu(systempkgpath)

        elif userinput.lower() == "a":
        	passed_test = 0
        	failed_test = 0

        	for f in files_as_list:
        		(output,passtest,failtest)=launch_test(test_directory,f)
        		passed_test = passed_test + passtest
        		failed_test = failed_test + failtest

        	total_tests = passed_test + failed_test
        	passrate = float(passed_test) * 100.0 / float(total_tests)
        	failrate = float(failed_test) * 100.0 / float(total_tests)

        	print (passrate, "% of tests passed - ", passed_test, "/", total_tests)
        	print (failrate, "% of tests failed - ", failed_test, "/", total_tests)


        	time.sleep(3)
        	continue

        # check if user prompt is not integer, report error
        if not userinput.isdigit():
            print ("Invalid format for user input, please type a number")
            time.sleep(1)
            continue


        userinput = int(userinput)

        if userinput >= 0 and userinput < testcount:
        	output = launch_test(test_directory,files_as_list[userinput])[0]
        	print (output)

        	time.sleep(3)
        else:
        	print ("Invalid Entry, please try again.")
        	time.sleep(1.0)


def eb_menu(ebpkg):

    os.system("clear")

    testroot_set = set()

    # walk through ebapp test directory and add all directories that contain no subdirectories
    for dirpath, subdir, files in os.walk(ebpkg):
    	for file in files:
    		# only add directory if no subdirectories exists
    		if len(subdir) == 0:
    			testroot_set.add(dirpath)

    app_tc_set = set()



    # translate directory path into app name/version and toolchain name/version
    for item in testroot_set:
        # directory format $BUILDTEST_TESTDIR/ebapps/software/version, ebapp only 2 directories up
        if os.path.basename(os.path.dirname(os.path.dirname(item))) == "ebapp":

            app = os.path.basename(os.path.dirname(item))
            ver = os.path.basename(item)

            app_ver = os.path.join(app,ver)
            toolchain = "NONE"
            app_tc_set.add(app_ver+","+toolchain)

		# directory format $BUILDTEST_TESTDIR/ebapps/software/version/toolchainname/toolchainver, ebapp only 4 directories up
        elif os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(item))))) == "ebapp":

            app = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(item))))
            ver = os.path.basename(os.path.dirname(os.path.dirname(item)))
            tcname = os.path.basename(os.path.dirname(item))
            tcver = os.path.basename(item)

            app_ver = os.path.join(app,ver)
            tcname_tcver = os.path.join(tcname,tcver)
            app_tc_set.add(app_ver+","+tcname_tcver)

        # directory format $BUILDTEST_TESTDIR/ebapps/software/version/package, ebapp only 3 directories up
        elif os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(item)))) == "ebapp":
            app = os.path.basename(os.path.dirname(os.path.dirname(item)))
            ver = os.path.basename(os.path.dirname(item))

            app_ver = os.path.join(app,ver)
            toolchain = "NONE"
            app_tc_set.add(app_ver+","+toolchain)


        # directory format $BUILDTEST_TESTDIR/ebapps/software/version/toolchainname/toolchainver/package, ebapp only 5 directories up
        elif os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(item)))))) == "ebapp":

            app = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(item)))))
            ver = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(item))))
            tcname = os.path.basename(os.path.dirname(os.path.dirname(item)))
            tcver = os.path.basename(os.path.dirname(item))

            app_ver = os.path.join(app,ver)
            tcname_tcver = os.path.join(tcname,tcver)
            app_tc_set.add(app_ver+","+tcname_tcver)


    app_tc_set = list(app_tc_set)
    app_tc_set.sort()

    while True:
        os.system("clear")

        text =  """
                ------------------------------------------------------------------
                |  ID   |  Application               |  Toolchain                |
                ------------------------------------------------------------------ """
        print (text)

        for i in range(len(app_tc_set)):
            app = app_tc_set[i].split(",")[0]
            toolchain = app_tc_set[i].split(",")[1]
            print ("\t|  ".expandtabs(16), (str(i)+"\t|  ").expandtabs(4), (app+"\t| ").expandtabs(25),(toolchain + "\t|").expandtabs(25))

        print ("""\
            ------------------------------------------------------------------ """)



        text = """

        Select Test # you want to run
         _____________________________
        |  m  |  Main Menu            |
        |_____|_______________________|
        |  e  |   Exit Program        |
        |_____|_______________________|

        User Input: """

        userinput = input(text)

        if userinput.lower() == "m":
            runtest_menu()
        elif userinput.lower() == "e":
            sys.exit(0)

        # check if user prompt is not integer, report error
        if not userinput.isdigit():
            print ("Invalid format for user input, please type a number")
            time.sleep(1)
            continue

        # force input to be int for checking with Test ID
        userinput = int(userinput)

        if userinput >= 0 and userinput < len(app_tc_set):
            break;
        else:
            print ("Invalid entry, please try again")
            time.sleep(1)


    app_selected = app_tc_set[userinput].split(",")[0]
    toolchain_selected = app_tc_set[userinput].split(",")[1]

    print (" Application:", app_selected, "  Toolchain: ", toolchain_selected)

    os.system("clear")

    if toolchain_selected == "NONE":
    	testdir = os.path.join(ebpkg,app_selected)
    else:
    	testdir = os.path.join(ebpkg,app_selected,toolchain_selected)



    output_list = []
    # adding all tests from a eb package in a list for printing
    for dirpath, subdir, files in os.walk(testdir):
        for file in files:
            if file.endswith(".sh") or file.endswith(".csh") or file.endswith(".bash"):
                output_list.append(os.path.join(dirpath,file))


    while True:

        print
        print ("Tests for Application: ", app_selected, "  Toolchain: ", toolchain_selected)
        print ("""
	       ---------------------------------------------------------------------------------------------------------------------------------------------------
           |  ID    |  TEST NAME                                                                                                                             |
	       --------------------------------------------------------------------------------------------------------------------------------------------------- """)

        for x in range(len(output_list)):
        	print ("\t|  ".expandtabs(8), (str(x) + "\t|").expandtabs(5), (output_list[x]+"\t|").expandtabs(45))


        print ("""\
           ---------------------------------------------------------------------------------------------------------------------------------------------------- """)
        userinput = userprompt()


        if userinput.lower() == "b":
            eb_menu(ebpkg)
        elif userinput.lower() == "m":
            runtest_menu()
        elif userinput.lower() == "e":
            sys.exit(0)

        elif userinput.lower() == "a":
        	total_pass = 0
        	total_fail = 0
        	for i in range(len(output_list)):
        		(output,passtest,failtest) = launch_test(os.path.dirname(output_list[i]),output_list[i])
        		total_pass = total_pass + passtest
        		total_fail = total_fail + failtest

        	total_test = total_pass + total_fail

        	passrate = float(total_pass) * 100.0 / float(total_test)
        	failrate = float(total_fail) * 100.0 / float(total_test)
        	print
        	print( "---------------------------------------------------------")
        	print( "Results:")
        	print ("---------------------------------------------------------")
        	print ("PASS RATE: ", passrate, "% with ", total_pass, "/", total_test)
        	print ("FAIL RATE: ", failrate, "% with ", total_fail, "/", total_test)

        	time.sleep(3)
        	continue

        if not userinput.isdigit():
            print ("Invalid format for user input, please type a number")
            time.sleep(1)
            continue

        userinput = int(userinput)

        if userinput >= 0 and userinput < len(output_list):
        	outputmsg = launch_test(os.path.dirname(output_list[userinput]),output_list[userinput])[0]
        	print (outputmsg)
        	time.sleep(3)

        else:
        	print ("Invalid entry, please try again")


def launch_test(testdir,test):
    os.chdir(testdir)
    shell_type = os.path.splitext(test)[1]
    # remove leading .
    shell_type = shell_type[1:]

    cmd = "time " + shell_type + " " + test
    ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (output,errormsg) = ret.communicate()
    ec = ret.returncode
    output = output.decode("utf-8")
    test_pass = 0
    test_fail = 0
    if ec == 0:
        test_pass = 1
        print ("TEST ", test, " PASSED")
    else:
        test_fail = 1
        print ("TEST ", test, " FAILED")
    return output, test_pass, test_fail


def userprompt():

    text = """

                Select Test # you want to run
    	        ______________________________
                |  a  |  Run All Tests        |
                |_____|_______________________|
                |  b  |  Go Back              |
                |_____|_______________________|
                |  m  |  Main Menu            |
                |_____|_______________________|
                |  e  |   Exit Program        |
                |_____|_______________________|

                User Input: """


    userinput = input(text)
    return userinput

def runtest_menu():

    os.system("clear")

    system_testdir = os.path.join(config_opts['BUILDTEST_TESTDIR'],"system")
    software_testdir = os.path.join(config_opts['BUILDTEST_TESTDIR'],"ebapp")
    text = """
    	_________________________________________________________________________
        |\							                                           /|
    	| \           Welcome to buildtest Interactive Testing Menu	          / |
        |  \_________________________________________________________________/  |
    	|  |								                                 |  |
    	|  |								                                 |  |
    	|  |  *****  *  *  *   *      *****  *******  ****   ****  ******    |  |
    	|  |  *   *  *  *  *   *      *    *    *     *     *         *      |  |
    	|  |  *****  *  *  *   *      *    *    *     ****   ***      *      |  |
        |  |  *	  *  *  *  *   *      *    *    *     *         *     *      |  |
    	|  |  *****  ****  *   *****  *****     *     ****  ****      *      |  |
        |  |_________________________________________________________________|  |
    	| /                                                                   \ |
    	|/_____________________________________________________________________\|



    	Select an Option:

    	_______________________________
    	|  1  |   System Packages     |
    	|_____|_______________________|
    	|  2  |   EasyBuild Packages  |
    	|_____|_______________________|
    	|  e  |   Exit                |
    	|_____|_______________________|



    	User Input: """


    while True:
    	userinput = input(text)

    	if userinput.lower() == "e":
    		sys.exit(0)

    	if not userinput.isdigit():
    		print ("Invalid format for user input, please type a number")
    		time.sleep(1)
    		continue


    	# force userinput to be integer in case its float or something else
    	userinput = int(userinput)
    	if userinput == 1:
    		systempkg_menu(system_testdir)
    	elif userinput == 2:
    		eb_menu(software_testdir)
    	else:
    		print ("Invalid Entry, please try again")
