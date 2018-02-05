import os, sys
from PIL import Image
import cv2
import imutils

PATH_IMG = "data/images/"
PATH_COLONY_DATA = "data/colony-data/"
PATH_IMG_TMP = "data/images-tmp/"


def build_fn():
	fn = str(time.time())						#TODO - bettr filename
	return fn

def capture_image(fn, b_verbose=False):
	path_fn = PATH_IMG + fn
	cmd = ["raspistill", "-o", path_fn]
	if b_verbose:
		cmd.exntend(["-v"])
	out = subprocess.check_output(cmd)
	return out
	
def load_image_pil(img_path_name):
	img = Image.open(img_path_name)
	return img
	
def load_image_cv(img_path_name):
	img = cv2.imread(img_path_name)
	return img
	
def save_image(img, save_dir, save_fn):
	img.save(save_Dir + save_fn)

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
#	check_for_already_running()	#?
#	out = subprocess.call(["python" , "-m", "SimpleHTTPServer"])
#	print out	#so we know what port to connect on
	
		
def main(b_display=False):
	
	#use fn as id for files in different data directories
	fn = build_fn()
	
	# raspitill -> images/fn
	cap_fn = fn + ".jpg"
	capture_image(cap_fn)						#TODO - add windows capture
	cap_img = load_image(cap_fn)
	
	# images/fn -> images-tmp/fn
	crop_fn = fn + ".jpg"
	crop_img = crop_img(cap_img)				#TODO - crop center, resize
	save_img(crop_img, PATH_IMG_TMP, crop_fn)
	
	# images-tmp/fn -> colony-data/fn
	cfu_input_fn = PATH_IMG_TMP + crop_fn
	run_opencfu(cfu_iput_fn)					#TODO - return data from output_text
	
	# colony-data/fn -> d
	data_fn = fn + ".csv"
	d = import_data(data_fn)
	
	# images-tmp/fn -> img_cv
	img_cv = load_image_cv(PATH_IMG_TMP + crop_fn)
	
	# d, img_cv -> image-annotate/fn
	x, y, radius = d['X'], d['Y'], d['Radius']	
	drawn_img = draw_colonies(img_cv, x, y, radius, max_colonies=0)
	drawn_fn = fn + ".jpg"
	save_img(drawn_img, PATH_ANNOTATE, drawn_fn)
	
	#images-annotate/ -> user
	#run_image_server()
	if b_display:
		display_img(drawn_img)
	
	print 'exiting main'
	

if __name__ == "__main__":
	
	if os.name == "nt":
		main(b_display=True)
	else:
		main(b_display=False)	#headless rpi
	
	