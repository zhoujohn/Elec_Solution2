import time
import sys
import json
import urllib
import httplib


def post_data(send_data, requrl, connection):
	#urlencode = urllib.urlencode(send_data)
	prefix = json.dumps({'from':'aicam','topic':'cam_test','qos':1,'encrypt':0,'payload':send_data})
	
	# requrl = "http://192.168.81.16/cgi-bin/python_test/test.py"
	headerdata = {"Detection":"Power Distribution Cabinet Autodetection"}

	# send data to url
	conn = httplib.HTTPConnection(connection)
	conn.request(method="POST",url=requrl,body=prefix,headers = headerdata) 
	response = conn.getresponse()
	res= response.read()
	print res


def test_load_config():
	counter = 0
	matrix = []
	with open("./config/anno.json") as load_f:
		load_dict = json.load(load_f)
		load_dict1 = load_dict["shapes"]
		for val in load_dict1:
			counter = counter + 1
			print val
			print counter
			matrix.append(val["label"])
			matrix.append(val["points"])
		print matrix
	return counter,matrix

def test_load_cam():
	width = 0
	height = 0
	expo = 0.0
	with open("./config/cam.json") as load_f:
		load_dict = json.load(load_f)
		width = load_dict["width"]
		height = load_dict["height"]
		expo = load_dict["exposure"]
	return width, height, expo


#send_data = {}
#counter,matrix = test_load_config()
#print counter,matrix
#j = 0
#while counter:
	#m0 = matrix[j*2]
	#m1 = matrix[j*2+1]
	#m11 = m1[0]
	#m12 = m1[1]
	#print j,counter,m0,m1,m11,m12
	#y0 = m11[1]
	#y1 = m12[1]
	#x0 = m11[0]
	#x1 = m12[0]
	#print y0,y1,x0,x1
	#j = j + 1
	#counter = counter - 1
	#send_data.update({str(j):j})
	#print send_data

#aaa = []
#bbb = []
#ccc = [0, 'E']
#ddd = [[1, 'E']]
#eee = [[0,'G'], [1,'R']]
#fff = [[0,'R'], [1,'N']]
#ggg = [[0,'N'], [1,'G']]
#hhh = [[0,'R'], [1,'G']]
#iii = [[0,'E'], [1,'E']]
#jjj = [[0,'N'], [1,'R']]
#kkk = [[0,'G'], [1,'N']]

#send_data = {}
#r_data = 10
#x_data = kkk
#x_data.append(ccc)
#print x_data
#m0 = "AA1.1111"
###############################################################
# style--> "name"(such as AA1.1141): value(such as 1,2,3)
# B Y G R, 0x00(B)00(Y)00(G)00(R), 0(1:OK,0:Err)0(1:On,0:Off)
###############################################################
'''
if x_data is None:
	r_data = 0  # default R:off, G:off
elif len(x_data):
	#parse status of lamp
	x = len(x_data)
	y = 0
	while x:
		tmp0 = x_data[y]
		print tmp0
		tmp1 = tmp0[1]
		print tmp1
		if tmp1 == 'R':
			r_data = r_data + 1
		elif tmp1 == 'G':
			r_data = r_data + 4
		elif tmp1 == 'E':
			r_data = 0
		else:
			r_data = r_data
		x = x - 1
		y = y + 1
		print ("lamp status data is %d", (r_data))
else:
	r_data = 0
send_data.update({m0 : r_data})
print send_data
send_data.update({"m0" : 3})
print send_data
send_data.update({"m1" : 3})
print send_data
'''

#print test_load_cam()
