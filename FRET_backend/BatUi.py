# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bat_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
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
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.GG_GR_Lifetime_button = QtWidgets.QPushButton(self.groupBox_2)
        self.GG_GR_Lifetime_button.setGeometry(QtCore.QRect(0, 20, 121, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GG_GR_Lifetime_button.sizePolicy().hasHeightForWidth())
        self.GG_GR_Lifetime_button.setSizePolicy(sizePolicy)
        self.GG_GR_Lifetime_button.setObjectName("GG_GR_Lifetime_button")
        self.GR_Lifetime_button = QtWidgets.QPushButton(self.groupBox_2)
        self.GR_Lifetime_button.setGeometry(QtCore.QRect(0, 50, 121, 32))
        self.GR_Lifetime_button.setObjectName("GR_Lifetime_button")
        self.verticalLayout.addWidget(self.groupBox_2, stretch=1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.BurstButton = QtWidgets.QPushButton(self.groupBox)
        self.BurstButton.setGeometry(QtCore.QRect(0, 20, 112, 32))
        self.BurstButton.setObjectName("BurstButton")
        self.AnalyzeButton = QtWidgets.QPushButton(self.groupBox)
        self.AnalyzeButton.setGeometry(QtCore.QRect(0, 50, 112, 32))
        self.AnalyzeButton.setObjectName("AnalyzeButton")
        self.IPTButton = QtWidgets.QPushButton(self.groupBox)
        self.IPTButton.setGeometry(QtCore.QRect(0, 80, 112, 32))
        self.IPTButton.setObjectName("IPTButton")
        self.verticalLayout.addWidget(self.groupBox, stretch=1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lifetime1_plot = MplWidget(self.centralwidget)
        self.lifetime1_plot.setObjectName("lifetime1_plot")
        self.gridLayout_2.addWidget(self.lifetime1_plot, 0, 0, 1, 1)
        self.interPht_plot = MplWidget(self.centralwidget)
        self.interPht_plot.setObjectName("interPht_plot")
        self.gridLayout_2.addWidget(self.interPht_plot, 2, 0, 1, 1)
        self.lifetime2_plot = MplWidget(self.centralwidget)
        self.lifetime2_plot.setObjectName("lifetime2_plot")
        self.gridLayout_2.addWidget(self.lifetime2_plot, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

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
        self.verticalLayout.addWidget(self.settings_box(), stretch=3)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
        max_inter_time_line = QLabel('max. Interph Time')
        max_inter_time_line.setFont(QFont(font_style, font_size))
        self.maxInterTime = QLineEdit()
        self.maxInterTime.setText('0.15')
        self.maxInterTime.setMaximumWidth(40)
        self.maxInterTime.setMinimumWidth(40)

        min_inter_t_noise = QLabel('min. Interph.\nTime Noise')
        min_inter_t_noise.setFont(QFont(font_style, font_size))
        self.minInterTimeNoise = QLineEdit()
        self.minInterTimeNoise.setText('0.15')
        self.minInterTimeNoise.setMaximumWidth(40)

        self.minTotalTick = QCheckBox()
        self.minTotalTick.setChecked(True)
        self.minTotalTick.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.minTotalTick.setText('min. Total')
        self.minTotalTick.setFont(QFont(font_style, font_size))
        self.minTotal = QLineEdit()
        self.minTotal.setMaximumWidth(40)
        self.minTotal.setText('70')

        gr_text = QLabel('G+R')
        gr_text.setFont(QFont(font_style, font_size))
        r0_text = QLabel('R0')
        r0_text.setFont(QFont(font_style, font_size))

        min_pho_text = QLabel('min.\nPhotons')
        min_pho_text.setFont(QFont(font_style, font_size))
        self.grBox = QLineEdit()
        self.grBox.setText('20')
        self.grBox.setMaximumWidth(40)
        self.r0Box = QLineEdit()
        self.r0Box.setText('40')
        self.r0Box.setMaximumWidth(40)


        self.leeFilterCheck = QCheckBox()
        self.leeFilterCheck.setChecked(True)
        self.leeFilterCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.leeFilterCheck.setText('LeeFilter')
        self.leeFilterCheck.setFont(QFont(font_style, font_size))
        self.leeFilterBox = QLineEdit()
        self.leeFilterBox.setText('4')
        self.leeFilterBox.setMaximumWidth(40)

        gGG_text = QLabel('gGG')
        gGG_text.setFont(QFont(font_style, font_size))
        gRR_text = QLabel('gRR')
        gRR_text.setFont(QFont(font_style, font_size))

        self.flaCheckbox = QCheckBox()
        self.flaCheckbox.setChecked(True)
        self.gGGBox = QLineEdit()
        self.gGGBox.setMaximumWidth(40)
        self.gGGBox.setText('1')
        self.gRRBox = QLineEdit()
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

        file_suffix_text = QLabel('File Suffix')
        file_suffix_text.setFont(QFont(font_style, font_size))
        self.fileSuffixBox = QLineEdit()
        self.fileSuffixBox.setMaximumWidth(40)
        self.fileSuffixBox.setText('1')

        files_per_bin_text = QLabel('Files per\n*.bin')
        files_per_bin_text.setFont(QFont(font_style, font_size))
        self.filesPerBinBox = QLineEdit()
        self.filesPerBinBox.setMaximumWidth(40)
        self.filesPerBinBox.setText('20')

        self.thirtythirtyCheck = QCheckBox()
        self.thirtythirtyCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.thirtythirtyCheck.setText('+30/-30')
        self.thirtythirtyCheck.setFont(QFont(font_style, font_size))

        self.refreshButton = QPushButton()
        self.refreshButton.setText('Refresh')
        self.refreshButton.setFont(QFont(font_style, font_size))




        # add widgets to grid
        grid = QGridLayout()
        grid.addWidget(max_inter_time_line, 0,0,1,2)
        grid.addWidget(self.maxInterTime, 0, 2)

        grid.addWidget(min_inter_t_noise, 1,0, 1,2)
        grid.addWidget(self.minInterTimeNoise, 1, 2)

        grid.addWidget(self.minTotalTick, 2, 0, 1, 2)
        grid.addWidget(self.minTotal, 2, 2)

        # Todo: Place them relative to the QLineEdit windows
        grid.addWidget(gr_text, 3,1)
        grid.addWidget(r0_text, 3,2)

        grid.addWidget(min_pho_text, 4,0)
        grid.addWidget(self.grBox, 4, 1)
        grid.addWidget(self.r0Box, 4, 2)

        grid.addWidget(self.leeFilterCheck, 5, 0)
        grid.addWidget(self.leeFilterBox, 5, 2)

        # Todo: Place them relative to the QLineEdit windows
        grid.addWidget(gGG_text, 6,1)
        grid.addWidget(gRR_text, 6,2)

        grid.addWidget(self.flaCheckbox, 7, 0)
        grid.addWidget(self.gGGBox, 7, 1)
        grid.addWidget(self.gRRBox, 7, 2)

        grid.addWidget(self.postAnaCheckbox, 8, 0)

        grid.addWidget(file_suffix_text,9,0)
        grid.addWidget(self.fileSuffixBox, 9, 1)

        grid.addWidget(files_per_bin_text, 10,0)
        grid.addWidget(self.filesPerBinBox, 10, 1)

        grid.addWidget(self.thirtythirtyCheck, 11, 0)
        grid.addWidget(self.refreshButton, 11, 2)



        groupBox.setLayout(grid)

        return groupBox

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Lifetime Windows"))
        self.GG_GR_Lifetime_button.setText(_translate("MainWindow", "GG + GR"))
        self.GR_Lifetime_button.setText(_translate("MainWindow", "GR"))
        self.groupBox.setTitle(_translate("MainWindow", "Show"))
        self.BurstButton.setText(_translate("MainWindow", "Burst"))
        self.AnalyzeButton.setText(_translate("MainWindow", "Analyze"))
        self.IPTButton.setText(_translate("MainWindow", "IPT Histogram"))
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