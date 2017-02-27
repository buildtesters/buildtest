## Application Testing
---
### Description
The Application Testing repository consist of test cases designed to test the software packages after installation. Each test is designed to check a specific functionality of the application. In most cases, the return code is checked to see if the command was executed successfully. 

---
### Setup
In order to write your test cases, please use the testgen script to generate your template test case. Afterward make any changes necessary appropriate for the test case.

The testgen.sh script is designed to test binaries, for instance if you want to write a test case to test a specific binary this can be done very quickly. The script testgen.sh will use the template file template.txt in order to write the test case. 

Please refer to **help** command in order to learn how to use the testgen.sh. Simply type **testgen.sh --help**

Each test case will reside in a directory <software>/<version> where software and version are specified in the testgen.sh script. The software and version must match the name of the module you are trying to test because it will use this for loading the appropriate module and put that in the test case. 

The command used to generate the  test case will be recorded in a file <software>/<version>/input.txt
Likewise, a file <software>/<version>/testall.sh will contain a list of test cases to run. This is only useful to run test cases in batch.
