import cv2
import numpy as np

kernel = np.ones((5,5),np.uint8)

# Take input from webcam
cap = cv2.VideoCapture(0)

# Reduce the size of video to 320x240 so rpi can process faster
#cap.set(3,320)
#cap.set(4,240)


def nothing(x):
    pass
# Creating a windows for later use
cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('closing')
cv2.namedWindow('tracking')


# Creating track bar for min and max for hue, saturation and value
cv2.createTrackbar('hmin', 'HueComp',95,179,nothing)
cv2.createTrackbar('hmax', 'HueComp',115,179,nothing)

cv2.createTrackbar('smin', 'SatComp',17,255,nothing)
cv2.createTrackbar('smax', 'SatComp',139,255,nothing)

cv2.createTrackbar('vmin', 'ValComp',152,255,nothing)
cv2.createTrackbar('vmax', 'ValComp',255,255,nothing)


while(1):

    is_sucessfully_read, frame = cap.read()
    
    if(is_sucessfully_read):
        
        #converting to HSV
        cv2.flip(frame,1)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        hue,sat,val = cv2.split(hsv)     

        # get info from track bar and appy to result
        hmn = cv2.getTrackbarPos('hmin','HueComp')
        hmx = cv2.getTrackbarPos('hmax','HueComp')

        smn = cv2.getTrackbarPos('smin','SatComp')
        smx = cv2.getTrackbarPos('smax','SatComp')

        vmn = cv2.getTrackbarPos('vmin','ValComp')
        vmx = cv2.getTrackbarPos('vmax','ValComp')

        # Apply thresholding
        hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
        sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
        vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))

        # AND h s and v
        tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))

        # Some morpholigical filtering
        dilation = cv2.dilate(tracking,kernel,iterations = 1)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
        closing = cv2.GaussianBlur(closing,(5,5),0)

        # Detect circles using HoughCircles 100/50
        circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,2,120,param1=70,param2=40,minRadius=10,maxRadius=20)

        #Draw Circles
        if circles is not None:
                for i in circles[0,:]:
                    print('x: '+str(round(i[0])))
                    print('y: '+str(round(i[1])))
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),1)
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),5)

        
        #Show the result in frames
        cv2.imshow('HueComp',hthresh)
        cv2.imshow('SatComp',sthresh)
        cv2.imshow('ValComp',vthresh)
        cv2.imshow('closing',closing)
        cv2.imshow('tracking',frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

cap.release()

cv2.destroyAllWindows()