# Import internal functions
from FRET_backend.sliderWidget import Ui_MainWindow
from FRET_backend.single_Well_Widget import Ui_MainWindow_Single_Well
from FRET_backend.pyt3eeSettingsUi import Ui_Settings
from PyQt5.QtWidgets import *


# import PyQT GUI functions
from PyQt5.QtWidgets import QGridLayout, QApplication, QDockWidget, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets

# Import libs
import sys
import os
import warnings
import numpy as np
import pandas as pd
import csv
from pathlib import Path

# Imports for plotting
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["toolbar"] = "toolmanager"
from matplotlib import ticker




# supress divide by zero warning !! better solution should be evaluated !!
warnings.filterwarnings('ignore', message="divide by zero encountered in log10")




# set up pandas display options
desired_width = 10000
desired_length = 10000
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', desired_width)
pd.set_option('display.max_rows', desired_length)


plt.rcParams['savefig.dpi'] = 500   #Extract high resolution plots from the program


# matplotlib.use('Qt5Agg')


SLIDER_CSS = """
.QSlider {
    min-width: 100px;
    
}
QSlider::groove:horizontal { 
	border: 1px solid #424242; 
	height: 10px; 
	border-radius: 4px;
}

QSlider::handle:horizontal { 
	background: #22B14C; 
	border: 2px solid #B5E61D; 
	width: 16px; 
	height: 20px; 
	line-height: 20px; 
	margin-top: -5px; 
	margin-bottom: -5px; 
	border-radius: 10px; 
}

QSlider::handle:horizontal:hover { 
	border-radius: 8px;
}
"""


def histc(Inp, bin):
    """Clone of MATLAB's histc function. From: https://stackoverflow.com/a/56062759

    Args:
        Inp (ndarray): Input array/matrix
        bin (ndarray): Array of bin values

    Returns:
        Array of ndarray: Counts and mapping to bin values
    """
    bin_map = np.digitize(Inp, bin)
    count = np.zeros(bin.shape)
    for i in bin_map:
        count[i-1] += 1
    return [count, bin_map]

class Bdata_selection(QDialog):
    '''
    QDialog window for user selected BData file type
    '''
    def __init__(self, parent=None, Bdata_files=list()):
        super(Bdata_selection, self).__init__(parent)

        # Def. default output
        self.Bdata_file_out = None

        self.resize(150, 100)
        layout = QGridLayout(self)
        self.polBox = QtWidgets.QComboBox()

        # fill combo box with Bdata file options
        for element in Bdata_files:
            self.polBox.addItem(element)

        layout.addWidget(self.polBox, 0, 0, 1, 0)

        # add selection buttons
        accept_button = QPushButton()
        accept_button.setText('OK')
        accept_button.clicked.connect(self.accept_event)

        cancel_button = QPushButton()
        cancel_button.setText('Cancel')
        cancel_button.clicked.connect(self.cancel_event)


        # add to layout
        layout.addWidget(accept_button, 1, 1)
        layout.addWidget(cancel_button, 1, 0)

    def accept_event(self):
        self.Bdata_file_out = self.polBox.currentText()
        self.close()

    def cancel_event(self):
        self.close()



class SettingsWindow(QtWidgets.QWidget, Ui_Settings):

    def __init__(self, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Settings")
        # geo = self.geometry()
        # geo.moveLeft(geo.left() + geo.width()/2)
        # geo.moveTop(geo.width()/2)
        # self.setGeometry(geo)``
        self.onlyInt = QtGui.QIntValidator()
        self.onlyDouble = QtGui.QDoubleValidator()
        self.onlyIntFunc()

    def onlyIntFunc(self):

        # define kind and range of accepted inputs for settings window Elements

        # all entries with range of values

        # set for lower

        self.leftAlex.setValidator(self.onlyInt)
        self.leftBr.setValidator(self.onlyInt)
        self.leftE.setValidator(self.onlyDouble)
        self.leftFRET.setValidator(self.onlyInt)
        self.leftN.setValidator(self.onlyInt)
        self.leftNG.setValidator(self.onlyInt)
        self.leftNGR.setValidator(self.onlyInt)
        self.leftNR.setValidator(self.onlyInt)
        self.leftNR0.setValidator(self.onlyInt)
        self.leftS.setValidator(self.onlyDouble)
        self.leftSGSR.setValidator(self.onlyInt)
        self.leftTB.setValidator(self.onlyInt)
        self.leftTau.setValidator(self.onlyDouble)
        self.leftTau2.setValidator(self.onlyDouble)
        self.leftdT.setValidator(self.onlyInt)
        self.leftrGG.setValidator(self.onlyDouble)
        self.leftrRR.setValidator(self.onlyDouble)

        # set for upper

        self.rightAlex.setValidator(self.onlyInt)
        self.rightBr.setValidator(self.onlyInt)
        self.rightE.setValidator(self.onlyDouble)
        self.rightFRET.setValidator(self.onlyInt)
        self.rightN.setValidator(self.onlyInt)
        self.rightNG.setValidator(self.onlyInt)
        self.rightNGR.setValidator(self.onlyInt)
        self.rightNR.setValidator(self.onlyInt)
        self.rightNR0.setValidator(self.onlyInt)
        self.rightS.setValidator(self.onlyDouble)
        self.rightSGSR.setValidator(self.onlyInt)
        self.rightTB.setValidator(self.onlyInt)
        self.rightTau.setValidator(self.onlyDouble)
        self.rightTau2.setValidator(self.onlyDouble)
        self.rightdT.setValidator(self.onlyInt)
        self.rightrGG.setValidator(self.onlyDouble)
        self.rightrRR.setValidator(self.onlyDouble)

        # single inputs

        self.beta.setValidator(self.onlyDouble)
        self.BinOffset.setValidator(self.onlyDouble)
        self.BinSize.setValidator(self.onlyDouble)
        self.gamma.setValidator(self.onlyDouble)
        self.alpha.setValidator(self.onlyDouble)
        self.delta.setValidator(self.onlyDouble)
        self.gGG.setValidator(self.onlyDouble)
        self.gRR.setValidator(self.onlyDouble)
        self.aveBG.setValidator(self.onlyDouble)
        self.aveBR.setValidator(self.onlyDouble)
        self.aveBR0.setValidator(self.onlyDouble)
        self.tauD0.setValidator(self.onlyDouble)



class tickwindow_left_save(QDialog):
    # obj to create a tickwindow dialogue for the left save button

    def __init__(self, parent=None):
        super(tickwindow_left_save, self).__init__(parent)

        self.input_given = False
        self.listCheckBox = ["Save All", "Save Current", "Save RAW", "Save .png", "Save .eps"]
        self.grid = QGridLayout()
        self.resize(150,100)
        self.label = QLabel('Test label')


        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i] = QCheckBox(v)
            self.grid.addWidget(self.listCheckBox[i], i, 0)

        # Default will activate save current
        self.listCheckBox[1].setChecked(True)


        # add textbox to safe all save file
        self.left_set_file_textbox_all = QLineEdit(self)
        self.left_set_file_textbox_all.setPlaceholderText('Enter file name')
        self.grid.addWidget(self.left_set_file_textbox_all,0,1)
        # hide till needed
        self.left_set_file_textbox_all.hide()

        # add textbox for current saved Settingsfile
        self.left_set_file_textbox_current = QLineEdit(self)
        self.left_set_file_textbox_current.setPlaceholderText('Enter file name')
        self.grid.addWidget(self.left_set_file_textbox_current,1,1)
        # hide till needed
        self.left_set_file_textbox_current.hide()

        # add textbox to save raw
        self.left_saveRaw_textbox = QLineEdit(self)
        self.left_saveRaw_textbox.setPlaceholderText('Enter file name')
        self.grid.addWidget(self.left_saveRaw_textbox,2,1)
        # hide till needed
        self.left_saveRaw_textbox.hide()


        # add textbox to save png and eps files
        self.left_png_textbox = QLineEdit(self)
        self.left_png_textbox.setPlaceholderText('Enter file name')
        self.grid.addWidget(self.left_png_textbox,3,1)
        # hide till needed
        self.left_png_textbox.hide()

        self.left_eps_textbox = QLineEdit(self)
        self.left_eps_textbox.setPlaceholderText('Enter file name')
        self.grid.addWidget(self.left_eps_textbox,4,1)
        # hide till needed
        self.left_eps_textbox.hide()
        self.ask_for_safe_file()

        self.listCheckBox[0].clicked.connect(self.ask_for_safe_file)
        self.listCheckBox[1].clicked.connect(self.ask_for_safe_file)

        self.listCheckBox[0].clicked.connect(self.toggle_controller_0)
        self.listCheckBox[1].clicked.connect(self.toggle_controller_1)



        self.button = QPushButton("OK")
        self.button.clicked.connect(self.checkboxChanged)
        self.labelResult = QLabel()

        self.grid.addWidget(self.button, 10, 0, 1,2)
        self.setLayout(self.grid)


    def toggle_controller_0(self):
        # given that user ticked 0 and its unticked now tick 1 if its not ticked already
       if self.listCheckBox[0].checkState() == 0 and self.listCheckBox[1].checkState() == 0:
           self.listCheckBox[1].setChecked(True)

    def toggle_controller_1(self):
        # given that user ticked 1 and its unticked now tick 0 if its not ticked already
        if self.listCheckBox[0].checkState() == 0 and self.listCheckBox[1].checkState() == 0:
            self.listCheckBox[0].setChecked(True)


    def ask_for_safe_file(self):
        # add global box for the settings file
        if self.listCheckBox[0].checkState() == 2 or self.listCheckBox[1].checkState() == 2:
            self.settings_file_textbox = QLineEdit(self)
            self.settings_file_textbox.setPlaceholderText('Enter Name for your settings file')
            self.grid.addWidget(self.settings_file_textbox,5,0)
            self.resize(300,150)
        else:
            try:
                self.settings_file_textbox.hide()
                self.resize(300,100)
            except AttributeError:
                # if no text box was opened before
                return


    def checkboxChanged(self):
        self.listLabel = []
        for i, v in enumerate(self.listCheckBox):
            self.listLabel.append(True if v.checkState() else False)

        # create a dictionary of the answers
        self.checklist = dict(zip([tick.text() for tick in self.listCheckBox], self.listLabel))
        self.input_given = True
        self.close()

class tickwindow_right_save(QDialog):

    # obj to create a tickwindow dialogue for the right save button
    def __init__(self, parent=None):
        super(tickwindow_right_save, self).__init__(parent)

        self.input_given = False
        self.listCheckBox = ["Save Data", "Save .png", "Save .eps"]
        grid = QGridLayout()
        self.label = QLabel('Test label')


        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i] = QCheckBox(v)
            grid.addWidget(self.listCheckBox[i], i, 0)


        self.button = QPushButton("OK")
        self.button.clicked.connect(self.checkboxChanged)
        self.labelResult = QLabel()

        grid.addWidget(self.button, 10, 0, 1,2)
        self.setLayout(grid)


    def checkboxChanged(self):
        self.listLabel = []
        for i, v in enumerate(self.listCheckBox):
            self.listLabel.append(True if v.checkState() else False)

        # create a dictionary of the answers
        self.checklist = dict(zip([tick.text() for tick in self.listCheckBox], self.listLabel))
        self.input_given = True
        self.close()

class tickwindow_single_well(QDialog):
    def __init__(self, parent=None):
        super(tickwindow_single_well, self).__init__(parent)

        self.input_given = False
        self.listCheckBox = ["Save Data", "Save RAW", "Save .png", "Save .eps"]
        self.grid = QGridLayout()
        self.label=QLabel('Test label')

        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i] = QCheckBox(v)
            self.grid.addWidget(self.listCheckBox[i],i,0)

        self.listCheckBox[0].clicked.connect(self.ask_for_safe_file)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.checkboxChanged)
        self.labelResult = QLabel()

        self.grid.addWidget(self.button, 10, 0, 1,2)
        self.setLayout(self.grid)

    def ask_for_safe_file(self):
        # add global box for the settings file
        if self.listCheckBox[0].checkState() == 2:
            self.settings_file_textbox = QLineEdit(self)
            self.settings_file_textbox.setPlaceholderText('Enter Name for your settings file')
            self.grid.addWidget(self.settings_file_textbox,5,0)
            self.resize(300,150)
        else:
            self.settings_file_textbox.hide()
            self.resize(150,100)

    def checkboxChanged(self):
        self.listLabel = []
        for i, v in enumerate(self.listCheckBox):
            self.listLabel.append(True if v.checkState() else False)

        # create a dictionary of the answers
        self.checklist = dict(zip([tick.text() for tick in self.listCheckBox], self.listLabel))
        self.input_given = True
        self.close()


