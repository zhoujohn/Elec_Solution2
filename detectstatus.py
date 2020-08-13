import numpy as np
import cv2
import time

cv_version = 36


### input value: draw=True,show, draw=False, not show
### return value:[1,'W']horizontal, [1,'H']vertical,[0,'N']no result
### detection region is inside 0.1~0.8
### steps: threshold & binarization --> erode & dilate --> findcontours --> discrimination
def detect_Lockgate_Status(inImg, rlevel, draw=False):
    if inImg is None:
        preresult = [0, 'N']
        return preresult

    w = inImg.shape[1]
    h = inImg.shape[0]
    if h < 120:
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

    low_thres = 10
    right = 1
    if rlevel == 1:
    	low_thres = 10
    if rlevel == 2:
        low_thres = 20
    elif rlevel == 3:
        low_thres = 30
    elif rlevel == 4:
        low_thres = 40
    elif rlevel == 5:
    	low_thres = 50
    elif rlevel == 6:
    	low_thres = 60
    elif rlevel == 7:
    	low_thres = 0
    	right = 2
    else:
        low_thres = 10

    scalar_med = cv2.mean(gray_img)
    scalar1 = np.uint16(np.around(scalar_med))[0]

    #print (scalar1)

    low_thres = scalar1 - low_thres
    #print (scalar1, low_thres)

    img = cv2.medianBlur(gray_img, 5)
    ret,th2 = cv2.threshold(img,low_thres,255,cv2.THRESH_BINARY_INV)
    
    kernel_size = int(int(scale * h)/30)    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_size, kernel_size))

    kernel_size1 = int(int(scale * h)/20)    
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_size, kernel_size1))


    #cv2.imshow("showimg",th2)
    #cv2.waitKey(5)
    #time.sleep(2)

    th2 = cv2.erode(th2, kernel)
    #cv2.imshow("showimg",th2)
    #cv2.waitKey(5)
    #time.sleep(2)
    th2 = cv2.dilate(th2, kernel1)
    #cv2.imshow("showimg",th2)
    #cv2.waitKey(5)
    #time.sleep(2)
    #draw = True
    contours,hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        for cnt in contours:
            area=cv2.contourArea(cnt)
            #print('w , h:',w , h)
            #print(area, minArea, maxArea)
            if area >  minArea/right and area < maxArea:                
                x,y,w,h=cv2.boundingRect(cnt)

                if draw == True:
                    img=cv2.rectangle(showimg,(x,y),(x+w,y+h),(0,255,0),2)

                #print('w , h:',w , h)

                if w > h:
                    if h < int(th2.shape[0]/1.5):
                        result =  [1,'W']
                    else:
                        result = [0, 'W']
                else:
                    if w < int(th2.shape[1]/1.5):
                        result =  [1,'H']
                    else:
                        result = [0, 'H']
                    
    if draw == True:
        cv2.imshow("showimg",showimg)
        cv2.waitKey(5)
        time.sleep(1)

    return result
    

