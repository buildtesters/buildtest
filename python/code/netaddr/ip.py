from netaddr import *
import pprint
ip = IPAddress('192.0.2.1')
print "IP Address= ", ip, "version:", ip.version

ip2= IPNetwork('192.0.2.0/24')
print "IP:", ip2.ip, "IP Broadcast", ip2.broadcast
