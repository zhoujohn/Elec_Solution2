import numpy as np
import cv2
import time

cv_version = 36


### input value: draw=True,show, draw=False, not show
### return value:[1,'W']horizontal, [1,'H']vertical,[0,'N']no result
### detection region is inside 0.1~0.8
def detect_Lockgate_Status(inImg, draw=False):
    if inImg is None:
        preresult = [0, 'N']
        return preresult

    w = inImg.shape[1]
    h = inImg.shape[0]
    if h < 100:
        scale = 2
    else:
        scale = 1

    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    result = [0,'N']

    areaThresh = resizeImg.shape[0]*resizeImg.shape[1]
    minArea = 0.1 * areaThresh
    maxArea = 0.6 * areaThresh

    showimg =resizeImg.copy()

    if inImg.shape[2] == 3:
        gray_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = np.copy(resizeImg)


    img = cv2.medianBlur(gray_img, 5)
    ret,th2 = cv2.threshold(img,90,255,cv2.THRESH_BINARY_INV)
    
    
    #print(ret,th2 )

    th2,contours,hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        for cnt in contours:
            area=cv2.contourArea(cnt)
           
            if area >  minArea and area < maxArea:                
                x,y,w,h=cv2.boundingRect(cnt)

                if draw == True:
                    img=cv2.rectangle(showimg,(x,y),(x+w,y+h),(0,255,0),2)

                #print('w , h:',w , h)

                if w > h:
                    if h < th2.shape[0]/2:
                        result =  [1,'W']
                    else:
                        result = [0, 'W']
                else:
                    if w < th2.shape[1]/2:
                        result =  [1,'H']
                    else:
                        result = [0, 'H']
                    

    if draw == True:
        cv2.imshow("showimg",showimg)
        cv2.waitKey(5)

    return result
    

def detect_LED_green(inImg, level):
    saturation = 130
    brightness = 40
    if level == 1:
        saturation = 140
        brightness = 120
    elif level == 2:
        saturation = 130
        brightness = 90
    elif level == 3:
        saturation = 130
        brightness = 75
    elif level == 4:
        saturation = 120
        brightness = 60
    elif level == 5:
        saturation = 100
        brightness = 40
    else:
        saturation = 120
        brightness = 40
    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 100:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    hsv_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2HSV)

    low_range1 = np.array([60, saturation, brightness])
    high_range1 = np.array([96, 255, 255])
    th1 = cv2.inRange(hsv_img, low_range1, high_range1)
    dilated = cv2.dilate(th1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)), iterations=2)
    #cv2.imshow('green', dilated)
    #cv2.waitKey(2)

    #dst = cv2.addWeighted(dilated, 0.5, dilated1, 0.5, 0);

    img = cv2.medianBlur(dilated, 5)
    
    
    #th2 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
  
    circles = [[0,0,0]]
    if cv_version == 24:
    	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=100,param2=10,minRadius=12,maxRadius=60) #10,40
    else:
    	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=100,param2=10,minRadius=12,maxRadius=60) #10,40

    #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=10,maxRadius=50)

    #print (circles)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
    else:
        print("cannot get valid value!")
    
    #if circles != None: 
    #if circles :
    
    #print ("green circle is:",circles)
    
    return circles

