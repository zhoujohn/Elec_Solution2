import numpy as np
import cv2
import time
import sys
import json
from detectstatus import detectstatus
from detectstatus import detectsingle
from detectstatus import detecthandle
#from network import post_data

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
	# read camera default internal config
	width = cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
	height = cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
	expo = cam.get(cv2.cv.CV_CAP_PROP_EXPOSURE)
	print ("camera width is %d, height is %d, exposure is %f" % (width,height,expo))
	# read camera config file
	width,height,expo,auto = load_cam_config()

	cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
	cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,height)
	if auto == 0:
		#cam.set(cv2.cv.CV_CAP_PROP_AUTO_EXPOSURE,0.25)  # set as manual exposure(0.75 auto, 0.25 manual)
		cam.set(cv2.cv.CV_CAP_PROP_EXPOSURE,expo)   # 0.1, 0.05, 0.02
	else:
		cam.set(cv2.cv.CV_CAP_PROP_EXPOSURE,0.0)  # manual exposure
	#cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

	width = cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
	height = cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
	expo = cam.get(cv2.cv.CV_CAP_PROP_EXPOSURE)
	print ("test camera width is %d, height is %d, exposure is %f" % (width,height,expo))
	
	return cam

anno_name = 'NONE00E04CE50066'
station_name = 'shouxiang'
frame_name = '001241137960'
##### anno configuration: level_R, level_G used for detection
##### anno configuration: r_bright, r_variance, g_bright, g_variance, r_pos used for identification
def read_anno_config():
	counter = 0
	matrix = []
	with open("./config/" + anno_name + "/" + frame_name + ".json") as load_f:
		load_dict = json.load(load_f)
		load_dict1 = load_dict["shapes"]
		for val in load_dict1:
			element = [val["label"],val["points"],val["level_R"],val["level_G"],val["bright_RR"],val["bright_RG"],val["bright_RB"],val["bright_GR"],val["bright_GG"],val["bright_GB"]]
			#element.append(val["label"])
			#element.append(val["points"])
			#element.append(val["level_R"])
			#element.append(val["level_G"])
			matrix.append(element)
			counter = counter + 1
			#print (val)
			#print (counter)
		#print (matrix)
	return counter,matrix


requrl = "/mqtt/send/offlinecache"
connection = "127.0.0.1:7788"

#reload(sys)
#sys.setdefaultencoding("utf-8")
send_data_prev1 = {}
send_data_prev2 = {}

img_counter = 0

