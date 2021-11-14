# -*- coding: utf-8 -*-
"""
Demonstrates very basic use of ImageItem to display image data inside a ViewBox.
"""

## Add path to library (just for examples; you do not need this)

from time import perf_counter

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import scipy.ndimage.interpolation
import pyqtgraph.examples.initExample

from rpinc.capture import MicrophoneRecorder

mic = MicrophoneRecorder()

app = pg.mkQApp("ImageItem Example")

## Create window with GraphicsView widget
win = pg.GraphicsLayoutWidget()
win.show()  ## show widget alone in its own window
win.setWindowTitle('pyqtgraph example: ImageItem')
view = win.addViewBox()

## lock the aspect ratio so pixels are always square
# view.setAspectLocked(True)

## Create image item
img = pg.ImageItem(border='w')
view.addItem(img)

## Set initial view bounds

BUFFER_DEPTH = 64

## Create random image
data = np.zeros(shape=(BUFFER_DEPTH, mic.chunksize))
i = 0

view.setRange(QtCore.QRectF(0, 0, BUFFER_DEPTH, mic.chunksize))

updateTime = perf_counter()
elapsed = 0

timer = QtCore.QTimer()
timer.setSingleShot(True)

mic.start()

# not using QTimer.singleShot() because of persistence on PyQt. see PR #1605

def updateData():
    global img, data, i, updateTime, elapsed, mic

    frames = mic.get_frames()

    if len(frames) > 0:
        print(len(frames[0]), frames[0].min(), frames[0].max())

        data[1:, :] = data[0:-1, :]
        data[0, :] = frames[0]

        ## Display the data
        img.setImage(data)
    # end if

    timer.start(1)
    now = perf_counter()
    elapsed_now = now - updateTime
    updateTime = now
    elapsed = elapsed * 0.9 + elapsed_now * 0.1

        # print(f"{1 / elapsed:.1f} fps")
    # end if


timer.timeout.connect(updateData)
updateData()

if __name__ == '__main__':
    pg.exec()
