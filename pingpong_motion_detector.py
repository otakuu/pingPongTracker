# USAGE
# python3 motion_detector.py

# import the necessary packages
from imutils.video import VideoStream
import asyncio
import argparse
import datetime
import imutils
import websockets
import time
import cv2

vs = VideoStream(src=0).start()

# loop over the frames of the video
async def time(websocket, path):
    print('connected')
    # initialize the first frame in the video stream
    firstFrame = None
    
    while True:
            frame = vs.read()
            
            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if frame is None:
                    break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            

            # if the first frame is None, initialize it
            if firstFrame is None:
                    firstFrame = gray
                    continue


            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

            # loop over the contours
            for c in cnts:
                    
                    if cv2.contourArea(c) < 100:
                            continue
                        
                    if cv2.contourArea(c) > 1000:
                            continue

                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    
                    if(w>50 or w<10):
                            continue
                        
                                        
                    if(h>30 or h<10):
                            continue
                        
                    if(y>330 or y<50):
                            continue
                    
                    if(x>485 or x<15):
                            continue
                    
                    print("x:"+str(x)+", y: "+str(y)+", width: "+str(w)+", height: "+str(h))
                    await websocket.send(str(x)+';'+str(y))
                    

start_server = websockets.serve(time, '10.0.1.44', 5678)
print('websocket started...')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()