def detect_LED_red(inImg, level):
    saturation = 130
    brightness = 60
    if level == 1:
        saturation = 140
        brightness = 130
    elif level == 11:
        saturation = 100
        brightness = 130  # special for some scenario, saturation is very low, but brightness is normal
    elif level == 2:
        saturation = 130
        brightness = 100
    elif level == 3:
        saturation = 130
        brightness = 80
    elif level == 4:
        saturation = 120
        brightness = 60
    elif level == 61:
        saturation = 130
        brightness = 160
    elif level == 62:
        saturation = 140
        brightness = 130
    else:
        saturation = 120
        brightness = 40
    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 100:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    hsv_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2HSV)

    low_range = np.array([130, saturation, brightness])
    high_range = np.array([180, 255, 255])
    th = cv2.inRange(hsv_img, low_range, high_range)
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)), iterations=2)
    #cv2.imshow('red', dilated)
    #cv2.waitKey(2)

    #dst = cv2.addWeighted(dilated, 0.5, dilated1, 0.5, 0);

    img = cv2.medianBlur(dilated, 5)
    
    
    #th2 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
  
    circles = [[0,0,0]]
    if cv_version == 24: 
    	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=100,param2=10,minRadius=12,maxRadius=60) #10,40
    else:
    	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=100,param2=10,minRadius=12,maxRadius=60) #10,40

    #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=10,maxRadius=50)

    #print (circles)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))  
    else:
        print("cannot get valid value!")
    
    
    #print ("red circles is:",circles)
    
    return circles


def detect_LED_yellow(inImg, level):
    saturation = 130
    brightness = 60
    if level == 1:
        saturation = 120
        brightness = 150
    elif level == 2:
        saturation = 120
        brightness = 150
    elif level == 3:
        saturation = 130
        brightness = 130
    elif level == 4:
        saturation = 120
        brightness = 120
    elif level == 51:
        saturation = 100
        brightness = 60
    else:
        saturation = 120
        brightness = 100
    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 100:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    hsv_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2HSV)

    low_range = np.array([15, saturation, brightness])
    high_range = np.array([50, 255, 255])
    th = cv2.inRange(hsv_img, low_range, high_range)
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8)), iterations=2)
    #cv2.imshow('yellow', dilated)
    #cv2.waitKey(2)

    #dst = cv2.addWeighted(dilated, 0.5, dilated1, 0.5, 0);

    img = cv2.medianBlur(dilated, 5)
    
    
    #th2 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
  
    circles = [[0,0,0]] 
    if cv_version == 24:
    	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=100,param2=10,minRadius=12,maxRadius=60) #10,40
    else:
    	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=100,param2=10,minRadius=12,maxRadius=60) #10,40

    #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=10,maxRadius=50)

    #print (circles)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
    else:
        print("cannot get valid value!")
    
    
    #print ("yellow circles is:",circles)
    
    return circles


def check_Hsv_LED(inImg,circles,level):
    #if inImg.size == 0:
    #    return
    thres_zero = 120
    thres_onoff = 120
    if level == 1:
        thres_zero = 120
        thres_onoff = 120
    elif level == 2:
        thres_zero = 120
        thres_onoff = 120
    elif level == 3:
        thres_zero = 110
        thres_onoff = 110
    elif level == 4:
        thres_zero = 110
        thres_onoff = 110
    elif level == 51:
        thres_zero = 200
        thres_onoff = 180
    elif level == 61:
        thres_zero = 80
        thres_onoff = 80
    elif level == 62:
        thres_zero = 120
        thres_onoff = 120
    else:
        thres_zero = 110
        thres_onoff = 110
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 100:
        scale = 2
    else:
        scale = 1
        
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    wigth_tmp = resizeImg.shape[1]
    light_imgs = []
    for i in circles[0,:]:
        x = i[0]
        
        y = i[1]
        r = i[2]
        #rect_x = (x - r)
        #rect_y = (y - r)
        #crop_img = resizeImg[rect_y:(y+r),rect_x:(x+r)]
        # for brightness check, only get the value with radius 15
        if r > 10:
        	r = 10
        rect_x = (x - r)
        rect_y = (y - r)
        crop_img = resizeImg[rect_y:(y+r),rect_x:(x+r)]
        light_imgs.append(crop_img)
        #cv2.imshow("cropped image", crop_img)
        #cv2.waitKey(2)

    light_colors = []

    for cropimg in light_imgs:
        
        if cropimg.shape[1] == 0 or cropimg.shape[0] == 0:
            continue
        light_color = 0
        img_gray = cv2.cvtColor(cropimg, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img_gray, 5)
        if img is None:
            light_colors.append(light_color)
            return light_colors
        ret, img = cv2.threshold(img,thres_zero,255,cv2.THRESH_TOZERO)
  
        #cv2.imshow("gray", img)
        #cv2.waitKey(2)

        scalar = cv2.mean(img)

        #print (scalar)
        uscalar = np.uint16(np.around(scalar))

        if uscalar[0] > thres_onoff:
            light_color = 1
        else:
            light_color = 0

        light_colors.append(light_color)

    #print (light_colors)
            
    return light_colors


