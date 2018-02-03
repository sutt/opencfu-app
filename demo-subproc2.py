import subprocess, os, sys, time
from PIL import Image

print os.name

if os.name == 'nt':
	print 'so windows'
	
if os.name == "nt":
	if len(sys.argv) > 1:
		print 'long'
	#out = subprocess.check_output(["arp", "-a"])
	out = subprocess.check_output("dir", shell=True)
	sys.exit()
else:
	out = subprocess.check_output(["ls", "-l"])


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

def crop_img(img_path_name, temp_img_path_name):
	
	
	#use any flag to do a demo
	if len(sys.argv) > 1:
		im = Image.open("data/samples/C.jpg")
	else:
		im = Image.open(img_path_name)
	print im.size 

	im2 = im.crop((0,0,400,400))
	print im2.size
	im2.save(temp_img_path_name)

temp_img_path_name = "data/images-tmp/" + img_name

crop_img(img_path_name, temp_img_path_name)

out = subprocess.check_output(["opencfu", "-i", temp_img_path_name])

print 'results of opencfu:'
print out


#print len(out.split("\n"))
#print out

	
