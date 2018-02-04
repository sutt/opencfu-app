import os, sys
from PIL import Image
import cv2
import imutils

PATH_IMG = "data/images/"
PATH_COLONY_DATA = "data/colony-data/"
PATH_IMG_TMP = "data/images-tmp/"


def build_img_path_name(img_ext=".jpg"):
	img_name = str(time.time())						#TODO - bettr filename
	img_name += img_ext
	img_path_name = PATH_IMG + img_name
	return img_path_name

def capture_image(img_path_name, b_verbose=False):
	cmd = ["raspistill", "-o", img_path_name]
	if b_verbose:
		cmd.exntend(["-v"])
	out = subprocess.check_output(cmd)
	return out
	
def load_image(img_path_name):
	img = Image.open(img_path_name)
	return img

def crop_img(img, b_save_to_tmp = True):
	img_crop = img.crop((0,0,400,400))
	if b_save_to_tmp:
		tmp_img_fn = PATH_IMG_TMP + "tmp.jpg"		#TODO - remove hard-code path
		im2.save(tmp_img_fn)		
	return img2
	
def run_opencfu(input_img_path_name, b_filesystem=True):
	cmd = ["opencfu", "-i", input_img_path_name]
	if b_filesystem:
		cmd.extend([">", path_to_colony_data])	#pipe to data/colony-data/
	output_text = subprocess.check_output(cmd)
	return output_text

def is_float(x):
    return str(float(x)) == x

def import_data(data_fn):
	
	f = open(data_fn, 'r')
	lines = f.readlines()
	f.close()
	
	lines = map(lambda x: x.replace("\n", ""),lines)
	lines = map(lambda x: x.split(','), lines)
	
	data_key = lines[0]
	data_type = lines[1]
	data = lines[1:]
	
	#all data is an int or float,
	#use type in first row, as type for whole column
	data_type = map(lambda x: is_float(x), data_type)

	d = {}
	for i_k,k in enumerate(data_key):
		d[k] = []
		for i_row, row in enumerate(data):
			try:
				s_v = row[i_k]
				v = float(s_v) if data_type[i] else int(s_v)
				d[k].append(v)
			except:
				print 'error parsing data elem ', str(k), ' line ', str(i_row)
				print 'problem string is: ', s_v
		
	return d


def draw_colony_circle(img, x, y, radius):
    #cv2.rectangle(img, rect[0], rect[1], (0, 255, 255), 3)
	cv2.circle(img, (int(x), int(y)), int(radius), (255), 2)
	return img

def draw_colonies(img, x, y, radius, max_colonies=0):
	max_i = min(max_colonies, len(x)) if bool(max_colonies) else len(x)
	for i in range(max_i):
		_x, _y, _radius = x[i], y[i], radius[i]
		img = draw_colony_circle(img, _x, _y, _radius)
	return img
	
def display_img(img, mod_=2, b_resize=True):
	
	if b_resize:
		_h, _w, _c = img.shape
		img = imutils.resize(img
							,width = int(_h/ mod_)
							,height = int(_w/mod_) 
							)
							
	cv2.imshow('annotated img', img)
	if cv2.waitKey(0) == ord('q'):
		return True
		
#TODO - add a way to run an image server locally
#def run_image_server():
#	out = subprocess.call(["python" , "-m", "SimpleHTTPServer"])
#	print out	#so we know what port to connect on
	
		
def main():
	
	data_fn = "data/colony-data/sample1.csv"
	img_fn = "data/samples/sample1.jpg"
	
	cap_img_fn = build_img_path_name()
	capture_image(cap_img_fn)
	
	cap_img = load_image(cap_img_fn)
	
	crop_img = crop_img(cap_img)
	save_img(crop_img)
	
	#run_opencfu(crop_img_fn)	#TODO add crop_img_fn
	
	d = import_data(data_fn)
	
	img_cv = cv2.imread(img_fn)
	
	x, y, radius = d['X'], d['Y'], d['Radius']	
	drawn_img = draw_colonies(img_cv, x, y, radius, max_colonies=0)
	
	display_img(drawn_img)
	
	print 'exiting main'
	

if __name__ == "__main__":
	main()
	
	