class custom_toolbar(NavigationToolbar):
    def __init__(self,plotCanvas):
        NavigationToolbar.__init__(self,plotCanvas)

        # remove subplot button
        POSITION_OF_CONFIGURE_SUBPLOTS_BTN = 6
        self.DeleteToolByPos(POSITION_OF_CONFIGURE_SUBPLOTS_BTN)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # global argument to check if data is uploaded by the user
        # is set to true in the openFolderSlot function
        self.data_available = False

        self.setupUi(self)
        self.user_warning(self)

        #Generate well ID's for easier access
        self.wellNum = []
        for num in np.arange(96):
            self.wellNum.append('ABCDEFGH'[(num) // 12] + '%02d' % ((num) % 12 + 1,))


        # add a detachable settings window to the left of the main window
        self.get_settings_window()

        # add a tickwindow
        self.Tickwindow_left = tickwindow_left_save()
        self.Tickwindow_right = tickwindow_right_save()


        #Set toolbars under plot areas for additional tools (saving etc.,)
        NavigationToolbar.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            (None, None, None, None),
            ('Pan', 'Left button pans, Right button zooms\nx/y fixes axis, CTRL fixes aspect', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Customize', 'Edit axis, curve and image parameters', 'qt4_editor_options', 'edit_parameters'),
            ('Save', 'Save the figure', 'filesave', 'save_figure')
        )




        self.toolbarLeft = NavigationToolbar(self.leftGraph.canvas, self, coordinates=True)
        self.toolbarLeft.setMinimumHeight(20)
        self.toolbarLeft.setStyleSheet("QToolBar { border: 0px }")
        self.leftGraphLayout.addWidget(self.toolbarLeft)


        self.toolbarRight = NavigationToolbar(self.rightGraph.canvas, self, coordinates=False)
        self.toolbarRight.setMinimumHeight(20)
        self.toolbarRight.setStyleSheet("QToolBar { border: 0px }")
        self.rightGraphLayout.addWidget(self.toolbarRight)


        #Hide range-specific functions when it's unchecked
        self.rangeText.hide()
        self.rangeLabel.hide()
        self.plotRangeButton.hide()

        #Define slider design with SLIDER_CSS
        self.wellSlider.setStyleSheet(SLIDER_CSS)

        # Connect range checkbox and plot button
        self.rangeCheck.stateChanged.connect(self.rangeStateChangeSlot)
        self.plotRangeButton.clicked.connect(self.plotRangeSlot)

        #Set shortcut and menu button connection
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openFolderSlot)

        #self.actionExtractRaw.triggered.connect(self.extractRawDataSlot)

        self.actionImportSettings.triggered.connect(self.ImportSettings)
        self.actionGetSettingsBack.triggered.connect(self.get_settings_window)

        self.actionSwitchSingle.triggered.connect(self.init_switch)

        #Slider change connection
        #Action for press on slider range or drag and move slider
        self.wellSlider.sliderMoved.connect(self.sliderChange)
        self.wellSlider.valueChanged.connect(self.sliderChange)

        #Contour/heatmap button connection
        #self.heatmapButton.clicked.connect(self.heatmapPlot)

        #Combobox connection
        self.leftComboBox.currentIndexChanged.connect(self.leftComboBoxSlot)
        self.rightComboBox.currentIndexChanged.connect(self.heatmapPlot)

        #Extract Button connections
        self.leftExtractButton.clicked.connect(self.leftExtractSlot)
        self.rightExtractButton.clicked.connect(self.rightExtractSlot)


        # Disable if no data is there
        if not self.data_available:
            self.leftExtractButton.setDisabled(True)
            self.rightExtractButton.setDisabled(True)
            #self.heatmapButton.setDisabled(True)




        self.connectSettingsSlots()

    def init_switch(self):
        self.switch_window.emit()

    def get_settings_window(self):
        #Set reference for the settings window
        try:
            self.settWin.close()
        except AttributeError:
            pass

        self.addWindow = []
        self.items=QDockWidget('Settings Window',self)

        self.settWin = SettingsWindow()
        self.settWin.show()
        self.settWin.setDisabled(True)
        self.addWindow.append(self.settWin)

        self.items.setWidget(self.settWin)
        self.items.setFloating(False)

        #Dock the settings window to the left and adjust the widget area
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.items)

        # self.items.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.items.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.settWin.setMinimumWidth(502)
        self.setMinimumWidth(1034+502)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)

        self.items.topLevelChanged.connect(self.dockChangedSlot)




    def connectSettingsSlots(self):
        """
        Slot or Callback connections for buttons in the GUI
        """

        self.settWin.leftNR0.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightNR0.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftAlex.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightAlex.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftFRET.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightFRET.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftdT.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightdT.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftE.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightE.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftNG.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightNG.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftNR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightNR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftTau.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightTau.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftTau2.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightTau2.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftTB.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightTB.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftS.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightS.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))

        self.settWin.leftSGSR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightSGSR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftN.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightN.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftrRR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightrRR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftrGG.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightrGG.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftNGR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightNGR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.leftBr.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.rightBr.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))

        self.settWin.gamma.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.alpha.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.beta.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))

        self.settWin.delta.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))

        self.settWin.aveBG.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.aveBR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.aveBR0.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))

        self.settWin.gGG.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))
        self.settWin.gRR.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))

        self.settWin.BinSize.returnPressed.connect(lambda: self.updateAllGraph(self.sliderVal))

        self.settWin.refreshButton.clicked.connect(lambda: self.updateAllGraph(self.sliderVal))


    def extract_setting_values(self):
        """
        function to extract current setting window values
        Returns: self.setting_values_dict -> Stores all values in dictionary

        """
        self.setting_values_dict = dict()
        self.setting_values_dict['leftNR0'] = self.settWin.leftNR0.text()
        self.setting_values_dict['rightNR0'] = self.settWin.rightNR0.text()
        self.setting_values_dict['leftAlex'] = self.settWin.leftAlex.text()
        self.setting_values_dict['rightAlex'] = self.settWin.rightAlex.text()
        self.setting_values_dict['leftFRET'] = self.settWin.leftFRET.text()
        self.setting_values_dict['rightFRET'] = self.settWin.rightFRET.text()
        self.setting_values_dict['leftdT'] = self.settWin.leftdT.text()
        self.setting_values_dict['rightdT'] = self.settWin.rightdT.text()
        self.setting_values_dict['leftE'] = self.settWin.leftE.text()
        self.setting_values_dict['rightE'] = self.settWin.rightE.text()
        self.setting_values_dict['leftNG'] = self.settWin.leftNG.text()
        self.setting_values_dict['rightNG'] = self.settWin.rightNG.text()
        self.setting_values_dict['leftNR'] = self.settWin.leftNR.text()
        self.setting_values_dict['rightNR'] = self.settWin.rightNR.text()
        self.setting_values_dict['leftTau'] = self.settWin.leftTau.text()
        self.setting_values_dict['rightTau'] = self.settWin.rightTau.text()
        self.setting_values_dict['leftTau2'] = self.settWin.leftTau2.text()
        self.setting_values_dict['rightTau2'] = self.settWin.rightTau2.text()
        self.setting_values_dict['leftTB'] = self.settWin.leftTB.text()
        self.setting_values_dict['rightTB'] = self.settWin.rightTB.text()
        self.setting_values_dict['leftS'] = self.settWin.leftS.text()
        self.setting_values_dict['rightS'] = self.settWin.rightS.text()

        self.setting_values_dict['leftSGSR'] = self.settWin.leftSGSR.text()
        self.setting_values_dict['rightSGSR'] = self.settWin.rightSGSR.text()
        self.setting_values_dict['leftN'] = self.settWin.leftN.text()
        self.setting_values_dict['rightN'] = self.settWin.rightN.text()
        self.setting_values_dict['leftrRR'] = self.settWin.leftrRR.text()
        self.setting_values_dict['rightrRR'] = self.settWin.rightrRR.text()
        self.setting_values_dict['leftrGG'] = self.settWin.leftrGG.text()
        self.setting_values_dict['rightrGG'] = self.settWin.rightrGG.text()
        self.setting_values_dict['leftNGR'] = self.settWin.leftNGR.text()
        self.setting_values_dict['leftBr'] = self.settWin.leftBr.text()
        self.setting_values_dict['rightBr'] = self.settWin.rightBr.text()

        self.setting_values_dict['gamma'] = self.settWin.gamma.text()
        self.setting_values_dict['alpha'] = self.settWin.alpha.text()
        self.setting_values_dict['beta'] = self.settWin.beta.text()

        self.setting_values_dict['delta'] = self.settWin.delta.text()

        self.setting_values_dict['aveBG'] = self.settWin.aveBG.text()
        self.setting_values_dict['aveBR'] = self.settWin.aveBR.text()
        self.setting_values_dict['aveBR0'] = self.settWin.aveBR0.text()

        self.setting_values_dict['gGG'] = self.settWin.gGG.text()
        self.setting_values_dict['gRR'] = self.settWin.gRR.text()




    def openFolderSlot(self):
        """
        Slot for opening and assigning data to the main variables.
        All file handling takes place here
        """
        self.fileList = list()
        self.dataDF = dict()
        self.keys = list()
        keyword = 'BData'

        df_columns = ["NN", "NG", "NGII", "NGT", "NR", "NRII", "NRT", "NR0", "NR0II", "NR0T", "BGII", "BGT", "BRII", "BRT",
              "BR0II", "BR0T", "TB", "FRET2CDE", "Alex2CDE", "dTGRTR0", "TauII","TauT", "Tau2II", "Tau2T", "temp"]


        #Open folder directory dialog to select the folder
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")

        # First get all files that contain BData (ignoring the suffix)
        for root, dirs, files in os.walk(str(folder)):
            for file in files:
                if keyword in file:
                    self.fileList.append(file)

        fileList = list(set(self.fileList))

        # Check of there are multiple occurances of files containing BData
        # If only one take it as the proper keyword --> Only one BData file per folder
        # If not trigger QDialog and let user decide what to take
        if len(fileList) == 1:
            keyword = fileList[0]
        elif len(fileList) > 1:
            self.User_Select_Bdata = Bdata_selection(Bdata_files=fileList)
            self.User_Select_Bdata.exec_()
            keyword = self.User_Select_Bdata.Bdata_file_out

        if not keyword:
            return


        self.fileDict = {}
        for root, dirs, files in os.walk(str(folder)):
            dirs.sort()  # Have to sort the dirs - otherwise the fileList is in arbitrary order
            for file in files:
                if keyword == file:
                    self.fileList.append(os.path.join(root, file))

                    self.fileDict[os.path.basename(root)] = self.fileList
                # self.folderName = np.append(self.folderName,os.path.basename(root))
            self.fileList = []
        del self.fileList


        # if the file dictionary is empty return -> no folder selected
        if not bool(self.fileDict) and not os.path.isdir(folder):
            return
        # wrong folder selected
        elif not bool(self.fileDict) and os.path.isdir(folder):
            self.settWin.setDisabled(True)
            self.msg.setIcon(self.crit_icon)
            self.msg.setText("The selected folder does not contain the expected elements")
            self.msg.setInformativeText('Please select an other folder')
            self.msg.exec()
            return

        if len(self.fileDict) > 0:
            # Enable the setting window and save data buttons if data is there
            self.settWin.setDisabled(False)
            self.leftExtractButton.setDisabled(False)
            self.rightExtractButton.setDisabled(False)
            #self.heatmapButton.setDisabled(False)
            self.data_available = True

            # init empty for append method
            self.dataList = np.empty((0, 25), int)

            # self.dataDict = defaultdict(list)
            dt = np.dtype('d')
            for key, values in self.fileDict.items():
                for fileName in values:
                    with Path(fileName).open('rb') as f:
                        fsz = os.fstat(f.fileno()).st_size
                        py_out_P = np.load(f, allow_pickle=True)
                        while f.tell() < fsz:
                            py_out_P = np.vstack((py_out_P, np.load(f, allow_pickle=True)))

                    self.dataList = np.append(self.dataList, py_out_P, axis=0)

                self.dataDF[key] = pd.DataFrame(self.dataList, columns=df_columns)
                self.keys.append(key)
                self.dataList = np.empty((0, 25), int)


            self.filePath = list(self.fileDict.keys())[0]
            self.statusbar.showMessage(str(self.filePath))

            self.wellSlider.setSliderPosition(0)
            self.sliderVal = 0
            # self.wellSlider.setMaximum(len(self.fileList)-1)
            self.wellSlider.setMaximum(len(self.fileDict.keys())-1)
            self.updateAllGraph(0)
            # initiate right graph
            #self.heatmapPlot()



    def sliderChange(self, val):
        """
        Callback function for change in slider value

        Args:
            val (int): Integer value of the updated slider position
        """
        try:
            self.sliderVal = val
            self.updateLeftGraph()


        except(IndexError, AttributeError):

            if self.sliderVal != 0:
                self.msg.setIcon(self.crit_icon)
                self.msg.setText("Please input your data")
                #self.msg.setInformativeText('Line 367')
                self.msg.exec()
                self.sliderVal = 0
                self.wellSlider.setSliderPosition(0)
                return
            else:
                pass

        except ValueError:

            if self.sliderVal != 0:
                self.msg.setIcon(self.crit_icon)
                self.msg.setText("The value is out of range")
                self.msg.setInformativeText('Please input an other')
                self.msg.exec()
                self.sliderVal = 0
                self.wellSlider.setSliderPosition(0)
                return
            else:
                pass

    def updateAllGraph(self,val):
        """
        General function for updating parameters of the current slider position

        Args:
            val (int): Integer value of the slider position
        """

        self.calculationFunc(self.sliderVal)
        self.leftComboBoxSlot(self.leftComboBox.currentIndex())
        self.heatmapPlot()

    def updateLeftGraph(self):

        """
        function to update only the left graph if the slider changed

        """
        self.calculationFunc(self.sliderVal)
        self.leftComboBoxSlot(self.leftComboBox.currentIndex())


    def heatmapPlot(self):
        """
        Function to update right hand plot (River plot)
        """


        self.hE_np = np.zeros((len(self.hE), len(self.keys)))  # E-histogram values
        self.hS_np = np.zeros((len(self.hS), len(self.keys)))  # S-histogram values
        self.hN_np = np.zeros((1, len(self.keys)))  # Number of molecules
        self.hTau_np = np.zeros((len(self.hTau), len(self.keys)))  # Tau(D(A))
        self.hTau2_np = np.zeros((len(self.hTau2), len(self.keys)))  # Tau(A)
        self.hrGG_np = np.zeros((len(self.hrGG), len(self.keys)))  # hrGG
        self.hrRR_np = np.zeros((len(self.hrRR), len(self.keys)))  # hrRR

        contour_levels = 30

        for i in np.arange(len(self.keys)):
            # calc all values of all values
            self.calculationFunc(i)
            # normalized values
            self.hE_np[:, i] = self.hE / sum(self.hE)
            # hS_np[:,i] = self.hS/sum(self.hS)
            self.hS_np[:, i] = self.hS
            self.hN_np[:, i] = sum(self.hE)
            self.hTau_np[:, i] = self.hTau
            self.hTau2_np[:, i] = self.hTau2
            self.hrGG_np[:, i] = self.hrGG
            self.hrRR_np[:, i] = self.hrRR

        if self.rightComboBox.currentIndex() == 0:
            self.rightGraph.canvas.ax.clear()

            '''cs = self.rightGraph.canvas.ax.contourf(self.edges, self.keys, self.hE_np.T,
                                                    locator=ticker.MaxNLocator(), cmap="jet")'''
            cs = self.rightGraph.canvas.ax.contourf(self.edges + self.BinSize, self.keys, self.hE_np.T,
                                                    levels=contour_levels, cmap="jet")


            #self.rightGraph.canvas.ax.plot([-0.1+self.BinOffset,1.1+self.BinOffset], [self.sliderVal,self.sliderVal])
            #self.rightGraph.canvas.ax.set_yticks()
            self.rightGraph.canvas.ax.yaxis.set_major_locator(ticker.MaxNLocator())
            self.rightGraph.canvas.ax.invert_yaxis()
            self.rightGraph.canvas.ax.set_xlabel("E")
            self.rightGraph.canvas.ax.set_ylabel("Well number")
            self.rightGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
            self.rightGraph.canvas.fig.tight_layout()
            self.rightGraph.canvas.draw()

        elif self.rightComboBox.currentIndex() == 1:
            self.rightGraph.canvas.ax.clear()
            self.rightGraph.canvas.ax.contourf(self.edges + self.BinSize, self.keys, self.hS_np.T, levels=contour_levels,
                                               cmap="jet")
            # self.rightGraph.canvas.ax.plot([-0.1+self.BinOffset,1.1+self.BinOffset], [self.sliderVal,self.sliderVal])
            self.rightGraph.canvas.ax.yaxis.set_major_locator(ticker.MaxNLocator())
            self.rightGraph.canvas.ax.invert_yaxis()
            self.rightGraph.canvas.ax.set_xlabel("S")
            self.rightGraph.canvas.ax.set_ylabel("Well number")
            self.rightGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
            self.rightGraph.canvas.fig.tight_layout()
            self.rightGraph.canvas.draw()

        elif self.rightComboBox.currentIndex() == 2:
            # Number of molecules in each well
            self.rightGraph.canvas.ax.clear()
            self.rightGraph.canvas.ax.scatter(self.hN_np, self.keys)
            # self.rightGraph.canvas.ax.plot([-0.1+self.BinOffset,1.1+self.BinOffset], [self.sliderVal,self.sliderVal])
            self.rightGraph.canvas.ax.yaxis.set_major_locator(ticker.MaxNLocator())
            self.rightGraph.canvas.ax.invert_yaxis()
            self.rightGraph.canvas.ax.set_xlabel("N")
            self.rightGraph.canvas.ax.set_ylabel("Well number")
            self.rightGraph.canvas.ax.set_xlim([-50, max(max(max(self.hN_np)) + 100, 2000)])
            self.rightGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
            self.rightGraph.canvas.fig.tight_layout()
            self.rightGraph.canvas.draw()

        elif self.rightComboBox.currentIndex() == 3:
            # Tau(D(A)) histogram
            self.rightGraph.canvas.ax.clear()
            self.rightGraph.canvas.ax.contourf(self.edgesTau, self.keys, self.hTau_np.T, levels=contour_levels,
                                               cmap="jet")
            self.rightGraph.canvas.ax.yaxis.set_major_locator(ticker.MaxNLocator())
            self.rightGraph.canvas.ax.invert_yaxis()
            self.rightGraph.canvas.ax.set_xlabel("$tau_{D(A)}$ (ns)")
            self.rightGraph.canvas.ax.set_ylabel("Well number")
            self.rightGraph.canvas.ax.set_xlim((-0.1, 8))
            self.rightGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
            self.rightGraph.canvas.fig.tight_layout()
            self.rightGraph.canvas.draw()

        elif self.rightComboBox.currentIndex() == 4:
            # Tau(A) histogram
            self.rightGraph.canvas.ax.clear()
            self.rightGraph.canvas.ax.contourf(self.edgesTau, self.keys, self.hTau2_np.T, levels=contour_levels,
                                               cmap="jet")
            self.rightGraph.canvas.ax.yaxis.set_major_locator(ticker.MaxNLocator())
            self.rightGraph.canvas.ax.invert_yaxis()
            self.rightGraph.canvas.ax.set_xlabel("$tau_{A}$ (ns)")
            self.rightGraph.canvas.ax.set_ylabel("Well number")
            self.rightGraph.canvas.ax.set_xlim((-0.1, 8))
            self.rightGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
            self.rightGraph.canvas.fig.tight_layout()
            self.rightGraph.canvas.draw()

        elif self.rightComboBox.currentIndex() == 5:
            # rGG histogram
            self.rightGraph.canvas.ax.clear()
            self.rightGraph.canvas.ax.contourf(self.edgesrGG, self.keys, self.hrGG_np.T, levels=contour_levels,
                                               cmap="jet")
            self.rightGraph.canvas.ax.yaxis.set_major_locator(ticker.MaxNLocator())
            self.rightGraph.canvas.ax.invert_yaxis()
            self.rightGraph.canvas.ax.set_xlabel("$r_{GG}$")
            self.rightGraph.canvas.ax.set_ylabel("Well number")
            self.rightGraph.canvas.ax.set_xlim((-0.6, 1.1))
            self.rightGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
            self.rightGraph.canvas.fig.tight_layout()
            self.rightGraph.canvas.draw()

        elif self.rightComboBox.currentIndex() == 6:
            # rRR histogram
            self.rightGraph.canvas.ax.clear()
            self.rightGraph.canvas.ax.contourf(self.edgesrGG, self.keys, self.hrRR_np.T, levels=contour_levels,
                                               cmap="jet")
            self.rightGraph.canvas.ax.yaxis.set_major_locator(ticker.MaxNLocator())
            self.rightGraph.canvas.ax.invert_yaxis()
            self.rightGraph.canvas.ax.set_xlabel("$r_{RR}$")
            self.rightGraph.canvas.ax.set_ylabel("Well number")
            self.rightGraph.canvas.ax.set_xlim((-0.6, 1.1))
            self.rightGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
            self.rightGraph.canvas.fig.tight_layout()
            self.rightGraph.canvas.draw()

        #except AttributeError:
        #    print("No data available")

    def grep_settings(self):

        self.aveBG = float(self.settWin.aveBG.text())
        self.aveBR = float(self.settWin.aveBR.text())
        self.aveBR0 = float(self.settWin.aveBR0.text())

        self.alpha = float(self.settWin.alpha.text())

        self.gamma = float(self.settWin.gamma.text())
        self.delta = float(self.settWin.delta.text())

        self.gGG = float(self.settWin.gGG.text())
        self.gRR = float(self.settWin.gRR.text())

        self.leftdT = float(self.settWin.leftdT.text())
        self.rightdT = float(self.settWin.rightdT.text())

        self.pol_set = self.settWin.polBox.currentText()

        try:
            self.beta = float(self.settWin.beta.text())
            self.recent_bata = self.beta #most recent input that throwed no error
        except ValueError:
            self.beta = self.recent_bata #reset beta to its last functional value
            self.msg.setIcon(self.crit_icon)
            self.msg.setText("The value is out of range")
            self.msg.setInformativeText('Please only input Int./Float for the Beta Parameter')
            self.msg.exec()
            return


        self.leftNR0 = float(self.settWin.leftNR0.text())
        self.rightNR0 = float(self.settWin.rightNR0.text())
        self.leftNR = float(self.settWin.leftNR.text())
        self.rightNR = float(self.settWin.rightNR.text())
        self.leftNG = float(self.settWin.leftNG.text())
        self.rightNG = float(self.settWin.rightNG.text())
        self.leftTB = float(self.settWin.leftTB.text())
        self.rightTB = float(self.settWin.rightTB.text())
        self.leftAlex = float(self.settWin.leftAlex.text())
        self.rightAlex = float(self.settWin.rightAlex.text())
        self.leftFRET = float(self.settWin.leftFRET.text())
        self.rightFRET = float(self.settWin.rightFRET.text())
        self.leftTau = float(self.settWin.leftTau.text())
        self.rightTau = float(self.settWin.rightTau.text())
        self.leftTau2 = float(self.settWin.leftTau2.text())
        self.rightTau2 = float(self.settWin.rightTau2.text())

        self.leftS = float(self.settWin.leftS.text())
        self.rightS = float(self.settWin.rightS.text())

        self.BinSize = float(self.settWin.BinSize.text())
        self.BinOffset = float(self.settWin.BinOffset.text())

        self.l1 = float(self.settWin.l1.text())
        self.l2 = float(self.settWin.l2.text())

    def calculationFunc(self,val):
        """
        Main calculation function which gives all the parameter values

        Args:
            val (int): Current slider position
        """

        # get all settings from set window
        self.grep_settings()

        self.Etot = []
        self.Stot = []
        self.Tautot = []
        self.Tau2tot = []
        self.FRET2CDEtot = []
        self.rGGtot = []
        self.rRRtot = []
        self.fLength = len(self.dataDF[self.keys[val]])



        self.Data_c = self.dataDF[self.keys[val]]

        mask_1 = ((self.leftdT <= (self.Data_c["dTGRTR0"])) & ((self.Data_c["dTGRTR0"]) <= self.rightdT) &
                  (float(self.settWin.leftNR0.text()) <= self.Data_c["NR0"]) & (self.Data_c["NR0"] <= float(self.settWin.rightNR0.text())) &
                  (float(self.settWin.leftNR.text()) <= self.Data_c["NR"]) & (self.Data_c["NR"] <= float(self.settWin.rightNR.text())) &
                  (float(self.settWin.leftNG.text()) <= self.Data_c["NG"]) & (self.Data_c["NG"] <= float(self.settWin.rightNG.text())) &
                  (float(self.settWin.leftTB.text()) <= abs(self.Data_c["TB"])) & (abs(self.Data_c["TB"]) <= float(self.settWin.rightTB.text())) &
                  (float(self.settWin.leftAlex.text()) <= self.Data_c["Alex2CDE"]) & (self.Data_c["Alex2CDE"] <= float(self.settWin.rightAlex.text())) &
                  (float(self.settWin.leftFRET.text()) <= self.Data_c["FRET2CDE"]) & (self.Data_c["FRET2CDE"] <= float(self.settWin.rightFRET.text())))


        # self.Data_c = self.dataList[val][:, mask_1]
        self.Data_c = self.Data_c[mask_1]


        self.BG = self.Data_c["BGII"] + self.Data_c["BGT"]
        self.BR = self.Data_c["BGII"] + self.Data_c["BRT"]
        self.BR0 = self.Data_c["BR0II"] + self.Data_c["BR0T"]

        self.NR_Red = self.Data_c["NR0"]/(self.Data_c["NR"]+self.Data_c["NR0"]+self.Data_c["NG"])

        if self.aveBG != 0:

            self.FG = self.Data_c["NG"]-self.aveBG*self.Data_c["TB"]*1000
        else:
            self.FG = self.Data_c["NG"]-self.BG*self.Data_c["TB"]

        if self.aveBR != 0:

            self.FR = self.Data_c["NR"]-self.aveBR*self.Data_c["TB"]*1000
        else:
            self.FR = self.Data_c["NR"]-self.BR*self.Data_c["TB"]

        if self.aveBR0 != 0:

            self.FR0 = self.Data_c["NR0"]-self.aveBR0*self.Data_c["TB"]*1000
        else:
            self.FR0 = self.Data_c["NR0"]-self.BR0*self.Data_c["TB"]

        self.FGII = self.Data_c["NGII"]-self.Data_c["BGII"]*self.Data_c["TB"]
        self.FGT = self.Data_c["NGT"]-self.Data_c["BGT"]*self.Data_c["TB"]
        self.FRII = self.Data_c["NRII"]-self.Data_c["BRII"]*self.Data_c["TB"]
        self.FRT = self.Data_c["NRT"]-self.Data_c["BRT"]*self.Data_c["TB"]
        self.FR0II = self.Data_c["NR0II"]-self.Data_c["BR0II"]*self.Data_c["TB"]
        self.FR0T = self.Data_c["NR0T"]-self.Data_c["BR0T"]*self.Data_c["TB"]

        self.N = self.Data_c["NR0"]+self.Data_c["NG"]+self.Data_c["NR"]

        self.Br = (self.Data_c["NG"]+self.Data_c["NR"])/self.Data_c["TB"]/1000

        self.E = (self.FR-self.alpha*self.FR0-self.beta*self.FG)/(self.FR-self.alpha*self.FR0-self.beta*self.FG+self.gamma*self.FG)
        self.S = (self.FR-self.alpha*self.FR0-self.beta*self.FG+self.gamma*self.FG) / \
                 (self.FR-self.alpha*self.FR0-self.beta*self.FG+self.gamma*self.FG+self.FR0/self.delta)

        # Todo: Calc Tau and Tau2 as "Tau Combined" per r g --> Clear double var part for taus if it works as intendet
        # " get l1 and l2
        # if user combined pol:
        # tau = formular with *gGG*, l1, l2
        # tau2 = formular with *gRR*, l1, l2
        # elif user 50/50: Add taus (both pol) / 2
        # tau =
        # tau2 =
        # elif user Tau part 1:
        # tau = tauII
        # tau2 = tau2II
        # elif user Tau part 2:
        # tau = tauT
        # tau2 = tau2T
        #
        # from Andreas formular "

        if self.pol_set == 'Combined Polarization':
            self.tauD = ((1-3 * self.l2) * self.gGG) / ((1-3 * self.l2) * self.gGG + (2-3 * self.l1)) * self.Data_c["TauII"]\
                        + (2-3 * self.l1) / ((1-3 * self.l2) * self.gGG + (2-3 * self.l1)) * self.Data_c["TauT"]


            self.tauA = ((1-3 * self.l2) * self.gRR) / ((1-3 * self.l2) * self.gRR + (2-3 * self.l1)) * self.Data_c["Tau2II"]\
                        + (2-3 * self.l1) / ((1-3 * self.l2) * self.gRR + (2-3 * self.l1)) * self.Data_c["Tau2T"]

            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)


        elif self.pol_set == 'Combined 50/50':
            self.tauD = (self.Data_c["NGII"]*self.Data_c["TauII"] + self.Data_c["NGT"]*self.Data_c["TauT"])/\
                        (self.Data_c["NGII"]+self.Data_c["NGT"])
            self.tauA = (self.Data_c["NGII"]*self.Data_c["Tau2II"] + self.Data_c["NGT"]*self.Data_c["Tau2T"])/\
                        (self.Data_c["NGII"]+self.Data_c["NGT"])


            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)

        elif self.pol_set == 'Tau part 1':
            self.tauD = self.Data_c["TauII"]
            self.tauA = self.Data_c["Tau2II"]

            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)

        elif self.pol_set == 'Tau part 2':
            self.tauD = self.Data_c["TauT"]
            self.tauA = self.Data_c["Tau2T"]

            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)

        self.rGG = (self.gGG*self.FGII-self.FGT)/(self.gGG*self.FGII+2*self.FGT)
        self.rRR = (self.gRR*self.FR0II-self.FR0T)/(self.gRR*self.FR0II+2*self.FR0T)

        self.rRR[np.isnan(self.rRR)] = 4.9

        self.NGR = self.Data_c["NG"]+self.Data_c["NR"]

        self.ratioSGSR = np.log10(self.Data_c["NG"]/self.Data_c["NR"])

        self.edges = np.arange(-0.1+self.BinOffset, 1.1+self.BinOffset, self.BinSize)
        self.edgesTau = np.arange(-0.1+self.BinOffset, 10+self.BinOffset, self.BinSize)
        self.edgesrGG = np.arange(-0.6+self.BinOffset, 1.1+self.BinOffset, self.BinSize)



        self.mask = ((float(self.settWin.leftSGSR.text()) < self.ratioSGSR) & (self.ratioSGSR < float(self.settWin.rightSGSR.text())) & (float(self.settWin.leftNGR.text()) < self.NGR) & (self.NGR < float(self.settWin.rightNGR.text()))  & (float(self.settWin.leftBr.text()) < self.Br) & (self.Br < float(self.settWin.rightBr.text()))
                     & (float(self.settWin.leftN.text()) < self.N) & (self.N < float(self.settWin.rightN.text())) & (float(self.settWin.leftS.text()) < self.S) & (self.S < float(self.settWin.rightS.text())) & (float(self.settWin.leftE.text()) < self.E) & (self.E < float(self.settWin.rightE.text())) & (float(self.settWin.leftrGG.text()) < self.rGG) & (self.rGG < float(self.settWin.rightrGG.text()))
                     & (float(self.settWin.leftrRR.text()) < self.rRR) & (self.rRR < float(self.settWin.rightrRR.text()))
                     & (self.leftTau <= self.Data_c["Tau"]) & (self.Data_c["Tau"] <= self.rightTau) &
                       (self.leftTau2 <= self.Data_c["Tau2"]) & (self.Data_c["Tau2"] <= self.rightTau2))


        self.E = self.E[self.mask]
        self.S = self.S[self.mask]
        self.Tau = self.Data_c["Tau"][self.mask]
        self.Tau2 = self.Data_c["Tau2"][self.mask]
        self.FRET2CDE = self.Data_c["FRET2CDE"][self.mask]
        [hEnew, I] = histc(self.E, self.edges)
        [hSnew, I] = histc(self.S, self.edges)
        [hTaunew, I] = histc(self.Tau, self.edgesTau)
        [hTau2new, I] = histc(self.Tau2, self.edgesTau)
        [hrGGnew, I] = histc(self.rGG[self.mask], self.edgesrGG)
        [hrRRnew, I] = histc(self.rRR[self.mask], self.edgesrGG)


        self.hE = np.zeros(len(hEnew))
        self.hS = np.zeros(len(hSnew))
        self.hTau = np.zeros(len(hTaunew))
        self.hTau2 = np.zeros(len(hTau2new))
        self.hrGG = np.zeros(len(hrGGnew))
        self.hrRR = np.zeros(len(hrRRnew))


        self.Etot.extend(self.E)
        self.Stot.extend(self.S)
        self.Tautot.extend(self.Tau)
        self.Tau2tot.extend(self.Tau2)
        self.FRET2CDEtot.extend(self.FRET2CDE)
        self.rGGtot.extend(self.rGG[self.mask])
        self.rRRtot.extend(self.rRR[self.mask])

        self.hE = self.hE + hEnew
        self.hS = self.hS + hSnew
        self.hTau = self.hTau + hTaunew
        self.hTau2 = self.hTau2 + hTau2new
        self.hrGG = self.hrGG + hrGGnew
        self.hrRR = self.hrRR + hrRRnew


        # [self.hEnew, I] = histc(self.E, self.edges)



    def rangeStateChangeSlot(self):
        """
        Slot for updating UI for range plotting
        """
        if self.rangeCheck.isChecked():
            self.rangeText.show()
            self.rangeLabel.show()
            self.plotRangeButton.show()
            self.leftComboBox.setDisabled(True) # disable because only one plot optionb for range slot
        else:
            self.rangeText.hide()
            self.rangeLabel.hide()
            self.plotRangeButton.hide()
            self.leftComboBox.setDisabled(False) # enable when range is unused

            # to not crash if no data is available
            try:
                self.updateLeftGraph()
            except AttributeError:
                return

    def plotRangeSlot(self):
        """
        Plotting function to generate cityscape of the selected ranges.

        Ranges are extracted which have ":" between them.
        Ex: A01:B01 extracts all the datasets from A01 to B01 in the order

        Individual datasets are seperated by ","
        Ex: A01,B01 extracts only A01 and B01 datasets
        """


        try:

            wellRanges  = [i.split(":") for i in self.rangeText.text().split(",")]

            indicesRange = []

            try:
                for value in wellRanges:
                    value.sort() # order does not matter any more
                    if len(value) > 1:
                        indicesRange.append([self.keys.index(i) for i in value])
                    else:
                        indicesRange.append([self.keys.index(value[0])])
            except ValueError:
                self.settWin.setDisabled(True)
                self.msg.setIcon(self.crit_icon)
                self.msg.setText("The well you entered does not exist")
                self.msg.setInformativeText('Existing wells in dataset:\n'
                                            f'{self.keys}')
                self.msg.exec()
                return

            # plot range on left graph
            self.leftGraph.canvas.ax.clear()
            folderIndices = []
            for val in indicesRange:
                if val:
                    if len(val) > 1:
                        for i in np.arange(val[0],val[-1]+1):

                            self.calculationFunc(i)
                            [hEnew, I] = histc(self.E, self.edges)
                            norm_hEnew = hEnew/np.trapz(hEnew)

                            self.leftGraph.canvas.ax.step(self.edges, norm_hEnew)
                            self.leftGraph.canvas.ax.set_xlabel("E")
                            self.leftGraph.canvas.ax.set_ylabel("Counts")
                            self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                            self.leftGraph.canvas.fig.tight_layout()
                            folderIndices.append(i)
                    else:
                        self.calculationFunc(val[0])
                        [hEnew, I] = histc(self.E, self.edges)
                        area = np.trapz(hEnew)
                        norm_hEnew = hEnew/area
                        self.leftGraph.canvas.ax.step(self.edges, norm_hEnew)
                        self.leftGraph.canvas.ax.set_xlabel("E")
                        self.leftGraph.canvas.ax.set_ylabel("Counts")
                        self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                        self.leftGraph.canvas.fig.tight_layout()
                        folderIndices.append(val[0])

            legend_captions = [self.keys[i] for i in folderIndices]
            self.leftGraph.canvas.ax.legend(legend_captions, fontsize = 6, ncol=2)
            self.leftGraph.canvas.draw()

        except AttributeError:
            print("Data not loaded")

    def leftComboBoxSlot(self, index):
        """
        Generate plots for the appropriate selection in the left combo box

        Args:
            index (int): Index of the combo box selection
        """


        if (index == 0):
            #E- histogram
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.bar(self.edges, self.hE, width=self.BinSize, color='grey', align='edge')
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_ylabel("Counts")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError as e:
                print(e)
        elif (index == 1):
            #S vs. E scatter plot
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.Stot, s=1)
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_ylabel("S")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")
        elif (index == 2):
            #E vs. Tau(D(A)) scatter plot
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Tautot, self.Etot, s=1)
                self.leftGraph.canvas.ax.set_xlabel("$tau_{D(A)}$")
                self.leftGraph.canvas.ax.set_ylabel("E")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_ylim((-0.1, 1.1))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 6))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 3):
            #Tau(D(A))/Tau(D(0)) vs. E scatter plot
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, np.array(self.Tautot)/float(self.settWin.tauD0.text()), s=1)
                self.leftGraph.canvas.ax.set_ylabel("$tau_{D(A)}/tau_{D(0)}$")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_ylim((-0.1, 1.1))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 4):
            #E vs. Tau(A) scatter plot
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Tau2tot,self.Etot, s=1)
                self.leftGraph.canvas.ax.set_ylabel("E")
                self.leftGraph.canvas.ax.set_xlabel("$tau_{A} (ns)$")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_ylim((-0.1, 1.1))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 8))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 5):
            #FRET-2CDE vs. E scatter plot
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.FRET2CDE, s=1)
                self.leftGraph.canvas.ax.set_ylabel("FRET-2CDE")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_ylim((0, 100))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 6):
            #rGG vs. E scatter plot
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.rGGtot, s=1)
                self.leftGraph.canvas.ax.set_ylabel("$r_{GG}$")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_ylim((-0.3, 0.6))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 7):
            #rRR vs. E scatter plot
            try:
                self.calculationFunc(self.sliderVal)
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.rRRtot, s=1)
                self.leftGraph.canvas.ax.set_ylabel("$r_{RR}$")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title(self.keys[self.sliderVal])
                self.leftGraph.canvas.ax.set_ylim((-0.3, 0.6))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")


    def leftExtractSlot(self):
        """
        Extract data displayed on the left hand side plot into a csv file
        """


        # when button pressed --> Open save Tickwindow dialog
        self.Tickwindow_left.exec() # open tickwindow

        try:
            checklist = self.Tickwindow_left.checklist # get output dict as var. checklist
        except AttributeError:
            return



        # user gave input (button pressed and ticks set)
        if self.Tickwindow_left.input_given and any(checklist.values()):

            # extract current settings from settings window
            self.extract_setting_values()

            # input in checklist given by user --> Open folder dialog

            folder = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Directory")

            if 'folder' not in locals():
                return


            # Internal order
            #1. Save Current -> Check for selected diagram type -> Save x/y + Independent check for RAW and .png save
            #2. Save All --> Check for selected diagram type -> Save all x/y

            # routines to save the current view
            if checklist['Save Current']:

                # Starting by defining general file path for current csv saves depending on slider and
                # combobox values

                filepath = os.path.join(folder, str(self.keys[self.sliderVal]) + '_' +
                                        self.leftComboBox.currentText().replace(' ','_').replace('/','_')+'.csv')
                #save current settings
                try:
                    if len(self.Tickwindow_left.settings_file_textbox.text()) == 0:
                        settings_file = os.path.join(folder, str(self.keys[self.sliderVal]) + '_' +
                                                     self.leftComboBox.currentText().replace(' ', '_').replace('/', '_')
                                                     + '_settings_file.csv')
                    else:
                        settings_file = os.path.join(folder, self.Tickwindow_left.settings_file_textbox.text() + '.csv')
                except NameError:
                    settings_file = os.path.join(folder, str(self.keys[self.sliderVal]) + '_' +
                                                 self.leftComboBox.currentText().replace(' ','_').replace('/','_')
                                                 + '_settings_file.csv')


                #dict to frame convert for single line csv save
                pd.DataFrame([self.setting_values_dict]).to_csv(settings_file, index=False)



                # if current view is E Histogram
                if self.leftComboBox.currentIndex() == 0:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/E'] + self.edges.tolist())
                        writer.writerow([self.keys[self.sliderVal]] + ['y/Counts'] + self.hE.tolist())


                # if current view is S vs. E
                elif self.leftComboBox.currentIndex() == 1:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/E'] + self.Etot)
                        writer.writerow([self.keys[self.sliderVal]] + ['y/S'] + self.Stot)

                # if current view is E vs. Tau(D(A))
                elif self.leftComboBox.currentIndex() == 2:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/Tau(D(A))'] + self.Tautot)
                        writer.writerow([self.keys[self.sliderVal]] + ['y/E'] + self.Etot)

                # if current view is Tau(D(A)/D0)) vs. E
                elif self.leftComboBox.currentIndex() == 3:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/E'] + self.Etot)
                        writer.writerow([self.keys[self.sliderVal]] + ['y/Tau(D(A)/D0))'] +
                                        (np.array(self.Tautot)/float(self.settWin.tauD0.text())).tolist())

                # if current view is E vs. Tau(A)
                elif self.leftComboBox.currentIndex() == 4:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/Tau(A)'] + self.Tau2tot)
                        writer.writerow([self.keys[self.sliderVal]] + ['y/E'] + self.Etot)

                # if current view is FRET-2CDE vs. E scatter plot
                elif self.leftComboBox.currentIndex() == 5:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/E'] + self.Etot)
                        writer.writerow([self.keys[self.sliderVal]] + ['y/FRET-2CDE'] + self.FRET2CDE.tolist())

                # if current view is rGG vs. E scatter plot
                elif self.leftComboBox.currentIndex() == 6:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/E'] + self.Etot)
                        writer.writerow([self.keys[self.sliderVal]] + ['y/rGG'] + self.rGGtot)

                # if current view is rRR vs. E scatter plot
                elif self.leftComboBox.currentIndex() == 7:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow([self.keys[self.sliderVal]] + ['x/E'] + self.Etot)
                        writer.writerow([self.keys[self.sliderVal]] + ['y/rRR'] + self.rRRtot)


                # save current png independent of the diagram type (its out of type if clause)
                if checklist['Save .png']:
                    png_path = os.path.join(folder, str(self.keys[self.sliderVal]) + '_' +
                                            self.leftComboBox.currentText().replace(' ','_').replace('/','_')+'.png')
                    self.leftGraph.canvas.fig.savefig(png_path)

                if checklist['Save .eps']:
                    eps_path = os.path.join(folder, str(self.keys[self.sliderVal]) + '_' +
                                            self.leftComboBox.currentText().replace(' ','_').replace('/','_')+'.eps')
                    self.leftGraph.canvas.fig.savefig(eps_path, format='eps')

                # save current raw data independent of the diagram type (its out type if clause)
                if checklist['Save RAW']:

                    self.dataDF[str(self.keys[self.sliderVal])].to_csv(folder+'/'+
                                                                       str(self.keys[self.sliderVal])+'_RAW_data.csv')

            # Save all at once
            if checklist['Save All']:

                initial_slider_val = self.sliderVal

                # define a file depending on the current combobox selection
                filepath = os.path.join(folder, 'All_' + str(self.leftComboBox.currentText().replace(' ','_')
                                                             .replace('/','_')+'.csv'))

                #save current settings
                try:
                    if len(self.Tickwindow_left.settings_file_textbox.text()) == 0:
                        settings_file = os.path.join(folder, 'All_' +
                                                     self.leftComboBox.currentText().replace(' ', '_').replace('/', '_')
                                                     + '_settings_file.csv')
                    else:
                        settings_file = os.path.join(folder,self.Tickwindow_left.settings_file_textbox.text()+'.csv')
                except NameError:
                    settings_file = os.path.join(folder, 'All_' +
                                                 self.leftComboBox.currentText().replace(' ','_').replace('/','_')
                                                 + '_settings_file.csv')

                #dict to frame convert for single line csv save
                pd.DataFrame([self.setting_values_dict]).to_csv(settings_file, index=False)

                # overwrite routine -> Writer needs to be in append mode in this case
                # this prevents it from appending to an existing csv file
                if os.path.isfile(filepath):
                    os.remove(filepath)

                for i in np.arange(len(self.keys)):
                    # calc all values of all values
                    self.calculationFunc(i)

                    # if current view is E Histogram
                    if self.leftComboBox.currentIndex() == 0:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/E'] + self.edges.tolist())
                            writer.writerow([self.keys[i]] + ['y/Counts'] + self.hE.tolist())

                    # if current view is S vs. E
                    elif self.leftComboBox.currentIndex() == 1:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/E'] + self.Etot)
                            writer.writerow([self.keys[i]] + ['y/S'] + self.Stot)

                    # if current view is E vs. Tau(D(A))
                    elif self.leftComboBox.currentIndex() == 2:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/Tau(D(A))'] + self.Tautot)
                            writer.writerow([self.keys[i]] + ['y/E'] + self.Etot)

                    # if current view is Tau(D(A)/D0)) vs. E
                    elif self.leftComboBox.currentIndex() == 3:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/E'] + self.Etot)
                            writer.writerow([self.keys[i]] + ['y/Tau(D(A)/D0))'] +
                                            (np.array(self.Tautot)/float(self.settWin.tauD0.text())).tolist())

                    # if current view is E vs. Tau(A)
                    elif self.leftComboBox.currentIndex() == 4:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/Tau(A)'] + self.Tau2tot)
                            writer.writerow([self.keys[i]] + ['y/E'] + self.Etot)

                    # if current view is FRET-2CDE vs. E scatter plot
                    elif self.leftComboBox.currentIndex() == 5:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/E'] + self.Etot)
                            writer.writerow([self.keys[i]] + ['y/FRET-2CDE'] + self.FRET2CDE.tolist())

                    # if current view is rGG vs. E scatter plot
                    elif self.leftComboBox.currentIndex() == 6:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/E'] + self.Etot)
                            writer.writerow([self.keys[i]] + ['y/rGG'] + self.rGGtot)

                    # if current view is rRR vs. E scatter plot
                    elif self.leftComboBox.currentIndex() == 7:

                        with open(filepath, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([self.keys[i]] + ['x/E'] + self.Etot)
                            writer.writerow([self.keys[i]] + ['y/rRR'] + self.rRRtot)

                    # reset the current calculation parameters to the setted slider val. in order to prevent
                    # unexpected app behaviour
                    self.calculationFunc(self.sliderVal)


                # Raw data save independent of selected diagram type
                if checklist['Save RAW']:

                    # create new folder since multiple files are created
                    try:
                        raw_sub_folder = os.path.join(folder ,'RAW_Data')
                        os.mkdir(raw_sub_folder)
                    except FileExistsError:
                        raw_sub_folder = os.path.join(folder, str(folder ,'RAW_Data'))

                    for i in np.arange(len(self.keys)):
                        # save all raw data values into independent csv files within the newly created subfolder
                        self.dataDF[str(self.keys[i])].to_csv(raw_sub_folder+'/' +
                                                              str(self.keys[i])+'_RAW_data.csv')

                if checklist['Save .png']:

                    try:
                        png_sub_folder = os.path.join(folder, str(self.leftComboBox.currentText().replace(' ','_'))
                                                      .replace('/','_')+'_Figures')
                        os.mkdir(png_sub_folder)
                    except FileExistsError:
                        png_sub_folder = os.path.join(folder, str(self.leftComboBox.currentText().replace(' ','_'))
                                                      .replace('/','_')+'_Figures')


                    initial_slider_val = self.sliderVal
                    # iteratively create all the figures
                    for i in np.arange(len(self.keys)):
                        # calc all values of all values
                        self.calculationFunc(i)
                        # creating graphs for each well
                        # tricking the function to think slider has changed
                        # internal slider val will be resetted after this loop
                        self.sliderVal = i
                        self.leftComboBoxSlot(self.leftComboBox.currentIndex())

                        # saving .png in new folders
                        png_path = os.path.join(png_sub_folder, str(self.keys[i]) + '_' +
                                                self.leftComboBox.currentText().replace(' ','_')
                                                .replace('/','_')+'.png')

                        self.leftGraph.canvas.fig.savefig(png_path, format='png')

                if checklist['Save .eps']:
                    try:
                        eps_sub_folder = os.path.join(folder, str(self.leftComboBox.currentText().replace(' ','_'))
                                                      .replace('/','_')+'_Figures_eps')
                        os.mkdir(eps_sub_folder)
                    except FileExistsError:
                        eps_sub_folder = os.path.join(folder, str(self.leftComboBox.currentText().replace(' ','_'))
                                                      .replace('/','_')+'_Figures_eps')



                    # iteratively create all the figures
                    for i in np.arange(len(self.keys)):
                        # calc all values of all values
                        self.calculationFunc(i)
                        # creating graphs for each well
                        # tricking the function to think slider has changed
                        # internal slider val will be resetted after this loop
                        self.sliderVal = i
                        self.leftComboBoxSlot(self.leftComboBox.currentIndex())

                        # saving .png in new folders
                        png_path = os.path.join(eps_sub_folder, str(self.keys[i]) + '_' +
                                                self.leftComboBox.currentText().replace(' ','_')
                                                .replace('/','_')+'.eps')

                        self.leftGraph.canvas.fig.savefig(png_path, format='eps')

                # resetting sliderval to its position before the saving began
                self.sliderVal = initial_slider_val
                # resetting all function values
                self.calculationFunc(self.sliderVal)
                self.updateLeftGraph()



    def rightExtractSlot(self):
        """
        Extract data from the river plot on the right into a csv file

        Currently only extract E-histogram
        """
        # when button pressed --> Open save Tickwindow dialog
        self.Tickwindow_right.exec() # open tickwindow

        try:
            checklist = self.Tickwindow_right.checklist # get output dict as var. checklist
        except AttributeError:
            return


        # extract current settings from settings window
        self.extract_setting_values()

        if self.Tickwindow_right.input_given and any(checklist.values()):
            # input in checklist given by user --> Open folder dialog

            folder = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Directory")

            if 'folder' not in locals():
                return

            if checklist['Save Data']:

                # Starting by defining general file path for current csv saves depending on slider and
                # combobox values

                filepath = os.path.join(folder,
                                        self.rightComboBox.currentText().replace(' ','_').replace('/','_')+'.csv')

                filepath_edges = os.path.join(folder,'edges_' +
                                              self.rightComboBox.currentText().replace(' ','_').replace('/','_')+'.csv')
                #save current settings
                settings_file = os.path.join(folder,
                                             self.rightComboBox.currentText().replace(' ','_').replace('/','_')
                                             + '_settings_file.csv')
                #dict to frame convert for single line csv save
                pd.DataFrame([self.setting_values_dict]).to_csv(settings_file, index=False)

                # E histogram current view
                if self.rightComboBox.currentIndex() == 0:

                    with open(filepath_edges, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['E historgram'] + ['edges'] + self.edges.tolist())
                        for well,xrow in zip(self.keys,self.hE_np.transpose()):
                            writer.writerow([well] + ['y'] + xrow.tolist())

                # S histogram current view
                elif self.rightComboBox.currentIndex() == 1:

                    with open(filepath_edges, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['S historgram'] + ['edges'] + self.edges.tolist())
                        for well, xrow in zip(self.keys,self.hS_np.transpose()):
                            writer.writerow([well] + ['y'] + xrow.tolist())

                # N - molecules current view
                elif self.rightComboBox.currentIndex() == 2:

                    print('Implement scatter save here!')

                # Tau(D(A)) current view
                elif self.rightComboBox.currentIndex() == 3:
                    with open(filepath_edges, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['Tau(D(A))'] + ['edges'] + self.edgesTau.tolist())
                        for well, xrow in zip(self.keys,self.hTau_np.transpose()):
                            writer.writerow([well] + ['y'] + xrow.tolist())

                # Tau(A) current view
                elif self.rightComboBox.currentIndex() == 4:
                    with open(filepath_edges, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['Tau(A)'] + ['edges'] + self.edgesTau.tolist())
                        for well, xrow in zip(self.keys,self.hTau2_np.transpose()):
                            writer.writerow([well] + ['y'] + xrow.tolist())

                # rGG current view
                elif self.rightComboBox.currentIndex() == 5:

                    with open(filepath_edges, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['Tau(A)'] + ['edges'] + self.edgesrGG.tolist())
                        for well, xrow in zip(self.keys,self.hrGG_np.transpose()):
                            writer.writerow([well] + ['y'] + xrow.tolist())

                # rRR current view
                elif self.rightComboBox.currentIndex() == 6:

                    with open(filepath_edges, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['Tau(A)'] + ['edges'] + self.edgesrGG.tolist())
                        for well, xrow in zip(self.keys,self.hrRR_np.transpose()):
                            writer.writerow([well] + ['y'] + xrow.tolist())

            if checklist['Save .png']:
                png_path = os.path.join(folder,
                                        self.rightComboBox.currentText().replace(' ','_').replace('/','_')+'.png')
                self.rightGraph.canvas.fig.savefig(png_path)

            if checklist['Save .eps']:
                eps_path = os.path.join(folder,
                                        self.rightComboBox.currentText().replace(' ','_').replace('/','_')+'.eps')
                self.rightGraph.canvas.fig.savefig(eps_path, format='eps')









    def ImportSettings(self):

        # get translater to set text in settings window
        _translate = QtCore.QCoreApplication.translate

        # set up custom file dialog
        dialog = QtWidgets.QFileDialog(self)
        dialog.setNameFilter(("CSV (*.csv)"))

        if dialog.exec_():
            fileName = dialog.selectedFiles()

        # return if no file is selected
        if 'fileName' not in locals():
            return

        # import csv from selected into pandas df
        settings_input = pd.read_csv(fileName[0])

        try:
            # change all the settings to values from the file
            for setting in settings_input.columns:
                getattr(self.settWin, f'{setting}') \
                    .setText(_translate("Settings", f"{str(settings_input[f'{setting}'].values[0])}"))

            # refresh current view
            self.updateAllGraph(self.sliderVal)

        except AttributeError:
            self.settWin.setDisabled(True)
            self.msg.setIcon(self.crit_icon)
            self.msg.setText("The settings file does not seem to be correctly formatted")
            self.msg.setInformativeText('Check the doc. for the correct format')
            self.msg.exec()
            return



    def extractRawDataSlot(self):
        """
        Extract raw (calculated) parameter data without any filters
        """
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        # with open('/Users/bcudevs/Python Scripts/python_scratch_folder/test_export_folder/test_export.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
        # w = csv.writer(f)
        # w.writeheader()
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass

        for key,df in self.dataDF.items():
            df.to_csv(folder+str(key)+'.csv')
            # w.writerows(self.dataDF.items())

    def dockChangedSlot(self, topLevel):
        """
        Slot to detect if settings window is docked or not

        Args:
            topLevel (bool): variable to indicate docking condition
        """
        if topLevel == True:
            self.setMinimumWidth(1037)
            self.resize(1037,600)
        else:
            self.setMinimumWidth(1037+502)

    def closeEvent(self, event):
        """
        Close windows (settings window etc.,) on the event of program closure

        """
        for i in self.addWindow:
            i.close()


class MainWindow_single_well(QtWidgets.QMainWindow, Ui_MainWindow_Single_Well):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MainWindow_single_well, self).__init__(*args, **kwargs)

        # global argument to check if data is uploaded by the user
        # is set to true in the openFolderSlot function
        self.data_available = False

        self.setupUi(self)
        self.user_warning(self)

        #Generate well ID's for easier access
        self.wellNum = []
        for num in np.arange(96):
            self.wellNum.append('ABCDEFGH'[(num) // 12] + '%02d' % ((num) % 12 + 1,))


        # add a detachable settings window to the left of the main window
        self.get_settings_window()

        # add a tickwindow
        self.Tickwindow_left = tickwindow_single_well()

        #Set toolbars under plot areas for additional tools (saving etc.,)
        NavigationToolbar.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            (None, None, None, None),
            ('Pan', 'Left button pans, Right button zooms\nx/y fixes axis, CTRL fixes aspect', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Customize', 'Edit axis, curve and image parameters', 'qt4_editor_options', 'edit_parameters'),
            ('Save', 'Save the figure', 'filesave', 'save_figure')
        )




        self.toolbarLeft = NavigationToolbar(self.leftGraph.canvas, self, coordinates=True)
        self.toolbarLeft.setMinimumHeight(20)
        self.toolbarLeft.setStyleSheet("QToolBar { border: 0px }")
        self.leftGraphLayout.addWidget(self.toolbarLeft)

        #Set shortcut and menu button connection
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openFolderSlot)


        self.actionImportSettings.triggered.connect(self.ImportSettings)
        self.actionGetSettingsBack.triggered.connect(self.get_settings_window)

        self.actionSwitchSingle.triggered.connect(self.init_switch)

        #Combobox connection
        self.leftComboBox.currentIndexChanged.connect(self.leftComboBoxSlot)

        #Extract Button connections
        self.leftExtractButton.clicked.connect(self.leftExtractSlot)

        # Disable if no data is there
        if not self.data_available:
            self.leftExtractButton.setDisabled(False)

        self.connectSettingsSlots()

    def init_switch(self):
        self.switch_window.emit()

    def get_settings_window(self):
        #Set reference for the settings window
        try:
            self.settWin.close()
        except AttributeError:
            pass

        self.addWindow = []
        self.items=QDockWidget('Settings Window',self)

        self.settWin = SettingsWindow()
        self.settWin.show()
        self.settWin.setDisabled(True)
        self.addWindow.append(self.settWin)

        self.items.setWidget(self.settWin)
        self.items.setFloating(False)

        #Dock the settings window to the left and adjust the widget area
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.items)

        # self.items.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.items.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.settWin.setMinimumWidth(502)
        self.setMinimumWidth(800+502)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)

        self.items.topLevelChanged.connect(self.dockChangedSlot)


    def connectSettingsSlots(self):
        """
        Slot or Callback connections for buttons in the GUI
        """

        self.settWin.leftNR0.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightNR0.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftAlex.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightAlex.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftFRET.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightFRET.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftdT.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightdT.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftE.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightE.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftNG.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightNG.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftNR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightNR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftTau.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightTau.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftTau2.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightTau2.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftTB.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightTB.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftS.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightS.returnPressed.connect(lambda: self.updateLeftGraph())

        self.settWin.leftSGSR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightSGSR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftN.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightN.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftrRR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightrRR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftrGG.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightrGG.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftNGR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightNGR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.leftBr.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.rightBr.returnPressed.connect(lambda: self.updateLeftGraph())

        self.settWin.gamma.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.alpha.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.beta.returnPressed.connect(lambda: self.updateLeftGraph())

        self.settWin.delta.returnPressed.connect(lambda: self.updateLeftGraph())

        self.settWin.aveBG.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.aveBR.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.aveBR0.returnPressed.connect(lambda: self.updateLeftGraph())

        self.settWin.gGG.returnPressed.connect(lambda: self.updateLeftGraph())
        self.settWin.gRR.returnPressed.connect(lambda: self.updateLeftGraph())

        self.settWin.refreshButton.clicked.connect(lambda: self.updateLeftGraph())

    def extract_setting_values(self):
        """
        function to extract current setting window values
        Returns: self.setting_values_dict -> Stores all values in dictionary

        """
        self.setting_values_dict = dict()
        self.setting_values_dict['leftNR0'] = self.settWin.leftNR0.text()
        self.setting_values_dict['rightNR0'] = self.settWin.rightNR0.text()
        self.setting_values_dict['leftAlex'] = self.settWin.leftAlex.text()
        self.setting_values_dict['rightAlex'] = self.settWin.rightAlex.text()
        self.setting_values_dict['leftFRET'] = self.settWin.leftFRET.text()
        self.setting_values_dict['rightFRET'] = self.settWin.rightFRET.text()
        self.setting_values_dict['leftdT'] = self.settWin.leftdT.text()
        self.setting_values_dict['rightdT'] = self.settWin.rightdT.text()
        self.setting_values_dict['leftE'] = self.settWin.leftE.text()
        self.setting_values_dict['rightE'] = self.settWin.rightE.text()
        self.setting_values_dict['leftNG'] = self.settWin.leftNG.text()
        self.setting_values_dict['rightNG'] = self.settWin.rightNG.text()
        self.setting_values_dict['leftNR'] = self.settWin.leftNR.text()
        self.setting_values_dict['rightNR'] = self.settWin.rightNR.text()
        self.setting_values_dict['leftTau'] = self.settWin.leftTau.text()
        self.setting_values_dict['rightTau'] = self.settWin.rightTau.text()
        self.setting_values_dict['leftTau2'] = self.settWin.leftTau2.text()
        self.setting_values_dict['rightTau2'] = self.settWin.rightTau2.text()
        self.setting_values_dict['leftTB'] = self.settWin.leftTB.text()
        self.setting_values_dict['rightTB'] = self.settWin.rightTB.text()
        self.setting_values_dict['leftS'] = self.settWin.leftS.text()
        self.setting_values_dict['rightS'] = self.settWin.rightS.text()

        self.setting_values_dict['leftSGSR'] = self.settWin.leftSGSR.text()
        self.setting_values_dict['rightSGSR'] = self.settWin.rightSGSR.text()
        self.setting_values_dict['leftN'] = self.settWin.leftN.text()
        self.setting_values_dict['rightN'] = self.settWin.rightN.text()
        self.setting_values_dict['leftrRR'] = self.settWin.leftrRR.text()
        self.setting_values_dict['rightrRR'] = self.settWin.rightrRR.text()
        self.setting_values_dict['leftrGG'] = self.settWin.leftrGG.text()
        self.setting_values_dict['rightrGG'] = self.settWin.rightrGG.text()
        self.setting_values_dict['leftNGR'] = self.settWin.leftNGR.text()
        self.setting_values_dict['leftBr'] = self.settWin.leftBr.text()
        self.setting_values_dict['rightBr'] = self.settWin.rightBr.text()

        self.setting_values_dict['gamma'] = self.settWin.gamma.text()
        self.setting_values_dict['alpha'] = self.settWin.alpha.text()
        self.setting_values_dict['beta'] = self.settWin.beta.text()

        self.setting_values_dict['delta'] = self.settWin.delta.text()

        self.setting_values_dict['aveBG'] = self.settWin.aveBG.text()
        self.setting_values_dict['aveBR'] = self.settWin.aveBR.text()
        self.setting_values_dict['aveBR0'] = self.settWin.aveBR0.text()

        self.setting_values_dict['gGG'] = self.settWin.gGG.text()
        self.setting_values_dict['gRR'] = self.settWin.gRR.text()

        self.setting_values_dict['l1'] = self.settWin.l1.text()
        self.setting_values_dict['l2'] = self.settWin.l2.text()




    def openFolderSlot(self):
        """
        Slot for opening and assigning data to the main variables.
        All file handling takes place here
        """

        self.dataDF = {}

        df_columns = ["NN", "NG", "NGII", "NGT", "NR", "NRII", "NRT", "NR0", "NR0II", "NR0T", "BGII", "BGT", "BRII",
                      "BRT","BR0II", "BR0T", "TB", "FRET2CDE", "Alex2CDE", "dTGRTR0", "TauII", "TauT", "Tau2II",
                      "Tau2T", "temp"]

        #Create a custom dialog to get a single BData file
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('Select a singe BData file')
        dialog.setNameFilter('(BData*)') # should only select a BData1.bin file
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        filename = None
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            filename = dialog.selectedFiles()[0]

        # init empty for append method
        self.dataList = np.empty((0, 25), int)

        # grap single well data
        try:
            self.single_well_data = np.fromfile(filename,dtype=np.dtype('d'))
            with Path(filename).open('rb') as f:
                py_out_P = np.load(f, allow_pickle=True)
        except AttributeError:
            return
        # reshape single well data to get the correct values for each smFRET variables
        self.dataList = np.append(self.dataList, py_out_P, axis=0)


        # store data in pandas
        self.dataDF['Well'] = pd.DataFrame(self.dataList, columns=df_columns)
        self.updateLeftGraph()
        self.settWin.setDisabled(False)



    def updateLeftGraph(self):

        """
        function to update only the left graph if the slider changed

        """
        self.calculationFunc()
        self.leftComboBoxSlot(self.leftComboBox.currentIndex())

    def grep_settings(self):

        self.aveBG = float(self.settWin.aveBG.text())
        self.aveBR = float(self.settWin.aveBR.text())
        self.aveBR0 = float(self.settWin.aveBR0.text())

        self.alpha = float(self.settWin.alpha.text())

        self.gamma = float(self.settWin.gamma.text())
        self.delta = float(self.settWin.delta.text())

        self.gGG = float(self.settWin.gGG.text())
        self.gRR = float(self.settWin.gRR.text())

        self.leftdT = float(self.settWin.leftdT.text())
        self.rightdT = float(self.settWin.rightdT.text())

        self.pol_set = self.settWin.polBox.currentText()

        try:
            self.beta = float(self.settWin.beta.text())
            self.recent_bata = self.beta #most recent input that throwed no error
        except ValueError:
            self.beta = self.recent_bata #reset beta to its last functional value
            self.msg.setIcon(self.crit_icon)
            self.msg.setText("The value is out of range")
            self.msg.setInformativeText('Please only input Int./Float for the Beta Parameter')
            self.msg.exec()
            return


        self.leftNR0 = float(self.settWin.leftNR0.text())
        self.rightNR0 = float(self.settWin.rightNR0.text())
        self.leftNR = float(self.settWin.leftNR.text())
        self.rightNR = float(self.settWin.rightNR.text())
        self.leftNG = float(self.settWin.leftNG.text())
        self.rightNG = float(self.settWin.rightNG.text())
        self.leftTB = float(self.settWin.leftTB.text())
        self.rightTB = float(self.settWin.rightTB.text())
        self.leftAlex = float(self.settWin.leftAlex.text())
        self.rightAlex = float(self.settWin.rightAlex.text())
        self.leftFRET = float(self.settWin.leftFRET.text())
        self.rightFRET = float(self.settWin.rightFRET.text())
        self.leftTau = float(self.settWin.leftTau.text())
        self.rightTau = float(self.settWin.rightTau.text())
        self.leftTau2 = float(self.settWin.leftTau2.text())
        self.rightTau2 = float(self.settWin.rightTau2.text())

        self.leftS = float(self.settWin.leftS.text())
        self.rightS = float(self.settWin.rightS.text())

        self.BinSize = float(self.settWin.BinSize.text())
        self.BinOffset = float(self.settWin.BinOffset.text())

        self.l1 = float(self.settWin.l1.text())
        self.l2 = float(self.settWin.l2.text())

    def calculationFunc(self):
        """
        Main calculation function which gives all the parameter values
        """

        # get all settings from set window
        self.grep_settings()

        self.Etot = []
        self.Stot = []
        self.Tautot = []
        self.Tau2tot = []
        self.FRET2CDEtot = []
        self.rGGtot = []
        self.rRRtot = []
        self.fLength = len(self.dataDF['Well'])



        self.Data_c = self.dataDF['Well']

        mask_1 = ((self.leftdT <= (self.Data_c["dTGRTR0"])) & ((self.Data_c["dTGRTR0"]) <= self.rightdT) &
                  (float(self.settWin.leftNR0.text()) <= self.Data_c["NR0"]) & (self.Data_c["NR0"] <= float(self.settWin.rightNR0.text())) &
                  (float(self.settWin.leftNR.text()) <= self.Data_c["NR"]) & (self.Data_c["NR"] <= float(self.settWin.rightNR.text())) &
                  (float(self.settWin.leftNG.text()) <= self.Data_c["NG"]) & (self.Data_c["NG"] <= float(self.settWin.rightNG.text())) &
                  (float(self.settWin.leftTB.text()) <= abs(self.Data_c["TB"])) & (abs(self.Data_c["TB"]) <= float(self.settWin.rightTB.text())) &
                  (float(self.settWin.leftAlex.text()) <= self.Data_c["Alex2CDE"]) & (self.Data_c["Alex2CDE"] <= float(self.settWin.rightAlex.text())) &
                  (float(self.settWin.leftFRET.text()) <= self.Data_c["FRET2CDE"]) & (self.Data_c["FRET2CDE"] <= float(self.settWin.rightFRET.text())))


        # self.Data_c = self.dataList[val][:, mask_1]
        self.Data_c = self.Data_c[mask_1]


        self.BG = self.Data_c["BGII"] + self.Data_c["BGT"]
        self.BR = self.Data_c["BGII"] + self.Data_c["BRT"]
        self.BR0 = self.Data_c["BR0II"] + self.Data_c["BR0T"]

        self.NR_Red = self.Data_c["NR0"]/(self.Data_c["NR"]+self.Data_c["NR0"]+self.Data_c["NG"])

        if self.aveBG != 0:

            self.FG = self.Data_c["NG"]-self.aveBG*self.Data_c["TB"]*1000
        else:
            self.FG = self.Data_c["NG"]-self.BG*self.Data_c["TB"]

        if self.aveBR != 0:

            self.FR = self.Data_c["NR"]-self.aveBR*self.Data_c["TB"]*1000
        else:
            self.FR = self.Data_c["NR"]-self.BR*self.Data_c["TB"]

        if self.aveBR0 != 0:

            self.FR0 = self.Data_c["NR0"]-self.aveBR0*self.Data_c["TB"]*1000
        else:
            self.FR0 = self.Data_c["NR0"]-self.BR0*self.Data_c["TB"]

        self.FGII = self.Data_c["NGII"]-self.Data_c["BGII"]*self.Data_c["TB"]
        self.FGT = self.Data_c["NGT"]-self.Data_c["BGT"]*self.Data_c["TB"]
        self.FRII = self.Data_c["NRII"]-self.Data_c["BRII"]*self.Data_c["TB"]
        self.FRT = self.Data_c["NRT"]-self.Data_c["BRT"]*self.Data_c["TB"]
        self.FR0II = self.Data_c["NR0II"]-self.Data_c["BR0II"]*self.Data_c["TB"]
        self.FR0T = self.Data_c["NR0T"]-self.Data_c["BR0T"]*self.Data_c["TB"]

        self.N = self.Data_c["NR0"]+self.Data_c["NG"]+self.Data_c["NR"]

        self.Br = (self.Data_c["NG"]+self.Data_c["NR"])/self.Data_c["TB"]/1000

        self.E = (self.FR-self.alpha*self.FR0-self.beta*self.FG)/(self.FR-self.alpha*self.FR0-self.beta*self.FG+self.gamma*self.FG)
        self.S = (self.FR-self.alpha*self.FR0-self.beta*self.FG+self.gamma*self.FG) / \
                 (self.FR-self.alpha*self.FR0-self.beta*self.FG+self.gamma*self.FG+self.FR0/self.delta)

        # Todo: Calc Tau and Tau2 as "Tau Combined" per r g --> Clear double var part for taus if it works as intendet
        # " get l1 and l2
        # if user combined pol:
        # tau = formular with *gGG*, l1, l2
        # tau2 = formular with *gRR*, l1, l2
        # elif user 50/50: Add taus (both pol) / 2
        # tau =
        # tau2 =
        # elif user Tau part 1:
        # tau = tauII
        # tau2 = tau2II
        # elif user Tau part 2:
        # tau = tauT
        # tau2 = tau2T
        #
        # from Andreas formular "

        if self.pol_set == 'Combined Polarization':
            self.tauD = ((1-3 * self.l2) * self.gGG) / ((1-3 * self.l2) * self.gGG + (2-3 * self.l1)) * self.Data_c["TauII"]\
                        + (2-3 * self.l1) / ((1-3 * self.l2) * self.gGG + (2-3 * self.l1)) * self.Data_c["TauT"]


            self.tauA = ((1-3 * self.l2) * self.gRR) / ((1-3 * self.l2) * self.gRR + (2-3 * self.l1)) * self.Data_c["Tau2II"]\
                        + (2-3 * self.l1) / ((1-3 * self.l2) * self.gRR + (2-3 * self.l1)) * self.Data_c["Tau2T"]

            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)


        elif self.pol_set == 'Combined 50/50':
            self.tauD = (self.Data_c["NGII"]*self.Data_c["TauII"] + self.Data_c["NGT"]*self.Data_c["TauT"])/(self.Data_c["NGII"]+self.Data_c["NGT"])
            self.tauA = (self.Data_c["NGII"]*self.Data_c["Tau2II"] + self.Data_c["NGT"]*self.Data_c["Tau2T"])/(self.Data_c["NGII"]+self.Data_c["NGT"])

            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)

        elif self.pol_set == 'Tau part 1':
            self.tauD = self.Data_c["TauII"]
            self.tauA = self.Data_c["Tau2II"]

            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)

        elif self.pol_set == 'Tau part 2':
            self.tauD = self.Data_c["TauT"]
            self.tauA = self.Data_c["Tau2T"]

            self.Data_c.insert(len(self.Data_c.columns), 'Tau', self.tauD, True)
            self.Data_c.insert(len(self.Data_c.columns), 'Tau2', self.tauA, True)

        self.rGG = (self.gGG*self.FGII-self.FGT)/(self.gGG*self.FGII+2*self.FGT)
        self.rRR = (self.gRR*self.FR0II-self.FR0T)/(self.gRR*self.FR0II+2*self.FR0T)

        self.rRR[np.isnan(self.rRR)] = 4.9

        self.NGR = self.Data_c["NG"]+self.Data_c["NR"]

        self.ratioSGSR = np.log10(self.Data_c["NG"]/self.Data_c["NR"])

        self.edges = np.arange(-0.1+self.BinOffset, 1.1+self.BinOffset, self.BinSize)
        self.edgesTau = np.arange(-0.1+self.BinOffset, 10+self.BinOffset, self.BinSize)
        self.edgesrGG = np.arange(-0.6+self.BinOffset, 1.1+self.BinOffset, self.BinSize)

        # Todo Add tau filter here with the new tau parameters

        #
        # (self.leftTau <= self.Data_c["Tau"]) & (self.Data_c["Tau"] <= self.rightTau) &
        # (self.leftTau2 <= self.Data_c["Tau2"]) & (self.Data_c["Tau2"] <= self.rightTau2))

        self.mask = ((float(self.settWin.leftSGSR.text()) < self.ratioSGSR)
                     & (self.ratioSGSR < float(self.settWin.rightSGSR.text()))
                     & (float(self.settWin.leftNGR.text()) < self.NGR)
                     & (self.NGR < float(self.settWin.rightNGR.text()))
                     & (float(self.settWin.leftBr.text()) < self.Br) & (self.Br < float(self.settWin.rightBr.text()))
                     & (float(self.settWin.leftN.text()) < self.N) & (self.N < float(self.settWin.rightN.text()))
                     & (float(self.settWin.leftS.text()) < self.S) & (self.S < float(self.settWin.rightS.text()))
                     & (float(self.settWin.leftE.text()) < self.E) & (self.E < float(self.settWin.rightE.text()))
                     & (float(self.settWin.leftrGG.text()) < self.rGG) & (self.rGG < float(self.settWin.rightrGG.text()))
                     & (float(self.settWin.leftrRR.text()) < self.rRR) & (self.rRR < float(self.settWin.rightrRR.text()))
                     & (self.leftTau <= self.Data_c["Tau"]) & (self.Data_c["Tau"] <= self.rightTau)
                     & (self.leftTau2 <= self.Data_c["Tau2"]) & (self.Data_c["Tau2"] <= self.rightTau2))


        self.E = self.E[self.mask]
        self.S = self.S[self.mask]
        self.Tau = self.Data_c["Tau"][self.mask]
        self.Tau2 = self.Data_c["Tau2"][self.mask]
        self.FRET2CDE = self.Data_c["FRET2CDE"][self.mask]
        [hEnew, I] = histc(self.E, self.edges)
        [hSnew, I] = histc(self.S, self.edges)
        [hTaunew, I] = histc(self.Tau, self.edgesTau)
        [hTau2new, I] = histc(self.Tau2, self.edgesTau)
        [hrGGnew, I] = histc(self.rGG[self.mask], self.edgesrGG)
        [hrRRnew, I] = histc(self.rRR[self.mask], self.edgesrGG)


        self.hE = np.zeros(len(hEnew))
        self.hS = np.zeros(len(hSnew))
        self.hTau = np.zeros(len(hTaunew))
        self.hTau2 = np.zeros(len(hTau2new))
        self.hrGG = np.zeros(len(hrGGnew))
        self.hrRR = np.zeros(len(hrRRnew))


        self.Etot.extend(self.E)
        self.Stot.extend(self.S)
        self.Tautot.extend(self.Tau)
        self.Tau2tot.extend(self.Tau2)
        self.FRET2CDEtot.extend(self.FRET2CDE)
        self.rGGtot.extend(self.rGG[self.mask])
        self.rRRtot.extend(self.rRR[self.mask])

        self.hE = self.hE + hEnew
        self.hS = self.hS + hSnew
        self.hTau = self.hTau + hTaunew
        self.hTau2 = self.hTau2 + hTau2new
        self.hrGG = self.hrGG + hrGGnew
        self.hrRR = self.hrRR + hrRRnew


        # [self.hEnew, I] = histc(self.E, self.edges)

    def leftComboBoxSlot(self, index):
        """
        Generate plots for the appropriate selection in the left combo box

        Args:
            index (int): Index of the combo box selection
        """


        if (index == 0):
            #E- histogram
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.bar(self.edges, self.hE, width=self.BinSize, align='edge')
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_ylabel("Counts")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError as e:
                print(e)
        elif (index == 1):
            #S vs. E scatter plot
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.Stot, s=1)
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_ylabel("S")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")
        elif (index == 2):
            #E vs. Tau(D(A)) scatter plot
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Tautot, self.Etot, s=1)
                self.leftGraph.canvas.ax.set_xlabel("$tau_{D(A)}$")
                self.leftGraph.canvas.ax.set_ylabel("E")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_ylim((-0.1, 1.1))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 6))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 3):
            #Tau(D(A))/Tau(D(0)) vs. E scatter plot
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, np.array(self.Tautot)/float(self.settWin.tauD0.text()), s=1)
                self.leftGraph.canvas.ax.set_ylabel("$tau_{D(A)}/tau_{D(0)}$")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_ylim((-0.1, 1.1))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 4):
            #E vs. Tau(A) scatter plot
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Tau2tot,self.Etot, s=1)
                self.leftGraph.canvas.ax.set_ylabel("E")
                self.leftGraph.canvas.ax.set_xlabel("$tau_{A} (ns)$")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_ylim((-0.1, 1.1))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 8))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 5):
            #FRET-2CDE vs. E scatter plot
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.FRET2CDE, s=1)
                self.leftGraph.canvas.ax.set_ylabel("FRET-2CDE")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_ylim((0, 100))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 6):
            #rGG vs. E scatter plot
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.rGGtot, s=1)
                self.leftGraph.canvas.ax.set_ylabel("$r_{GG}$")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_ylim((-0.3, 0.6))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

        elif (index == 7):
            #rRR vs. E scatter plot
            try:
                self.calculationFunc()
                self.leftGraph.canvas.ax.clear()
                self.leftGraph.canvas.ax.scatter(self.Etot, self.rRRtot, s=1)
                self.leftGraph.canvas.ax.set_ylabel("$r_{RR}$")
                self.leftGraph.canvas.ax.set_xlabel("E")
                self.leftGraph.canvas.ax.set_title('Well')
                self.leftGraph.canvas.ax.set_ylim((-0.3, 0.6))
                self.leftGraph.canvas.ax.set_xlim((-0.1, 1.1))
                self.leftGraph.canvas.ax.tick_params(direction='in', top=True, right=True)
                self.leftGraph.canvas.fig.tight_layout()
                self.leftGraph.canvas.draw()
            except AttributeError:
                print("Error")

    def leftExtractSlot(self):
        """
        Extract data displayed on the left hand side plot into a csv file
        """


        # when button pressed --> Open save Tickwindow dialog
        self.Tickwindow_left.exec() # open tickwindow

        try:
            checklist = self.Tickwindow_left.checklist # get output dict as var. checklist
        except AttributeError:
            return


        # extract current settings from settings window
        self.extract_setting_values()

        # user gave input (button pressed and ticks set)
        if self.Tickwindow_left.input_given and any(checklist.values()):

            # input in checklist given by user --> Open folder dialog

            folder = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Directory")

            if 'folder' not in locals():
                return


            # Internal order
            #1. Save Current -> Check for selected diagram type -> Save x/y + Independent check for RAW and .png save
            #2. Save All --> Check for selected diagram type -> Save all x/y
            # routines to save the current view
            if checklist['Save Data']:

                # Starting by defining general file path for current csv saves depending on slider and
                # combobox values

                filepath = os.path.join(folder, 'Well' + '_' +
                                        self.leftComboBox.currentText().replace(' ','_').replace('/','_')+'.csv')
                #save current settings
                try:
                    settings_file = os.path.join(folder,self.Tickwindow_left.settings_file_textbox.text()+'.csv')
                except NameError:
                    settings_file = os.path.join(folder, 'Well' + '_' +
                                                 self.leftComboBox.currentText().replace(' ','_').replace('/','_')
                                                 + '_settings_file.csv')
                #dict to frame convert for single line csv save
                pd.DataFrame([self.setting_values_dict]).to_csv(settings_file, index=False)



                # if current view is E Histogram
                if self.leftComboBox.currentIndex() == 0:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/E'] + self.edges.tolist())
                        writer.writerow(['y/Counts'] + self.hE.tolist())


                # if current view is S vs. E
                elif self.leftComboBox.currentIndex() == 1:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/E'] + self.Etot)
                        writer.writerow(['y/S'] + self.Stot)

                # if current view is E vs. Tau(D(A))
                elif self.leftComboBox.currentIndex() == 2:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/Tau(D(A))'] + self.Tautot)
                        writer.writerow(['y/E'] + self.Etot)

                # if current view is Tau(D(A)/D0)) vs. E
                elif self.leftComboBox.currentIndex() == 3:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/E'] + self.Etot)
                        writer.writerow(['y/Tau(D(A)/D0))'] +
                                        (np.array(self.Tautot)/float(self.settWin.tauD0.text())).tolist())

                # if current view is E vs. Tau(A)
                elif self.leftComboBox.currentIndex() == 4:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/Tau(A)'] + self.Tau2tot)
                        writer.writerow(['y/E'] + self.Etot)

                # if current view is FRET-2CDE vs. E scatter plot
                elif self.leftComboBox.currentIndex() == 5:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/E'] + self.Etot)
                        writer.writerow(['y/FRET-2CDE'] + self.FRET2CDE.tolist())

                # if current view is rGG vs. E scatter plot
                elif self.leftComboBox.currentIndex() == 6:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/E'] + self.Etot)
                        writer.writerow(['y/rGG'] + self.rGGtot)

                # if current view is rRR vs. E scatter plot
                elif self.leftComboBox.currentIndex() == 7:

                    with open(filepath, "w") as f:
                        writer = csv.writer(f)
                        writer.writerow(['x/E'] + self.Etot)
                        writer.writerow(['y/rRR'] + self.rRRtot)


                # save current png independent of the diagram type (its out of type if clause)
                if checklist['Save .png']:
                    png_path = os.path.join(folder,
                                            self.leftComboBox.currentText().replace(' ','_').replace('/','_')+'.png')
                    self.leftGraph.canvas.fig.savefig(png_path)

                if checklist['Save .eps']:
                    eps_path = os.path.join(folder,
                                            self.leftComboBox.currentText().replace(' ','_').replace('/','_')+'.eps')
                    self.leftGraph.canvas.fig.savefig(eps_path, format='eps')

                # save current raw data independent of the diagram type (its out type if clause)
                if checklist['Save RAW']:

                    self.dataDF['Well'].to_csv(folder+'/'+'RAW_data.csv')






    def ImportSettings(self):

        # get translater to set text in settings window
        _translate = QtCore.QCoreApplication.translate

        # set up custom file dialog
        dialog = QtWidgets.QFileDialog(self)
        dialog.setNameFilter(("CSV (*.csv)"))

        if dialog.exec_():
            fileName = dialog.selectedFiles()

        # return if no file is selected
        if 'fileName' not in locals():
            return

        # import csv from selected into pandas df
        settings_input = pd.read_csv(fileName[0])

        try:
            # change all the settings to values from the file
            for setting in settings_input.columns:
                getattr(self.settWin, f'{setting}') \
                    .setText(_translate("Settings", f"{str(settings_input[f'{setting}'].values[0])}"))

            # refresh current view
            self.updateAllGraph(self.sliderVal)

        except AttributeError:
            self.settWin.setDisabled(True)
            self.msg.setIcon(self.crit_icon)
            self.msg.setText("The settings file does not seem to be correctly formatted")
            self.msg.setInformativeText('Check the doc. for the correct format')
            self.msg.exec()
            return

    def dockChangedSlot(self, topLevel):
        """
        Slot to detect if settings window is docked or not

        Args:
            topLevel (bool): variable to indicate docking condition
        """
        if topLevel == True:
            self.setMinimumWidth(1037)
            self.resize(1037,600)
        else:
            self.setMinimumWidth(1037+502)

    def closeEvent(self, event):
        """
        Close windows (settings window etc.,) on the event of program closure

        """
        for i in self.addWindow:
            i.close()


