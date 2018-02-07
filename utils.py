import os, sys, time
from PIL import Image
import cv2
import imutils
import subprocess

PATH_IMG = "data/images/"
PATH_COLONY_DATA = "data/colony-data/"
PATH_IMG_TMP = "data/images-tmp/"
PATH_ANNOTATE = "data/images-annotate/"
CAM_CV_ENUM = 1

def build_fn():
	fn = str(time.time())						#TODO - bettr filename
	return fn

def capture_image_pi(fn, b_verbose=False):
	path_fn = PATH_IMG + fn
	cmd = ["raspistill", "-o", path_fn]
	if b_verbose:
		cmd.exntend(["-v"])
	out = subprocess.check_output(cmd)
	return out
	
def capture_image_cv(cam_enum = CAM_CV_ENUM, b_verbose=False):
	try:
		vc = cv2.VideoCapture(cam_enum)
	except:
		print 'failed to create a VideoCapture. breaking...'
		return False
	try:
	tries = 0
	while(vc.isOpened()):
		tries += 1
		try:
			ret,frame = vc.read()
		except:
			print 'unable to read from cam try: ', str(tries)
		if ret:
			return frame
		if tries > 10:
			print 'after 10 tries, failed to capture'
			vc.release()
			break
	return frame
	
def load_image_pil(img_path_name):
	img = Image.open(img_path_name)
	return img
	
def load_image_cv(img_path_name):
	img = cv2.imread(img_path_name)
	return img
	
def save_image(img, save_dir, save_fn):
	img.save(save_dir + save_fn)
	
def save_image_cv(img, save_dir, save_fn):
	cv2.imwrite(save_dir + save_fn, img)

def crop_img(img, b_save_to_tmp = True):
	img_crop = img.crop((0,0,600,400))
	if b_save_to_tmp:
		tmp_img_fn = PATH_IMG_TMP + "tmp.jpg"		#TODO - remove hard-code path
		img_crop.save(tmp_img_fn)		
	return img_crop
	
def run_opencfu(input_img_path_name, fn, b_windows=False, b_filesystem=True):
	cmd = ["opencfu", "-i", input_img_path_name]
	if b_windows:
		wsl_path = "c:/windows/SysNative/wsl.exe"
		cmd = [wsl_path, "opencfu", "-i", input_img_path_name]
	if b_filesystem:
		path_to_colony_data = PATH_COLONY_DATA + fn + ".csv"
		cmd.extend([">", path_to_colony_data])	#pipe to data/colony-data/
	output_text = subprocess.check_output(cmd, shell=False)
	return output_text

def is_float(x):
    return str(float(x)) == x

def import_data(data_fn):
	
	#TODO - split this top section off into import_file vs parse_text_output
	f = open(data_fn, 'r')
	lines = f.readlines()
	f.close()
	
	lines = map(lambda x: x.replace("\n", ""),lines)
	lines = map(lambda x: x.split(','), lines)
	
	if len(lines) <= 1:					#TODO - better no-colonies-found check
		return {}
	
	data_key = lines[0]
	data_type = lines[1]
	data = lines[1:]
	
	#all data is an int or float,
	#use type in first row, as type for whole column
	#actually it looks like this doesnt work, make everything a float for now
	#data_type = map(lambda x: is_float(x), data_type)
	data_type = [True] * len(data_key)

	d = {}
	for i_k,k in enumerate(data_key):
		d[k] = []
		for i_row, row in enumerate(data):
			try:
				s_v = row[i_k]
				v = float(s_v) if data_type[i_k] else int(s_v)
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
	
# NOTE: this uses both PIL and cv2 for image viewing/editing.
#		When using cv2 images use func_cv functions to load/save image
#		where PIL images have no suffix.
	
		
def main(b_display=False, b_windows=False):
	
	#use fn as id for files in different data directories
	fn = build_fn()
	print 'fn: ', str(fn)
	
	# raspitill -> images/fn
	cap_fn = fn + ".jpg"
	if b_windows:
		cap_img_cv = capture_image_cv()
		save_image_cv(cap_img_cv, PATH_IMG, cap_fn)
	else:
		capture_image_pi(cap_fn)	
	cap_img = load_image_pil(PATH_IMG + cap_fn)		#TODO - cv-cap -> pil-import - bad?
	
	# images/fn -> images-tmp/fn
	crop_fn = fn + ".jpg"
	var_crop_img = crop_img(cap_img)				#TODO - crop center, resize
	save_image(var_crop_img, PATH_IMG_TMP, crop_fn)
	
	# images-tmp/fn -> colony-data/fn
	cfu_input_fn = PATH_IMG_TMP + crop_fn
	run_opencfu(cfu_input_fn, fn, b_windows)		#TODO - return data from output_text
	
	# colony-data/fn -> d
	data_fn = PATH_COLONY_DATA + fn + ".csv"
	d = import_data(data_fn)
	
	# images-tmp/fn -> img_cv
	img_cv = load_image_cv(PATH_IMG_TMP + crop_fn)
	
	# d, img_cv -> images-annotate/fn
	x, y, radius = d['X'], d['Y'], d['Radius']	
	x = map(lambda elem: int(elem), x)
	y = map(lambda elem: int(elem), y)
	radius = map(lambda elem: int(elem), radius)
	
	drawn_img = draw_colonies(img_cv, x, y, radius, max_colonies=0)
	drawn_fn = fn + ".jpg"
	save_image_cv(drawn_img, PATH_ANNOTATE, drawn_fn)
	
	#images-annotate/ -> user
	#run_image_server()
	if b_display:
		display_img(drawn_img, b_resize=False)
	
	print 'exiting main'
	

if __name__ == "__main__":
	
	if os.name == "nt":
		main(b_display=True, b_windows=True)	
	else:
		main(b_display=False, b_windows=False)	#headless rpi
	
	