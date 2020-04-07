import numpy as np
import cv2
import time

cv_version = 36


### input value: draw=True,show, draw=False, not show
### return value:[1,'W']horizontal, [1,'H']vertical,[0,'N']no result
### detection region is inside 0.1~0.8
def detect_Lockgate_Status(inImg, rlevel, draw=False):
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

    low_thres = 90
    if rlevel == 2:
        low_thres = 90
    elif rlevel == 3:
        low_thres = 110
    elif rlevel == 4:
        low_thres = 140
    else:
        low_thres = 90

    img = cv2.medianBlur(gray_img, 5)
    ret,th2 = cv2.threshold(img,low_thres,255,cv2.THRESH_BINARY_INV)
    
    
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
    saturation = 43
    brightness = 40
    hue_start = 76
    hue_end = 99
    param_2 = 10
    if level == 1:
        saturation = 43
        brightness = 40
    elif level == 2:
        saturation = 43
        brightness = 40
    elif level == 3:
        saturation = 43
        brightness = 40
        hue_start = 35
    elif level == 4:
        saturation = 43
        brightness = 30
    elif level == 5:
        saturation = 43
        brightness = 20
    elif level == 51:
        saturation = 30
        brightness = 10
        hue_start = 50
        hue_end = 120
    elif level == 52:
        saturation = 30
        brightness = 10
        hue_start = 50
        hue_end = 140
    elif level == 53:
        saturation = 30
        brightness = 10
        hue_start = 60
        hue_end = 120
    elif level == 54:
        saturation = 30
        brightness = 0
        hue_start = 40
        hue_end = 148
    elif level == 55:
        saturation = 50
        brightness = 40
        hue_start = 70
        hue_end = 148
    elif level == 61:
        saturation = 43
        brightness = 40
        param_2 = 16
    else:
        saturation = 43
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

    low_range1 = np.array([hue_start, saturation, brightness])
    high_range1 = np.array([hue_end, 255, 255])
    #low_range1 = np.array([76, saturation, brightness])
    #high_range1 = np.array([99, 255, 255])
    th1 = cv2.inRange(hsv_img, low_range1, high_range1)

    #cv2.imshow('green', th1)
    #cv2.waitKey(2)
    #time.sleep(1)

    ###------------------###### change hole value from 3 to 8 according to different brightness of light
    convsize = [(1,1),(3,3),(8,8),(10,10)]

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
        #for i in circles[0,:]:
        #    x = i[0]
        #    y = i[1]
        #    r = i[2]
        #    cv2.circle(resizeImg,(x,y),r,(0,0,255),-1)
        #cv2.imshow('xxx', resizeImg)
        #cv2.waitKey(2)
        #time.sleep(1)
    #else:
    #    print("cannot get valid value!")
    
    #if circles != None: 
    #if circles :
    
    #print ("green circle is:",circles)
    
    return circles

def detect_LED_red(inImg, level):
    saturation = 100
    brightness = 60
    hough_para2 = 12
    if level == 1:
        saturation = 100
        brightness = 60
    elif level == 11:
        saturation = 100
        brightness = 60  # special for some scenario, saturation is very low, but brightness is normal
    elif level == 2:
        saturation = 100
        brightness = 60
    elif level == 3:
        saturation = 100
        brightness = 40
        hough_para2 = 10
    elif level == 4:
        saturation = 100
        brightness = 30
        hough_para2 = 8
    elif level == 5:
        saturation = 100
        brightness = 60
    elif level == 51:
        saturation = 100
        brightness = 40
        hough_para2 = 8
    elif level == 52:
        saturation = 100
        brightness = 40
        hough_para2 = 8
    elif level == 61:
        saturation = 100
        brightness = 40
        hough_para2 = 8
    elif level == 62:
        saturation = 100
        brightness = 60
    else:
        saturation = 100
        brightness = 60
    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]

    #print (w,h)
    
    if h < 100:
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
    low_range = np.array([150, saturation, brightness])
    high_range = np.array([180, 255, 255])
    th = cv2.inRange(hsv_img, low_range, high_range)

    ###------------------###### change hole value from 3 to 8 according to different brightness of light
    convsize = [(1,1),(3,3),(8,8)]

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
        	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,80,param1=100,param2=hough_para2,minRadius=12,maxRadius=60) #10,40
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


