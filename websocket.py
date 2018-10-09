import cv2
import numpy as np
import asyncio
import datetime
import random
import websockets

# C:\Users\dalleman\AppData\Local\Programs\Python\Python36-32\python.exe websocket.py

async def time(websocket, path):
    player = 0
    while True:
        if(player % 2==0):
            x = random.randint(0, 410)
        else:
            x = random.randint(410, 820)
        y = random.randint(0, 616)
        await websocket.send(str(x)+';'+str(y))
        await asyncio.sleep(0.75)
        player+=1
				
start_server = websockets.serve(time, '127.0.0.1', 5678)
print('websocket started...')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

