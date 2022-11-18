# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1073, 558)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.homeButton = QtWidgets.QPushButton(self.centralwidget)
        self.homeButton.setObjectName("homeButton")
        self.horizontalLayout.addWidget(self.homeButton)
        self.closeConnButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeConnButton.setObjectName("closeConnButton")
        self.horizontalLayout.addWidget(self.closeConnButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.setHomeButton = QtWidgets.QPushButton(self.centralwidget)
        self.setHomeButton.setObjectName("setHomeButton")
        self.verticalLayout_3.addWidget(self.setHomeButton)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.moveToPosButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveToPosButton.setObjectName("moveToPosButton")
        self.verticalLayout.addWidget(self.moveToPosButton)
        self.moveToPosition = QtWidgets.QPushButton(self.centralwidget)
        self.moveToPosition.setStyleSheet("background-color: rgba(89, 255, 74, 179)")
        self.moveToPosition.setObjectName("moveToPosition")
        self.verticalLayout.addWidget(self.moveToPosition)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, -1, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.folderDir_label = QtWidgets.QLabel(self.centralwidget)
        self.folderDir_label.setObjectName("folderDir_label")
        self.gridLayout_2.addWidget(self.folderDir_label, 0, 1, 1, 1)
        self.folderDir = QtWidgets.QLineEdit(self.centralwidget)
        self.folderDir.setObjectName("folderDir")
        self.gridLayout_2.addWidget(self.folderDir, 0, 2, 1, 1)
        self.measTime_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measTime_label.sizePolicy().hasHeightForWidth())
        self.measTime_label.setSizePolicy(sizePolicy)
        self.measTime_label.setWordWrap(True)
        self.measTime_label.setObjectName("measTime_label")
        self.gridLayout_2.addWidget(self.measTime_label, 2, 1, 1, 1)
        self.measTime = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measTime.sizePolicy().hasHeightForWidth())
        self.measTime.setSizePolicy(sizePolicy)
        self.measTime.setObjectName("measTime")
        self.gridLayout_2.addWidget(self.measTime, 2, 2, 1, 1)
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setObjectName("browseButton")
        self.gridLayout_2.addWidget(self.browseButton, 0, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.graphicsView = CustomGraphicsView(self.centralwidget)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setAutoFillBackground(True)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_4.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # create x/y min/max boxes 

        # x min. 
        self.xmin_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.xmin_label.sizePolicy().hasHeightForWidth())
        self.xmin_label.setSizePolicy(sizePolicy)
        self.xmin_label.setWordWrap(True)
        self.xmin_label.setObjectName("xmin_label")
        self.gridLayout_2.addWidget(self.xmin_label, 3, 1, 1, 1)

        self.xmin = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy.setHeightForWidth(self.xmin.sizePolicy().hasHeightForWidth())
        self.xmin.setSizePolicy(sizePolicy)
        self.xmin.setObjectName("xmin")
        self.gridLayout_2.addWidget(self.xmin, 3, 2, 1, 1)
        self.xmin.setText('-inf')

        # x max.
        self.xmax_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.xmax_label.sizePolicy().hasHeightForWidth())
        self.xmax_label.setSizePolicy(sizePolicy)
        self.xmax_label.setWordWrap(True)
        self.xmax_label.setObjectName("xmax_label")
        self.gridLayout_2.addWidget(self.xmax_label, 3, 3, 1, 1)

        self.xmax = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy.setHeightForWidth(self.xmax.sizePolicy().hasHeightForWidth())
        self.xmax.setSizePolicy(sizePolicy)
        self.xmax.setObjectName("xmax")
        self.gridLayout_2.addWidget(self.xmax, 3, 4, 1, 1)
        self.xmax.setText('inf')

        # y min. 
        self.ymin_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.ymin_label.sizePolicy().hasHeightForWidth())
        self.ymin_label.setSizePolicy(sizePolicy)
        self.ymin_label.setWordWrap(True)
        self.ymin_label.setObjectName("ymin_label")
        self.gridLayout_2.addWidget(self.ymin_label, 4, 1, 1, 1)

        self.ymin = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy.setHeightForWidth(self.ymin.sizePolicy().hasHeightForWidth())
        self.ymin.setSizePolicy(sizePolicy)
        self.ymin.setObjectName("ymin")
        self.gridLayout_2.addWidget(self.ymin, 4, 2, 1, 1)
        self.ymin.setText('-inf')

        #y max.
        self.ymax_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy.setHeightForWidth(self.ymax_label.sizePolicy().hasHeightForWidth())
        self.ymax_label.setSizePolicy(sizePolicy)
        self.ymax_label.setWordWrap(True)
        self.ymax_label.setObjectName("ymax_label")
        self.gridLayout_2.addWidget(self.ymax_label, 4, 3, 1, 1)

        self.ymax = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy.setHeightForWidth(self.ymax.sizePolicy().hasHeightForWidth())
        self.ymax.setSizePolicy(sizePolicy)
        self.ymax.setObjectName("ymax")
        self.gridLayout_2.addWidget(self.ymax, 4, 4, 1, 1)
        self.ymax.setText('inf')

        # User comment 
        self.comment_win = QtWidgets.QLineEdit(self.centralwidget, placeholderText="Enter a measurement comment")
        #sizePolicy.setHeightForWidth(self.comment_win.sizePolicy().hasHeightForWidth())
        self.comment_win.setObjectName('comment_win')
        self.gridLayout_2.addWidget(self.comment_win, 7, 1, 1, 4)
        #self.gridLayout_2.setRowStretch(7, 3)




        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.homeButton, self.closeConnButton)
        MainWindow.setTabOrder(self.closeConnButton, self.setHomeButton)
        MainWindow.setTabOrder(self.setHomeButton, self.moveToPosition)
        MainWindow.setTabOrder(self.moveToPosition, self.graphicsView)
        MainWindow.setTabOrder(self.graphicsView, self.folderDir)
        MainWindow.setTabOrder(self.folderDir, self.browseButton)
        MainWindow.setTabOrder(self.browseButton, self.measTime)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.homeButton.setText(_translate("MainWindow", "Home"))
        self.closeConnButton.setText(_translate("MainWindow", "Close connection"))
        self.setHomeButton.setText(_translate("MainWindow", "Set home position"))
        self.moveToPosButton.setText(_translate("MainWindow", "Move to position"))
        self.moveToPosition.setText(_translate("MainWindow", "Start measurement"))
        self.folderDir_label.setText(_translate("MainWindow", "Folder directory"))
        self.measTime_label.setText(_translate("MainWindow", "Measurement time at each position (minutes)"))
        self.measTime.setText(_translate("MainWindow", "20"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.xmin_label.setText(_translate('MainWindow','Minimum x position (mm):'))
        self.xmax_label.setText(_translate('MainWindow','Maximum x position (mm):'))
        self.ymin_label.setText(_translate('MainWindow','Minimum y position (mm):'))
        self.ymax_label.setText(_translate('MainWindow','Maximum y position (mm):'))

from customgraphicsview import CustomGraphicsView
import resource_test_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