#### level settings:=== strength of brightness:0-9; scope of HUE:0x-9x; saturation:0xx-9xx; param_2:0xxx-9xxx; g_detect
def detect_LED_green(inImg, level):
    saturation = 43
    brightness = 40
    hue_start = 76
    hue_end = 99
    param_2 = 10

    level = int(level)
    lev_bright = int(level%10)
    lev_hue = int(level%100)
    lev_hue = int(lev_hue/10)
    lev_sat = int(level%1000)
    lev_sat = int(lev_sat/100)
    lev_param = int(level/1000)

    #print (level, lev_bright, lev_hue, lev_sat, lev_param)

    # brightness
    if lev_bright == 0:
    	brightness = 40
    elif lev_bright == 1:
    	brightness = 60
    elif lev_bright == 2:
    	brightness = 100
    elif lev_bright == 3:
    	brightness = 30
    elif lev_bright == 4:
    	brightness = 20
    elif lev_bright == 5:
    	brightness = 0
    elif lev_bright == 6:
    	brightness = 50
    else:
    	brightness = 40

    # HUE
    if lev_hue == 0:
    	hue_start = 72
    	hue_end = 99
    elif lev_hue == 1:
    	hue_start = 72
    	hue_end = 110    # already used
    elif lev_hue == 2:
    	hue_start = 26
    	hue_end = 77     # special case like yellow light
    elif lev_hue == 3:
    	hue_start = 72
    	hue_end = 120    # already used
    elif lev_hue == 4:
    	hue_start = 72
    	hue_end = 140    # special use, for very low light
    elif lev_hue == 5:
    	hue_start = 70
    	hue_end = 99     # special for some green light, low luminance
    elif lev_hue == 6:
    	hue_start = 70
    	hue_end = 120
    
    # Saturation
    if lev_sat == 0:
    	saturation = 43
    elif lev_sat == 1:
    	saturation = 40
    elif lev_sat == 2:
    	saturation = 30

    convsize = []
    # Param_2
    if lev_param == 0:
    	param_2 = 10
    	convsize = [(1,1),(3,3)]
    elif lev_param == 1:
    	param_2 = 12
    	convsize = [(1,1),(3,3)]
    elif lev_param == 2:
    	param_2 = 16
    	convsize = [(1,1)]

    #print (brightness, hue_start, hue_end, saturation)

    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    scale = 1
    if h < 120:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    hsv_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2HSV)

    low_range1 = np.array([hue_start, saturation, brightness])
    high_range1 = np.array([hue_end, 255, 255])
    #low_range1 = np.array([76, saturation, brightness])
    #high_range1 = np.array([99, 255, 255])
    th1 = cv2.inRange(hsv_img, low_range1, high_range1)

    #cv2.imshow('green', th1)
    #cv2.waitKey(2)
    #time.sleep(1)

    ###------------------###### change hole value from 3 to 8 according to different brightness of light
    #convsize = [(1,1),(3,3),(8,8)]

    circles = [[]]
    #### try to use different parameter to meet different brightness of image
    for conv in convsize:
        dilated = cv2.dilate(th1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, conv), iterations=2)
        
        #cv2.imshow('green', dilated)
        #cv2.waitKey(2)
        #time.sleep(1)

        #dst = cv2.addWeighted(dilated, 0.5, dilated1, 0.5, 0);

        img = cv2.medianBlur(dilated, 5)
        
        
        #th2 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
      
        circles = [[0,0,0]]
        if cv_version == 24:
        	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,80,param1=80,param2=param_2,minRadius=12,maxRadius=60) #10,40
        else:
        	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,80,param1=80,param2=param_2,minRadius=12,maxRadius=60) #10,40

        #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=10,maxRadius=50)

        #print (circles)
        #if circles is not None:
        x = 0
        if circles is not None:
            #circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                x = i[0]
                break
            if x != 0:
                break
            break
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            x = i[0]
            if x == 0:
                circles = [[]]
                break
            #cv2.circle(resizeImg, (i[0], i[1]), i[2], (0,0,255), 4)
        #cv2.imshow('xxx', resizeImg)
        #cv2.waitKey(2)
        #time.sleep(1)
        #print (circles)
    #else:
    #    print("cannot get valid value!")
    
    #if circles != None: 
    #if circles :
    
    #print ("green circle is:",circles)
    
    return circles


