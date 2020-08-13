import os
import numpy
import cv2
import time


# 定义鼠标交互函数
def mouseColor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Gray:', gray[y, x])  #输出图像坐标(x,y)处的GRAY的值

station = "ruichen"
device = "0012413d873e"
picture = "AA2.1.GREEN"
img = cv2.imread("D:\\Tools\\camera\\" + station + "\\" + device + "\\" + picture + ".jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #变成GRAY格式
#gray = img
cv2.namedWindow("Color Picker")
cv2.setMouseCallback("Color Picker", mouseColor)
cv2.imshow("Color Picker", img)
if cv2.waitKey(0):
    cv2.destroyAllWindows()
