import os
import sys

from PIL import Image

#Dev/Testing Zone
if os.name == 'nt':
	fn = "data/samples/C.jpg"
	im = Image.open(fn)
	print im.size 
	
	im2 = im.crop((0,0,400,400))
	print im2.size
	im2.save("data/images-tmp/C400.jpg")
	sys.exit()

img_dir = "data/images/"
img_dir2 = "data/images-tmp/"

file_names = os.listdir(img_dir)

print file_names

i = 1
fn = file_names[i]
im = Image.open(fn)

print im.size