#### level settings:=== strength of brightness:0-9; scope of HUE:0x-9x; saturation:0xx-9xx; param_2:0xxx-9xxx; r_detect
def detect_LED_red(inImg, level):
    saturation = 100
    brightness = 60
    hough_para2 = 12
    minRadius = 12
    hue_start = 150
    hue_end = 180

    level = int(level)
    lev_bright = int(level%10)
    lev_hue = int(level%100)
    lev_hue = int(lev_hue/10)
    lev_sat = int(level%1000)
    lev_sat = int(lev_sat/100)
    lev_param = int(level/1000)

    # brightness
    if lev_bright == 0:
    	brightness = 60
    elif lev_bright == 1:
    	brightness = 100
    elif lev_bright == 2:
    	brightness = 80
    elif lev_bright == 3:
    	brightness = 40
    elif lev_bright == 4:
    	brightness = 30
    else:
    	brightness = 60

    # HUE
    if lev_hue == 0:
    	hue_start = 150
    	hue_end = 180
    elif lev_hue == 1:
    	hue_start = 160
    	hue_end = 180
    elif lev_hue == 2:
    	hue_start = 130
    	hue_end = 180
    
    
    # Saturation
    if lev_sat == 0:
    	saturation = 90
    elif lev_sat == 1:
    	saturation = 60
    elif lev_sat == 2:
    	saturation = 50

    convsize = []
    # Param_2
    if lev_param == 0:
    	hough_para2 = 10
    	convsize = [(1,1),(3,3)]
    elif lev_param == 1:
    	hough_para2 = 8
    	convsize = [(1,1),(3,3)]
    	minRadius = 9


    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]

    #print (w,h)
    
    if h < 120:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    hsv_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2HSV)

    #hsv_img = cv2.GaussianBlur(hsv_img,(3,3),0)
    #low_range = np.array([156, saturation, brightness])
    #low_range = np.array([156, 100, 40])
    low_range = np.array([hue_start, saturation, brightness])
    high_range = np.array([hue_end, 255, 255])
    th = cv2.inRange(hsv_img, low_range, high_range)

    ###------------------###### change hole value from 3 to 8 according to different brightness of light
    

    circles = [[]]
    #### try to use different parameter to meet different brightness of image
    for conv in convsize:
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, conv), iterations=2)
        #cv2.imshow('red', dilated)
        #cv2.waitKey(2)
        #time.sleep(1)

        #dst = cv2.addWeighted(dilated, 0.5, dilated1, 0.5, 0);

        img = cv2.medianBlur(dilated, 5)
        
        
        #th2 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
      
        circles = [[0,0,0]]
        if cv_version == 24: 
        	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,80,param1=100,param2=12,minRadius=12,maxRadius=60) #10,40
        else:
        	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,80,param1=80,param2=hough_para2,minRadius=minRadius,maxRadius=60) #10,40
        #print (circles, conv)
        x = 0
        if circles is not None:
            #circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                x = i[0]
                break
            if x != 0:
                break


    #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=10,maxRadius=50)

    #print (circles)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            x = i[0]
            if x == 0:
                circles = [[]]
                break
            
        #for i in circles[0,:]:
        #    x = i[0]
        #    y = i[1]
        #    r = i[2]
        #    cv2.circle(resizeImg,(x,y),r,(0,0,255),-1)
        #cv2.imshow('xxx', resizeImg)
        #cv2.waitKey(2)
        #time.sleep(1)
        #print (circles)
    #else:
    #    print("cannot get valid value!")
    
    
    #print ("red circles is:",circles)
    
    return circles


