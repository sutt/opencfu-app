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

path_name = "data/images/"

img_path_name = path_name + img_name


out = subprocess.check_output(["raspistill", "-o", img_path_name, "-v"])

print 'raspistill output:'
print out
	
out = subprocess.check_output(["ls", "-l", "data/images/"])
print 'files in data/images/:'
print 'yours: ', img_name
print out

out = subprocess.check_output(["opencfu", "-i", img_path_name])

print 'results of opencfu:'
print out


#print len(out.split("\n"))
#print out

	
