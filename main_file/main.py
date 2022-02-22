from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi("main_file/form.ui", self)

        # Read_data
        x, y = self.read_data()

        # Plot data
        self.plot(x, y)

        # RR Interval
        qrs_filter, similarity, index_r = self.RR_interval(y)
        # print(qrs_filter)
        self.plot_2(qrs_filter)
        self.plot_2(similarity)

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
    
    def plot_2(self, y_axis):
        x_axis = list(range(1, len(y_axis)+1))
        
        # style
        # self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))

        self.graphWidget_2.plot(x_axis, y_axis, pen=pen)

    def RR_interval2(self, data):
        # Container
        highest_index_array = []
        RR_interval = []

        # Compute
        # data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        len_data = len(data)
        chunk_size = len_data // 6
        # chunk_size = 10

        chunked_list = list()
        for i in range(0, len_data, chunk_size):
            chunked_list.append(data[i:i+chunk_size])
        # print(len(chunked_list))

        # Find highest
        len_chunked_list = len(chunked_list)
        for i in range(0, len_chunked_list-1):
            highest = max(chunked_list[i])
            # print(highest)
            highest_index = data.index(highest)
            highest_index_array.append(highest_index)
            # print(highest_index)

        # Find interval
        for i in range(0, len(highest_index_array)):
            if i == len(highest_index_array)-1:
                break
            RR_interval.append(highest_index_array[i+1] - highest_index_array[i])
        
        print('highest_index_array =', highest_index_array)
        print('RR interval =', RR_interval)

    def RR_interval(self, data):
        ecg_signal = data

        # linear spaced vector between 0.5 pi and 1.5 pi 
        t = np.linspace(0.5 * np.pi, 1.5 * np.pi, 15)

        # use sine to approximate QRS feature
        qrs_filter = np.sin(t)

        # stage 1: compute cross correlation between ecg and qrs filter
        similarity = np.correlate(ecg_signal, qrs_filter, mode="same")

        # stage 2: find peaks using a threshold
        peaks = []

        threshold = max(similarity[0:900])*np.sqrt(2)/2
        # spk = 0.13 * max(similarity[0:200]) * 0.2
        # npk = 0.1 * spk
        # threshold = 0.25 * spk + 0.75 * npk

        for i in range(0, len(similarity)):
            if similarity[i] > threshold:
                peaks.append(similarity[i])

        # threshold = max(ecg_signal)*np.sqrt(2)/2
        # spk = 0.13 * max(ecg_signal) * 0.2
        # npk = 0.1 * spk
        # threshold = 0.25 * spk + 0.75 * npk
        # for i in range(0, len(ecg_signal)):
        #     if ecg_signal[i] > threshold:
        #         peaks.append(ecg_signal[i])

        print('threshold =', threshold)
        print('peaks count =', len(peaks))

        true_peaks = []
        for i in range(0, len(peaks)):
            if i == len(peaks)-1:
                break
            if peaks[i] > peaks[i+1]:
                true_peaks.append(peaks[i])
        print('true_peaks count =', len(true_peaks))
        # print(true_peaks)

        similarity_list = similarity.tolist()
        index_r = []
        for i in range(0, len(true_peaks)-1):
            temp = similarity_list.index(true_peaks[i+1]) - similarity_list.index(true_peaks[i])
            if temp > 10:
                index_r.append(similarity_list.index(true_peaks[i]))
        print('index_r =', index_r)

        return qrs_filter, similarity, index_r
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