#### level settings:=== strength of brightness:0-9; scope of HUE:0x-9x; saturation:0xx-9xx; param_2:0xxx-9xxx; r_detect
def detect_LED_yellow(inImg, level):
    saturation = 130
    brightness = 60
    hue_start = 26
    hue_end = 77

    level = int(level)
    lev_bright = int(level%10)
    lev_hue = int(level%100)
    lev_hue = int(lev_hue/10)
    lev_sat = int(level%1000)
    lev_sat = int(lev_sat/100)
    lev_param = int(level/1000)

    # brightness
    if lev_bright == 0:
    	brightness = 60
    elif lev_bright == 1:
    	brightness = 100
    elif lev_bright == 2:
    	brightness = 80
    elif lev_bright == 3:
    	brightness = 40
    elif lev_bright == 4:
    	brightness = 30
    else:
    	brightness = 60

    # HUE
    if lev_hue == 0:
    	hue_start = 26
    	hue_end = 77
    elif lev_hue == 1:
    	hue_start = 26
    	hue_end = 77
    
    
    # Saturation
    if lev_sat == 0:
    	saturation = 120
    elif lev_sat == 1:
    	saturation = 130
    elif lev_sat == 2:
    	saturation = 100

    # Param_2
    if lev_param == 0:
    	hough_para2 = 12


    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]

    #print (w,h)
    
    if h < 120:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    hsv_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2HSV)

    #low_range = np.array([15, saturation, brightness])
    #high_range = np.array([50, 255, 255])
    low_range = np.array([hue_start, saturation, brightness])
    high_range = np.array([hue_end, 255, 255])
    th = cv2.inRange(hsv_img, low_range, high_range)

    convsize = [(1,1),(3,3)]
    circles = [[]]
    #### try to use different parameter to meet different brightness of image
    for conv in convsize:
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, conv), iterations=2)
        #cv2.imshow('yellow', dilated)
        #cv2.waitKey(2)
        #time.sleep(5)

        #dst = cv2.addWeighted(dilated, 0.5, dilated1, 0.5, 0);

        img = cv2.medianBlur(dilated, 5)
        
        #th2 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
      
        circles = [[0,0,0]] 
        if cv_version == 24:
        	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=100,param2=hough_para2,minRadius=12,maxRadius=60) #10,40
        else:
        	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=100,param2=hough_para2,minRadius=12,maxRadius=60) #10,40

        #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=10,maxRadius=50)

        #print (circles)
        if circles is not None:
            break
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        #for i in circles[0,:]:
        #    x = i[0]
        #    y = i[1]
        #    r = i[2]
        #    cv2.circle(resizeImg,(x,y),r,(0,0,255),-1)
        #cv2.imshow('xxx', resizeImg)
        #cv2.waitKey(2)
        #time.sleep(1)
        #print (circles)
    #else:
    #    print("cannot get valid value!")
    
    
    #print ("yellow circles is:",circles)
    
    return circles


def choose_brightest_area(inImg, radius, ksize):
    if radius <= ksize:
        ksize = radius

    w = inImg.shape[1]
    h = inImg.shape[0]

    loop_w = np.uint16((w/ksize)*2)
    loop_h = np.uint16((h/ksize)*2)
    loop_h_s = loop_h
    steps = np.uint16(ksize/2)

    #print ('--------------------')
    #print (w, h, radius, ksize, loop_w, loop_h, steps)
    scalar_can = []

    x = 0
    y = 0
    #resizeImg[rect_y:(y+rr),rect_x:(x+rr)]
    while loop_w:
        while loop_h:
            tmp = cv2.mean(inImg[y:(y+ksize),x:(x+ksize)])
            tmp = np.uint16(np.around(tmp))
            scalar_can.append(tmp[0])
            x+=np.uint16(ksize/2)
            loop_h -=1
        x = 0
        loop_h = loop_h_s
        y+=np.uint16(ksize/2)
        loop_w-=1
        #print (x,y,scalar_can)
        #time.sleep(1)
    #print (x,y,scalar_can)
    # We get an array with ksize*ksize conv and steps, next step is calculate the max value in it
    max_v = 0
    for v in scalar_can:
        if v > max_v:
            max_v = v
    #print (max_v)

    return max_v
    #time.sleep(100)


