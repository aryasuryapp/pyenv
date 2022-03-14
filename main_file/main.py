from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import pdb # For debugging
import math

# importing Qt widgets
from PyQt5.QtWidgets import *

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
        qrs_filter, similarity, index_r, r_interval = self.RR_interval(y)
        # print(qrs_filter)
        self.plot_2(qrs_filter)
        self.plot_2(similarity)

        # HR
        mean_hr_list = self.hr(r_interval)

        # RMSSD, SDNN
        self.RMSSD(r_interval)
        self.SDNN(r_interval)

        RR_diff = self.RR_diff(r_interval)
        self.SDSD(RR_diff)
        self.pNN50(RR_diff)

        #HRV tachogram
        self.plot_3(mean_hr_list)

        # Histogram
        histo = self.histo(r_interval)
        self.plot_4(histo)

    def read_data(self):
        y = []
        for line in open('Sinyal ECG_5menit.txt', 'r'):
            line = line.rstrip("\n")
            line = int(line)
            y.append(line)
        print('real_data_count =', len(y))
        # y = y[0:1000] # Cut data on 1000
        len_y = len(y)

        # build x and y axis
        seconds = len_y/200
        # print(seconds)
        x = np.linspace(0, seconds, len_y)
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

    def plot_3(self, y_axis):
        x_axis = list(range(1, len(y_axis)+1))
        
        # style
        # self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))

        self.graphWidget_3.plot(x_axis, y_axis, pen=pen)

    def plot_4(self, histo):
        # creating a widget object
        widget = QtWidgets.QWidget()
 
        # # creating a push button object
        # btn = QPushButton('Push Button')
 
        # # creating a line edit widget
        # text = QLineEdit("Line Edit")
 
        # # creating a check box widget
        # check = QCheckBox("Check Box")
 
        # creating a plot window
        plot = pg.plot()
 
        # create list for y-axis
        # y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2]
        y1 = list(histo.values())
 
        # create horizontal list i.e x-axis
        # x = [*histo]
        x = list(histo.keys())
        # x = [1, 2, 3, 4, 6, 5, 7, 8, 9, 10]
 
        # create pyqt5graph bar graph item
        # with width = 0.6
        # with bar colors = green
        bargraph = pg.BarGraphItem(x = x, height = y1, width = 2, brush ='g')
 
        # add item to plot window
        # adding bargraph item to the plot window
        plot.addItem(bargraph)
 
        # Creating a grid layout
        layout = QGridLayout()
 
        # setting this layout to the widget
        widget.setLayout(layout)
 
        # adding widgets in the layout in their proper positions
        # # button goes in upper-left
        # layout.addWidget(btn, 0, 0)
 
        # # text edit goes in middle-left
        # layout.addWidget(text, 1, 0)
 
        # # check box widget goes in bottom-left
        # layout.addWidget(check, 3, 0)
 
        # plot window goes on right side, spanning 3 rows
        layout.addWidget(plot, 0, 1, 3, 1)
 
        # setting this widget as central widget of the main window
        self.setCentralWidget(widget)

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
        for i in range(0, len(peaks)-1):
            if peaks[i] > peaks[i+1] and peaks[i] > peaks[i-1]:
                true_peaks.append(peaks[i])
        print('true_peaks count =', len(true_peaks))
        # print(true_peaks)

        # Find R_index
        similarity_list = similarity.tolist()

        index_r = []
        for i in range(0, len(true_peaks)):
            index_r.append(similarity_list.index(true_peaks[i]))

        print('index_r =', index_r[0:5])

        # Find RR_interval
        RR_interval = []
        for i in range(0, len(index_r)-1):
            temp = index_r[i+1] - index_r[i]
            ms_dist = (temp / 200) * 1000
            RR_interval.append(ms_dist)
            
        print('RR_interval =', RR_interval[0:5], 'in ms')
        # pdb.set_trace()

        return qrs_filter, similarity, index_r, RR_interval
    
    def hr(self, rr):
        mean_hr = 60 * 1000/np.mean(rr)
        print('mean_hr =', mean_hr)

        mean_hr_list = []
        for i in range(0, len(rr)):
            temp = 60 * 1000/rr[i]
            mean_hr_list.append(temp)
        print('mean_hr_list', mean_hr_list[0:5])

        return mean_hr_list

    def RMSSD(self, rr):
        rmssd = np.sqrt(np.mean(np.square(np.diff(rr))))
        print('RMSSD =', rmssd, 'ms')

    def SDNN(self, rr):
        sdnn = np.std(rr)
        print('SDNN =', sdnn, 'ms')

    def SDSD(self, rr):
        sdsd = np.std(rr)
        print('SDSD =', sdsd)

    def pNN50(self, rr):
        RR_diff = rr
        # pdb.set_trace()
        nn50 = [x for x in RR_diff if (x>50)]
        pnn50 = float(len(nn50)) / float(len(RR_diff)) #Note the use of float(), because we don't want Python to think we want an int() and round the proportion to 0 or 1
        print("pNN50:", pnn50)

    def RR_diff(self, rr):
        RR_diff = []
        RR_sqdiff = []
        RR_list = rr
        # RR_list = measures['RR_list']
        cnt = 1 #Use counter to iterate over RR_list

        while (cnt < (len(RR_list)-1)): #Keep going as long as there are R-R intervals
            RR_diff.append(abs(RR_list[cnt] - RR_list[cnt+1])) #Calculate absolute difference between successive R-R interval
            RR_sqdiff.append(math.pow(RR_list[cnt] - RR_list[cnt+1], 2)) #Calculate squared difference
            cnt += 1
        
        return RR_diff

    def histo(self, rr):
        hist = {}
        for i in rr:
            hist[i] = hist.get(i, 0) + 1
        
        return hist

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
