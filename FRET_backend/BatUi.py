# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bat_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from FRET_backend.mplwidget import MplWidget
import platform


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)


        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lifetime1_plot = MplWidget(self.centralwidget)
        self.lifetime1_plot.setObjectName("lifetime1_plot")

        # Define IRF shift buttons for top plot

        self.button_grid_Top = QtWidgets.QGridLayout()
        self.MinusIRFButton_Top = QtWidgets.QPushButton()
        self.MinusIRFButton_Top.setText('-')
        self.MinusIRFButton_Top.setDisabled(False)
        self.MinusIRFButton_Top.setMaximumWidth(40)
        self.button_grid_Top.addWidget(self.MinusIRFButton_Top, 0, 0, 1, 1)

        self.PlusIRFButton_Top = QtWidgets.QPushButton()
        self.PlusIRFButton_Top.setText('+')
        self.PlusIRFButton_Top.setDisabled(False)
        self.PlusIRFButton_Top.setMaximumWidth(40)
        self.button_grid_Top.addWidget(self.PlusIRFButton_Top, 0, 1, 1, 1)

        # Define IRF shift buttons for middle plot
        self.button_grid_Mid = QtWidgets.QGridLayout()
        self.MinusIRFButton_Mid = QtWidgets.QPushButton()
        self.MinusIRFButton_Mid.setText('-')
        self.MinusIRFButton_Mid.setDisabled(False)
        self.MinusIRFButton_Mid.setMaximumWidth(40)
        self.button_grid_Mid.addWidget(self.MinusIRFButton_Mid, 0, 0, 1, 1)

        self.PlusIRFButton_Mid = QtWidgets.QPushButton()
        self.PlusIRFButton_Mid.setText('+')
        self.PlusIRFButton_Mid.setDisabled(False)
        self.PlusIRFButton_Mid.setMaximumWidth(40)
        self.button_grid_Mid.addWidget(self.PlusIRFButton_Mid, 0, 1, 1, 1)




        self.interPht_plot = MplWidget(self.centralwidget)
        self.interPht_plot.setObjectName("interPht_plot")
        self.lifetime2_plot = MplWidget(self.centralwidget)
        self.lifetime2_plot.setObjectName("lifetime2_plot")
        MainWindow.setCentralWidget(self.centralwidget)

        # Fill plot grid

        # First plot
        self.gridLayout_2.addWidget(self.lifetime1_plot, 0, 0, 2, 1)
        # Plus minus first plot
        self.gridLayout_2.addItem(self.button_grid_Top, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        # second plot
        self.gridLayout_2.addWidget(self.lifetime2_plot, 2, 0, 2, 1)
        # Plus minus second plot
        self.gridLayout_2.addItem(self.button_grid_Mid, 3, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        # Third plot
        self.gridLayout_2.addWidget(self.interPht_plot, 4, 0, 1, 1)

        # add plot grid to main layout
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # open file slot
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        #import settings slot
        self.actionImportSettings = QtWidgets.QAction(MainWindow)
        self.actionImportSettings.setObjectName("actionImportSettings")

        #export settings slot
        self.actionExprotSettings = QtWidgets.QAction(MainWindow)
        self.actionExprotSettings.setObjectName("actionExprotSettings")


        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionImportSettings)
        self.menuFile.addAction(self.actionExprotSettings)
        self.menubar.addAction(self.menuFile.menuAction())

        # create a settings box
        self.verticalLayout.addWidget(self.LifetimeBox(), stretch=1)
        self.verticalLayout.addWidget(self.correction_box(), stretch=1)
        self.verticalLayout.addWidget(self.ShowBox(), stretch=1)
        self.verticalLayout.addWidget(self.settings_box(), stretch=3)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def ShowBox(self):
        groupBox = QGroupBox()
        groupBox.setTitle('Show')
        groupBox.setMaximumWidth(200)
        grid = QGridLayout()

        if platform.system() == 'Darwin':
            font_size = 10
            font_style = 'Arial'
        elif platform.system() == 'Windows':
            font_size = 8
            font_style = 'Arial'
        else:
            # Todo: Test what setting is best on linux
            font_size = 10
            font_style = 'Arial'

        self.RawDataButton = QtWidgets.QPushButton()
        self.RawDataButton.setText('Raw Data')
        self.RawDataButton.setDisabled(True)
        grid.addWidget(self.RawDataButton, 0, 0, 1, 2)

        self.AnalyzeButton = QtWidgets.QPushButton()
        self.AnalyzeButton.setText('Analyze')
        self.AnalyzeButton.setDisabled(True)
        grid.addWidget(self.AnalyzeButton, 1, 0, 1, 2)

        groupBox.setLayout(grid)
        return groupBox

    def LifetimeBox(self):
        groupBox = QGroupBox()
        groupBox.setTitle('Lifetime Windows')
        groupBox.setMaximumWidth(200)
        grid = QGridLayout()

        if platform.system() == 'Darwin':
            font_size = 12
            font_style = 'Arial'
        elif platform.system() == 'Windows':
            font_size = 8
            font_style = 'Arial'
        else:
            # Todo: Test what setting is best on linux
            font_size = 12
            font_style = 'Arial'

        # create Widgets

        self.DD_DA_Button = QtWidgets.QPushButton()
        self.DD_DA_Button.setText('DD + DA')
        self.DD_DA_Button.setDisabled(True)
        grid.addWidget(self.DD_DA_Button, 0, 0, 1, 4)

        self.AA_Button = QtWidgets.QPushButton()
        self.AA_Button.setText('AA')
        self.AA_Button.setDisabled(True)
        grid.addWidget(self.AA_Button, 1, 0, 1, 4)

        '''self.lower_Norm = QLineEdit()
        self.lower_Norm.setText('1')
        self.lower_Norm.setDisabled(True)
        self.lower_Norm.setValidator(QIntValidator())
        grid.addWidget(self.lower_Norm, 2, 0)

        ToText = QLabel('to')
        ToText.setFont(QFont(font_style, font_size))
        grid.addWidget(ToText, 2, 1, 1, 1)

        self.upper_Norm = QLineEdit()
        self.upper_Norm.setText('10')
        self.upper_Norm.setValidator(QIntValidator())
        self.upper_Norm.setDisabled(True)
        grid.addWidget(self.upper_Norm, 2, 2)

        ChannelText = QLabel('channels')
        ChannelText.setFont(QFont(font_style, font_size))
        grid.addWidget(ChannelText, 2, 3)

        self.NormButton = QtWidgets.QPushButton()
        self.NormButton.setText('Correct')
        self.NormButton.setDisabled(True)
        grid.addWidget(self.NormButton, 3, 0, 1, 4)'''




        groupBox.setLayout(grid)


        return groupBox

    def correction_box(self):

        groupBox = QGroupBox()
        groupBox.setTitle('Background substracted view')
        groupBox.setMaximumWidth(200)
        grid = QGridLayout()

        if platform.system() == 'Darwin':
            font_size = 12
            font_style = 'Arial'
        elif platform.system() == 'Windows':
            font_size = 8
            font_style = 'Arial'
        else:
            # Todo: Test what setting is best on linux
            font_size = 12
            font_style = 'Arial'

        self.lower_Norm = QLineEdit()
        self.lower_Norm.setText('1')
        self.lower_Norm.setDisabled(True)
        self.lower_Norm.setValidator(QIntValidator())
        grid.addWidget(self.lower_Norm, 0, 0)

        ToText = QLabel('to')
        ToText.setFont(QFont(font_style, font_size))
        grid.addWidget(ToText, 0, 1, 1, 1)

        self.upper_Norm = QLineEdit()
        self.upper_Norm.setText('10')
        self.upper_Norm.setValidator(QIntValidator())
        self.upper_Norm.setDisabled(True)
        grid.addWidget(self.upper_Norm, 0, 2)

        ChannelText = QLabel('channels')
        ChannelText.setFont(QFont(font_style, font_size))
        grid.addWidget(ChannelText, 0, 3)

        self.NormButton = QtWidgets.QPushButton()
        self.NormButton.setText('Display')
        self.NormButton.setDisabled(True)
        grid.addWidget(self.NormButton, 1, 0, 1, 4)

        groupBox.setLayout(grid)

        return groupBox

    def settings_box(self):

        groupBox = QGroupBox()
        groupBox.setTitle('Settings')
        groupBox.setMaximumWidth(200)
        if platform.system() == 'Darwin':
            font_size = 10
            font_style = 'Arial'
        elif platform.system() == 'Windows':
            font_size = 8
            font_style = 'Arial'
        else:
            # Todo: Test what setting is best on linux
            font_size = 10
            font_style = 'Arial'

        # Create the widgets
        max_inter_time_line = QLabel("max. IPT<sub>Burst")
        max_inter_time_line.setFont(QFont(font_style, font_size))
        self.maxInterTime = QLineEdit()
        self.maxInterTime.setText('0.03')
        self.maxInterTime.setValidator(QDoubleValidator())
        self.maxInterTime.setMaximumWidth(40)
        self.maxInterTime.setMinimumWidth(40)

        min_inter_t_noise = QLabel("min. IPT<sub>BG")
        min_inter_t_noise.setFont(QFont(font_style, font_size))
        self.minInterTimeNoise = QLineEdit()
        self.minInterTimeNoise.setValidator(QDoubleValidator())
        self.minInterTimeNoise.setText('0.03')
        self.minInterTimeNoise.setMaximumWidth(40)

        self.minTotalTick = QCheckBox()
        self.minTotalTick.setChecked(True)
        self.minTotalTick.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.minTotalTick.setText("min. Nph")
        self.minTotalTick.setFont(QFont(font_style, font_size))
        self.minTotal = QLineEdit()
        self.minTotal.setValidator(QIntValidator())
        self.minTotal.setMaximumWidth(40)
        self.minTotal.setText('70')

        gr_text = QLabel('N<sub>DD + DA')
        gr_text.setFont(QFont(font_style, font_size))
        r0_text = QLabel('N<sub>AA')
        r0_text.setFont(QFont(font_style, font_size))

        min_pho_text = QLabel('min.\nPhotons')
        min_pho_text.setFont(QFont(font_style, font_size))
        self.grBox = QLineEdit()
        self.grBox.setValidator(QIntValidator())
        self.grBox.setText('20')
        self.grBox.setMaximumWidth(40)
        self.r0Box = QLineEdit()
        self.r0Box.setValidator(QIntValidator())
        self.r0Box.setText('40')
        self.r0Box.setMaximumWidth(40)


        self.leeFilterCheck = QCheckBox()
        self.leeFilterCheck.setChecked(True)
        self.leeFilterCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.leeFilterCheck.setText('Lee\nFilter')
        self.leeFilterCheck.setFont(QFont(font_style, font_size))
        self.leeFilterBox = QLineEdit()
        self.leeFilterBox.setValidator(QIntValidator())
        self.leeFilterBox.setText('4')
        self.leeFilterBox.setMaximumWidth(40)

        gGG_text = QLabel('gGG')
        gGG_text.setFont(QFont(font_style, font_size))
        gRR_text = QLabel('gRR')
        gRR_text.setFont(QFont(font_style, font_size))

        self.flaCheckbox = QCheckBox()
        self.flaCheckbox.setChecked(True)
        self.gGGBox = QLineEdit()
        self.gGGBox.setValidator(QIntValidator())
        self.gGGBox.setMaximumWidth(40)
        self.gGGBox.setText('1')
        self.gRRBox = QLineEdit()
        self.gRRBox.setValidator(QIntValidator())
        self.gRRBox.setMaximumWidth(40)
        self.gRRBox.setText('1')
        self.flaCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.flaCheckbox.setText('FLA')
        self.flaCheckbox.setFont(QFont(font_style, font_size))

        self.postAnaCheckbox = QCheckBox()
        self.postAnaCheckbox.setChecked(True)
        self.postAnaCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.postAnaCheckbox.setText('Post\nAna.')
        self.postAnaCheckbox.setFont(QFont(font_style, font_size))

        file_suffix_text = QLabel('File\nSuffix')
        file_suffix_text.setFont(QFont(font_style, font_size))
        self.fileSuffixBox = QLineEdit()
        self.fileSuffixBox.setMaximumWidth(40)
        self.fileSuffixBox.setText('1')

        files_per_bin_text = QLabel('Files per\n*.bin')
        files_per_bin_text.setFont(QFont(font_style, font_size))
        self.filesPerBinBox = QLineEdit()
        self.filesPerBinBox.setValidator(QIntValidator())
        self.filesPerBinBox.setMaximumWidth(40)
        self.filesPerBinBox.setText('20')

        # crate core selection
        CoreSelectText = QLabel('Number\ncores')
        CoreSelectText.setFont(QFont(font_style, font_size))
        self.CoreSelectBox = QLineEdit()
        self.CoreSelectBox.setMaximumWidth(40)
        self.CoreSelectBox.setText('Auto')


        self.thirtythirtyCheck = QCheckBox()
        self.thirtythirtyCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.thirtythirtyCheck.setText('+30/-30')
        self.thirtythirtyCheck.setFont(QFont(font_style, font_size))

        self.refreshButton = QPushButton()
        self.refreshButton.setText('Refresh')
        self.refreshButton.setFont(QFont(font_style, font_size))

        self.tauFRETtext = QLabel('Tau\n(FRET-2CDE)')
        self.tauFRETtext.setFont(QFont(font_style, font_size))
        self.tauFRETbox = QLineEdit()
        self.tauFRETbox.setValidator(QIntValidator())
        self.tauFRETbox.setText('45')
        self.tauFRETbox.setMaximumWidth(40)

        self.tauALEXtext = QLabel('Tau\n(ALEX-2CDE)')
        self.tauALEXtext.setFont(QFont(font_style, font_size))
        self.tauALEXbox = QLineEdit()
        self.tauALEXbox.setValidator(QIntValidator())
        self.tauALEXbox.setText('75')
        self.tauALEXbox.setMaximumWidth(40)


        # add widgets to grid

        grid = QGridLayout()
        grid.addWidget(max_inter_time_line, 0,0,1,2)
        grid.addWidget(self.maxInterTime, 0, 2)
        grid.addWidget(QLabel('ms'), 0,3)

        grid.addWidget(min_inter_t_noise, 1, 0, 1,2)
        grid.addWidget(self.minInterTimeNoise, 1, 2)
        grid.addWidget(QLabel('ms'),1,3)

        grid.addWidget(self.minTotalTick, 2, 0, 1, 2)
        grid.addWidget(self.minTotal, 2, 2)


        grid.addWidget(self.tauFRETtext, 3,0,1,2)
        grid.addWidget(self.tauFRETbox, 3,2)
        grid.addWidget(QLabel('µs'),3,3)

        grid.addWidget(self.tauALEXtext, 4,0,1,2)
        grid.addWidget(self.tauALEXbox, 4,2)
        grid.addWidget(QLabel('µs'),4,3)

        grid.addWidget(gr_text, 5, 1, 2, 1)
        grid.addWidget(r0_text, 5, 2, 2, 1)

        grid.addWidget(min_pho_text, 6, 0)
        grid.addWidget(self.grBox, 6, 1)
        grid.addWidget(self.r0Box, 6, 2)

        grid.addWidget(self.leeFilterCheck, 7, 0)
        grid.addWidget(self.leeFilterBox, 7, 2)

        grid.addWidget(self.flaCheckbox,8,0)

        grid.addWidget(file_suffix_text,9,0)
        grid.addWidget(self.fileSuffixBox, 9, 1)

        grid.addWidget(CoreSelectText, 10, 0)
        grid.addWidget(self.CoreSelectBox, 10, 2)

        grid.addWidget(self.thirtythirtyCheck, 11, 0)
        grid.addWidget(self.refreshButton, 11, 2,1,2)




        groupBox.setLayout(grid)

        return groupBox

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open file"))
        self.actionImportSettings.setText(_translate("MainWindow", "Import settings"))
        self.actionExprotSettings.setText(_translate("MainWindow", "Export settings"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