while True:
	#cam = set_camera()
	#time.sleep(5)
	target_num = 0
	target_num,target_matrix = read_anno_config()
	#print (target_num, target_matrix)

	#while cam.isOpened():
	#xxx = 50
	xxx = 1
	
	while xxx:
	#	ret, frame = cam.read()
	#	if not ret:
	#		break
		#crop image and detect status
		print (time.time())
		xxx -= 1
		if xxx < 10:
			yyy = str(xxx)
		else:
			yyy = str(xxx)
		yyy = '49'
		frame = cv2.imread("D:\\Tools\\camera\\" + station_name + "\\" + frame_name + "\\" + frame_name + yyy +".jpg")
		#frame = cv2.imread("F:\\BaiduYunDownload\\Video\\PICTURES\\20191127-DONGSHENG\\001241442e50\\001241442e50"+".jpg")
		print ("D:\\Tools\\camera\\" + station_name + "\\" + frame_name + "\\" + frame_name + yyy +".jpg")
		

		i = target_num
		j = 0
		send_data = {}
		while i:
			m0 = target_matrix[j][0]
			m1 = target_matrix[j][1]
			m11 = m1[0]
			m12 = m1[1]
			rlevel = target_matrix[j][2]
			glevel = target_matrix[j][3]
			rrbright = target_matrix[j][4]
			rgbright = target_matrix[j][5]
			rbbright = target_matrix[j][6]
			grbright = target_matrix[j][7]
			ggbright = target_matrix[j][8]
			gbbright = target_matrix[j][9]
			#print j,counter,m0,m1,m11,m12
			y0 = int(m11[1])
			y1 = int(m12[1])
			x0 = int(m11[0])
			x1 = int(m12[0])
			#print (y0,y1,x0,x1)
			cropped = frame[y0:y1,x0:x1]   #[y0:y1, x0:x1]
			#cv2.imwrite("D:\\Tools\\camera\\" + station_name + "\\" + frame_name + "\\" + m0 + ".jpg",cropped)
			print (m0)

			r_data = 0;
			###############################################################
			# style--> "name"(such as AA1.1141): value(such as 1,2,3)
			# B Y G R, 0x00(B)00(Y)00(G)00(R), 0(1:OK,0:Err)0(1:On,0:Off)
			###############################################################
			hand1 = m0.find("HANDLE")
			if hand1 >= 0:
				m0 = m0[0:hand1-1]
				x_data = detecthandle(cropped, rlevel)
				if x_data[0] == 1:
					if x_data[1] == 'W':
						r_data = 0xC0
					else:
						r_data = 0x80
				else:
					r_data = 0x00
			else:
				pos1 = m0.find("GREEN")
				pos2 = m0.find("RED")
				pos3 = m0.find("YELLOW")
				if pos1 >= 0:  # GREEN
					m0 = m0[0:pos1-1]
					tmp = send_data.get(m0)
					if tmp == None:
						tmp = 0
					r_data = tmp
					x_data = detectsingle(cropped,"GREEN",rlevel,rrbright,rgbright,rbbright)
					if x_data[0][1] == 'On':
						r_data = r_data + 12
					elif x_data[0][1] == 'Off':
						r_data = r_data + 8
					else:
						r_data = r_data
				elif pos2 >= 0: # RED
					m0 = m0[0:pos2-1]
					tmp = send_data.get(m0)
					if tmp == None:
						tmp = 0
					r_data = tmp
					x_data = detectsingle(cropped,"RED",rlevel,rrbright,rgbright,rbbright)
					if len(x_data) > 0:
						if x_data[0][1] == 'On':
							r_data = r_data + 3
						elif x_data[0][1] == 'Off':
							r_data = r_data + 2
						else:
							r_data = r_data
				elif pos3 >= 0: # YELLOW
					m0 = m0[0:pos3-1]
					tmp = send_data.get(m0)
					if tmp == None:
						tmp = 0
					r_data = tmp
					x_data = detectsingle(cropped,"YELLOW",rlevel,rrbright,rgbright,rbbright)
					if len(x_data) > 0:
						if x_data[0][1] == 'On':
							r_data = r_data + 48
						elif x_data[0][1] == 'Off':
							r_data = r_data + 32
						else:
							r_data = r_data
				else:
					r_data = 0
					x_data = detectstatus(cropped,rlevel,glevel,rrbright,rgbright,rbbright,grbright,ggbright,gbbright)
					if x_data is not None:
						x = len(x_data)
						y = 0
						while x:
							tmp0 = x_data[y]
							tmp1 = tmp0[0]
							tmp2 = tmp0[1]
							if tmp1 == 0: # red
								if tmp2 == 'On':
									r_data = r_data + 3
								elif tmp2 == 'Off':
									r_data = r_data + 2
								else:
									r_data = r_data
							else: # green
								if tmp2 == 'On':
									r_data = r_data + 12
								elif tmp2 == 'Off':
									r_data = r_data + 8
								else:
									r_data = r_data
							x = x - 1
							y = y + 1
							#print ("lamp status data is %d", (r_data))
					else:
						r_data = 0
			send_data.update({m0: r_data})
			i = i - 1
			j = j + 1
		#send detection result to network
		#print (send_data)
		#print (send_data_prev1)
		#print (send_data_prev2)

		if send_data == send_data_prev1 and send_data == send_data_prev2:
			print ("***************************************")
		send_data_prev2 = send_data_prev1
		send_data_prev1 = send_data
		print (send_data)
		#post_data(send_data,requrl,connection)
		#img_counter += 1
		#print("frame counter is: %d" %(img_counter))
		#time.sleep(1)

	break
	#cam.release()
	cv2.destroyAllWindows()
	#time.sleep(5)	#delay 5s

