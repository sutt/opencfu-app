import subprocess, os, sys, platform

#System Diagnostics
print os.name
print platform.architecture()

if os.name == 'nt':
	print os.environ['SystemRoot']

print sys.maxsize
print '2^31=', str(2 ** 31)

if int(sys.maxsize) > (2 ** 31):
	print 'so, 64-bit'
else:
	print 'so, 32-bit'


print 'stage1'
if os.name == 'nt':
	#check_call works and echos to terminal
	subprocess.check_call("python hello.py")
	subprocess.check_call("python hello.py", shell=True)
else:
	#check_call does not within wsl, use check_output
	out = subprocess.check_output(["python", "hello.py"])
	print out


print 'stage2'

if os.name == 'nt':
	#Runs but doesn't pipe to .txt
	subprocess.check_call("python hello.py > aaa.txt")
else:
	#Runs but doesn't pipe to .txt
	out = subprocess.check_output(["python", "hello.py", ">", "aaa-wsl.txt"])
	print out
#> echo 'hello' > tmp.txt  #does work so pipe is available in windows
#stdout=PIPE?
#or is this because piping doesn't accept python print?
	#lets check on windows without a subproc call:
		#Works: >python hello.py > aaa.txt
	#lets check on linux
		#none of this works in wsl

print 'stage3'
#Can you run wsl from check_call? - No
#subprocess.check_call("c:/windows/system32/wsl.exe python hello.py", shell=True)
subprocess.check_call("c:/windows/SysNative/wsl.exe python hello.py")
#NOTE: WSL python is 64-bit

print 'stage4'
try:
	subprocess.check_call("C:/Windows/System32/bash.exe")
except Exception as e:
	print e
print 'with sys native...'

#Note - unknown
try:
	subprocess.check_output(["C:/Windows/SysNative/wsl.exe)
except Exception as e:
	print e

#Note this works and will output your terminal into wsl
try:
	subprocess.check_call("C:/Windows/SysNative/bash.exe")
except Exception as e:
	print e


#Try with SO example, neither work as python subproc, 
#but both work in windows terminal (?)
#subprocess.check_call('echo "hello bash" ')
#subprocess.check_call("""bash -c 'echo "hello bash"'""")

#https://stackoverflow.com/questions/44576617/call-bash-from-python-on-windows-10
#Use SysNative/bash?

#out = subprocess.check_output(["python", "hello.py"], shell=True)	
#out = subprocess.check_output(["python", "hello.py"], shell=False)	
#out = subprocess.check_output(["c:/windows/system32/wsl.exe", "python", "hello.py"])	
#out = subprocess.check_output(["c://windows//system32//wsl.exe", "python", "hello.py"])	
#out = subprocess.check_output(["c://windows//system32//wsl.exe", "ls", "-l"], shell=True)	
#out = subprocess.check_output(["wsl", "ls", "-l"])	
#out = subprocess.check_output(["c:\\windows\\system32\\wsl.exe", "python", "hello.py"])	
#out = subprocess.check_output(["wsl", "python", "demo-subproc.py"])	
#out = subprocess.check_output(["wsl", "python", "demo-subproc.py"])

#print 'heres the out:'
#print out
#print out

#maybe system attributes on .jpg?
#maybe do [windows]-python call subproc("wsl" "python" "subproc-shell.py")
				#-> subproc("opencfu" "-i" "img") [subproc-shell.py]
				
#Explicit_PATH_to_WSL
#c:/windows/system32/wsl.exe

#can use check_call or other thing
#https://blogs.msdn.microsoft.com/wsl/2016/10/19/windows-and-ubuntu-interoperability/

#This works:
#>wsl ls /mnt/c/Windows/
	
