from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys

import Globals


class Visualizer(object):
    def __init__(self, refresh_int=10):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()

        self.verbose = Globals.graph_verbose
        self.refresh_int = refresh_int

        self.w.opts['distance'] = 40
        self.w.setWindowTitle('Devkit Motion Sensor: Tracking...')
        self.w.setGeometry(0, 110, 1280, 720)
        self.w.show()
        if self.verbose:
            print("Visualizer:: Started main window...")

        pg.setConfigOptions(useOpenGL=True)
        self.draw_back_grid()

        self.n = 1000
        self.dist = 5
        self.t = np.linspace(0, 3, self.n)
        self.counter = 1

    def draw_back_grid(self):
        # create the background grids
        if self.verbose:
            print("Visualizer:: Started drawing background grid...")
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
        if self.verbose:
            print("Visualizer:: Drawing background grid finished...")

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        if self.verbose and Globals.viz_update_flag:
            print(f"Visualizer:: Starting update ...")
        if Globals.viz_update_flag:
            xdot = Globals.xdot
            ydot = Globals.ydot
            # print(f"Xdot: {xdot} Ydot:{ydot}")
            # print(f"type of x:{type(xdot)} and y:{type(ydot)}")
            if self.verbose:
                print("Visualizer:: Update flag set...")
            if self.verbose or Globals.graph_update_info:
                print("Visualizer:: Drawing line # : {} - {} ".format(xdot, ydot))

            # xx = self.t[self.counter - 1] * np.sin(25 * self.t[self.counter - 1])
            # yx = self.t[self.counter - 1] * np.cos(25 * self.t[self.counter - 1])
            # zx = self.dist * self.t[self.counter - 1] - 10
            #
            # xy = self.t[self.counter] * np.sin(25 * self.t[self.counter])
            # yy = self.t[self.counter] * np.cos(25 * self.t[self.counter])
            # zy = self.dist * self.t[self.counter] - 10
            #
            # xdot = (xx, yx, zx)
            # ydot = (xy, yy, zy)

            # print(f"in old Xdot: {xdot} Ydot:{ydot}")
            # print(f"in old type of x:{type(xdot)} and y:{type(ydot)}")

            pts = np.array([xdot, ydot])
            plot = gl.GLLinePlotItem(pos=pts, color=pg.mkColor(
                (3, 9)), width=3, antialias=True)
            self.w.addItem(plot)
            if self.verbose:
                print("Visualizer:: Resetting update flag...")
            Globals.viz_update_flag = False
            if self.verbose:
                print("Visualizer:: Finished update...")
        else:
            if self.verbose:
                print("Visualizer:: Update flag is reset. Skipping update...")

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        if self.verbose:
            print(f"Visualizer:: Hooked QTTimer for interval :{self.refresh_int} ...")
        timer.start(self.refresh_int)
        self.start()


'''
# if self.counter < self.n and update_flag:
            # xx = self.t[self.counter - 1] * np.sin(25 * self.t[self.counter - 1])
            # yx = self.t[self.counter - 1] * np.cos(25 * self.t[self.counter - 1])
            # zx = self.dist * self.t[self.counter - 1] - 10
            #
            # xy = self.t[self.counter] * np.sin(25 * self.t[self.counter])
            # yy = self.t[self.counter] * np.cos(25 * self.t[self.counter])
            # zy = self.dist * self.t[self.counter] - 10

            # Xdot = (xx, yx, zx)
            # Ydot = (xy, yy, zy)

'''
