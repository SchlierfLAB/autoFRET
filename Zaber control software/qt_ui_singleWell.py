#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Qt-based GUI for controlling Zaber microscope stage 

Schlierf Lab - BCUBE, TU Dresden

"""


import sys
import re
import serial
import os

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, QRunnable, QThreadPool
from PyQt5.QtGui import QPen, QColor, QFont

from zaber_motion import Library
from zaber_motion.ascii import Connection
from zaber_motion import Units
from zaber_motion import CommandFailedException

from itertools import groupby

from scan_ui_single_gui import Ui_MainWindow_Single
from initUi import Ui_initDevices

import tttrmode


class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        self.m_color = False


class automateMove(QRunnable):

    def __init__(self, measTime, XAxis,YAxis, homeX, homeY, path):
        super(automateMove, self).__init__()
        self.measTime = measTime
        self.XAxis = XAxis
        self.YAxis = YAxis
        self.homeX = homeX
        self.homeY = homeY
        self.path = path
        self.savePath = ""
        self.increment = 0

    def createFolder(self, path, item):
        try:
            self.fullDir = str(path) + "/" + item
            os.mkdir(self.fullDir)
            self.savePath = self.fullDir + "/" + item + "_" + str(self.increment) + ".ht3"
            print(self.savePath)
        except OSError:
            print("Cannot create directory")
        else:
            print("Created directory: {}".format(self.fullDir))

    def run(self):
        # print(self.sortedItems)
        

        tttrmode.initttR(1000*int(self.measTime.text()))

        # Basically name of the output file #
        item = 'Single_Well'

        self.textX, self.textY = strMatch.match(item).groups()  # Seperate rows and column number/text
        print("XAxis: {} | YAxis: {}".format(self.homeY, self.homeX))
        print("Current position: {}, {}".format(self.XAxis.get_position(Units.LENGTH_MILLIMETRES),
                                                 self.YAxis.get_position(Units.LENGTH_MILLIMETRES)))
        try:
            #For axis-inverted configuration
            # self.XAxis.move_absolute(self.homeX+(int(self.textY)-1)*9, Units.LENGTH_MILLIMETRES)
            # self.YAxis.move_absolute(self.homeY+(ord(self.textX)-65)*9, Units.LENGTH_MILLIMETRES)

            self.XAxis.move_absolute(self.homeX, Units.LENGTH_MILLIMETRES)
            self.YAxis.move_absolute(self.homeY, Units.LENGTH_MILLIMETRES)
            self.createFolder(self.path, item)

            # Measure for user given measurement time on single well
            for i in range(int(self.measTime.text())):
                self.savePath = self.fullDir + "/" + item + "_" + str(self.increment) + ".ht3"
                tttrmode.startttR(1000*60,self.savePath)
                self.increment = self.increment + 1
                
            # print(self.textY)
            # QThread.msleep(1000*int(self.measTime.text()))         #Wait time ( Probably implement measurement function here?? )
            self.increment = 0
            QThread.msleep(1000)

        except CommandFailedException as e:
            msgBox = QMessageBox()
            msgBox.setText("Error: " + str(e))
            msgBox.exec()

        tttrmode.closeDevices()
        axisPosText = "X-axis, Y-Axis: {} {}".format(self.XAxis.get_position(
            Units.LENGTH_MILLIMETRES), self.YAxis.get_position(Units.LENGTH_MILLIMETRES))
        
    
class initDevices(QtWidgets.QMainWindow, Ui_initDevices):

    def __init__(self, *args, obj=None, **kwargs):
        super(QtWidgets.QMainWindow,self).__init__(*args, **kwargs)
        self.setupUi(self)
        # init with all available devices
        self.showDevices()
        self.findDevices.clicked.connect(self.showDevices)
        self.portListWidget.itemClicked.connect(self.selectedPort)
    

    def privious_selection(self):
        # function for selection save and grap routines

        # grap root for selection saves in class
        self.project_root = os.path.dirname(os.path.abspath(__file__))

        # create/open file for privious selection grap
        file_dir = os.path.join(self.project_root,'last_selection.txt')

        if os.path.isfile(file_dir):
            file_reader = open(file_dir, 'r')
            cont = file_reader.read()
            file_reader.close()

            #Todo: define fixed structure for the file 
            if cont:
                return cont
            else:
                print('Empty file')
                return None
        else:
            print('No previous selection')
            return None

    def write_selection(self, port):
         self.project_root = os.path.dirname(os.path.abspath(__file__))

         # create/open file for privious selection grap
         file_dir = os.path.join(self.project_root,'last_selection.txt')
         file_writer = open(file_dir,'w')
         file_writer.write(port)
         file_writer.close()



    def showDevices(self):
        result = []
        ports = ['COM%s' % (i + 1) for i in range(256)]
        # clear current port list to only show refreshed items
        self.portListWidget.clear()
        # get privious select if applicable
        pre_sel = self.privious_selection()

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                # Mark previously selected port 
                if pre_sel:
                    if pre_sel == port:
                        port = port + ' (*)'
                result.append(port)
                self.portListWidget.addItem(port)
            except (OSError, serial.SerialException):
                pass
    
    def selectedPort(self):
        commPort = self.portListWidget.currentItem().text()
        self.write_selection(port=commPort)
        connection = Connection.open_serial_port(commPort)
        # catch devices in port selection
        try:
            device_list = connection.detect_devices()
        # if fail show user warning window and return
        except:
            # close connection to prevent crashes --> else reopen connect and possible fail due to multi access
            connection.close()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Device search fail')
            msg.setInformativeText('No device found.\nPlease select an other port')
            msg.exec_()
            return

        print("Found {} devices".format(len(device_list)))
        device = device_list[1]

        self.hide()
        self.window2 = MainWindow(device ,self)
        self.window2.setWindowTitle('Single Well Measurement')
        
        self.window2.show()
            # ex = Example(device)
            # sys.exit(app.exec_())
        # print(self.portListWidget.currentItem().text())


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow_Single):

    def __init__(self,device,init_device,*args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self._init_device = init_device
        self.setupUi(self)


        font = QFont("Arial", 12)

        side = 43

        # Get device and axis variables
        self.device = device
        self.XAxis = self.device.get_axis(1)
        self.YAxis = self.device.get_axis(2)

        # Relative home get home values
        [self.homeX,self.homeY] = self.privious_home()

        # grap min max vals 
        [self.xmi, self.xma, self.ymi, self.yma] = self.min_max_xy_grep()


        self.threadpool = QThreadPool()
        self._current_selection = []

        self.path = ""

        # Assign connections to buttons
        self.homeButton.clicked.connect(self.goToHomePos)
        self.closeConnButton.clicked.connect(self.closeConn)
        self.setHomeButton.clicked.connect(self.setHome)
        self.moveToPosition.clicked.connect(self.startMeas)

        self.browseButton.clicked.connect(self.browseSlot)

        # Assign connection to the x/y min/max boxes 
        self.xmin.returnPressed.connect(self.write_min_max_xy_file)
        self.xmax.returnPressed.connect(self.write_min_max_xy_file)
        self.ymin.returnPressed.connect(self.write_min_max_xy_file)
        self.ymax.returnPressed.connect(self.write_min_max_xy_file)


    
    def select_items(self, items, on):
        if on:
            for item in items:
                item.setBrush(Qt.red)
        else:
            for item in items:
                item.setBrush(Qt.blue)


    def goToHomePos(self):
        '''
        Go to home position - here it's manually set to 10 mm in Axis 1 to avoid damage to objective
        '''
        # self.device.all_axes.home()
        try: 
            [self.xmi, self.xma, self.ymi, self.yma] = self.min_max_xy_grep()

            if self.homeX < self.xmi or self.homeX > self.xma:
                print('X out of defined range')
                return
            elif self.homeY < self.ymi or self.homeY > self.yma:
                print('Y out of defined range')
                return

            self.XAxis.move_absolute(self.homeX,Units.LENGTH_MILLIMETRES)
            self.YAxis.move_absolute(self.homeY,Units.LENGTH_MILLIMETRES)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Home postion')
            msg.setInformativeText('No home postion defined.\nPlease select a home position')
            msg.exec_()
            print('Home position is not defined')

    def setHome(self):
        '''
        Set home position
        '''
        self.homeX = self.XAxis.get_position(Units.LENGTH_MILLIMETRES)
        self.homeY = self.YAxis.get_position(Units.LENGTH_MILLIMETRES)

        # Only accept home position if its inside boundarys

        [self.xmi, self.xma, self.ymi, self.yma] = self.min_max_xy_grep()

        if self.homeX < self.xmi or self.homeX > self.xma:
            print('X home out of defined range')
            return

        elif self.homeY < self.ymi or self.homeY > self.yma:
            print('Y home out of defined range')
            return

        print("WellX: {}; WellY: {}".format(self.homeX,self.homeY))

        # save selection in file 
        self.write_home_sle(self.homeX, self.homeY)

    def startMeas(self):
        '''
        Automated movement of the stage to the selected wells
        '''
        # self.get_thread = automateMove(self.measTime,self.XAxis,self.YAxis, self.homeX,self.homeY)
        # self.get_thread.moveToThread(self.thread)
        # self.get_thread.run()

        # no border controle
        worker = automateMove(self.measTime,self.XAxis,self.YAxis, self.homeX,self.homeY, self.path)
        self.threadpool.start(worker)
        self.write_comment(self.comment_win.text())


    def closeConn(self):
        '''
        Close the connection and quit the application
        '''
        self.device.connection.close()
        tttrmode.closeDevices()
        QtWidgets.QApplication.instance().quit()

    def closeEvent(self, event):
        # super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
        print("closing MainWindow")
        try:
            self.device.connection.close()
            tttrmode.closeDevices()
        except:
            print("Device already disconnected")
    
    def browseSlot(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        options |= QtWidgets.QFileDialog.DontUseCustomDirectoryIcons

        dialog = QtWidgets.QFileDialog()
        dialog.setOptions(options)
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)

        self.path = dialog.getExistingDirectory(self,"Select a directory")
        self.folderDir.setText(str(self.path))

    def privious_home(self):
        '''
        function for selection save and grep routines
        '''

        # grap root for selection saves in class
        project_root = os.path.dirname(os.path.abspath(__file__))

        # create/open file for privious selection grap
        file_dir = os.path.join(project_root,'last_single_well_pos.txt')

        if os.path.isfile(file_dir):
            file_reader = open(file_dir, 'r')
            cont = file_reader.read()
            file_reader.close()
            #Todo: define fixed structure for the file 
            if cont:
                cont = cont.split(',')
                return [float(el) for el in cont]
            else:
                print('Empty file')
                return [None, None]
        else:
            print('No previous selection')
            return [None, None]

    def write_comment(self, comment_text):
        comment_file_dir = os.path.join(self.path, 'comment.txt')
        comment_writer = open(comment_file_dir,'w')
        comment_writer.write(comment_text)
        comment_writer.close()

    def write_home_sle(self, x_home, y_home):

         '''
         write home selection to file 
         '''

         project_root = os.path.dirname(os.path.abspath(__file__))

         # create/open file for privious selection grap
         file_dir = os.path.join(project_root,'last_single_well_pos.txt')
         file_writer = open(file_dir,'w')
         file_writer.write(f'{x_home},{y_home}')
         file_writer.close()

    def min_max_xy_grep(self):
        # function to init. read in of min/max positions

        project_root = os.path.dirname(os.path.abspath(__file__))

        file_dir = os.path.join(project_root, 'min_max_pos.txt')


        gui_input = [float(self.xmin.text()), float(self.xmax.text()), float(self.ymin.text()), float(self.ymax.text())]

        if os.path.isfile(file_dir) and gui_input == [float('-inf'), float('inf'), float('-inf'), float('inf')]: 
            file_reader = open(file_dir, 'r')
            out = file_reader.read()
            file_reader.close()

            if out: 
                out = out.split(',')
                # set text to boxes for read in values 
                self.xmin.setText(out[0])
                self.xmax.setText(out[1])
                self.ymin.setText(out[2])
                self.ymax.setText(out[3])
                return [float(el) for el in out]
            else:
                print('Min Max file empty') 
                return gui_input
        elif os.path.isfile(file_dir) and gui_input != [float('-inf'), float('inf'), float('-inf'), float('inf')]:
            # prefere non default user input over the file --> Init still always file or inf 
            return gui_input
        else: 
           # if no file found just take the user input/default values (inf)
            return gui_input

    def write_min_max_xy_file(self):
        # just get values and write them to standard file
        project_root = os.path.dirname(os.path.abspath(__file__))
        file_dir = os.path.join(project_root, 'min_max_pos.txt')

        self.xmax.text()

        file_writer = open(file_dir, 'w')
        file_writer.write(f'{self.xmin.text()},{self.xmax.text()},{self.ymin.text()},{self.ymax.text()}')



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Library.enable_device_db_store()
    
    window = initDevices()
    window.show()
    sys.exit(app.exec_())
    
    # with Connection.open_serial_port("COM3") as connection:
    #     device_list = connection.detect_devices()
    #     print("Found {} devices".format(len(device_list)))
    #     device = device_list[1]
    #     window = MainWindow(device)
    #     window.show()
    #     # ex = Example(device)
    #     sys.exit(app.exec_())


if __name__ == "__main__":
    print('Init main run scanning software')
    main()