def detect_LED_yellow(inImg, level):
    saturation = 130
    brightness = 60
    if level == 1:
        saturation = 120
        brightness = 60
    elif level == 2:
        saturation = 120
        brightness = 60
    elif level == 3:
        saturation = 130
        brightness = 60
    elif level == 4:
        saturation = 120
        brightness = 60
    elif level == 51:
        saturation = 100
        brightness = 60
    else:
        saturation = 120
        brightness = 60
    rects = []
    w = inImg.shape[1]
    h = inImg.shape[0]

    #print (w,h)
    
    if h < 100:
        scale = 2
    else:
        scale = 1

    #cv2.imshow('input', inImg)
    #cv2.waitKey(2)
    
    resizeImg = cv2.resize(inImg, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    hsv_img = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2HSV)

    #low_range = np.array([15, saturation, brightness])
    #high_range = np.array([50, 255, 255])
    low_range = np.array([26, 43, brightness])
    high_range = np.array([77, 255, 255])
    th = cv2.inRange(hsv_img, low_range, high_range)

    convsize = [(1,1),(3,3),(8,8)]
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
        	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=100,param2=12,minRadius=12,maxRadius=60) #10,40
        else:
        	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=100,param2=12,minRadius=12,maxRadius=60) #10,40

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


def check_Hsv_LED_red(inImg,circles,level):
    #if inImg.size == 0:
    #    return
    thres_highest = 190
    thres_zero = 160
    thres_onoff_a = 25
    thres_onoff_b = 60
    if level == 1:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 25
        thres_onoff_b = 60
    elif level == 2:
        thres_highest = 190
        thres_zero = 120
        thres_onoff_a = 25
        thres_onoff_b = 60
    elif level == 3:
        thres_highest = 90
        thres_zero = 56
        thres_onoff_a = 20
        thres_onoff_b = 50
    elif level == 4:
        thres_highest = 100
        thres_zero = 70
        thres_onoff_a = 35
        thres_onoff_b = 60
    elif level == 5:
        thres_highest = 100
        thres_zero = 70
        thres_onoff_a = 14
        thres_onoff_b = 13
    elif level == 11:
        thres_highest = 90
        thres_zero = 55
        thres_onoff_a = 20
        thres_onoff_b = 50
    elif level == 51:
        thres_highest = 150
        thres_zero = 90
        thres_onoff_a = 55
        thres_onoff_b = 80
    elif level == 52:
        thres_highest = 180
        thres_zero = 120
        thres_onoff_a = 60
        thres_onoff_b = 80
    elif level == 61:
        thres_highest = 160
        thres_zero = 120
        thres_onoff_a = 35
        thres_onoff_b = 60
    elif level == 62:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 25
        thres_onoff_b = 60
    else:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 25
        thres_onoff_b = 60
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 100:
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
    if x < r:
        r = x
    if (x + r) > resizeImg.shape[1]:
        r = resizeImg.shape[1] - x
    if y < r:
        r = y
    if (y + r) > resizeImg.shape[0]:
        r = resizeImg.shape[0] - y
    #print (x,y,r)


    #if r > 10:
    #    rr = 10
    #else:
    #    rr = r
    #rect_x = (x - rr)
    #rect_y = (y - rr)
    #crop_img = resizeImg[rect_y:(y+rr),rect_x:(x+rr)]

    crop_img1 = resizeImg[(y-r):(y+r),(x-r):(x+r)]
    #crop_img2 = resizeImg[(y-r):(y+r),(x-r-r):(x+r+r)]

    img_gray_in = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)
    img_med = cv2.medianBlur(img_gray_in, 5)
    #ret, img = cv2.threshold(img,thres_zero,255,cv2.THRESH_TOZERO)
    scalar_med = cv2.mean(img_med)
    scalar1 = np.uint16(np.around(scalar_med))[0]
    #print (circle_max)
    #cv2.imshow("cropped image", img_med)
    #cv2.waitKey(2)
    #time.sleep(2)

    light_colors = []

    if crop_img1 is None:
        light_colors.append(light_color)
        return light_colors

    img_gray = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img_gray, 5)
    #ret, img = cv2.threshold(img,thres_zero,255,cv2.THRESH_TOZERO)
    #scalar1 = cv2.mean(inImg)

    scalar_a = choose_brightest_area(img, r, 32)

    #print (scalar_a, scalar1)

    ### We have a very bright environment, so we think if environment brightness is higher than max area brightness, we think light is off
    ### since if light is on, it will be over exposure regarding to environment brightness.
    #print (scalar1, scalar_a)
    if scalar1 > scalar_a:
        light_color = 0
    else:
        ### In some case especially in the single light area, the light area is almost the same with image area.
        if scalar1 > thres_zero:
            delta_s = scalar_a - scalar1
            if delta_s > thres_onoff_a:
                light_color = 1
            else:
                light_color = 0
        else:
            delta_s = scalar_a - scalar1
            if delta_s > thres_onoff_b:
                light_color = 1
            else:
                light_color = 0
    if scalar_a > thres_highest and scalar1 > thres_zero:
        light_color = 1

    light_colors.append(light_color)

    #print (light_colors)
            
    return light_colors

