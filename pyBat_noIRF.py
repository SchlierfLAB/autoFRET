# Import GUI
import os
import pickle

from FRET_backend.BatUi import Ui_MainWindow
from FRET_backend.GetBurstAll import par_burst, get_files, check_for_bdata_files
from FRET_backend.BatFileDIalog import File_DD_Dialog
from FRET_backend.ChannelSelectWindow import ChannelSelectionWindow
from FRET_backend.BatOverriteFilesDialog import ask_override_files

from FRET_backend.Read_PTU_Obj import Read_PTU

# Basic imports
import sys
import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# PyQT imports
from PyQt5.QtWidgets import QGridLayout,  QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


from FRET_backend.read_hhd import read_hhd
from FRET_backend.read_ht3_vect import histc
from FRET_backend.lee_filter import leeFilter
from FRET_backend.burst_locator import burstLoc
import time
import multiprocessing




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        '''
        Backend for the pyBAT tool
        Args:
            *args:
            **kwargs:
        '''

        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)

        #Set shortcut and menu button connection
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openFileSlot)

        self.actionExprotSettings.triggered.connect(self.export_settings)
        self.actionImportSettings.triggered.connect(self.import_settings)

        # Set up file dialog window
        self.drag_drop_files = File_DD_Dialog()

        self.duplicate_files_di = ask_override_files()

        #Set button connections
        self.DD_DA_Button.clicked.connect(self.GG_GR_Slot)
        # will be enabled when data is loaded
        self.DD_DA_Button.setDisabled(True)
        self.AA_Button.clicked.connect(self.RR_Slot)
        self.NormButton.setDisabled(True)
        self.NormButton.clicked.connect(self.NormButtonEvent)

        # will be enabled when GG_GR is set
        self.AA_Button.setDisabled(True)
        self.RawDataButton.clicked.connect(self.BurstButtonEvent)
        # will be enabled when the GG_GR and RR are set
        self.RawDataButton.setDisabled(True)
        self.AnalyzeButton.clicked.connect(self.AnalyzeButtonEvent)
        self.AnalyzeButton.setDisabled(True)

        # IRF shift buttons
        self.PlusIRFButton_Top.setDisabled(True)
        self.PlusIRFButton_Top.clicked.connect(self.irf_shifts)
        self.MinusIRFButton_Top.setDisabled(True)
        self.MinusIRFButton_Top.clicked.connect(self.irf_shifts)
        self.PlusIRFButton_Mid.setDisabled(True)
        self.PlusIRFButton_Mid.clicked.connect(self.irf_shifts)
        self.MinusIRFButton_Mid.setDisabled(True)
        self.MinusIRFButton_Mid.clicked.connect(self.irf_shifts)

        self.refreshButton.clicked.connect(self.init_execute)

        # Toggle behaviour of min Pht vs min total
        self.minTotalTick.clicked.connect(self.tick_switch)
        self.grBox.setDisabled(True)
        self.r0Box.setDisabled(True)

        # get burst detect method

        self.data_in = False

        # well thats defined for some reason :D
        self.BinSize = 1

        self.Brd_GGR = []
        self.Brd_RR = []

    def irf_shifts(self):

        '''
        Control over +/- buttons to shift the irfs. Will also refresh the lifetimes for every step
        Returns:

        '''

        sender = self.sender()
        if sender == self.PlusIRFButton_Top:
            self.normIRF_G_plot = np.roll(self.normIRF_G_plot, 1)
            self.plot_lifetime1()
        elif sender == self.MinusIRFButton_Top:
            self.normIRF_G_plot = np.roll(self.normIRF_G_plot, -1)
            self.plot_lifetime1()
        elif sender == self.PlusIRFButton_Mid:
            self.normIRF_R_plot = np.roll(self.normIRF_R_plot, 1)
            self.plot_lifetime2()
        elif sender == self.MinusIRFButton_Mid:
            self.normIRF_R_plot = np.roll(self.normIRF_R_plot, -1)
            self.plot_lifetime2()



    def tick_switch(self):
        '''
        Creates a switch for the listed tick boxes
        Returns:

        '''

        if self.minTotalTick.isChecked():
            self.grBox.setDisabled(True)
            self.r0Box.setDisabled(True)
        elif not self.minTotalTick.isChecked():
            self.grBox.setDisabled(False)
            self.r0Box.setDisabled(False)

    def openFileSlot(self):
        '''
        Intitial file read in. Takes a single ht3 file to be displayed in the panels in order to adjust the
        settings. Further HHD files are getting imported. Further Raw data gets analyzed / histograms are computed
        to get first plots. Execution function gets triggered to initialize plots and first computes.
        Returns:

        '''

        ## Channel selection ##
        channel_dialog = ChannelSelectionWindow(self)
        if channel_dialog.exec_() == QDialog.Accepted:
            self.channel_remap = channel_dialog.channel_mapping
        else:
            return  # User cancelled

        ## Start file grabbing ##

        self.drag_drop_files.exec_()

        # Dict info
        # self.drag_drop_files.file_dir_dictionary ['HT3','HHD1','HHD2'] stores file path
        try:
            file_dict = self.drag_drop_files.file_dir_dict
        # If nothing selected do nothing
        except AttributeError:
            return

        self.data_dir = os.path.dirname(os.path.dirname(file_dict['HT3']))
        print(file_dict)
        # check for empty
        if all(file_dict.values()):
            # if three files are selected
            pass
        elif file_dict['HT3'] and not file_dict['HHD1'] and not file_dict['HHD2']:
            print('No correction files provided. Continue with less stats')
            # Todo: Create a Warning Window!
            pass

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
            file_instance = Read_PTU(self.ht3file, self.channel_remap)
            file_instance.further_process()
            self.Data = file_instance.all_out
            #self.Data = read_ht3_raw(self.ht3file)
            self.RawData = self.Data['RawData']
            self.RawInt = self.Data['RawInt']
            self.repRate = self.Data['SyncRate']
            self.dtBin = self.Data['varout4']


        except (IndexError, FileNotFoundError):
            print('Error no ht3 data given')

        # Todo: Add user input for bin size
        self.edges2 = np.arange(0,4096,1)

        self.hGII=histc(self.RawData[np.equal(self.RawData[:,0], 2)][:,1],self.edges2)[0]
        self.hGT=histc(self.RawData[np.equal(self.RawData[:,0], 4)][:,1],self.edges2)[0]
        self.hRII=histc(self.RawData[np.equal(self.RawData[:,0], 1)][:,1],self.edges2)[0]
        self.hRT=histc(self.RawData[np.equal(self.RawData[:,0], 3)][:,1],self.edges2)[0]

        # get non neg. len for plotting axis
        #top plot
        Det2_4_Xaxis = np.max([len(self.hGII[self.hGII > 0]), len(self.hGT[self.hGT > 0])])
        #middle plot
        Det1_3_Xaxis = np.max([len(self.hRII[self.hRII > 0]), len(self.hRT[self.hRT > 0])])
        #global lim
        self.xlimit = np.max([Det2_4_Xaxis, Det1_3_Xaxis])


        self.numCh=(1e12/self.repRate/self.dtBin)
        self.midCh=(round(self.numCh/2))

        self.interPhT=(self.RawData[1:,2]-self.RawData[0:-1,2])*1e-6

        try:
            self.RHHD_G = read_hhd(self.hhdfileG)
        except FileNotFoundError:
            if not self.hhdfileG:
                self.RHHD_G = [[np.zeros(65536), np.zeros(65536), np.zeros(65536), np.zeros(65536)], 0]
        except IndexError:
            print('No hhdG file')
            return

        try:
            self.RHHD_R = read_hhd(self.hhdfileR)
        except FileNotFoundError:
            if not self.hhdfileR:
                self.RHHD_R = [[np.zeros(65536), np.zeros(65536), np.zeros(65536), np.zeros(65536)], 0]
        except IndexError:
            print('No hhdR file')
            return
        # Enable GG_GR button when data is there
        if self.RHHD_G and self.RHHD_R:
            self.DD_DA_Button.setDisabled(False)
            self.NormButton.setDisabled(False)
            self.lower_Norm.setDisabled(False)
            self.upper_Norm.setDisabled(False)
            self.PlusIRFButton_Top.setDisabled(False)
            self.MinusIRFButton_Top.setDisabled(False)
            self.PlusIRFButton_Mid.setDisabled(False)
            self.MinusIRFButton_Mid.setDisabled(False)
            self.data_in = True

        # execute with new data calculations and plotting part
        self.init_execute()

        ## End readout ##


    def calculations(self):

        '''
        Normalizes the IRF's and splitts raw data into channels and parallel + perpendicular parts
        Returns:

        '''

        ## Mathemagic ##
        IRF_AllG = self.RHHD_G[0]
        self.IRF_G = IRF_AllG[1] + IRF_AllG[3]

        self.IRF_G = self.IRF_G - np.mean(self.IRF_G[int(self.numCh) - 601:int(self.numCh) - 100])
        #origIRF_G = self.IRF_G
        #corrIRF_G = 0

        IRF_AllR = self.RHHD_R[0]
        self.IRF_R = IRF_AllR[0] + IRF_AllR[2]

        self.IRF_R = self.IRF_R - np.mean(self.IRF_R[int(self.midCh) - 501:int(self.midCh) - 100])
        #origIRF_R = self.IRF_R
        #corrIRF_R = 0

        self.maxhG = np.max(np.max([self.hGII, self.hGT]))
        self.normIRF_G = self.IRF_G / max(self.IRF_G) * self.maxhG
        self.normIRF_G_plot = self.normIRF_G[self.normIRF_G > 0]

        self.maxhR = np.max(np.max([self.hRII, self.hRT]))
        self.normIRF_R = self.IRF_R / max(self.IRF_R) * self.maxhR
        self.normIRF_R_plot = self.normIRF_R[self.normIRF_R > 0]

        # split PARALLEL (II) and PERPENDICULAR (T)


        # GREEN (G) part -> Donor
        self.IRF_G_II = IRF_AllG[1]
        self.IRF_G_T = IRF_AllG[3]

        self.IRF_G_II = self.IRF_G_II - np.mean(self.IRF_G_II[int(self.numCh) - 601:int(self.numCh) - 100])
        self.IRF_G_T = self.IRF_G_T - np.mean(self.IRF_G_T[int(self.numCh) - 601:int(self.numCh) - 100])

        self.maxhG_II = np.max(self.hGII)
        self.maxhG_T = np.max(self.hGT)

        self.normIRF_G_II = self.IRF_G_II / max(self.IRF_G_II) * self.maxhG_II
        self.normIRF_G_T = self.IRF_G_T / max(self.IRF_G_T) * self.maxhG_T

        # RED (R) part -> Acceptor
        self.IRF_R_II = IRF_AllR[0]
        self.IRF_R_T = IRF_AllR[2]

        self.IRF_R_II = self.IRF_R_II - np.mean(self.IRF_R_II[int(self.midCh) - 501:int(self.midCh) - 100])
        self.IRF_R_T = self.IRF_R_T - np.mean(self.IRF_R_T[int(self.midCh) - 501:int(self.midCh) - 100])

        self.maxhR_II = np.max(self.hRII)
        self.maxhR_T = np.max(self.hRT)

        self.normIRF_R_II = self.IRF_R_II / max(self.IRF_R_II) * self.maxhR_II
        self.normIRF_R_T = self.IRF_R_T / max(self.IRF_R_T) * self.maxhR_T


    def plot_lifetime1(self):

        '''
        Plots the lifetime for channels 2 & 4 (top panel)
        Returns:

        '''

        self.lifetime1_plot.canvas.ax.clear()
        self.lifetime1_plot.canvas.ax.semilogy(self.edges2, self.hGII, color='green',
                                               linewidth=0.5, nonpositive='clip')

        self.lifetime1_plot.canvas.ax.semilogy(self.edges2, self.hGT, color='green',
                                               alpha=0.5, linewidth=0.5, nonpositive='clip')


        self.lifetime1_plot.canvas.ax.semilogy(np.where(self.normIRF_G > 0)[0],
                                               self.normIRF_G_plot, color='grey', linewidth=0.5)
        self.lifetime1_plot.canvas.ax.set_xlabel("Channels")
        self.lifetime1_plot.canvas.ax.set_ylabel("Detector 2 & 4")

        # x axis lims
        self.lifetime1_plot.canvas.ax.set_xlim((0, self.xlimit))

        self.lifetime1_plot.canvas.fig.tight_layout()
        self.lifetime1_plot.canvas.draw()

    def plot_lifetime2(self):

        '''
        Plots the lifetime for channels 1 & 3 (mid panel)
        Returns:

        '''

        self.lifetime2_plot.canvas.ax.clear()
        self.lifetime2_plot.canvas.ax.semilogy(self.edges2, self.hRII, color='red',
                                               linewidth=0.5, nonpositive='clip')
        self.lifetime2_plot.canvas.ax.semilogy(self.edges2, self.hRT, color='red',
                                               alpha=0.5, linewidth=0.5, nonpositive='clip')

        self.lifetime2_plot.canvas.ax.semilogy(self.edges2[np.where(self.normIRF_R > 0)],
                                               self.normIRF_R_plot, color='grey', linewidth=0.5)
        self.lifetime2_plot.canvas.ax.set_xlabel("Channels")
        self.lifetime2_plot.canvas.ax.set_ylabel("Detector 1 & 3")

        # def x axis lim
        self.lifetime2_plot.canvas.ax.set_xlim((0, self.xlimit))

        self.lifetime2_plot.canvas.fig.tight_layout()
        self.lifetime2_plot.canvas.draw()

    def plot_interPht(self):

        '''
        Plots the interphoton time (bottom panel)
        Returns:

        '''

        self.interPht_plot.canvas.ax.clear()
        self.interPht_plot.canvas.ax.plot(self.interPhT, linewidth=0.5)
        self.interPht_plot.canvas.ax.set_xlabel("$Photon_{i+1 -> i}$")
        self.interPht_plot.canvas.ax.set_ylabel("Interphoton time (ms)")
        self.interPht_plot.canvas.fig.tight_layout()
        self.interPht_plot.canvas.draw()

    def init_execute(self):
        '''
        Executes initial calculations to get plotting variables -> Plots the data in the three slots
        -> To be used after data readin
        Afterwards several buttons in the interface are enabled
        '''

        self.get_current_settings()
        self.calculations()
        self.plot_lifetime1()
        self.plot_lifetime2()
        self.plot_interPht()

        if self.data_in:
            # If refresh after first init it is still drawn
            if len(self.Brd_GGR) == 2:
                self.green_span_top = self.lifetime1_plot.canvas.ax.axvspan(self.Brd_GGR[0], self.Brd_GGR[1], facecolor='green', alpha=0.4)
                self.green_span_bottom = self.lifetime2_plot.canvas.ax.axvspan(self.Brd_GGR[0], self.Brd_GGR[1], facecolor='green', alpha=0.4)
                self.lifetime1_plot.canvas.draw()
                self.lifetime2_plot.canvas.draw()
            if len(self.Brd_RR) == 2:
                self.red_span = self.lifetime2_plot.canvas.ax.axvspan(self.Brd_RR[0], self.Brd_RR[1], facecolor='red', alpha=0.4)
                self.lifetime2_plot.canvas.draw()
                self.Filter()
                self.Show_Bursts()

            #self.newIRF_G = self.IRF_G[self.Brd_GGR[0] - 1:self.Brd_GGR[1]]
            #self.newIRF_G_II = self.IRF_G_II[self.Brd_GGR[0] - 1:self.Brd_GGR[1]]
            #self.newIRF_G_T = self.IRF_G_T[self.Brd_GGR[0] - 1:self.Brd_GGR[1]]


            self.DD_DA_Button.setDisabled(False)
            self.NormButton.setDisabled(False)
            self.lower_Norm.setDisabled(False)
            self.upper_Norm.setDisabled(False)
            self.PlusIRFButton_Top.setDisabled(False)
            self.MinusIRFButton_Top.setDisabled(False)
            self.PlusIRFButton_Mid.setDisabled(False)
            self.MinusIRFButton_Mid.setDisabled(False)
            self.AnalyzeButton.setDisabled(False)
            self.AA_Button.setDisabled(False)
            self.RawDataButton.setDisabled(False)






    def GG_GR_Slot(self):
        '''
        Triggers when DD + DA button in interface pressed. Checks if user trys to overwrite the current selection.
        Changes cursor to cross within the plot. Triggers function to grap the interval after mouse press.
        Returns:

        '''
        # reset
        if len(self.Brd_GGR) == 2:
            self.green_span_top.remove()
            self.green_span_bottom.remove()
            self.Brd_GGR = []

        # change cursor style
        self.lifetime1_plot.setCursor(QtCore.Qt.CrossCursor)

        self.cid = self.lifetime1_plot.canvas.mpl_connect("button_press_event", self.get_Brd_GGR)


    def get_Brd_GGR(self, event):
        '''
                Gets tge x,y interval for channel 2 & 4 (Top plot), draws the span into the plot. Enables the AA
                button and resets cursor.
                Args:
                    event: Klick event

                Returns:

        '''

        self.Brd_GGR.append(round(event.xdata))

        # Brd_GGR are the selected x coordinates of the top plot
        if len(self.Brd_GGR) == 2:
            self.green_span_top = self.lifetime1_plot.canvas.ax.axvspan(self.Brd_GGR[0], self.Brd_GGR[1], facecolor='green', alpha=0.4)
            self.green_span_bottom = self.lifetime2_plot.canvas.ax.axvspan(self.Brd_GGR[0], self.Brd_GGR[1], facecolor='green', alpha=0.4)
            self.lifetime1_plot.canvas.draw()
            self.lifetime2_plot.canvas.draw()


            self.newIRF_G = self.IRF_G[self.Brd_GGR[0]-1:self.Brd_GGR[1]]
            self.newIRF_G_II = self.IRF_G_II[self.Brd_GGR[0] - 1:self.Brd_GGR[1]]
            self.newIRF_G_T = self.IRF_G_T[self.Brd_GGR[0] - 1:self.Brd_GGR[1]]

            self.AA_Button.setDisabled(False)

            # if two selected reset cursor style
            self.lifetime1_plot.setCursor(QtCore.Qt.ArrowCursor)

            return


        elif len(self.Brd_GGR) == 1:
            pass

        else:
            print('Condition in GG + GR not fullfilled:\nlen(self.Brd_GGR) != 2')




    def RR_Slot(self):

        '''
        Triggers when AA button in interface pressed. Checks if user trys to overwrite the current selection.
        Changes cursor to cross within the plot. triggers function to grap the interval after mouse press.
        Returns:

        '''
        # reset
        if len(self.Brd_RR) == 2:
            self.red_span.remove()
            self.Brd_RR = []


        # change cursor style
        self.lifetime2_plot.setCursor(QtCore.Qt.CrossCursor)
        self.cid = self.lifetime2_plot.canvas.mpl_connect("button_press_event", self.get_Brd_RR)

    def get_Brd_RR(self, event):

        '''
        Gets tge x,y interval for channel 1 & 3, draws the span into the plot and applies the filters. Afterwards
        cursor gets reset.
        -> Has to be done after the GRR part
        Args:
            event: Klick event

        Returns:

        '''

        self.Brd_RR.append(round(event.xdata))

        if len(self.Brd_RR) == 2:

            self.lifetime2_plot.canvas.mpl_disconnect(self.cid)
            self.red_span = self.lifetime2_plot.canvas.ax.axvspan(self.Brd_RR[0], self.Brd_RR[1], facecolor='red', alpha=0.4)
            #self.lifetime1_plot.canvas.ax.axvspan(self.Brd_RR[0], self.Brd_RR[1], facecolor='red', alpha=0.4)
            self.lifetime2_plot.canvas.draw()
            self.lifetime1_plot.canvas.draw()

            self.newIRF_R = self.IRF_R[self.Brd_RR[0]-1:self.Brd_RR[1]]

            self.newIRF_R_II = self.IRF_R_II[self.Brd_RR[0]-1:self.Brd_RR[1]]
            self.newIRF_R_T = self.IRF_R_T[self.Brd_RR[0]-1:self.Brd_RR[1]]

            # enable burst (and in future analyze)
            self.RawDataButton.setDisabled(False)
            self.AnalyzeButton.setDisabled(False)

            # if two selected reset cursor style
            self.lifetime2_plot.setCursor(QtCore.Qt.ArrowCursor)

            # apply filter with user inputted Brd_GGR and Brd_RR
            self.Filter()
            self.Show_Bursts()

        elif len(self.Brd_RR) == 1:
            pass
        else:
            print('Condition in GR not fullfilled:\nlen(self.Brd_RR) != 2')

    def NormButtonEvent(self):
        '''
        Event triggered when Display is pressed by user. Channel range can be provided. This will alter the
        lifetime plots and computes new Parallel II and Perpendicular T values for the channels
        Returns:

        '''

        # get current channel settings
        channels = [int(self.lower_Norm.text()), int(self.upper_Norm.text())]

        # subtract channel selection from total
        self.hGII = self.hGII - np.mean(self.hGII[channels[0]-1:channels[1]])
        self.hGT = self.hGT - np.mean(self.hGT[channels[0]-1:channels[1]])

        self.hRII = self.hRII - np.mean(self.hRII[channels[0]-1:channels[1]])
        self.hRT = self.hRT - np.mean(self.hRT[channels[0]-1:channels[1]])

        # update lifetime plots
        self.plot_lifetime1()
        self.plot_lifetime2()



    def Filter(self):

        ind = ((self.Brd_GGR[0] <= self.RawData[:, 1]) & (self.RawData[:, 1] <= self.Brd_GGR[1])) | \
              (((self.RawData[:, 0] == 1) | (self.RawData[:, 0] == 3)) & (self.Brd_RR[0] <= self.RawData[:, 1]) \
               & (self.RawData[:, 1] <= self.Brd_RR[1]))



        tt = np.arange(1,len(self.RawInt[0])+2)
        self.meastime = tt[-1] / 1000 * self.BinSize

        self.reduData = self.RawData[ind, :]

        numArr = self.meastime * 1000 / self.BinSize + 1
        reduInt = np.zeros(int(numArr))
        self.reduR = np.zeros(int(numArr))
        self.reduG = np.zeros(int(numArr))
        self.reduRR = np.zeros(int(numArr))

        timeWindow = np.array([0, 999999*self.BinSize], dtype=np.uint64)

        iterInt = 0
        for i in range(len(self.reduData)):
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

        '''
        Event after the Raw Data button in the GUI gets pressed. Creates three plots.
        1. Macrotime plot
        2. Donor - Acceptor over time
        3. Total vs. Time (s) Histogram
        Returns:

        '''

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

    def handle_duplicated_files(self):

        '''
        Triggers when there is a file conflict -> Analysis dir already contains BData files.
        -> User can decide if files should be overwritten or new suffix should be used

        '''

        # Trigger dialog on how to handle file conflicts

        self.duplicate_files_di.exec_()
        self.HowToTreatFiles = self.duplicate_files_di.decision

        if self.HowToTreatFiles == 'Stop':
            return

        # If user wants to overwrite
        elif self.HowToTreatFiles == 'Overwrite Files':
            for sub in os.listdir(self.folder):
                if not sub.startswith('.'):
                    if os.path.isdir(self.folder + '/' + sub):
                        override_fp_Bdata = self.folder + '/' + sub + '/' + 'BData' + str(self.suffix)+'.bin'
                        Path(override_fp_Bdata).open('w')
                        override_fp_Pdata = self.folder + '/' + sub + '/' + 'PData' + str(self.suffix)+'.bin'
                        Path(override_fp_Pdata).open('w')

            # restart Analyze button without checking files again since they are there but empty and ready to take
            # new data
            self.AnalyzeButtonEvent(IRF_calcs=True, Check_Files=False)

        # If user wants to change the suffix
        elif self.HowToTreatFiles == 'Change Suffix':

            self.NewSuffix = self.duplicate_files_di.suffix_box.text()

            if self.NewSuffix == self.suffix:
                self.handle_duplicated_files()
            else:
                self.suffix = self.NewSuffix
                self.fileSuffixBox.setText(self.suffix)
                self.AnalyzeButtonEvent(IRF_calcs=True, Check_Files=False)

        # fallback --> Do nothing
        else:
            return

    def AnalyzeButtonEvent(self, dummy=True, IRF_calcs=True, Check_Files=True):

        '''
        Does the full burst analysis
        Args:
            dummy: dummy required to prevent error (no one knows why)
            IRF_calcs: Channel based IRF averaging
            Check_Files: Check if there are already analysis files (bdata) in the selected folder
            -> If that is the case user will be asked if they should be overwritten. If not user
            has to change the file suffix

        Returns:

        '''

        # load current settings
        self.get_current_settings()

        # extract current settings as dictionary
        self.get_settings_dict()

        if IRF_calcs:
            meanIRFG = (np.sum(np.arange(1, len(self.newIRF_G) + 1, 1) * self.newIRF_G) / np.sum(self.newIRF_G) +
                        self.Brd_GGR[0]) * self.dtBin / 1000

            meanIRFG_II = (np.sum(np.arange(1, len(self.newIRF_G_II) + 1, 1) * self.newIRF_G_II) / np.sum(self.newIRF_G_II) +
                        self.Brd_GGR[0]) * self.dtBin / 1000
            meanIRFG_T = (np.sum(np.arange(1, len(self.newIRF_G_T) + 1, 1) * self.newIRF_G_T) / np.sum(self.newIRF_G_T) +
                        self.Brd_GGR[0]) * self.dtBin / 1000

            meanIRFR = (np.sum(np.arange(1, len(self.newIRF_R) + 1, 1) * self.newIRF_R) / np.sum(self.newIRF_R) +
                        self.Brd_RR[0]) * self.dtBin / 1000

            meanIRFR_II = (np.sum(np.arange(1, len(self.newIRF_R_II) + 1, 1) * self.newIRF_R_II) / np.sum(self.newIRF_R_II) +
                        self.Brd_RR[0]) * self.dtBin / 1000
            meanIRFR_T = (np.sum(np.arange(1, len(self.newIRF_R_T) + 1, 1) * self.newIRF_R_T) / np.sum(self.newIRF_R_T) +
                        self.Brd_RR[0]) * self.dtBin / 1000

        if Check_Files:
            # open a full 96 well folder
            # Open folder directory dialog to select the folder
            self.folder = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Directory", directory=self.data_dir)

            eval_folder = get_files(self.folder)
            meas_file_check = check_for_bdata_files(eval_folder, self.suffix)

            if meas_file_check:
                self.handle_duplicated_files()
                return

        eval_folder = get_files(self.folder)

        workers = self.numCores # max. num of concurrently running jobs -> -2 == All but one are used

        if self.numCores > 0:
            print(f'Run with {self.numCores} workers')
        else:
            print(f'Run with {multiprocessing.cpu_count() + (self.numCores+1)} workers')

        # get burst method
        # ["Time-Based", "Intensity-Based" (with thresholds)]

        if self.burst_method == "Time-Based":
            thresh_based = False
        elif self.burst_method == "Intensity-Based":
            thresh_based = True
        else:
            print('Selected method not available')
            return

        print(f'\nSelected detection method: {self.burst_method}')

        start = time.time()


        par_burst(eval_folder, self.suffix, self.Brd_GGR, self.Brd_RR, self.threIT, self.threITN, self.minPhs, self.newIRF_G_II, self.newIRF_G_T,
                  meanIRFG_II, meanIRFG_T, self.newIRF_R_II, self.newIRF_R_T, meanIRFR_II, meanIRFR_T, self.dtBin, self.setLeeFilter, self.boolFLA,
                  self.boolTotal, self.minGR, self.minR0, self.boolPostA, self.tauFRET, self.tauALEX, self.settings_dict, thresh_based, self.channel_remap, workers)


        print(f'\n\nTook {time.time()-start} seconds to analyze')

    def IPTButtonEvent(self):
        # event after IPT button pressed
        # --> Placeholder backend
        pass

    def get_current_settings(self):
        '''
        Reads in all settings from the GUI, changes format (str -> float/int/bool)
        '''

        # read Setting Values
        # get integer values of boxes
        self.setLeeFilter = int(self.leeFilterBox.text())
        self.threIT = float(self.maxInterTime.text())
        self.threITN = float(self.minInterTimeNoise.text())
        self.minPhs = int(self.minTotal.text())
        self.minGR = int(self.grBox.text())
        self.minR0 = int(self.r0Box.text())
        self.filesBin = int(self.filesPerBinBox.text())
        self.numCores = self.CoreSelectBox.text()

        # for tau
        self.tauFRET = float(self.tauFRETbox.text())
        self.tauALEX = float(self.tauALEXbox.text())

        if self.numCores == 'Auto':
            self.numCores = -2
        else:
            try:
                self.numCores = int(self.numCores)
                if self.numCores > multiprocessing.cpu_count():
                    self.numCores = multiprocessing.cpu_count()

                elif self.numCores == 0:
                    self.numCores = 1

            except ValueError:
                print('Give proper core number as integer')


        self.suffix = self.fileSuffixBox.text()



        # gives a bool for tickboxes
        self.boolFLA = self.flaCheckbox.isChecked()
        self.boolLee = self.leeFilterCheck.isChecked()
        self.boolPostA = self.postAnaCheckbox.isChecked()
        self.boolTotal = self.minTotalTick.isChecked()
        self.thirty_thirty = self.thirtythirtyCheck.isChecked()

        # get selected burst method
        self.burst_method = self.method_select.currentText()




    def get_settings_dict(self):

        '''
        Creates a highly standarderized settings dictionary. Note that the keys are actually variables used in the
        settings definiations of the BatUi. This is key to easily import settings from a file.
        Returns: None

        '''

        self.get_current_settings() #get current settings just in case they are not updated
        self.settings_dict = dict() #init dict for output

        # setting values do have to have key equivalent to the setting "box" object name
        # all the integers/floats/general values
        self.settings_dict['leeFilterBox'] = self.setLeeFilter
        self.settings_dict['maxInterTime'] = self.threIT
        self.settings_dict['minInterTimeNoise'] = self.threITN
        self.settings_dict['minTotal'] = self.minPhs
        self.settings_dict['grBox'] = self.minGR
        self.settings_dict['r0Box'] = self.minR0
        self.settings_dict['filesPerBinBox'] = self.filesBin
        self.settings_dict['tauFRETbox'] = self.tauFRET
        self.settings_dict['tauALEXbox'] = self.tauALEX
        self.settings_dict['CoreSelectBox'] = self.numCores

        #bools for the tickboxes
        self.settings_dict['flaCheckbox'] = self.boolFLA
        self.settings_dict['leeFilterCheck'] = self.boolLee
        self.settings_dict['postAnaCheckbox'] = self.boolPostA
        self.settings_dict['minTotalTick'] = self.boolTotal
        self.settings_dict['thirtythirtyCheck'] = self.thirty_thirty


        self.settings_dict['Brd_GGR'] = self.Brd_GGR
        self.settings_dict['Brd_RR'] = self.Brd_RR


    def export_settings(self):

        '''
        Creates a .csv file containing all current settings of pyBAT. Standard format guided by settings dictionary
        -> Can be read again by the software using import settings
        Returns: Nothing if file path is not selected -> User closes the window


        '''

        # get current settings as dictionary
        self.get_settings_dict()

        filepath = QtWidgets.QFileDialog.getSaveFileName(self, caption="Give File Name",filter='*.csv')


        # if nothing selected
        if filepath[0] == '':
            return

        # save to file
        pd.DataFrame([self.settings_dict]).to_csv(filepath[0], index=False)

    def import_settings(self):

        '''
        Function that imports a standard format settings .csv file. File NEEDS to be in correct format.
        Order of settings in file does not matter but the naming is important. Uses literal eval.
        Returns: Return nothing if fail

        '''
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
                if setting == 'Brd_GGR':
                    self.Brd_GGR = ast.literal_eval(settings_input[setting][0])
                elif setting == 'Brd_RR':
                    self.Brd_RR = ast.literal_eval(settings_input[setting][0])

                elif not isinstance(settings_input[setting].values[0], (np.bool_)):
                    getattr(self, f'{setting}') \
                        .setText(_translate("Settings", f"{str(settings_input[f'{setting}'].values[0])}"))
                # if bool its a checkbox
                elif isinstance(settings_input[setting].values[0], (np.bool_)):
                    getattr(self, f'{setting}') \
                        .setChecked(settings_input[setting].values[0])

            # refresh current view
            if self.data_in:
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


        if indexSig.size == 0 or indexSigN.size == 0:
            print('Selected file has to much background noise')
            return

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
        bursts_found = len(bStartLong)
        background_found = len(bStartLongN)


        self.interPht_plot.canvas.ax.text(0.99, 0.98, f'Brusts: {bursts_found}\nBackground: {background_found}',
                                          horizontalalignment='right',
                                          verticalalignment='top',
                                          transform=self.interPht_plot.canvas.ax.transAxes,
                                          color='Red')




        self.interPht_plot.canvas.ax.set_xlim([0,7500])
        self.interPht_plot.canvas.draw()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationDisplayName("pyBAT")
    app.setWindowIcon(QtGui.QIcon('requirements/batIcon.png'))
    w = MainWindow()
    w.setWindowTitle('pyBAT - Burst Analysis Tool')
    w.show()
    sys.exit(app.exec_())