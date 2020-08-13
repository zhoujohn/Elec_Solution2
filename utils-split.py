import os
import numpy
import cv2
import time
from detectstatus import detectstatus
from detectstatus import detectsingle
from detectstatus import detecthandle 


station = "ruichen"
device = "0012413d7742"
picture = "AA2.1.GREEN"
img = cv2.imread("D:\\Tools\\camera\\" + station + "\\" + device + "\\" + picture + ".jpg")
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #变成GRAY格式
b,g,r = cv2.split(img)

cv2.imshow("blue", b)
cv2.imshow("green", g)
cv2.imshow("red", r)

avgb = cv2.mean(b)
avgg = cv2.mean(g)
avgr = cv2.mean(r)
print (avgb, avgg, avgr)


cv2.waitKey(1)
time.sleep(5)
cv2.destroyAllWindows()


