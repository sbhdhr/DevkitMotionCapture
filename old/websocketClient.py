import asyncio
import websockets
import numpy as np
import time

async def sendData():
    uri = "ws://localhost:8765"
    for i in range(1,n+1):
        async with websockets.connect(uri) as websocket:
        
            x = t[i] * np.sin(25 * t[i])
            y = t[i] * np.cos(25 * t[i])
            z = dist * t[i] - 10

            payload=";".join(str(x) for x in [x,y,z])
            print(payload)
            await websocket.send(payload)
            print(f"Sent #{i}...")

            # ack = await websocket.recv()
            # print(f"Received ack:{ack}")

            time.sleep(.05)
            

n = 1000
dist = 5
t = np.linspace(0, 3, n)
asyncio.get_event_loop().run_until_complete(sendData())