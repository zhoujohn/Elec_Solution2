import numpy as np
import cv2
import time
import sys
import json

def load_cam_config():
	width = 0
	height = 0
	expo = 0.0
	auto = 1
	with open("./config/cam.json") as load_f:
		load_dict = json.load(load_f)
		width = load_dict["width"]
		height = load_dict["height"]
		expo = load_dict["exposure"]
		auto = load_dict["auto"]
	return width, height, expo, auto


def set_camera():
	cam = cv2.VideoCapture(0)
	width = cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
	height = cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
	expo = cam.get(cv2.cv.CV_CAP_PROP_EXPOSURE)*100
	print ("default camera width is %d, height is %d, exposure is %f" % (width,height,expo))
	# read camera config file
	width,height,expo,auto = load_cam_config()

	cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,height)
	if auto == 0:
		#cam.set(cv2.cv.CAP_PROP_AUTO_EXPOSURE,0.25)  # manual exposure
		cam.set(cv2.cv.CV_CAP_PROP_EXPOSURE,expo)   # 0.1, 0.05, 0.02
	else:
		cam.set(cv2.cv.CV_CAP_PROP_EXPOSURE,0.0)  # auto exposure
	#cam.set(cv2.cv.CV_CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

	width = cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
	height = cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
	expo = cam.get(cv2.cv.CV_CAP_PROP_EXPOSURE)*100
	print ("test camera width is %d, height is %d, exposure is %f" % (width,height,expo))
	
	return cam


def read_config():
	return



reload(sys)
sys.setdefaultencoding("utf-8")

img_counter = 3
cam = set_camera()
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#cam = cv2.VideoCapture(0)
time.sleep(5)

while img_counter:
	if cam.isOpened():
		ret, frame = cam.read()
		if not ret:
			break
		cv2.imwrite('../'+str(img_counter)+'.jpg',frame )
		print ("image file saved")
	
	time.sleep(2) #Sleep(2)
	img_counter = img_counter - 1

cam.release()
cv2.destroyAllWindows()