#### level settings:=== strength of average brightness:r_bright; variance:r_variance;  
#### standard1: brightness difference between area inside the circle and outside the circle;
#### standard2: variance of the image which including the circle but not triple bigger than the circle
#### pos: 0--r/left,g/right; 1-g/left,r/right
def check_Hsv_LED_red(inImg,circles,r_bright,g_bright,b_bright):
    #if inImg.size == 0:
    #    return

    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 120:
        scale = 2
    else:
        scale = 1
        
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    circle_max = circles[0][0]
    #print (circles)
    r_max = circle_max[2]
    for i in circles[0,:]:
        x = i[0]
        y = i[1]
        r = i[2]
        if r > r_max:
            r_max = r
            circle_max = i
        #rect_x = (x - r)
        #rect_y = (y - r)
        #crop_img = resizeImg[rect_y:(y+r),rect_x:(x+r)]
        # for brightness check, only get the value with radius 15
        #if r > 10:
        #   r = 10
    #print (circle_max)
    x = circle_max[0]
    y = circle_max[1]
    r = circle_max[2]
    if r < 16:
    	r = r-4
    elif r < 32:
    	r = r-8
    else:
    	r = r-12

    if x < r:
        r = x
    if (x + r) > resizeImg.shape[1]:
        r = resizeImg.shape[1] - x
    if y < r:
        r = y
    if (y + r) > resizeImg.shape[0]:
        r = resizeImg.shape[0] - y
    if r > resizeImg.shape[0]/4:
    	r = int(r/2)
    #print (x,y,r, resizeImg.shape[0], resizeImg.shape[1])

    crop_img1 = resizeImg[(y-(r-0)):(y+(r-0)),(x-(r-0)):(x+(r-0))]
    #crop_img2 = resizeImg[(y-r):(y+r),(x-r-r):(x+r+r)]
    #cv2.imshow('xxx', crop_img1)
    #cv2.waitKey(2)
    #time.sleep(1)

    light_colors = []

    if crop_img1 is None:
        light_colors.append(light_color)
        return light_colors

    b,g,r = cv2.split(crop_img1)
    b = cv2.medianBlur(b, 3)
    g = cv2.medianBlur(g, 3)
    r = cv2.medianBlur(r, 3)
    
    avgb = cv2.mean(b)
    avgg = cv2.mean(g)
    avgr = cv2.mean(r)

    #print (scalar_a, scalar1)

    ### We have a very bright environment, so we think if environment brightness is higher than max area brightness, we think light is off
    ### since if light is on, it will be over exposure regarding to environment brightness.
    #print (avgb, avgg, avgr)
    if int(avgr[0]) >= r_bright and int(avgg[0]) >= g_bright and int(avgb[0]) >= b_bright:
        light_color = 1
    else:
        light_color = 0

    light_colors.append(light_color)

    #print (light_colors)
            
    return light_colors


#### level settings:=== strength of average brightness:g_bright; average hue:g_hue;  
#### standard1: brightness difference between area inside the circle and outside the circle;
#### standard2: chromatic aberration inside the circle
def check_Hsv_LED_green(inImg,circles,r_bright,g_bright,b_bright):
    #if inImg.size == 0:
    #    return

    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 120:
        scale = 2
    else:
        scale = 1
        
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    circle_max = circles[0][0]
    #print (circles)
    r_max = circle_max[2]
    for i in circles[0,:]:
        x = i[0]
        y = i[1]
        r = i[2]
        if r > r_max:
            r_max = r
            circle_max = i
        #rect_x = (x - r)
        #rect_y = (y - r)
        #crop_img = resizeImg[rect_y:(y+r),rect_x:(x+r)]
        # for brightness check, only get the value with radius 15
        #if r > 10:
        #   r = 10
    #print (circle_max)
    x = circle_max[0]
    y = circle_max[1]
    r = circle_max[2]
    if r < 16:
    	r = r-4
    elif r < 32:
    	r = r-8
    else:
    	r = r-12

    if x < r:
        r = x
    if (x + r) > resizeImg.shape[1]:
        r = resizeImg.shape[1] - x
    if y < r:
        r = y
    if (y + r) > resizeImg.shape[0]:
        r = resizeImg.shape[0] - y
    if r > resizeImg.shape[0]/4:
    	r = int(r/2)
    #print (x,y,r)


    crop_img1 = resizeImg[(y-(r-0)):(y+(r-0)),(x-(r-0)):(x+(r-0))]
    #cv2.imshow('xxx', crop_img1)
    #cv2.waitKey(2)
    #time.sleep(1)
    #crop_img2 = resizeImg[(y-r):(y+r),(x-r-r):(x+r+r)]
    #print (y,x,r)

    light_colors = []

    if crop_img1 is None:
        light_colors.append(light_color)
        return light_colors

    b,g,r = cv2.split(crop_img1)
    b = cv2.medianBlur(b, 3)
    g = cv2.medianBlur(g, 3)
    r = cv2.medianBlur(r, 3)
    
    avgb = cv2.mean(b)
    avgg = cv2.mean(g)
    avgr = cv2.mean(r)

    #print (scalar_a, scalar1)

    ### We have a very bright environment, so we think if environment brightness is higher than max area brightness, we think light is off
    ### since if light is on, it will be over exposure regarding to environment brightness.
    #print (avgb, avgg, avgr)
    if int(avgr[0]) >= r_bright and int(avgg[0]) >= g_bright and int(avgb[0]) >= b_bright:
        light_color = 1
    else:
        light_color = 0

    light_colors.append(light_color)

    #print (light_colors)
            
    return light_colors


