import asyncio
import websockets
import numpy as np


async def receiveData(websocket, path):
    global i
    payload = await websocket.recv()

    print(f"Received Data:{payload}")

    t=payload.split(';')
    cltData=np.asarray(t, dtype=np.float64, order='C')

    print(f"Parsed data:\nx:{cltData[0]}\ny:{cltData[1]}\nz:{cltData[2]}\n\n")

    await websocket.send(f"Ack#{i}")
    i+=1

i=0
start_server = websockets.serve(receiveData, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
