import os, sys
from PIL import Image
import cv2
import imutils


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
	
	data_type = map(lambda x: is_float(x), data_type)

	d = {}
	for i_k,k in enumerate(data_key):
		d[k] = []
		for i_row, row in enumerate(data):
			try:
				s_v = row[i_k]
				v = float(s_v) if is_float(s_v) else int(s_v)
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
	if cv2.waitKey(0)== ord('q'):
		return True
		
def main():
	
	data_fn = "data/colony-data/sample1.csv"
	img_fn = "data/samples/sample1.jpg"
	
	d = import_data(data_fn)
	img = cv2.imread(img_fn)
	
	x, y, radius = d['X'], d['Y'], d['Radius']	
	img = draw_colonies(img, x, y, radius, max_colonies=0)
	
	display_img(img)
	
	print 'exiting main'
	

if __name__ == "__main__":
	main()
	
	