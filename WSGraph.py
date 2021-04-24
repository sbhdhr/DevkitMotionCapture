
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
from simple_websocket_server import WebSocketServer, WebSocket
from threading import Thread

class Visualizer(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.w.setGeometry(0, 110, 1280, 720)
        self.w.show()

        pg.setConfigOptions(useOpenGL=True)

        # create the background grids
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.w.addItem(gz)

        self.counter = 1
        self.n = 1000
        self.dist = 5
        self.t = np.linspace(0, 3, self.n)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        if self.counter < self.n:
            xx = self.t[self.counter-1] * np.sin(25 * self.t[self.counter-1])
            yx = self.t[self.counter-1] * np.cos(25 * self.t[self.counter-1])
            zx = self.dist*self.t[self.counter-1]-10

            xy = self.t[self.counter] * np.sin(25 * self.t[self.counter])
            yy = self.t[self.counter] * np.cos(25 * self.t[self.counter])
            zy = self.dist*self.t[self.counter]-10

            Xdot = (xx, yx, zx)
            Ydot = (xy, yy, zy)
            print("Drawing line #{} : {} - {} ".format(self.counter, Xdot, Ydot))
            pts = np.array([Xdot, Ydot])
            plot = gl.GLLinePlotItem(pos=pts, color=pg.mkColor(
                (self.counter, 9)), width=3, antialias=True)
            self.w.addItem(plot)
            self.counter += 1

    def animation(self):
        # timer = QtCore.QTimer()
        # timer.timeout.connect(self.update)
        # timer.start(16)
        self.start()



class WSServer(WebSocket):
    def handle(self):
        print(f"Received Data:{self.data}")
        #v.update()

        t = self.data.split(';')
        cltData = np.asarray(t, dtype=np.float64, order='C')

        #print(f"Parsed data:\nx:{cltData[0]}\ny:{cltData[1]}\nz:{cltData[2]}\n\n")

        self.send_message(f"Ack#{1}")

    #
    # def connected(self):
    #     print(self.address, 'connected')
    #
    # def handle_close(self):
    #     print(self.address, 'closed')


def runServer():
    server = WebSocketServer('localhost', 8765, WSServer)
    server.serve_forever()


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    ws_run = Thread(target=runServer)
    ws_run.start()

    v = Visualizer()
    v.animation()






'''

async def receiveData(websocket, path):
    global cnt
    global v
    print("waiting connection...")
    payload = await websocket.recv()

    print(f"Received Data:{payload}")
    v.update()

    t=payload.split(';')
    cltData=np.asarray(t, dtype=np.float64, order='C')

    print(f"Parsed data:\nx:{cltData[0]}\ny:{cltData[1]}\nz:{cltData[2]}\n\n")

    await websocket.send(f"Ack#{cnt}")
    cnt+=1

'''