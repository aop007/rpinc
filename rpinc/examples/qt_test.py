import sys
import asyncio
from qasync import QEventLoop, asyncSlot, Queue
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
from time import time
import sounddevice as sd

class OptionViz(QtCore.QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.p = pg.plot()
        self.p.setWindowTitle("pyqtgraph example: PlotSpeedTest")
        self.p.setRange(QtCore.QRectF(0, -10, 5000, 20))
        self.p.setLabel("bottom", "Index", units="B")
        self.curve = self.p.plot()

        self.data = np.random.normal(size=(50, 5000))
        self.ptr = 0
        self.lastTime = time()
        self.fps = None

        q_in = Queue()

        def callback(indata, frame_count, time_info, status):
            loop.call_soon_threadsafe(q_in.put_nowait, (indata.copy(), status))
        # end callbac()

        stream = sd.InputStream(callback=callback, channels=1, device=2)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(0)

    @asyncSlot()
    async def update(self):
        self.curve.setData(self.data[self.ptr % 10])
        self.ptr += 1
        now = time()
        dt = now - self.lastTime
        self.lastTime = now
        if self.fps is None:
            fps = 1.0 / dt
        else:
            s = np.clip(dt * 3.0, 0, 1)
            self.fps = self.fps * (1 - s) + (1.0 / dt) * s

        self.p.setTitle("%0.2f fps" % fps)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    viz = OptionViz(app)
    loop.run_forever()
# end if
