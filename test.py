import os
import numpy
import cv2
import time
from detectstatus import detectstatus
from detectstatus import detectsingle
from detectstatus import detecthandle

station = "shouxiang"
device = "001241137b9e"
picture = "AA14.001.YELLOW"
frame = cv2.imread("D:\\Tools\\camera\\" + station + "\\" + device + "\\" + picture + ".jpg")
#frame = cv2.imread("F:\\BaiduYunDownload\\Video\\PICTURES\\20191127-DONGSHENG\\001241442e50\\001241442e50"+".jpg")
#print ("D:\\Tools\\camera\\1fullimage\\20191127-DONGSHENG\\001241442dd7\\test1.jpg")
        

#detectsingle(cropped,"GREEN",rlevel,rrbright,rgbright,rbbright)
#x_data = detectsingle(frame,"GREEN",10,0,200,100)
#x_data = detectsingle(frame,"RED",0,200,0,100)
x_data = detectsingle(frame,"YELLOW",0,0,200,100)
#x_data = detectstatus(cropped,rlevel,glevel,rrbright,rgbright,rbbright,grbright,ggbright,gbbright)
#x_data = detectstatus(frame,0,10,200,0,100,0,200,100)

print (x_data)