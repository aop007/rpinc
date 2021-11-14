# -*- coding: utf-8 -*-
"""
Demonstrates very basic use of ImageItem to display image data inside a ViewBox.
"""

## Add path to library (just for examples; you do not need this)

from time import perf_counter

import numpy
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import scipy.ndimage.interpolation
import pyqtgraph.examples.initExample

from rpinc.capture import MicrophoneRecorder

CHUNKSIZE = 512
POWER_MIN = -80
POWER_MAX = 20

mic = MicrophoneRecorder(rate=24000, chunksize=CHUNKSIZE)

app = pg.mkQApp("ImageItem Example")

## Create window with GraphicsView widget
win = pg.GraphicsLayoutWidget()
win.show()  ## show widget alone in its own window
win.setWindowTitle('pyqtgraph example: ImageItem')
view = win.addViewBox()

## lock the aspect ratio so pixels are always square
# view.setAspectLocked(True)

## Create image item
img = pg.ImageItem(border='w', autoLevels=False)
view.addItem(img)

## Set initial view bounds

BUFFER_DEPTH = 128

## Create random image

BUFFER_WIDTH = int(CHUNKSIZE / 2 + 1)

data = numpy.zeros(shape=(BUFFER_DEPTH, BUFFER_WIDTH))
i = 0

view.setRange(QtCore.QRectF(0, 0, BUFFER_DEPTH, BUFFER_WIDTH))

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
        current_frame = frames[-1]
        fft_frame = numpy.fft.rfft(current_frame / len(current_frame) ** 2)

        # print(fft_frame.shape, current_frame.shape)

        # Shift specthrograph
        data[1:, :] = data[0:-1, :]
        # data[0, :] = current_frame

        log_fft = 20 * numpy.log10(numpy.abs(fft_frame))
        log_fft = numpy.clip(log_fft, -80, 20)

        data[0, :] = log_fft

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
