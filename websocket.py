import asyncio
import datetime
import random
import websockets
import cv2
import numpy as np

kernel = np.ones((5,5),np.uint8)

# Take input from webcam
cap = cv2.VideoCapture(0)
print(str(cap.get(3))+' x '+str(cap.get(4)))

hmn = 11
hmx = 135

smn = 18
smx = 66

vmn = 56
vmx = 110

async def time(websocket, path):
    print('connected')
    while True:
        is_sucessfully_read, frame = cap.read()
        
        cv2.flip(frame,1)
                
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        hue,sat,val = cv2.split(hsv)
        
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
        circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,2,120,param1=70,param2=40,minRadius=5,maxRadius=10)

        x = 0
        y = 0
        
        #Draw Circles
        if circles is not None:
                for i in circles[0,:]:
                    x  = int(round(i[0]))
                    y  = int(round(i[1]))
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),1)
                    cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),5)
        
        if(x>0 and y>0):
            #print('x: '+str(x))
            #print('y: '+str(y))
            await websocket.send(str(x)+';'+str(y))
            
        #await asyncio.sleep(0.1)
				
start_server = websockets.serve(time, '10.0.1.44', 5678)
print('websocket started...')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