def check_Hsv_LED_green(inImg,circles,level):
    #if inImg.size == 0:
    #    return
    thres_highest = 190
    thres_zero = 160
    thres_onoff_a = 30
    thres_onoff_b = 60
    thres_onoff_c = 15
    if level == 1:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 60
    elif level == 2:
        thres_highest = 190
        thres_zero = 130
        thres_onoff_a = 30
        thres_onoff_b = 60
        thres_onoff_c = 30
    elif level == 3:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 60
    elif level == 4:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 60
    elif level == 51:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 20
    elif level == 52:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 60
    elif level == 53:
        thres_highest = 120
        thres_zero = 90
        thres_onoff_a = 12
        thres_onoff_b = 10
    elif level == 54:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 60
        thres_onoff_b = 80
    elif level == 55:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 60
    elif level == 61:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 60
    elif level == 62:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 40
    else:
        thres_highest = 190
        thres_zero = 160
        thres_onoff_a = 30
        thres_onoff_b = 60
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 100:
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
    if x < r:
        r = x
    if (x + r) > resizeImg.shape[1]:
        r = resizeImg.shape[1] - x
    if y < r:
        r = y
    if (y + r) > resizeImg.shape[0]:
        r = resizeImg.shape[0] - y
    #print (x,y,r)


    #if r > 10:
    #    rr = 10
    #else:
    #    rr = r
    #rect_x = (x - rr)
    #rect_y = (y - rr)
    #crop_img = resizeImg[rect_y:(y+rr),rect_x:(x+rr)]

    crop_img1 = resizeImg[(y-r):(y+r),(x-r):(x+r)]

    if level == 53:
        img_gray_in = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)
    else:
        img_gray_in = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2GRAY)

    img_med = cv2.medianBlur(img_gray_in, 5)
    #ret, img = cv2.threshold(img,thres_zero,255,cv2.THRESH_TOZERO)
    scalar_med = cv2.mean(img_med)
    scalar1 = np.uint16(np.around(scalar_med))[0]
    #print (circle_max)
    #cv2.imshow("cropped image", img_med)
    #cv2.waitKey(2)
    #time.sleep(2)

    light_colors = []

    if crop_img1 is None:
        light_colors.append(light_color)
        return light_colors

    img_gray = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img_gray, 5)
    #ret, img = cv2.threshold(img,thres_zero,255,cv2.THRESH_TOZERO)
    #scalar1 = cv2.mean(inImg)

    scalar_a = choose_brightest_area(img, r, 16)

    #print (scalar1, scalar_a)

    ### We have a very bright environment, so we think if environment brightness is higher than max area brightness, we think light is off
    ### since if light is on, it will be over exposure regarding to environment brightness.
    if scalar1 > scalar_a:
        light_color = 0
    else:
        ### In some case especially in the single light area, the light area is almost the same with image area.
        if scalar1 > thres_zero:
            delta_s = scalar_a - scalar1
            if delta_s > thres_onoff_a:
                light_color = 1
            else:
                light_color = 0
        else:
            delta_s = scalar_a - scalar1
            if delta_s > thres_onoff_b:
                light_color = 1
            else:
                light_color = 0
        if scalar_a > thres_highest and (scalar_a - scalar1) > thres_onoff_c:
            light_color = 1

    light_colors.append(light_color)

    #print (light_colors)
            
    return light_colors