class controller:
    """
    Window controller --> Enables switching between multiple window classes
    """
    def __init__(self):
        pass

    def show_main(self): # show multi well window
        try:
            self.mainWin.show() # if it was already executed just show it and not load it again (data preserved)

            try:
                self.single_well_win.hide() # if single well window is currently open hide it
            except:
                pass

        except: # if its the first time run the execution
            self.mainWin = MainWindow()
            self.mainWin.setWindowTitle('pyVIZ - Multiwell explorer')
            self.mainWin.switch_window.connect(self.show_single_well)
            try:
                self.single_well_win.hide() # hide single well window if its currently open
            except:
                pass
            self.mainWin.show()


    def show_single_well(self): # show sinle well window
        try:
            self.single_well_win.show() # if it was already executed just show it and not load it again (data preserved)
            try:
                self.mainWin.hide() # if multi well windo is currently open hide it
            except:
                pass
        except: # if its the first time run the execution
            self.single_well_win = MainWindow_single_well()
            self.single_well_win.setWindowTitle('pyVIZ Single-Well explorer')
            self.single_well_win.switch_window.connect(self.show_main)
            try:
                self.mainWin.hide() # hide multi well window if its currently open
            except:
                pass
            self.single_well_win.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('requirements/pyT3Icon.png'))
    Controller = controller()
    Controller.show_main()
    sys.exit(app.exec_())