################Testing####################################        
#src = cv2.imread("D:\\video\\pic\\rgb_r2.png") #rgb_r1.png #rgb_r2 #rgb_r3 #rgb_r4 #rgb_r5 rgb_r6
#only valid for check green and red leds
def detectstatus(src, rlevel, glevel):
    w = src.shape[1]
    h = src.shape[0]
    if h < 100:
        scale = 2
    else:
        scale = 1
       
    #print (w,h)
    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)
    
    light_colors = []
    light_color = []
    circles = [[]]

    # detect green
    circles = detect_LED_green(resizeImg,glevel)

    if circles is not None:
        status = check_Hsv_LED(resizeImg,circles,glevel)
        if len(status) > 0:
            if status[0] == 1:
                light_color = [1, "On"]
            else:
                light_color = [1, "Off"]
        else:
            light_color = [1, "Err"]
    else: 
        light_color = [1, 'Err']

    light_colors.append(light_color)

    #detect red
    circles = detect_LED_red(resizeImg,rlevel)

    if circles is not None:
        status = check_Hsv_LED(resizeImg,circles,rlevel)
        if len(status) > 0:
            if status[0] == 1:
                light_color = [0, "On"]
            else:
                light_color = [0, "Off"]
        else:
            light_color = [0, 'Err']
    else: 
        light_color = [0, 'Err']

    light_colors.append(light_color)

    #print (light_colors)
    
    return light_colors


def detectsingle(src, type, level):
    w = src.shape[1]
    h = src.shape[0]
    if h < 100:
        scale = 2
    else:
        scale = 1
        
    #print (w,h)
    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)
    
    color_index = 0
    circles = [[]]
    if type == "GREEN":
        color_index = 1
        circles = detect_LED_green(resizeImg,level)
    elif type == "YELLOW":
        color_index = 2
        circles = detect_LED_yellow(resizeImg,level)
    else:
        color_index = 0
        circles = detect_LED_red(resizeImg,level)

    light_colors = []
    light_color = []
    if circles is not None:
        status = check_Hsv_LED(resizeImg,circles,level)
        if len(status) > 0:
            if status[0] == 1:
                light_color = [color_index, "On"]
            else:
                light_color = [color_index, "Off"]
        else:
            light_color = [color_index, 'Err']
    else: 
        light_color = [color_index, 'Err']

    light_colors.append(light_color)
    #print (light_colors)
    
    return light_colors

def test():
    src = cv2.imread("F:\\Pic\\test8.jpg") #
    #lock_gate-1.jpg
    #lock_gate-2.jpg
    #lock_gate-3.jpg
    
    w = src.shape[1]
    h = src.shape[0]
    if h < 100:
        scale = 2
    else:
        scale = 1


    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    light_colors = []
    light_color = []
    #result = detect_spatial_LED(resizeImg)
    result = detect_LED_yellow(resizeImg)
    if result is not None:
        status = check_Hsv_LED(resizeImg, result)
        if status[0] == 1:
            light_color = [0, "On"]
        else:
            light_color = [0, "Off"]
    else:
        light_color = [[0,"Err"]]
    #result = detect_Lockgate_Status(resizeImg,draw = False)
    light_colors.append(light_color)
    print (light_colors)

    time.sleep(15)


def detecthandle(src):
    w = src.shape[1]
    h = src.shape[0]
    if h < 100:
        scale = 2
    else:
        scale = 1

    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    result = detect_Lockgate_Status(resizeImg,draw = False)

    return result


#detectstatus()

