import subprocess, os, sys

print os.name

if os.name == 'nt':
	print 'so windows'
	
if os.name == "nt":
	#out = subprocess.check_output(["arp", "-a"])
	#out = subprocess.check_output("dir", shell=True)
	pass
	print 'past here'
else:
	out = subprocess.check_output(["ls", "-l"])
#print out

#These do no work as WoW64 can not find wsl in System32	
#out = subprocess.check_output(["wsl", "opencfu", "-i", "data/samples/blah.jpg"], shell=True)
#out = subprocess.check_output(["wsl", "opencfu", "-i", "data/samples/blah.jpg"])

#This works when calling from windows >wsl python demo-subproc.py
#out = subprocess.check_output(["opencfu", "-i", "data/samples/blah.jpg"])

#This works from windows calling windows python >python demo-subproc.py
wsl_path = "c:/windows/SysNative/wsl.exe"
out = subprocess.check_output([wsl_path, "opencfu", "-i", "data/samples/blah.jpg"])

#Also we do have pipe
cmd = [wsl_path, "opencfu", "-i", "data/samples/blah.jpg"]
cmd.extend([">", "aaa-pipe.txt"])
out = subprocess.check_output(cmd)
if os.name == "nt":
	out = subprocess.check_output("dir", shell=True)
	print 'direcctory contents should contains aaa-pipe.txt'
	print out

print 'len: ', str(len(out))
print 'len 0: ', str(len(out[0]))
print '0: ', str(out[0])
print out[95:98]

print len(out.split("\n"))

#print out

#maybe system attributes on .jpg?
#maybe do [windows]-python call subproc("wsl" "python" "subproc-shell.py")
				#-> subproc("opencfu" "-i" "img") [subproc-shell.py]
				
#OK so python

#https://stackoverflow.com/questions/39812882/python-subprocess-call-cannot-find-windows-bash-exe
	
	#how to first call anything with wsl?
	
	#Explicit_PATH_to_WSL
	#c:/windows/system32/wsl.exe
	
	#Explicit_FULL_PATH_to_data
	#C:\Python27\python.exe