def check_Hsv_LED_yellow(inImg,circles,level):
    #if inImg.size == 0:
    #    return
    thres_highest = 200
    thres_zero = 160
    thres_onoff_a = 40
    thres_onoff_b = 60
    if level == 1:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    elif level == 2:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    elif level == 3:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    elif level == 4:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    elif level == 51:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    elif level == 61:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    elif level == 62:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    else:
        thres_highest = 200
        thres_zero = 160
        thres_onoff_a = 40
        thres_onoff_b = 60
    w = inImg.shape[1]
    h = inImg.shape[0]
    
    if h < 100:
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
    if x < r:
        r = x
    if (x + r) > resizeImg.shape[1]:
        r = resizeImg.shape[1] - x
    if y < r:
        r = y
    if (y + r) > resizeImg.shape[0]:
        r = resizeImg.shape[0] - y
    #print (x,y,r)


    #if r > 10:
    #    rr = 10
    #else:
    #    rr = r
    #rect_x = (x - rr)
    #rect_y = (y - rr)
    #crop_img = resizeImg[rect_y:(y+rr),rect_x:(x+rr)]

    crop_img1 = resizeImg[(y-r):(y+r),(x-r):(x+r)]

    img_gray_in = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2GRAY)
    img_med = cv2.medianBlur(img_gray_in, 5)
    #ret, img = cv2.threshold(img,thres_zero,255,cv2.THRESH_TOZERO)
    scalar_med = cv2.mean(img_med)
    scalar1 = np.uint16(np.around(scalar_med))[0]
    #print (circle_max)
    #cv2.imshow("cropped image", img_med)
    #cv2.waitKey(2)
    #time.sleep(2)

    light_colors = []

    if crop_img1 is None:
        light_colors.append(light_color)
        return light_colors

    img_gray = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img_gray, 5)
    #ret, img = cv2.threshold(img,thres_zero,255,cv2.THRESH_TOZERO)
    #scalar1 = cv2.mean(inImg)

    scalar_a = choose_brightest_area(img, r, 16)

    #print (scalar_a, scalar1)

    ### We have a very bright environment, so we think if environment brightness is higher than max area brightness, we think light is off
    ### since if light is on, it will be over exposure regarding to environment brightness.
    if scalar1 > scalar_a:
        light_color = 0
    else:
        ### In some case especially in the single light area, the light area is almost the same with image area.
        if scalar1 > thres_zero:
            delta_s = scalar_a - scalar1
            if delta_s > thres_onoff_a:
                light_color = 1
            else:
                light_color = 0
        else:
            delta_s = scalar_a - scalar1
            if delta_s > thres_onoff_b:
                light_color = 1
            else:
                light_color = 0

    if scalar1 > thres_highest:
        light_color = 1

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
        
    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)
    
    light_colors = []
    light_color = []
    circles = [[]]

    # detect green
    circles = detect_LED_green(resizeImg,glevel)

    if circles is not None and len(circles[0]) != 0:
        status = check_Hsv_LED_green(resizeImg,circles,glevel)
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
        status = check_Hsv_LED_red(resizeImg,circles,rlevel)
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
            status = check_Hsv_LED_green(resizeImg,circles,level)
        elif type == "YELLOW":
            status = check_Hsv_LED_yellow(resizeImg,circles,level)
        else:
            status = check_Hsv_LED_red(resizeImg,circles,level)
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
    
    if h < 100:
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
    result = detect_LED_yellow(resizeImg,2)
    if result is not None:
        status = check_Hsv_LED(resizeImg, result,2)
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


def detecthandle(src, rlevel):
    w = src.shape[1]
    h = src.shape[0]
    if h < 100:
        scale = 2
    else:
        scale = 1

    resizeImg = cv2.resize(src, (int(scale * w), int(scale* h)), interpolation=cv2.INTER_CUBIC)

    result = detect_Lockgate_Status(resizeImg,rlevel,draw = False)

    return result


#detectstatus()

