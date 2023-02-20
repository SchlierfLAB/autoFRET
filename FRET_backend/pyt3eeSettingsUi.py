from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(502, 612)
        self.Settings_2 = QtWidgets.QGroupBox(Settings)
        self.Settings_2.setGeometry(QtCore.QRect(10, 10, 291, 601))
        self.Settings_2.setObjectName("Settings_2")
        self.leftSGSR = QtWidgets.QLineEdit(self.Settings_2)
        self.leftSGSR.setGeometry(QtCore.QRect(10, 570, 61, 21))
        self.leftSGSR.setAlignment(QtCore.Qt.AlignCenter)
        self.leftSGSR.setObjectName("leftSGSR")
        self.label = QtWidgets.QLabel(self.Settings_2)
        self.label.setGeometry(QtCore.QRect(80, 30, 101, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.leftAlex = QtWidgets.QLineEdit(self.Settings_2)
        self.leftAlex.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.leftAlex.setAlignment(QtCore.Qt.AlignCenter)
        self.leftAlex.setObjectName("leftAlex")
        self.rightAlex = QtWidgets.QLineEdit(self.Settings_2)
        self.rightAlex.setGeometry(QtCore.QRect(190, 30, 61, 21))
        self.rightAlex.setAlignment(QtCore.Qt.AlignCenter)
        self.rightAlex.setObjectName("rightAlex")
        self.leftFRET = QtWidgets.QLineEdit(self.Settings_2)
        self.leftFRET.setGeometry(QtCore.QRect(10, 60, 61, 21))
        self.leftFRET.setAlignment(QtCore.Qt.AlignCenter)
        self.leftFRET.setObjectName("leftFRET")
        self.label_2 = QtWidgets.QLabel(self.Settings_2)
        self.label_2.setGeometry(QtCore.QRect(80, 60, 101, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.leftdT = QtWidgets.QLineEdit(self.Settings_2)
        self.leftdT.setGeometry(QtCore.QRect(10, 90, 61, 21))
        self.leftdT.setAlignment(QtCore.Qt.AlignCenter)
        self.leftdT.setObjectName("leftdT")
        self.label_3 = QtWidgets.QLabel(self.Settings_2)
        self.label_3.setGeometry(QtCore.QRect(80, 90, 101, 16))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.rightdT = QtWidgets.QLineEdit(self.Settings_2)
        self.rightdT.setGeometry(QtCore.QRect(190, 90, 61, 21))
        self.rightdT.setAlignment(QtCore.Qt.AlignCenter)
        self.rightdT.setObjectName("rightdT")
        self.label_13 = QtWidgets.QLabel(self.Settings_2)
        self.label_13.setGeometry(QtCore.QRect(260, 90, 21, 16))
        self.label_13.setObjectName("label_13")
        self.rightBr = QtWidgets.QLineEdit(self.Settings_2)
        self.rightBr.setGeometry(QtCore.QRect(190, 120, 61, 21))
        self.rightBr.setAlignment(QtCore.Qt.AlignCenter)
        self.rightBr.setObjectName("rightBr")
        self.label_14 = QtWidgets.QLabel(self.Settings_2)
        self.label_14.setGeometry(QtCore.QRect(260, 120, 31, 16))
        self.label_14.setObjectName("label_14")
        self.label_4 = QtWidgets.QLabel(self.Settings_2)
        self.label_4.setGeometry(QtCore.QRect(80, 120, 101, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.leftBr = QtWidgets.QLineEdit(self.Settings_2)
        self.leftBr.setGeometry(QtCore.QRect(10, 120, 61, 21))
        self.leftBr.setAlignment(QtCore.Qt.AlignCenter)
        self.leftBr.setObjectName("leftBr")
        self.leftTau = QtWidgets.QLineEdit(self.Settings_2)
        self.leftTau.setGeometry(QtCore.QRect(10, 180, 61, 21))
        self.leftTau.setAlignment(QtCore.Qt.AlignCenter)
        self.leftTau.setObjectName("leftTau")
        self.label_7 = QtWidgets.QLabel(self.Settings_2)
        self.label_7.setGeometry(QtCore.QRect(80, 180, 101, 16))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.rightTau = QtWidgets.QLineEdit(self.Settings_2)
        self.rightTau.setGeometry(QtCore.QRect(190, 180, 61, 21))
        self.rightTau.setAlignment(QtCore.Qt.AlignCenter)
        self.rightTau.setObjectName("rightTau")
        self.label_15 = QtWidgets.QLabel(self.Settings_2)
        self.label_15.setGeometry(QtCore.QRect(260, 180, 21, 16))
        self.label_15.setObjectName("label_15")
        self.rightTau2 = QtWidgets.QLineEdit(self.Settings_2)
        self.rightTau2.setGeometry(QtCore.QRect(190, 210, 61, 21))
        self.rightTau2.setAlignment(QtCore.Qt.AlignCenter)
        self.rightTau2.setObjectName("rightTau2")
        self.label_16 = QtWidgets.QLabel(self.Settings_2)
        self.label_16.setGeometry(QtCore.QRect(260, 210, 21, 16))
        self.label_16.setObjectName("label_16")
        self.label_6 = QtWidgets.QLabel(self.Settings_2)
        self.label_6.setGeometry(QtCore.QRect(80, 210, 101, 16))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.leftTau2 = QtWidgets.QLineEdit(self.Settings_2)
        self.leftTau2.setGeometry(QtCore.QRect(10, 210, 61, 21))
        self.leftTau2.setAlignment(QtCore.Qt.AlignCenter)
        self.leftTau2.setObjectName("leftTau2")
        self.leftS = QtWidgets.QLineEdit(self.Settings_2)
        self.leftS.setGeometry(QtCore.QRect(10, 240, 61, 21))
        self.leftS.setAlignment(QtCore.Qt.AlignCenter)
        self.leftS.setObjectName("leftS")
        self.label_8 = QtWidgets.QLabel(self.Settings_2)
        self.label_8.setGeometry(QtCore.QRect(80, 240, 101, 16))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.rightS = QtWidgets.QLineEdit(self.Settings_2)
        self.rightS.setGeometry(QtCore.QRect(190, 240, 61, 21))
        self.rightS.setAlignment(QtCore.Qt.AlignCenter)
        self.rightS.setObjectName("rightS")
        self.rightTB = QtWidgets.QLineEdit(self.Settings_2)
        self.rightTB.setGeometry(QtCore.QRect(190, 270, 61, 21))
        self.rightTB.setAlignment(QtCore.Qt.AlignCenter)
        self.rightTB.setObjectName("rightTB")
        self.label_17 = QtWidgets.QLabel(self.Settings_2)
        self.label_17.setGeometry(QtCore.QRect(260, 270, 21, 16))
        self.label_17.setObjectName("label_17")
        self.label_5 = QtWidgets.QLabel(self.Settings_2)
        self.label_5.setGeometry(QtCore.QRect(80, 270, 101, 16))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.leftTB = QtWidgets.QLineEdit(self.Settings_2)
        self.leftTB.setGeometry(QtCore.QRect(10, 270, 61, 21))
        self.leftTB.setAlignment(QtCore.Qt.AlignCenter)
        self.leftTB.setObjectName("leftTB")
        self.leftrGG = QtWidgets.QLineEdit(self.Settings_2)
        self.leftrGG.setGeometry(QtCore.QRect(10, 320, 61, 21))
        self.leftrGG.setAlignment(QtCore.Qt.AlignCenter)
        self.leftrGG.setObjectName("leftrGG")
        self.label_12 = QtWidgets.QLabel(self.Settings_2)
        self.label_12.setGeometry(QtCore.QRect(80, 320, 101, 16))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.rightrGG = QtWidgets.QLineEdit(self.Settings_2)
        self.rightrGG.setGeometry(QtCore.QRect(190, 320, 61, 21))
        self.rightrGG.setAlignment(QtCore.Qt.AlignCenter)
        self.rightrGG.setObjectName("rightrGG")
        self.rightrRR = QtWidgets.QLineEdit(self.Settings_2)
        self.rightrRR.setGeometry(QtCore.QRect(190, 350, 61, 21))
        self.rightrRR.setAlignment(QtCore.Qt.AlignCenter)
        self.rightrRR.setObjectName("rightrRR")
        self.label_10 = QtWidgets.QLabel(self.Settings_2)
        self.label_10.setGeometry(QtCore.QRect(80, 350, 101, 16))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.leftrRR = QtWidgets.QLineEdit(self.Settings_2)
        self.leftrRR.setGeometry(QtCore.QRect(10, 350, 61, 21))
        self.leftrRR.setAlignment(QtCore.Qt.AlignCenter)
        self.leftrRR.setObjectName("leftrRR")
        self.leftE = QtWidgets.QLineEdit(self.Settings_2)
        self.leftE.setGeometry(QtCore.QRect(10, 380, 61, 21))
        self.leftE.setAlignment(QtCore.Qt.AlignCenter)
        self.leftE.setObjectName("leftE")
        self.label_11 = QtWidgets.QLabel(self.Settings_2)
        self.label_11.setGeometry(QtCore.QRect(80, 380, 101, 16))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.rightE = QtWidgets.QLineEdit(self.Settings_2)
        self.rightE.setGeometry(QtCore.QRect(190, 380, 61, 21))
        self.rightE.setAlignment(QtCore.Qt.AlignCenter)
        self.rightE.setObjectName("rightE")
        self.rightN = QtWidgets.QLineEdit(self.Settings_2)
        self.rightN.setGeometry(QtCore.QRect(190, 410, 61, 21))
        self.rightN.setAlignment(QtCore.Qt.AlignCenter)
        self.rightN.setObjectName("rightN")
        self.label_9 = QtWidgets.QLabel(self.Settings_2)
        self.label_9.setGeometry(QtCore.QRect(80, 410, 101, 16))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.leftN = QtWidgets.QLineEdit(self.Settings_2)
        self.leftN.setGeometry(QtCore.QRect(10, 410, 61, 21))
        self.leftN.setAlignment(QtCore.Qt.AlignCenter)
        self.leftN.setObjectName("leftN")
        self.leftNR0 = QtWidgets.QLineEdit(self.Settings_2)
        self.leftNR0.setGeometry(QtCore.QRect(10, 450, 61, 21))
        self.leftNR0.setAlignment(QtCore.Qt.AlignCenter)
        self.leftNR0.setObjectName("leftNR0")
        self.label_18 = QtWidgets.QLabel(self.Settings_2)
        self.label_18.setGeometry(QtCore.QRect(80, 450, 101, 16))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.rightNR0 = QtWidgets.QLineEdit(self.Settings_2)
        self.rightNR0.setGeometry(QtCore.QRect(190, 450, 61, 21))
        self.rightNR0.setAlignment(QtCore.Qt.AlignCenter)
        self.rightNR0.setObjectName("rightNR0")
        self.rightNR = QtWidgets.QLineEdit(self.Settings_2)
        self.rightNR.setGeometry(QtCore.QRect(190, 480, 61, 21))
        self.rightNR.setAlignment(QtCore.Qt.AlignCenter)
        self.rightNR.setObjectName("rightNR")
        self.label_19 = QtWidgets.QLabel(self.Settings_2)
        self.label_19.setGeometry(QtCore.QRect(80, 480, 101, 16))
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.leftNR = QtWidgets.QLineEdit(self.Settings_2)
        self.leftNR.setGeometry(QtCore.QRect(10, 480, 61, 21))
        self.leftNR.setAlignment(QtCore.Qt.AlignCenter)
        self.leftNR.setObjectName("leftNR")
        self.leftNG = QtWidgets.QLineEdit(self.Settings_2)
        self.leftNG.setGeometry(QtCore.QRect(10, 510, 61, 21))
        self.leftNG.setAlignment(QtCore.Qt.AlignCenter)
        self.leftNG.setObjectName("leftNG")
        self.label_20 = QtWidgets.QLabel(self.Settings_2)
        self.label_20.setGeometry(QtCore.QRect(80, 510, 101, 16))
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.rightNG = QtWidgets.QLineEdit(self.Settings_2)
        self.rightNG.setGeometry(QtCore.QRect(190, 510, 61, 21))
        self.rightNG.setAlignment(QtCore.Qt.AlignCenter)
        self.rightNG.setObjectName("rightNG")
        self.rightNGR = QtWidgets.QLineEdit(self.Settings_2)
        self.rightNGR.setGeometry(QtCore.QRect(190, 540, 61, 21))
        self.rightNGR.setAlignment(QtCore.Qt.AlignCenter)
        self.rightNGR.setObjectName("rightNGR")
        self.label_21 = QtWidgets.QLabel(self.Settings_2)
        self.label_21.setGeometry(QtCore.QRect(80, 540, 101, 16))
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.leftNGR = QtWidgets.QLineEdit(self.Settings_2)
        self.leftNGR.setGeometry(QtCore.QRect(10, 540, 61, 21))
        self.leftNGR.setAlignment(QtCore.Qt.AlignCenter)
        self.leftNGR.setObjectName("leftNGR")
        self.label_22 = QtWidgets.QLabel(self.Settings_2)
        self.label_22.setGeometry(QtCore.QRect(80, 570, 101, 16))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.rightSGSR = QtWidgets.QLineEdit(self.Settings_2)
        self.rightSGSR.setGeometry(QtCore.QRect(190, 570, 61, 21))
        self.rightSGSR.setAlignment(QtCore.Qt.AlignCenter)
        self.rightSGSR.setObjectName("rightSGSR")
        self.rightFRET = QtWidgets.QLineEdit(self.Settings_2)
        self.rightFRET.setGeometry(QtCore.QRect(190, 60, 61, 21))
        self.rightFRET.setAlignment(QtCore.Qt.AlignCenter)
        self.rightFRET.setObjectName("rightFRET")
        self.groupBox = QtWidgets.QGroupBox(Settings)
        self.groupBox.setGeometry(QtCore.QRect(310, 470, 181, 131))
        self.groupBox.setObjectName("groupBox")
        self.tauD0 = QtWidgets.QLineEdit(self.groupBox)
        self.tauD0.setGeometry(QtCore.QRect(80, 30, 71, 21))
        self.tauD0.setObjectName("tauD0")


        # generate combo box -> Drop down options
        self.polBox = QtWidgets.QComboBox(self.groupBox)
        self.polBox.addItem("Combined Polarization")
        self.polBox.addItem("Combined 50/50")
        self.polBox.addItem("Tau part 1")
        self.polBox.addItem("Tau part 2")
        self.polBox.move(0, 60)


        self.refreshButton = QtWidgets.QPushButton(self.groupBox)
        self.refreshButton.setGeometry(QtCore.QRect(110, 100, 71, 21))
        self.refreshButton.setObjectName('refreshButton')

        self.label_34 = QtWidgets.QLabel(self.groupBox)
        self.label_34.setGeometry(QtCore.QRect(10, 30, 58, 16))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.groupBox)
        self.label_35.setGeometry(QtCore.QRect(160, 30, 16, 16))
        self.label_35.setObjectName("label_35")
        self.Binning = QtWidgets.QGroupBox(Settings)
        self.Binning.setGeometry(QtCore.QRect(310, 10, 181, 101))
        self.Binning.setObjectName("Binning")
        self.BinSize = QtWidgets.QLineEdit(self.Binning)
        self.BinSize.setGeometry(QtCore.QRect(100, 30, 71, 21))
        self.BinSize.setObjectName("BinSize")
        self.BinOffset = QtWidgets.QLineEdit(self.Binning)
        self.BinOffset.setGeometry(QtCore.QRect(100, 60, 71, 21))
        self.BinOffset.setObjectName("BinOffset")
        self.label_23 = QtWidgets.QLabel(self.Binning)
        self.label_23.setGeometry(QtCore.QRect(20, 30, 58, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.Binning)
        self.label_24.setGeometry(QtCore.QRect(20, 60, 58, 16))
        self.label_24.setObjectName("label_24")
        self.CorFactor = QtWidgets.QGroupBox(Settings)
        self.CorFactor.setGeometry(QtCore.QRect(310, 110, 181, 351))
        self.CorFactor.setObjectName("CorFactor")
        self.gamma = QtWidgets.QLineEdit(self.CorFactor)
        self.gamma.setGeometry(QtCore.QRect(90, 30, 81, 21))
        self.gamma.setObjectName("gamma")
        self.beta = QtWidgets.QLineEdit(self.CorFactor)
        self.beta.setGeometry(QtCore.QRect(90, 60, 81, 21))
        self.beta.setObjectName("beta")
        self.label_25 = QtWidgets.QLabel(self.CorFactor)
        self.label_25.setGeometry(QtCore.QRect(20, 30, 58, 16))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.CorFactor)
        self.label_26.setGeometry(QtCore.QRect(20, 60, 58, 16))
        self.label_26.setObjectName("label_26")
        self.alpha = QtWidgets.QLineEdit(self.CorFactor)
        self.alpha.setGeometry(QtCore.QRect(90, 90, 81, 21))
        self.alpha.setObjectName("alpha")
        self.label_27 = QtWidgets.QLabel(self.CorFactor)
        self.label_27.setGeometry(QtCore.QRect(20, 90, 58, 16))
        self.label_27.setObjectName("label_27")
        self.delta = QtWidgets.QLineEdit(self.CorFactor)
        self.delta.setGeometry(QtCore.QRect(90, 120, 81, 21))
        self.delta.setObjectName("delta")
        self.label_28 = QtWidgets.QLabel(self.CorFactor)
        self.label_28.setGeometry(QtCore.QRect(20, 120, 58, 16))
        self.label_28.setObjectName("label_28")
        self.gGG = QtWidgets.QLineEdit(self.CorFactor)
        self.gGG.setGeometry(QtCore.QRect(90, 150, 81, 21))
        self.gGG.setObjectName("gGG")
        self.label_29 = QtWidgets.QLabel(self.CorFactor)
        self.label_29.setGeometry(QtCore.QRect(20, 150, 58, 16))
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.CorFactor)
        self.label_30.setGeometry(QtCore.QRect(20, 180, 58, 16))
        self.label_30.setObjectName("label_30")
        self.gRR = QtWidgets.QLineEdit(self.CorFactor)
        self.gRR.setGeometry(QtCore.QRect(90, 180, 81, 21))
        self.gRR.setObjectName("gRR")

        self.label_l1 = QtWidgets.QLabel(self.CorFactor)
        self.label_l1.setGeometry(QtCore.QRect(20, 210, 58, 16))
        self.label_l1.setObjectName("label_l1")
        self.l1 = QtWidgets.QLineEdit(self.CorFactor)
        self.l1.setGeometry(QtCore.QRect(90, 210, 81, 21))
        self.l1.setObjectName("l1")

        self.label_l2 = QtWidgets.QLabel(self.CorFactor)
        self.label_l2.setGeometry(QtCore.QRect(20, 240, 58, 16))
        self.label_l2.setObjectName("label_l2")
        self.l2 = QtWidgets.QLineEdit(self.CorFactor)
        self.l2.setGeometry(QtCore.QRect(90, 240, 81, 21))
        self.l2.setObjectName("l2")


        self.label_31 = QtWidgets.QLabel(self.CorFactor)
        self.label_31.setGeometry(QtCore.QRect(20, 270, 58, 16))
        self.label_31.setObjectName("label_31")
        self.aveBG = QtWidgets.QLineEdit(self.CorFactor)
        self.aveBG.setGeometry(QtCore.QRect(90, 270, 81, 21))
        self.aveBG.setObjectName("aveBG")
        self.label_32 = QtWidgets.QLabel(self.CorFactor)
        self.label_32.setGeometry(QtCore.QRect(20, 300, 58, 16))
        self.label_32.setObjectName("label_32")
        self.aveBR = QtWidgets.QLineEdit(self.CorFactor)
        self.aveBR.setGeometry(QtCore.QRect(90, 300, 81, 21))
        self.aveBR.setObjectName("aveBR")
        self.aveBR0 = QtWidgets.QLineEdit(self.CorFactor)
        self.aveBR0.setGeometry(QtCore.QRect(90, 325, 81, 21))
        self.aveBR0.setObjectName("aveBR0")
        self.label_33 = QtWidgets.QLabel(self.CorFactor)
        self.label_33.setGeometry(QtCore.QRect(20, 325, 58, 16))
        self.label_33.setObjectName("label_33")

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)
        Settings.setTabOrder(self.leftAlex, self.rightAlex)
        Settings.setTabOrder(self.rightAlex, self.leftFRET)
        Settings.setTabOrder(self.leftFRET, self.rightFRET)
        Settings.setTabOrder(self.rightFRET, self.leftdT)
        Settings.setTabOrder(self.leftdT, self.rightdT)
        Settings.setTabOrder(self.rightdT, self.leftBr)
        Settings.setTabOrder(self.leftBr, self.rightBr)
        Settings.setTabOrder(self.rightBr, self.leftTau)
        Settings.setTabOrder(self.leftTau, self.rightTau)
        Settings.setTabOrder(self.rightTau, self.leftTau2)
        Settings.setTabOrder(self.leftTau2, self.rightTau2)
        Settings.setTabOrder(self.rightTau2, self.leftS)
        Settings.setTabOrder(self.leftS, self.rightS)
        Settings.setTabOrder(self.rightS, self.leftTB)
        Settings.setTabOrder(self.leftTB, self.rightTB)
        Settings.setTabOrder(self.rightTB, self.leftrGG)
        Settings.setTabOrder(self.leftrGG, self.rightrGG)
        Settings.setTabOrder(self.rightrGG, self.leftrRR)
        Settings.setTabOrder(self.leftrRR, self.rightrRR)
        Settings.setTabOrder(self.rightrRR, self.leftE)
        Settings.setTabOrder(self.leftE, self.rightE)
        Settings.setTabOrder(self.rightE, self.leftN)
        Settings.setTabOrder(self.leftN, self.rightN)
        Settings.setTabOrder(self.rightN, self.leftNR0)
        Settings.setTabOrder(self.leftNR0, self.rightNR0)
        Settings.setTabOrder(self.rightNR0, self.leftNR)
        Settings.setTabOrder(self.leftNR, self.rightNR)
        Settings.setTabOrder(self.rightNR, self.leftNG)
        Settings.setTabOrder(self.leftNG, self.rightNG)
        Settings.setTabOrder(self.rightNG, self.leftNGR)
        Settings.setTabOrder(self.leftNGR, self.rightNGR)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Form"))
        self.Settings_2.setTitle(_translate("Settings", "Settings"))
        self.leftSGSR.setText(_translate("Settings", "-10"))
        self.label.setText(_translate("Settings", "< ALEX-2CDE <"))
        self.leftAlex.setText(_translate("Settings", "-1"))
        self.rightAlex.setText(_translate("Settings", "1000"))
        self.leftFRET.setText(_translate("Settings", "-1"))
        self.label_2.setText(_translate("Settings", "< FRET-2CDE <"))
        self.leftdT.setText(_translate("Settings", "-1"))
        self.label_3.setText(_translate("Settings", "< |TGX - TRR| <"))
        self.rightdT.setText(_translate("Settings", "1000"))
        self.label_13.setText(_translate("Settings", "ms"))
        self.rightBr.setText(_translate("Settings", "5000"))
        self.label_14.setText(_translate("Settings", "kHz"))
        self.label_4.setText(_translate("Settings", "< mol. Bright <"))
        self.leftBr.setText(_translate("Settings", "-1"))
        self.leftTau.setText(_translate("Settings", "-0.1"))
        self.label_7.setText(_translate("Settings", "< Tau_D(A) <"))
        self.rightTau.setText(_translate("Settings", "100"))
        self.label_15.setText(_translate("Settings", "ns"))
        self.rightTau2.setText(_translate("Settings", "100"))
        self.label_16.setText(_translate("Settings", "ns"))
        self.label_6.setText(_translate("Settings", "< Tau_A <"))
        self.leftTau2.setText(_translate("Settings", "-0.1"))
        self.leftS.setText(_translate("Settings", "-0.1"))
        self.label_8.setText(_translate("Settings", "< S <"))
        self.rightS.setText(_translate("Settings", "1.1"))
        self.rightTB.setText(_translate("Settings", "1000"))
        self.label_17.setText(_translate("Settings", "ms"))
        self.label_5.setText(_translate("Settings", "< TB <"))
        self.leftTB.setText(_translate("Settings", "0"))
        self.leftrGG.setText(_translate("Settings", "-5"))
        self.label_12.setText(_translate("Settings", "< rGG <"))
        self.rightrGG.setText(_translate("Settings", "5"))
        self.rightrRR.setText(_translate("Settings", "5"))
        self.label_10.setText(_translate("Settings", "< rRR <"))
        self.leftrRR.setText(_translate("Settings", "-5"))
        self.leftE.setText(_translate("Settings", "-0.1"))
        self.label_11.setText(_translate("Settings", "< E <"))
        self.rightE.setText(_translate("Settings", "1.1"))
        self.rightN.setText(_translate("Settings", "3000"))
        self.label_9.setText(_translate("Settings", "< N <"))
        self.leftN.setText(_translate("Settings", "-1"))
        self.leftNR0.setText(_translate("Settings", "-1"))
        self.label_18.setText(_translate("Settings", "< NR0 <"))
        self.rightNR0.setText(_translate("Settings", "3000"))
        self.rightNR.setText(_translate("Settings", "3000"))
        self.label_19.setText(_translate("Settings", "< NR <"))
        self.leftNR.setText(_translate("Settings", "-1"))
        self.leftNG.setText(_translate("Settings", "-1"))
        self.label_20.setText(_translate("Settings", "< NG <"))
        self.rightNG.setText(_translate("Settings", "3000"))
        self.rightNGR.setText(_translate("Settings", "3000"))
        self.label_21.setText(_translate("Settings", "< NG+NR <"))
        self.leftNGR.setText(_translate("Settings", "-1"))
        self.label_22.setText(_translate("Settings", "< NG/NR <"))
        self.rightSGSR.setText(_translate("Settings", "10"))
        self.rightFRET.setText(_translate("Settings", "1000"))
        self.groupBox.setTitle(_translate("Settings", "GroupBox"))
        self.tauD0.setText(_translate("Settings", "3.8"))
        self.label_34.setText(_translate("Settings", "TauD(0)"))
        self.label_35.setText(_translate("Settings", "ns"))
        self.Binning.setTitle(_translate("Settings", "Binning"))
        self.BinSize.setText(_translate("Settings", "0.033"))
        self.BinOffset.setText(_translate("Settings", "0.015"))
        self.label_23.setText(_translate("Settings", "Size"))
        self.label_24.setText(_translate("Settings", "Offset"))
        self.CorFactor.setTitle(_translate("Settings", "Correction Factors"))
        self.gamma.setText(_translate("Settings", "1"))
        self.beta.setText(_translate("Settings", "0"))
        self.label_25.setText(_translate("Settings", "Gamma"))
        self.label_26.setText(_translate("Settings", "Beta"))
        self.alpha.setText(_translate("Settings", "0"))
        self.label_27.setText(_translate("Settings", "Alpha"))
        self.delta.setText(_translate("Settings", "1"))
        self.label_28.setText(_translate("Settings", "Delta"))
        self.gGG.setText(_translate("Settings", "1"))
        self.label_29.setText(_translate("Settings", "g(GG)"))
        self.label_30.setText(_translate("Settings", "g(RR)"))
        self.gRR.setText(_translate("Settings", "1"))
        self.label_31.setText(_translate("Settings", "<BG>"))
        self.aveBG.setText(_translate("Settings", "0"))
        self.label_32.setText(_translate("Settings", "<html><head/><body><p>&lt;BR&gt;</p></body></html>"))
        self.aveBR.setText(_translate("Settings", "0"))
        self.aveBR0.setText(_translate("Settings", "0"))
        self.label_33.setText(_translate("Settings", "<BR0>"))

        self.label_l1.setText(_translate("Settings", "l1"))
        self.l1.setText(_translate("Settigns", "0"))
        self.label_l2.setText(_translate("Settings", "l2"))
        self.l2.setText(_translate("Settigns", "0"))

        self.refreshButton.setText('Refresh')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Settings = QtWidgets.QWidget()
    ui = Ui_Settings()
    ui.setupUi(Settings)
    Settings.show()
    sys.exit(app.exec_())
