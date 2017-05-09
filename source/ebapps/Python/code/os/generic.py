import os

print "name:", os.name
print "kernel: ",os.uname()
print "environment: ", os.environ
print "group id: ", os.getgid()
print "groups: ",os.getgroups()
print "terminal id:", os.ctermid()
print "current directory:", os.getcwd()
print "login:", os.getlogin()
print "pid: ", os.getpid()
print "ppid:", os.getppid()
print "uid:", os.getuid()
print "list root directories:", os.listdir("/")
