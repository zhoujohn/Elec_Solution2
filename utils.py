import os
import numpy
import cv2
import time


# 定义鼠标交互函数
def mouseColor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('HSV:', hsv[y, x])  #输出图像坐标(x,y)处的HSV的值


station = "shouxiang"
device = "001241137b9e"
picture = "AA14.001.YELLOW"
img = cv2.imread("D:\\Tools\\camera\\" + station + "\\" + device + "\\" + picture + ".jpg")


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #变成HSV格式

cv2.namedWindow("Color Picker")
cv2.setMouseCallback("Color Picker", mouseColor)
cv2.imshow("Color Picker", img)
if cv2.waitKey(0):
    cv2.destroyAllWindows()