'''
while True:
	cam = set_camera()
	time.sleep(5)
	target_num = 0
	target_num,target_matrix = read_anno_config()
	print target_num, target_matrix

	while cam.isOpened():
		ret, frame = cam.read()
		if not ret:
			break
		#crop image and detect status
		i = target_num
		j = 0
		send_data = {}
		while i:
			m0 = target_matrix[j*2]
			m1 = target_matrix[j*2+1]
			m11 = m1[0]
			m12 = m1[1]
			#print j,counter,m0,m1,m11,m12
			y0 = m11[1]
			y1 = m12[1]
			x0 = m11[0]
			x1 = m12[0]
			#print y0,y1,x0,x1
			cropped = frame[y0:y1,x0:x1]   #[y0:y1, x0:x1]
			r_data = 0;
			###############################################################
			# style--> "name"(such as AA1.1141): value(such as 1,2,3)
			# B Y G R, 0x00(B)00(Y)00(G)00(R), 0(1:OK,0:Err)0(1:On,0:Off)
			###############################################################
			pos1 = m0.find("GREEN")
			pos2 = m0.find("RED")
			pos3 = m0.find("YELLOW")
			if pos1 >= 0:  # GREEN
				m0 = m0[0:pos1-1]
				tmp = send_data.get(m0)
				if tmp == None:
					tmp = 0
				r_data = tmp
				x_data = detectsingle(cropped,"GREEN")
				if x_data[0][1] == 'On':
					r_data = r_data + 12
				elif x_data[0][1] == 'Off':
					r_data = r_data + 8
				else:
					r_data = r_data
			elif pos2 >= 0: # RED
				m0 = m0[0:pos2-1]
				tmp = send_data.get(m0)
				if tmp == None:
					tmp = 0
				r_data = tmp
				x_data = detectsingle(cropped,"RED")
				if len(x_data) > 0:
					if x_data[0][1] == 'On':
						r_data = r_data + 3
					elif x_data[0][1] == 'Off':
						r_data = r_data + 2
					else:
						r_data = r_data
			elif pos3 >= 0: # YELLOW
				m0 = m0[0:pos3-1]
				tmp = send_data.get(m0)
				if tmp == None:
					tmp = 0
				r_data = tmp
				x_data = detectsingle(cropped,"YELLOW")
				if len(x_data) > 0:
					if x_data[0][1] == 'On':
						r_data = r_data + 48
					elif x_data[0][1] == 'Off':
						r_data = r_data + 32
					else:
						r_data = r_data
			else:
				r_data = 0
				x_data = detectstatus(cropped)
				if x_data is not None:
					x = len(x_data)
					y = 0
					while x:
						tmp0 = x_data[y]
						tmp1 = tmp0[0]
						tmp2 = tmp0[1]
						if tmp1 == 0: # red
							if tmp2 == 'On':
								r_data = r_data + 3
							elif tmp2 == 'Off':
								r_data = r_data + 2
							else:
								r_data = r_data
						else: # green
							if tmp2 == 'On':
								r_data = r_data + 12
							elif tmp2 == 'Off':
								r_data = r_data + 8
							else:
								r_data = r_data
						x = x - 1
						y = y + 1
						#print ("lamp status data is %d", (r_data))
				else:
					r_data = 0
			send_data.update({m0: r_data})
			i = i - 1
			j = j + 1
		#send detection result to network
		print send_data
		post_data(send_data,requrl,connection)
		img_counter += 1
		print("frame counter is: %d" %(img_counter))
		time.sleep(2)

	cam.release()
	cv2.destroyAllWindows()
	time.sleep(5)	#delay 5s
'''