#### level settings:=== strength of average brightness:r_bright; average hue:r_hue;  
#### standard1: brightness difference between area inside the circle and outside the circle;
#### standard2: chromatic aberration inside the circle
def check_Hsv_LED_yellow(inImg,circles,r_bright,g_bright,b_bright):
    #if inImg.size == 0:
    #    return

    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 120:
        scale = 2
    else:
        scale = 1
        
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    circle_max = circles[0][0]
    #print (circles)
    r_max = circle_max[2]
    for i in circles[0,:]:
        x = i[0]
        y = i[1]
        r = i[2]
        if r > r_max:
            r_max = r
            circle_max = i
        #rect_x = (x - r)
        #rect_y = (y - r)
        #crop_img = resizeImg[rect_y:(y+r),rect_x:(x+r)]
        # for brightness check, only get the value with radius 15
        #if r > 10:
        #   r = 10
    #print (circle_max)
    x = circle_max[0]
    y = circle_max[1]
    r = circle_max[2]
    if r < 16:
    	r = r-4
    elif r < 32:
    	r = r-8
    else:
    	r = r-12

    if x < r:
        r = x
    if (x + r) > resizeImg.shape[1]:
        r = resizeImg.shape[1] - x
    if y < r:
        r = y
    if (y + r) > resizeImg.shape[0]:
        r = resizeImg.shape[0] - y
    if r > resizeImg.shape[0]/4:
    	r = int(r/2)
    #print (x,y,r)

    crop_img1 = resizeImg[(y-(r-0)):(y+(r-0)),(x-(r-0)):(x+(r-0))]
    #cv2.imshow('xxx', crop_img1)
    #cv2.waitKey(2)
    #time.sleep(1)
    #crop_img2 = resizeImg[(y-r):(y+r),(x-r-r):(x+r+r)]

    light_colors = []

    if crop_img1 is None:
        light_colors.append(light_color)
        return light_colors

    b,g,r = cv2.split(crop_img1)
    b = cv2.medianBlur(b, 3)
    g = cv2.medianBlur(g, 3)
    r = cv2.medianBlur(r, 3)
    
    avgb = cv2.mean(b)
    avgg = cv2.mean(g)
    avgr = cv2.mean(r)

    #print (scalar_a, scalar1)

    ### We have a very bright environment, so we think if environment brightness is higher than max area brightness, we think light is off
    ### since if light is on, it will be over exposure regarding to environment brightness.
    #print (avgb, avgg, avgr)
    if int(avgr[0]) >= r_bright and int(avgg[0]) >= g_bright and int(avgb[0]) >= b_bright:
        light_color = 1
    else:
        light_color = 0

    light_colors.append(light_color)

    #print (light_colors)
            
    return light_colors


################Testing####################################        
#src = cv2.imread("D:\\video\\pic\\rgb_r2.png") #rgb_r1.png #rgb_r2 #rgb_r3 #rgb_r4 #rgb_r5 rgb_r6
#only valid for check green and red leds
def detectstatus(src, rlevel, glevel, rr_bright, rg_bright, rb_bright,gr_bright, gg_bright, gb_bright):
    w = src.shape[1]
    h = src.shape[0]
    if h < 120:
        scale = 2
    else:
        scale = 1
        
    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)
    
    light_colors = []
    light_color = []
    circles = [[]]

    # detect green
    circles = detect_LED_green(resizeImg,glevel)

    if circles is not None and len(circles[0]) != 0:
        status = check_Hsv_LED_green(resizeImg,circles,gr_bright,gg_bright,gb_bright)
        if len(status) > 0:
            if status[0] == 1:
                light_color = [1, "On"]
            else:
                light_color = [1, "Off"]
        else:
            light_color = [1, 'Err']
    else: 
        light_color = [1, 'Err']

    light_colors.append(light_color)

    #detect red
    circles = detect_LED_red(resizeImg,rlevel)

    if circles is not None and len(circles[0]) != 0:
        status = check_Hsv_LED_red(resizeImg,circles,rr_bright,rg_bright,rb_bright)
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


