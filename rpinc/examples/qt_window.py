#!/usr/bin/env python

import os
import sys

from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        MainWindow.__init__(self, *args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)
    # end plot()
# end MainWindow()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
# end main()


if __name__ == '__main__':
    main()
# end if
