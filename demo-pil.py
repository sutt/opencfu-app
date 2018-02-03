import os
import sys

from PIL import Image


img_dir = "data/images/"
img_dir2 = "data/images-tmp/"

file_names = os.listdir(img_dir)

print file_names

#i = 0
#fn = file_names[i]
#Image.open(fn)