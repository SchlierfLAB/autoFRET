# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyt3ee_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1167, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rightGraphWidget = MplWidget(self.centralwidget)
        self.rightGraphWidget.setGeometry(QtCore.QRect(590, 90, 551, 471))
        self.rightGraphWidget.setObjectName("rightGraphWidget")
        self.leftGraphWidget = MplWidget(self.centralwidget)
        self.leftGraphWidget.setGeometry(QtCore.QRect(20, 90, 541, 471))
        self.leftGraphWidget.setObjectName("leftGraphWidget")
        self.leftComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.leftComboBox.setGeometry(QtCore.QRect(20, 50, 241, 32))
        self.leftComboBox.setObjectName("leftComboBox")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.rightComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.rightComboBox.setGeometry(QtCore.QRect(590, 50, 241, 32))
        self.rightComboBox.setObjectName("rightComboBox")
        self.rightComboBox.addItem("")
        self.rightComboBox.addItem("")
        self.rightComboBox.addItem("")
        self.meanButton = QtWidgets.QPushButton(self.centralwidget)
        self.meanButton.setGeometry(QtCore.QRect(860, 50, 112, 32))
        self.meanButton.setObjectName("meanButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1167, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTest = QtWidgets.QMenu(self.menubar)
        self.menuTest.setObjectName("menuTest")
        MainWindow.setMenuBar(self.menubar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.actiontest_menu = QtWidgets.QAction(MainWindow)
        self.actiontest_menu.setObjectName("actiontest_menu")
        self.action_openFolder = QtWidgets.QAction(MainWindow)
        self.action_openFolder.setObjectName("action_openFolder")
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_openFolder)
        self.menuTest.addAction(self.actiontest_menu)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTest.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.leftComboBox.setItemText(0, _translate("MainWindow", "S vs. E"))
        self.leftComboBox.setItemText(1, _translate("MainWindow", "Tau_D(A)/Tau_D(0) vs. E"))
        self.leftComboBox.setItemText(2, _translate("MainWindow", "E vs. Tau_D(A)"))
        self.leftComboBox.setItemText(3, _translate("MainWindow", "E vs. Tau_A"))
        self.leftComboBox.setItemText(4, _translate("MainWindow", "FRET-2CDE vs. E"))
        self.leftComboBox.setItemText(5, _translate("MainWindow", "1/S vs. E"))
        self.leftComboBox.setItemText(6, _translate("MainWindow", "TGR - TR0 vs Alex-2CDE"))
        self.leftComboBox.setItemText(7, _translate("MainWindow", "rGG vs. Tau_D(A)"))
        self.leftComboBox.setItemText(8, _translate("MainWindow", "rRR vs. Tau_A"))
        self.leftComboBox.setItemText(9, _translate("MainWindow", "NA+ND vs. E"))
        self.rightComboBox.setItemText(0, _translate("MainWindow", "E-histogram"))
        self.rightComboBox.setItemText(1, _translate("MainWindow", "S-histogram"))
        self.rightComboBox.setItemText(2, _translate("MainWindow", "E(Tau)-Histogram"))
        self.meanButton.setText(_translate("MainWindow", "Mean"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTest.setTitle(_translate("MainWindow", "Test"))
        self.action_open.setText(_translate("MainWindow", "Open file"))
        self.actiontest_menu.setText(_translate("MainWindow", "test_menu"))
        self.action_openFolder.setText(_translate("MainWindow", "Open folder/subfolders"))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

