# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'init_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_initDevices(object):
    def setupUi(self, initDevices):
        initDevices.setObjectName("initDevices")
        initDevices.resize(566, 294)
        self.horizontalLayoutWidget = QtWidgets.QWidget(initDevices)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 520, 194))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.findDevices = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.findDevices.setObjectName("findDevices")
        self.horizontalLayout_5.addWidget(self.findDevices)
        self.portListWidget = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portListWidget.sizePolicy().hasHeightForWidth())
        self.portListWidget.setSizePolicy(sizePolicy)
        self.portListWidget.setObjectName("portListWidget")
        self.horizontalLayout_5.addWidget(self.portListWidget)

        self.retranslateUi(initDevices)
        QtCore.QMetaObject.connectSlotsByName(initDevices)

    def retranslateUi(self, initDevices):
        _translate = QtCore.QCoreApplication.translate
        initDevices.setWindowTitle(_translate("initDevices", "Port selection"))
        self.findDevices.setText(_translate("initDevices", "Refresh devices"))