# Import GUI
from FRET_backend.BatUi import Ui_MainWindow

# Basic imports
import sys
import os
import numpy as np
import pandas as pd
import collections
import matplotlib.pyplot as plt

# PyQT imports
from PyQt5.QtWidgets import QGridLayout,  QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# Import eval functions
from FRET_backend.read_hhd import read_hhd
from FRET_backend.read_ht3_vect import read_ht3_raw, histc
from FRET_backend.getBurstAll import getBurstAll
from FRET_backend.lee_filter import leeFilter
from FRET_backend.burst_locator import burstLoc

import time

class File_DD_Dialog(QDialog):

    def __init__(self, parent=None):
        super(File_DD_Dialog, self).__init__(parent)
        self.setWindowTitle("Drag and Drop")
        self.setAcceptDrops(True)
        self.grid = QGridLayout()
        self.resize(250,200)


        # total 4 elements for 200 pixels -> boxes y coords -> 1. 1-50, 2. 51-101, 3. 102-152

        # build fields
        self.file1Widget = QLineEdit(self)
        self.file1Widget.setPlaceholderText('Drag ht3 File')
        self.grid.addWidget(self.file1Widget,0,0)

        # build fields
        self.file2Widget = QLineEdit(self)
        self.file2Widget.setPlaceholderText('Drag first hhd File')
        self.grid.addWidget(self.file2Widget,1,0)

        # build fields
        self.file3Widget = QLineEdit(self)
        self.file3Widget.setPlaceholderText('Drag second hhd File')
        self.grid.addWidget(self.file3Widget,2,0)

        # Close with selection button
        self.select_button = QPushButton("OK")
        self.select_button.clicked.connect(self.ok_button_pressed)
        self.labelResult = QLabel()
        self.grid.addWidget(self.select_button, 10, 0, 1,2)

        # Buttons for file dialogs

        # First define a Folder Icon
        pixmapi = getattr(QStyle, 'SP_DirOpenIcon')
        icon = self.style().standardIcon(pixmapi)

        # File 1 Button
        self.file1Button = QPushButton('')
        self.file1Button.setIcon(icon)
        self.file1Button.clicked.connect(self.folder_button1_select)
        self.grid.addWidget(self.file1Button, 0,1)

        # File 2 Button
        self.file2Button = QPushButton('')
        self.file2Button.setIcon(icon)
        self.file2Button.clicked.connect(self.folder_button2_select)
        self.grid.addWidget(self.file2Button, 1,1)

        # File 3 Button
        self.file3Button = QPushButton('')
        self.file3Button.setIcon(icon)
        self.file3Button.clicked.connect(self.folder_button3_select)
        self.grid.addWidget(self.file3Button, 2,1)

        self.setLayout(self.grid)

    def folder_button1_select(self):
        self.first_file = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select File", "", "*.ht3")
        try: # if nothing selected the empty var wont have an index and the program will return (same below)
            self.file1Widget.setText(self.first_file[0][0])
        except IndexError:
            return

    def folder_button2_select(self):
        self.first_file = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select File", "", "*.hhd")
        try:
            self.file2Widget.setText(self.first_file[0][0])
        except IndexError:
            return

    def folder_button3_select(self):
        self.first_file = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select File", "", "*.hhd")
        try:
            self.file3Widget.setText(self.first_file[0][0])
        except IndexError:
            return



    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        # Define vertical coordinates for accepted boxes in a given file widget position
        # it does scale with the window size therefore coordinates as ranges are defined

        self.ycoord_range_pos1 = \
            [self.file1Widget.pos().y()+self.file1Widget.size().height()+10,
             self.file1Widget.pos().y()-self.file1Widget.size().height()-10]
        self.ycoord_range_pos2 = \
            [self.file2Widget.pos().y()+self.file2Widget.size().height()+10,
             self.file2Widget.pos().y()-self.file2Widget.size().height()-10]
        self.ycoord_range_pos3 = \
            [self.file3Widget.pos().y()+self.file3Widget.size().height()+10,
             self.file3Widget.pos().y()-self.file3Widget.size().height()-10]

        files = [u.toLocalFile() for u in event.mimeData().urls()]

        if event.pos().y() <= self.ycoord_range_pos1[0] and event.pos().y() > self.ycoord_range_pos1[1]:
            if files[0].endswith('.ht3'): # only if correct ht3 file type
                self.file1Widget.setText(files[0])
        elif event.pos().y() <= self.ycoord_range_pos2[0] and event.pos().y() >=  self.ycoord_range_pos2[1]:
            if files[0].endswith('.hhd'): # only if correct hhd file type
                self.file2Widget.setText(files[0])
        elif event.pos().y() <= self.ycoord_range_pos3[0] and event.pos().y() >= self.ycoord_range_pos3[1]:
            if files[0].endswith('.hhd'): # only if correct hhd file type
                self.file3Widget.setText(files[0])




    def ok_button_pressed(self):
        # Store the selected file path's in a dictionary
        self.file_dir_dict = dict()
        self.file_dir_dict['HT3'] = self.file1Widget.text()
        self.file_dir_dict['HHD1'] = self.file2Widget.text()
        self.file_dir_dict['HHD2'] = self.file3Widget.text()
        self.close()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        #Set shortcut and menu button connection
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openFileSlot)

        self.actionExprotSettings.triggered.connect(self.export_settings)
        self.actionImportSettings.triggered.connect(self.import_settings)

        self.minTotalTick.clicked.connect(self.minTot_Phot_controller)
        self.grBox.setDisabled(True)
        self.r0Box.setDisabled(True)

        # Set up file dialog window
        self.drag_drop_files = File_DD_Dialog()

        #Set button connections
        self.GG_GR_Lifetime_button.clicked.connect(self.GG_GR_Slot)
        # will be enabled when data is loaded
        self.GG_GR_Lifetime_button.setDisabled(True)
        self.GR_Lifetime_button.clicked.connect(self.RR_Slot)
        # will be enabled when GG_GR is set
        self.GR_Lifetime_button.setDisabled(True)
        self.BurstButton.clicked.connect(self.BurstButtonEvent)
        # will be enabled when the GG_GR and RR are set
        self.BurstButton.setDisabled(True)
        self.AnalyzeButton.clicked.connect(self.AnalyzeButtonEvent)
        self.AnalyzeButton.setDisabled(True)

        self.IPTButton.clicked.connect(self.IPTButtonEvent)
        self.IPTButton.hide()

        self.refreshButton.clicked.connect(self.init_execute)


        # well thats defined for some reason :D
        self.BinSize = 1

    def minTot_Phot_controller(self):
        if self.minTotalTick.isChecked():
            self.grBox.setDisabled(True)
            self.r0Box.setDisabled(True)
        else:
            self.grBox.setDisabled(False)
            self.r0Box.setDisabled(False)


    def openFileSlot(self):


        ## Start file grabbing ##

        self.drag_drop_files.exec_()

        # Dict info
        # self.drag_drop_files.file_dir_dictionary ['HT3','HHD1','HHD2'] stores file path
        try:
            file_dict = self.drag_drop_files.file_dir_dict
        # If nothing selected do nothing
        except AttributeError:
            return

        # check for empty
        if all(file_dict.values()):
            # if three files are selected
            pass
        elif not all(file_dict.values()) and any(file_dict.values()):
            # give an error dialog if the user has selected <3 files (not a heart :D)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("File Selection Incomplete")
            #msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Input Error")
            msg.setDetailedText("Please select a total of three files. One HT3 and two HHD files are required")
            msg.exec_()
            return
        else:
            # if nothing entered it will do nothing.... ha take this user
            return

        # hand paths to object vars
        self.ht3file = file_dict['HT3']
        self.hhdfileG = file_dict['HHD1']
        self.hhdfileR = file_dict['HHD2']


        ## finished file grabbing ##

        ## Start Readout ##

        try:
            self.Data = read_ht3_raw(self.ht3file)
            self.RawData = self.Data['RawData']
            self.RawInt = self.Data['RawInt']
            self.repRate = self.Data['SyncRate']
            self.dtBin = self.Data['varout4']

        except (IndexError, FileNotFoundError):
            print('Error no ht3 data given')

        self.edges2 = np.arange(0,4096,1)


        self.hGII=histc(self.RawData[np.equal(self.RawData[:,0], 2)][:,1],self.edges2)[0]
        self.hGT=histc(self.RawData[np.equal(self.RawData[:,0], 4)][:,1],self.edges2)[0]
        self.hRII=histc(self.RawData[np.equal(self.RawData[:,0], 1)][:,1],self.edges2)[0]
        self.hRT=histc(self.RawData[np.equal(self.RawData[:,0], 3)][:,1],self.edges2)[0]

        self.numCh=(1e12/self.repRate/self.dtBin)
        self.midCh=(round(self.numCh/2))

        self.interPhT=(self.RawData[1:,2]-self.RawData[0:-1,2])*1e-6

        try:
            self.RHHD_G = read_hhd(self.hhdfileG)
        except IndexError:
            print('No hhdG file')
            return

        try:
            self.RHHD_R = read_hhd(self.hhdfileR)
        except IndexError:
            print('No hhdR file')
            return

        # Enable GG_GR button when data is there
        if self.RHHD_G and self.RHHD_R:
            self.GG_GR_Lifetime_button.setDisabled(False)

        # execute with new data calculations and plotting part
        self.init_execute()

        ## End readout ##


    def calculations(self):
        ## Mathemagic ##
        IRF_AllG = self.RHHD_G[0]
        self.IRF_G = IRF_AllG[1] + IRF_AllG[3]
        self.IRF_G = self.IRF_G - np.mean(self.IRF_G[int(self.numCh) - 601:int(self.numCh) - 100])
        origIRF_G = self.IRF_G
        corrIRF_G = 0

        IRF_AllR = self.RHHD_R[0]
        self.IRF_R = IRF_AllR[0] + IRF_AllR[2]
        self.IRF_R = self.IRF_R - np.mean(self.IRF_R[int(self.midCh) - 501:int(self.midCh) - 100])
        origIRF_R = self.IRF_R
        corrIRF_R = 0

        self.maxhG = np.max(np.max([self.hGII, self.hGT]))
        self.normIRF_G = self.IRF_G / max(self.IRF_G) * self.maxhG


        self.maxhR = np.max(np.max([self.hRII, self.hRT]))
        self.normIRF_R = self.IRF_R / max(self.IRF_R) * self.maxhR


    def plot_lifetime1(self):

        self.lifetime1_plot.canvas.ax.clear()
        self.lifetime1_plot.canvas.ax.semilogy(self.edges2[self.hGII > 0], self.hGII[self.hGII > 0], color='green',
                                               linewidth=0.5)
        self.lifetime1_plot.canvas.ax.semilogy(self.edges2[self.hGT > 0], self.hGT[self.hGT > 0], color='green',
                                               alpha=0.5, linewidth=0.5)
        self.lifetime1_plot.canvas.ax.semilogy(self.edges2[np.where(self.normIRF_G > 0)],
                                               self.normIRF_G[self.normIRF_G > 0], color='grey', linewidth=0.5)
        self.lifetime1_plot.canvas.ax.set_xlabel("Channels")
        self.lifetime1_plot.canvas.ax.set_ylabel("GG")
        # self.lifetime_plot.canvas.ax.set_title(self.keys[self.sliderVal])
        # self.lifetime_plot.canvas.ax.set_xlim((-0.1, 1.1))
        # self.lifetime_plot.canvas.ax.tick_params(direction='in', top=True, right=True)
        self.lifetime1_plot.canvas.fig.tight_layout()
        self.lifetime1_plot.canvas.draw()

    def plot_lifetime2(self):

        self.lifetime2_plot.canvas.ax.clear()
        self.lifetime2_plot.canvas.ax.semilogy(self.edges2[self.hRII > 0], self.hRII[self.hRII > 0], color='red',
                                               linewidth=0.5)
        self.lifetime2_plot.canvas.ax.semilogy(self.edges2[self.hRT > 0], self.hRT[self.hRT > 0], color='red',
                                               alpha=0.5, linewidth=0.5)
        self.lifetime2_plot.canvas.ax.semilogy(self.edges2[np.where(self.normIRF_R > 0)],
                                               self.normIRF_R[self.normIRF_R > 0], color='grey', linewidth=0.5)
        self.lifetime2_plot.canvas.ax.set_xlabel("Channels")
        self.lifetime2_plot.canvas.ax.set_ylabel("GR, RR")
        # self.lifetime_plot.canvas.ax.set_title(self.keys[self.sliderVal])
        # self.lifetime_plot.canvas.ax.set_xlim((-0.1, 1.1))
        # self.lifetime_plot.canvas.ax.tick_params(direction='in', top=True, right=True)
        self.lifetime2_plot.canvas.fig.tight_layout()
        self.lifetime2_plot.canvas.draw()

    def plot_interPht(self):

        self.interPht_plot.canvas.ax.clear()
        self.interPht_plot.canvas.ax.plot(self.interPhT[0:7500], linewidth=0.5)
        self.interPht_plot.canvas.ax.set_xlabel("$Photon_{i+1 -> i}$")
        self.interPht_plot.canvas.ax.set_ylabel("Interphoton time (ms)")
        # self.lifetime_plot.canvas.ax.set_title(self.keys[self.sliderVal])
        # self.lifetime_plot.canvas.ax.set_xlim((-0.1, 1.1))
        # self.lifetime_plot.canvas.ax.tick_params(direction='in', top=True, right=True)
        self.interPht_plot.canvas.fig.tight_layout()
        self.interPht_plot.canvas.draw()

    def init_execute(self):
        '''
        Executes initial calculations to get plotting variables -> Plots the data in the three slots
        --> To be used after data readin
        '''

        self.get_current_settings()
        self.calculations()
        self.plot_lifetime1()
        self.plot_lifetime2()
        self.plot_interPht()



    def GG_GR_Slot(self):

        # change cursor style
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.Brd_GGR = []
        self.cid = self.lifetime1_plot.canvas.mpl_connect("button_press_event", self.get_Brd_GGR)


    def get_Brd_GGR(self, event):

        self.Brd_GGR.append(round(event.xdata))

        # Brd_GGR are the selected x coordinates of the top plot
        if len(self.Brd_GGR) == 2:
            self.lifetime1_plot.canvas.ax.axvspan(self.Brd_GGR[0], self.Brd_GGR[1], facecolor='green', alpha=0.4)
            self.lifetime2_plot.canvas.ax.axvspan(self.Brd_GGR[0], self.Brd_GGR[1], facecolor='green', alpha=0.4)
            self.lifetime1_plot.canvas.draw()
            self.lifetime2_plot.canvas.draw()


            self.newIRF_G = self.IRF_G[self.Brd_GGR[0]-1:self.Brd_GGR[1]]


            self.GR_Lifetime_button.setDisabled(False)

            # if two selected reset cursor style
            QApplication.restoreOverrideCursor()


        else:
            print('Condition in GG + GR not fullfilled:\nlen(self.Brd_GGR) != 2')


    def RR_Slot(self):
        # change cursor style
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.Brd_RR = []
        # self.yG = []
        self.cid = self.lifetime2_plot.canvas.mpl_connect("button_press_event", self.get_Brd_RR)

    def get_Brd_RR(self, event):

        self.Brd_RR.append(round(event.xdata))

        if len(self.Brd_RR) == 2:

            self.lifetime2_plot.canvas.mpl_disconnect(self.cid)
            self.lifetime2_plot.canvas.ax.axvspan(self.Brd_RR[0], self.Brd_RR[1], facecolor='red', alpha=0.4)
            #self.lifetime1_plot.canvas.ax.axvspan(self.Brd_RR[0], self.Brd_RR[1], facecolor='red', alpha=0.4)
            self.lifetime2_plot.canvas.draw()
            self.lifetime1_plot.canvas.draw()

            self.newIRF_R = self.IRF_R[self.Brd_RR[0]-1:self.Brd_RR[1]]

            # enable burst (and in future analyze)
            self.BurstButton.setDisabled(False)
            self.AnalyzeButton.setDisabled(False)

            # if two selected reset cursor style
            QApplication.restoreOverrideCursor()



            # apply filter with user inputted Brd_GGR and Brd_RR
            self.Filter()
            self.Show_Bursts()

        else:
            print('Condition in GR not fullfilled:\nlen(self.Brd_RR) != 2')

    def Filter(self):

        ind = ((self.Brd_GGR[0] <= self.RawData[:, 1]) & (self.RawData[:, 1] <= self.Brd_GGR[1])) | \
              (((self.RawData[:, 0] == 1) | (self.RawData[:, 0] == 3)) & (self.Brd_RR[0] <= self.RawData[:, 1]) \
               & (self.RawData[:, 1] <= self.Brd_RR[1]))



        # Todo: Figure out if those values should be precalculated at different position
        tt = np.arange(1,len(self.RawInt[0])+2)
        self.meastime = tt[-1] / 1000 * self.BinSize

        self.reduData = self.RawData[ind, :]

        numArr = self.meastime * 1000 / self.BinSize + 1
        reduInt = np.zeros(int(numArr))
        self.reduR = np.zeros(int(numArr))
        self.reduG = np.zeros(int(numArr))
        self.reduRR = np.zeros(int(numArr))

        timeWindow = timeWindow = np.array([0, 999999*self.BinSize] ,dtype=np.uint64)

        iterInt = 0

        for i in range(len(self.reduData)):
            print(timeWindow)
            if ((self.reduData[i,2] >= timeWindow[0]) & (self.reduData[i,2] <= timeWindow[1])):

                reduInt[iterInt] = reduInt[iterInt]+1

                if ((self.reduData[i,0] == 2) | (self.reduData[i,0] == 4)) & (self.reduData[i,1] >= self.Brd_GGR[0]) & \
                        (self.reduData[i,1] <= self.Brd_GGR[1]):

                    self.reduG[iterInt] = self.reduG[iterInt] + 1

                elif ((self.reduData[i,0] == 1) | (self.reduData[i,0] == 3)) & (self.reduData[i,1] >= self.Brd_RR[0]) & \
                        (self.reduData[i,1] <= self.Brd_RR[1]):

                    self.reduRR[iterInt] = self.reduRR[iterInt] + 1

                else:
                    self.reduR[iterInt] = self.reduR[iterInt] + 1

            else:
                iterInt += 1
                reduInt[iterInt] = reduInt[iterInt] + 1

                if ((self.reduData[i,0] == 2) | (self.reduData[i,0] == 4)) & (self.reduData[i,1] >= self.Brd_GGR[0]) & \
                        (self.reduData[i,1] <= self.Brd_GGR[1]):

                    self.reduG[iterInt] = self.reduG[iterInt] + 1

                elif ((self.reduData[i,0] == 1) | (self.reduData[i,0] == 3)) & (self.reduData[i,1] >= self.Brd_RR[0]) & \
                        (self.reduData[i,1] <= self.Brd_RR[1]):

                    self.reduRR[iterInt] = self.reduRR[iterInt] + 1

                else:
                    self.reduR[iterInt] = self.reduR[iterInt] + 1

                timeWindow = timeWindow + 1000000 * self.BinSize



    def BurstButtonEvent(self):
        # event after Burst button pressed

        self.get_current_settings()


        Photons = self.RawData[(self.RawData[:,0] != 15) & ((self.RawData[:,1] >= self.Brd_GGR[0]) &
                                                            (self.RawData[:,1] <= self.Brd_GGR[1]) |
                                                            ((self.RawData[:,1] >= self.Brd_RR[0]) &
                                                             (self.RawData[:,1] <= self.Brd_RR[1])))]

        # keep just real data and seperate them in channels
        #PhotonsSGR0 = Photons[(Photons[:,0]==1) | (Photons[:,0]==2) | (Photons[:,0]==3) | (Photons[:,0]==4), 0:3]
        self.PhotonsSG = Photons[(Photons[:,0]==2) | (Photons[:,0]==4) ,0:3]
        self.PhotonsSR = Photons[((Photons[:,0]==1) | (Photons[:,0]==3)) & (Photons[:,1]>=self.Brd_GGR[0]) &
                                 (Photons[:,1]<=self.Brd_GGR[1]) ,0:3]
        self.PhotonsSR0 = Photons[((Photons[:,0]==1) | (Photons[:,0]==3)) & (Photons[:,1] >= self.Brd_RR[0])
                                  & (Photons[:,1] <= self.Brd_RR[1]),0:3]


        # Plot the Photon trace MF

        # First plot Macrotimes
        fig1, [ax1,ax2] = plt.subplots(nrows=2,ncols=1, sharex=True)

        #top plot
        ax1.scatter(self.PhotonsSG[:,2]*1e-9,np.ones(len(self.PhotonsSG)), c='green')#, marker='o', linestyle=None)
        ax1.scatter(self.PhotonsSR[:,2]*1e-9,np.zeros(len(self.PhotonsSR)), c='red')#, lw=10)
        ax1.scatter(self.PhotonsSR0[:,2]*1e-9,np.ones(len(self.PhotonsSR0))*-1, c='red')#, lw=10)
        ax1.set_yticks([-1,0,1])
        ax1.set_yticklabels(['Acceptor only', 'Acceptor', 'Donor'])
        ax1.set_xlabel('Macrotime (s)')
        ax1.set_ylim([-2,2])
        fig1.tight_layout()

        # bottom plot
        ax2.plot(Photons[1:-1,2] * 1e-9,(Photons[1:-1,2] - Photons[0:-2,2]) * 1e-6, c='blue')
        ax2.set_xlabel('Macrotime (s)')
        ax2.set_ylabel('Interphoton Time')


        fig1.show()


        tt = np.arange(1,len(self.reduR)+1)

        # second plot Donor - Acceptor and Acceptor only time (s) plot
        del ax1, ax2
        fig2, [ax1,ax2] = plt.subplots(nrows=2,ncols=1, sharex=True)

        ax1.plot(tt/1000 * self.BinSize, self.reduR,c='red')
        ax1.plot(tt/1000 * self.BinSize,self.reduG*-1,c='green')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Donor - Acceptor')


        ax2.plot(tt/1000* self.BinSize, self.reduRR, c='red')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Acceptor only')
        fig2.tight_layout()
        fig2.show()

        # third plot Total vs. Time (s)
        del ax1

        fig3, ax1 = plt.subplots()
        ax1.plot(tt/1000*self.BinSize, self.reduR + self.reduG + self.reduRR, c='blue')
        ax2.set_xlabel('Time rm(s)')
        ax2.set_ylabel('Total')

        fig3.show()

    def AnalyzeButtonEvent(self):

        # load current settings
        self.get_current_settings()

        # obtain average IRF shift
        meanIRFG = (np.sum(np.arange(1,len(self.newIRF_G)+1,1) * self.newIRF_G) / np.sum(self.newIRF_G) +
                    self.Brd_GGR[0]) * self.dtBin/1000


        meanIRFR = (np.sum(np.arange(1,len(self.newIRF_R)+1,1) * self.newIRF_R) / np.sum(self.newIRF_R) +
                    self.Brd_RR[0]) * self.dtBin/1000

        # open a full 96 well folder
        #Open folder directory dialog to select the folder
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")


        # get subfolder and file locations

        ht3_locations = dict()
        try:
            for path, subdirs, files in os.walk(folder):
                for name in files:
                    if name.endswith('.ht3'):
                        try:
                            ht3_locations[name[0:3]] = ht3_locations[name[0:3]] + [os.path.join(path,name)]
                        except KeyError:
                            ht3_locations[name[0:3]] = [os.path.join(path,name)]

        except FileNotFoundError:
            return

        def sort_fun_key(string):
            string = string.split('/')[-1]
            if len(string) == 10:
                return string[0:6]
            else:
                return string[0:4] + '0' + string[4]

        # sort the folders
        for keys in ht3_locations.keys():
            ht3_locations[keys] = sorted(ht3_locations[keys], key=sort_fun_key)

        ht3_locations = collections.OrderedDict(sorted(ht3_locations.items()))

        # Todo: Should check inner be user given or just turned off for later version?
        existCB = 0
        checkInner = 0
        folder_counter = 0


        for folder in ht3_locations.keys():
            folder_counter += 1
            print(f'\nStart analyzing measurement folder {folder_counter} of {len(ht3_locations.keys())}\n')

            arrData = []

            # get folder dir from file dir --> Robust since if the file can be handeld the folder is also correct
            folder_path = '/'.join(ht3_locations[folder][0].translate(str.maketrans({'/': '\\'})).split('\\')[0:-1])
            print(folder_path)

            # save empty file for usage in getBurstAll
            dataAll = dict()
            dataAll['photonHIST'] = np.zeros([4096,2])
            str_path_dA = folder_path + '/allHIST.npy'
            np.save(str_path_dA, dataAll)

            dataN = dict()
            dataN['backHIST'] = np.zeros([4096,2])
            dataN['time'] = [0]
            str_pathdN = folder_path + '/backHIST.npy'
            np.save(str_pathdN, dataN)

            # define six subplots per folder to be shown to the user --> row major for accessing the subplots
            # figure set to be in HD (1920x1080)
            fig, ((ax1,ax2,ax3), (ax4,ax5,ax6)) = plt.subplots(nrows=2, ncols=3, figsize=(19.2, 10.8))

            plt.ion()
            lastBN = 0
            File_counter = 0

            start = time.time()
            print('Start the whole GetBurstAll process')

            for file in ht3_locations[folder]:
                File_counter += 1
                print(f'Start analyzing file {File_counter} of {len(ht3_locations[folder])}\n')

                file = file.translate(str.maketrans({'/': '\\'}))
                fileName = file.split('\\')[-1]
                folderName = '/'.join(file.split('\\')[0:-1])

                BurstData = getBurstAll(fileName, folderName, self.suffix, lastBN, self.Brd_GGR, self.Brd_RR,self.threIT \
                                        , self.threITN, self.minPhs, 10, self.newIRF_G, meanIRFG, self.newIRF_R, \
                                        meanIRFR, self.Brd_GGR, self.Brd_RR, self.dtBin, self.setLeeFilter, \
                                        self.boolFLA, self.gGG, self.gRR, self.boolTotal, self.minGR, self.minR0, \
                                        self.boolPostA, checkInner)
                lastBN += len(BurstData)

                if BurstData.any():
                    NG = BurstData[:, 1]
                    NGII = BurstData[:, 2]
                    NGT = BurstData[:, 3]
                    NR = BurstData[:, 4]
                    NRII = BurstData[:, 5]
                    NRT = BurstData[:, 6]
                    NR0 = BurstData[:, 7]
                    NR0II = BurstData[:, 8]
                    NR0T = BurstData[:, 9]
                    BGII = BurstData[:, 10]
                    BGT = BurstData[:, 11]
                    BRII = BurstData[:, 12]
                    BRT = BurstData[:, 13]
                    BR0II = BurstData[:, 14]
                    BR0T = BurstData[:, 15]
                    TB = BurstData[:, 16]
                    valueCDE = BurstData[:, 17]
                    valueCDE2 = BurstData[:, 18]
                    dtGR_TR0 = BurstData[:, 19]
                    tauArrD = BurstData[:, 20]
                    tauArrA = BurstData[:, 21]
                    FGII = NGII - BGII * TB
                    FGT = NGT - BGT * TB
                    FRII = NRII - BRII * TB
                    FRT = NRT - BRT * TB
                    FR0II = NR0II - BR0II * TB
                    FR0T = NR0T - BR0T * TB

                    FG = FGII + FGT
                    FR = FRII + FRT
                    FR0 = FR0II + FR0T

                    E = FR / (FG + FR)
                    S = (FG + FR) / (FG + FR + FR0)
                    rGG = (FGII - FGT) / (FGII + 2 * FGT)
                    rRR = (FR0II - FR0T) / (FR0II + 2 * FR0T)

                    # perform dynamic append on list(arrData)
                    # if its empty just fill else stack current iteration to the old one

                    if arrData == []:
                        arrData = np.array([E, S, rGG, rRR, tauArrD, tauArrA, valueCDE, valueCDE2, dtGR_TR0]).T


                    else:
                        arrData = np.append(arrData,
                                            np.array([E, S, rGG, rRR, tauArrD, tauArrA, valueCDE, valueCDE2,
                                                      dtGR_TR0]).T, axis=0)

                    plot1 = ax1.scatter(arrData[:, 0], arrData[:, 1], c='b', s=1)
                    ax1.set_xlim([-0.1, 1.1])
                    ax1.set_ylim([-0.1, 1.1])
                    ax1.set_xlabel('E')
                    ax1.set_ylabel('S')

                    plot2 = ax2.scatter(arrData[:, 0], arrData[:, 6], c='b', s=1)
                    ax2.set_xlim([-0.1, 1.1])
                    ax2.set_ylim([0, 80])
                    ax2.set_xlabel('E')
                    ax2.set_ylabel('FRET-2CDE')

                    plot3 = ax3.scatter(arrData[:, 4], arrData[:, 2], c='g', s=1)
                    plot3_1 = ax3.scatter(arrData[:, 5], arrData[:, 3], c='r', s=1)
                    ax3.set_xlim([0, 8])
                    ax3.set_ylim([-0.2, 0.5])
                    ax3.set_xlabel('\u03C4 (ns)')
                    ax3.set_ylabel('r')

                    plot4 = ax4.scatter(arrData[:, 7], arrData[:, 8], c='b', s=1)
                    ax4.set_xlim([0, 100])

                    limYax4 = np.max([np.max(arrData[:, 8]) - np.min(arrData[:, 8])])
                    if limYax4 != np.nan:
                        ax4.set_ylim([-limYax4, limYax4])

                    ax4.set_xlabel('ALEX-2CDE')
                    ax4.set_ylabel('T_G_R-T_R_0')

                    plot5 = ax5.scatter(arrData[:, 4], arrData[:, 0], c='b', s=1)
                    ax5.set_ylim([-0.1, 1.1])
                    ax5.set_xlim([0, 6])
                    ax5.set_xlabel('\u03C4 D(A) (ns)')
                    ax5.set_ylabel('E')

                    plot6 = ax6.scatter(arrData[:, 5], arrData[:, 0], c='b', s=1)
                    ax6.set_ylim([-0.1, 1.1])
                    ax6.set_xlim([0, 6])
                    ax6.set_xlabel('\u03C4 A (ns)')
                    ax6.set_ylabel('E')

                    plt.pause(0.01)

                    fig.tight_layout()
                    plt.show()

            plt.close()
            print(f'Took: {time.time()-start} s')
        print(f'Total time: {time.time()-start}')

    def IPTButtonEvent(self):
        # event after IPT button pressed
        # --> Placeholder backend
        print('IPT button pressed')
        pass

    def get_current_settings(self):
        # read Setting Values
        # get integer values of boxes
        self.setLeeFilter = int(self.leeFilterBox.text())
        self.gGG = int(self.gGGBox.text())
        self.gRR = int(self.gRRBox.text())
        self.threIT = float(self.maxInterTime.text())
        self.threITN = float(self.minInterTimeNoise.text())
        self.minPhs = int(self.minTotal.text())
        self.minGR = int(self.grBox.text())
        self.minR0 = int(self.r0Box.text())
        self.filesBin = int(self.filesPerBinBox.text())


        self.suffix = self.fileSuffixBox.text()



        # gives a bool for tickboxes
        self.boolFLA = self.flaCheckbox.isChecked()
        self.boolLee = self.leeFilterCheck.isChecked()
        self.boolPostA = self.postAnaCheckbox.isChecked()
        self.boolTotal = self.minTotalTick.isChecked()
        self.thirty_thirty = self.thirtythirtyCheck.isChecked()

    def get_settings_dict(self):
        self.get_current_settings() #get current settings just in case they are not updated
        self.settings_dict = dict() #init dict for output

        # setting values do have to have key equivalent to the setting "box" object name
        # all the integers/floats/general values
        self.settings_dict['leeFilterBox'] = self.setLeeFilter
        self.settings_dict['gGGBox'] = self.gGG
        self.settings_dict['gRRBox'] = self.gRR
        self.settings_dict['maxInterTime'] = self.threIT
        self.settings_dict['minInterTimeNoise'] = self.threITN
        self.settings_dict['minTotal'] = self.minPhs
        self.settings_dict['grBox'] = self.minGR
        self.settings_dict['r0Box'] = self.minR0
        self.settings_dict['filesPerBinBox'] = self.filesBin
        self.settings_dict['filesPerBinBox'] = self.filesBin

        #bools for the tickboxes
        self.settings_dict['flaCheckbox'] = self.boolFLA
        self.settings_dict['leeFilterCheck'] = self.boolLee
        self.settings_dict['postAnaCheckbox'] = self.boolPostA
        self.settings_dict['minTotalTick'] = self.boolTotal
        self.settings_dict['thirtythirtyCheck'] = self.thirty_thirty




    def export_settings(self):

        # get current settings as dictionary
        self.get_settings_dict()

        filepath = QtWidgets.QFileDialog.getSaveFileName(self, caption="Give File Name",filter='*.csv')
        #folder = QtWidgets.QFileDialog.getExistingDirectory(
        #    self, "Select Directory")

        # if nothing selected
        if filepath[0] == '':
            return

        # save to file
        pd.DataFrame([self.settings_dict]).to_csv(filepath[0], index=False)

    def import_settings(self):

        # getting setting file
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, caption="Select a settings file (.csv)",
                                                          filter='*.csv')

        # return if no file is selected
        if file_path[0] == '':
            return


        # import csv from selected into pandas df
        settings_input = pd.read_csv(file_path[0])

        # get translater to set text in settings window
        _translate = QtCore.QCoreApplication.translate


        try:
            # change all the settings to values from the file
            for setting in settings_input.columns:

                # if its not a bool its not a checkbox
                if not isinstance(settings_input[setting].values[0], (np.bool_)):
                    getattr(self, f'{setting}') \
                        .setText(_translate("Settings", f"{str(settings_input[f'{setting}'].values[0])}"))
                # if bool its a checkbox
                elif isinstance(settings_input[setting].values[0], (np.bool_)):
                    getattr(self, f'{setting}') \
                        .setChecked(settings_input[setting].values[0])

            # refresh current view
            self.init_execute()

        # exception if file format is not correct
        except AttributeError:

            self.msg = QtWidgets.QMessageBox()
            self.crit_icon = QtWidgets.QMessageBox.Critical
            self.msg.setIcon(self.crit_icon)
            self.msg.setText("The settings file does not seem to be correctly formatted")
            self.msg.setInformativeText('Check the doc. for the correct format')
            self.msg.exec()

            return


    def Show_Bursts(self):

        # read current settings (contains minGR, minR0, minPhs)
        self.get_current_settings()

        Photons = self.RawData[(self.RawData[:,0] != 15) & ((self.RawData[:,1] >= self.Brd_GGR[0]) &
                                                            (self.RawData[:,1] <= self.Brd_GGR[1]) |
                                                            ((self.RawData[:,1] >= self.Brd_RR[0]) &
                                                             (self.RawData[:,1] <= self.Brd_RR[1])))]

        # keep just real data
        PhotonsSGR0 = Photons[(Photons[:,0]==1) | (Photons[:,0]==2) | (Photons[:,0]==3) | (Photons[:,0]==4), 0:3]

        # inter-photon time
        interPhT = PhotonsSGR0[1:,2] - PhotonsSGR0[0:-1,2]
        self.sizeIPT = len(interPhT)

        interLee = leeFilter(interPhT, self.setLeeFilter)

        # show interphoton times?!

        # first filter
        indexSig = np.where(interLee < (self.threIT*1e6))[0]
        indexSigN = np.where(interLee > (self.threITN*1e6))[0]

        bStart, bLength = burstLoc(indexSig,1)
        bStartN, bLengthN = burstLoc(indexSigN, 1)


        # 2nd filter
        # minimum photons per burst

        if self.boolTotal:
            bStartLong = bStart[bLength > self.minPhs]
            bLengthLong = bLength[bLength > self.minPhs]

        else:
            boolInd = np.zeros(len(bStart))

            for i in range(len(bStart)):
                phBurst = PhotonsSGR0[(bStart[i]+1):bStart[i]+int(bLength[i]),:]

                NG = len((phBurst[:,0] == 2) + len(phBurst[phBurst[:,0] == 4]))
                NR0 = len(phBurst[((phBurst[:,0] == 1) | (phBurst[:,0] == 3)) & (phBurst[:,1] >= self.Brd_RR[0]) & \
                                  (phBurst[:,1] <= self.Brd_RR[1])])
                NR = len(phBurst[((phBurst[:,0] == 1) | (phBurst[:,0] == 3)) & (phBurst[:,1] <= self.Brd_RR[0])])

                if ((NG + NR) >= self.minGR) & (NR0 >= self.minR0):
                    boolInd[i] = 1
                else:
                    boolInd[i] = 0

            bStartLong = bStart[boolInd == 1]
            bLengthLong = bLength[boolInd == 1]

        # 2nd filter
        # minimum photons per burst

        bStartLongN = bStartN[bLengthN > 160]+30
        bLengthLongN = bLengthN[bLengthN > 160]-60


        # collect photons
        for i in range(len(bStartLong)):
            self.interPht_plot.canvas.ax.plot(np.arange(bStartLong[i],bStartLong[i]+int(bLengthLong[i])),
                                              interPhT[(bStartLong[i]):(bStartLong[i]+int(bLengthLong[i]))]*1e-6,
                                              c='red',
                                              linewidth=1)


        BackPh = np.zeros(len(bStartLongN))

        for i in range(len(bStartLongN)):

            self.interPht_plot.canvas.ax.plot(np.arange(bStartLongN[i],bStartLongN[i]+int(bLengthLongN[i])),
                                              interPhT[(bStartLongN[i]):(bStartLongN[i]+int(bLengthLongN[i]))]*1e-6,
                                              c='green',
                                              linewidth=1)
            BackPh[i] = np.mean(interPhT[int(bStartLongN[i]):int((bStartLongN[i]+bLengthLongN[i]-1))]*1e-6)


        # plot Interphotn Times and Threshold
        self.interPht_plot.canvas.ax.plot(np.arange(0,7500), [self.threITN]*7500, c='r', ls='--')

        # display bursts and background
        #self.interPht_plot.canvas.



        self.interPht_plot.canvas.ax.set_xlim([0,7500])
        self.interPht_plot.canvas.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("pyBat")
    app.setWindowIcon(QtGui.QIcon('requirements/batIcon.png'))
    w = MainWindow()
    w.setWindowTitle('pyBat')
    w.show()
    sys.exit(app.exec_())