def detectsingle(src, type, level, r_bright, g_bright, b_bright):
    w = src.shape[1]
    h = src.shape[0]
    if h < 120:
        scale = 2
    else:
        scale = 1
        
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
    if circles is not None and len(circles[0]) != 0:
        if type == "GREEN":
            status = check_Hsv_LED_green(resizeImg,circles,r_bright,g_bright,b_bright)
        elif type == "YELLOW":
            status = check_Hsv_LED_yellow(resizeImg,circles,r_bright,g_bright,b_bright)
        else:
            status = check_Hsv_LED_red(resizeImg,circles,r_bright,g_bright,b_bright)
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

def detect_LED_gray(src):
    print (src)

    inImg = cv2.imread(src)
    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 120:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    img_gray = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img_gray, 5)
    img_bin = cv2.threshold(img,110,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('green', img_gray)
    cv2.waitKey(2)
    time.sleep(1)
    


    ###------------------###### change hole value from 3 to 8 according to different brightness of light
    convsize = [(1,1)]

    circles = [[]]
    #### try to use different parameter to meet different brightness of image
    for conv in convsize:
        dilated = cv2.dilate(img, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, conv), iterations=2)
        img = dilated
        #dst = cv2.addWeighted(dilated, 0.5, dilated1, 0.5, 0);
        #img = cv2.medianBlur(dilated, 5)
        #ret,img = cv2.threshold(img,60,255,cv2.THRESH_BINARY_INV)
        #cv2.imshow('green', img)
        #cv2.waitKey(2)
        #time.sleep(1)
        
        
        #img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
      
        circles = [[0,0,0]]
        if cv_version == 24:
            circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,10,param1=250,param2=20,minRadius=12,maxRadius=60) #10,40
        else:
            circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,param1=250,param2=20,minRadius=12,maxRadius=60) #10,40

        #circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=10,maxRadius=50)

        #print (circles)
        if circles is not None:
            break
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            x = i[0]
            y = i[1]
            r = i[2]
            cv2.circle(resizeImg,(x,y),r,(0,0,255),-1)
        #cv2.imshow('xxx', resizeImg)
        #cv2.waitKey(2)
        #time.sleep(1)
    #else:
    #    print("cannot get valid value!")
    
    #if circles != None: 
    #if circles :
    
    #print ("green circle is:",circles)
    
    return circles

def detecthandle(src, rlevel):
    w = src.shape[1]
    h = src.shape[0]
    if h < 120:
        scale = 2
    else:
        scale = 1

    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    result = detect_Lockgate_Status(resizeImg,rlevel,draw = False)

    return result


#detectstatus()

#detect_Lockgate_Status()

#print(cv2.__version__)
#frame = cv2.imread("D:\\Tools\\camera\\dongsheng\\exception\\0012414457ed\\AA15.1.HANDLE2020071808-54-25.jpg")

#detecthandle(frame, 2)
"""
level = 1000

lev_bright = int(level%10)
lev_hue = int(level%100)
lev_hue = int(lev_hue/10)
lev_sat = int(level%1000)
lev_sat = int(lev_sat/100)
lev_param = int(level/1000)

print(lev_bright, lev_hue, lev_sat, lev_param)

scalar_med = 19.124
scalar_std = 3.678
scalar1 = np.uint16(scalar_med)
std1 = np.uint16(scalar_std)
print(scalar1, std1)
"""
