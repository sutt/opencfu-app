import subprocess, os, sys, time

print os.name

if os.name == 'nt':
	print 'so windows'
	
if os.name == "nt":
	#out = subprocess.check_output(["arp", "-a"])
	out = subprocess.check_output("dir", shell=True)
else:
	out = subprocess.check_output(["ls", "-l"])
#print out

img_ext = ".jpg"
img_name = str(time.time())
img_name += img_ext

out = subprocess.check_output(["raspistill", "-o", img_name, "-v"])

print 'raspistill output:'
print out
	
out = subprocess.check_output(["ls", "-l", "data/images/"])
print 'files in data/images/:'
print 'yours: ', img_name
print out

#out = subprocess.check_output(["opencfu", "-i", "samples/C.jpg"])
#print len(out.split("\n"))
#print out

	
