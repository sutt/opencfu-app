import subprocess, os, sys

print os.name

if os.name == 'nt':
	print 'so windows'
	
if os.name == "nt":
	#out = subprocess.check_output(["arp", "-a"])
	out = subprocess.check_output("dir", shell=True)
else:
	out = subprocess.check_output(["ls", "-l"])
#print out

	
out = subprocess.check_output(["opencfu", "-i", "samples/C.jpg"])

print 'len: ', str(len(out))
print 'len 0: ', str(len(out[0]))
print '0: ', str(out[0])
print out[95:98]

print len(out.split("\n"))

print out

	
