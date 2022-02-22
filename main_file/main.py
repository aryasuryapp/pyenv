from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi("main_file/form.ui", self)

        # Read_data
        x, y = self.read_data()

        # Plot data
        self.plot(x, y)

    def read_data(self):
        y = []
        for line in open('Sinyal ECG_5menit.txt', 'r'):
            line = line.rstrip("\n")
            line = int(line)
            y.append(line)
        y = y[0:1000]
        len_y = len(y)

        # build x and y axis
        x = list(range(1, len_y+1))
        x_axis = x
        y_axis = y
        return x_axis, y_axis

    def plot(self, x_axis, y_axis):
        # style
        # self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))

        self.graphWidget.plot(x_axis, y_axis, pen=pen)

    def RR_interval(self):
        # Compute
        print('x')

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
