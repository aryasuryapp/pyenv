from doctest import Example
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # create graph
        def graph():
            self.graphWidget = pg.PlotWidget()
            self.setCentralWidget(self.graphWidget)

            # read_data
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
            # x_axis = [1,2,3,4,5,6,7,8,9,10]
            # y_axis = [30,32,34,32,33,31,29,32,35,45]

            # style
            self.graphWidget.setBackground('w')
            pen = pg.mkPen(color=(255, 0, 0))

            # plot data: x, y values
            self.graphWidget.plot(x_axis, y_axis, pen=pen)
        
        # create graph
        graph()

        # self.setWindowTitle("This is Main Window")
        # self.resize(270, 110)
        # # Create a QVBoxLayout instance
        # layout = QVBoxLayout()
        # # Add widgets to the layout
        # layout.addWidget(QPushButton("Top"))
        # layout.addWidget(QPushButton("Center"))
        # layout.addWidget(QPushButton("Bottom"))
        # # Set the layout on the application's window
        # self.setLayout(layout)


def main():
    app = QtWidgets.QApplication(sys.argv)
    # app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()