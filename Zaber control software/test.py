"""
Zaber controller with PyQt5 GUI
"""

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QAction, QApplication,
                             QPushButton, QGridLayout, QProgressDialog, QLineEdit, QMessageBox, QLabel, QDialog)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from zaber_motion import Library
from zaber_motion.ascii import Connection
from zaber_motion import Units
from zaber_motion import CommandFailedException


class Example(QWidget):

    def __init__(self, device):
        super().__init__()
        # Get device and axis variables
        self.device = device
        self.XAxis = self.device.get_axis(1)
        self.YAxis = self.device.get_axis(2)

        # Relative home axis values
        self.homeX = 0.0
        self.homeY = 0.0

        # Timer variables
        self.numTimesInt = 1  # Number of times at each position

        self.initUI()

    def initUI(self):
        # Initilize grid layout and tooltip font
        grid = QGridLayout()
        grid.setSpacing(10)
        QToolTip.setFont(QFont('SansSerif', 10))

        # Limit axis values to integers
        onlyInt = QIntValidator(-150, 150, self)
        onlyIntTimer = QIntValidator(0, 5000, self)
        onlyIntTimerNum = QIntValidator(1, 10, self)

        # Initialize pushbuttons and text edits on the layout
        homeButton = QPushButton('Home')
        closeButton = QPushButton('Close connection')
        connectButton = QPushButton("Connect to device (unimplemented)")

        moveXPosLabel = QLabel("Move to X-Position")
        moveYPosLabel = QLabel("Move to Y-Position")

        self.currentPosition = QLabel("Current position (X,Y) : {} {}".format(self.XAxis.get_position(
            Units.LENGTH_MILLIMETRES), self.YAxis.get_position(Units.LENGTH_MILLIMETRES)))

        timerValueLabel = QLabel("Timer value (ms)")
        numPosLabel = QLabel("Number of positions")

        # Set custom home co-ordinates
        setHomeButton = QPushButton("Set as home co-ordinates")

        # (Testing: Automate button for pre-defined automated stage movement)
        automateButton = QPushButton("Start automated movement")

        # Set integer validator for the line/text edits
        self.moveXPosEdit = QLineEdit()
        self.moveXPosEdit.setValidator(onlyInt)
        self.moveYPosEdit = QLineEdit()
        self.moveYPosEdit.setValidator(onlyInt)

        startPosLabel = QLabel("Start position")
        stopPosLabel = QLabel("Stop position")

        self.startPos = QLineEdit("A1")
        self.stopPos = QLineEdit("A2")

        # Timer for automated measurements
        self.timerValue = QLineEdit("5000")  # Wait time at each position (ms)
        self.timerValue.setValidator(onlyIntTimer)
        self.numTimes = QLineEdit("5")       # Number of positions
        self.numTimes.setValidator(onlyIntTimerNum)

        # Set tooltip for the homebutton and resize button to their text
        homeButton.setToolTip('Move axis to home position')
        homeButton.resize(homeButton.sizeHint())
        closeButton.resize(closeButton.sizeHint())

        # Add widgets to the main windows
        grid.addWidget(homeButton, 1, 0)
        grid.addWidget(connectButton, 2, 0)
        grid.addWidget(closeButton, 2, 1)

        grid.addWidget(moveXPosLabel, 3, 0)
        grid.addWidget(self.moveXPosEdit, 3, 1)

        grid.addWidget(moveYPosLabel, 4, 0)
        grid.addWidget(self.moveYPosEdit, 4, 1)

        grid.addWidget(self.currentPosition, 5, 0)

        grid.addWidget(setHomeButton, 6, 0)
        grid.addWidget(timerValueLabel, 6, 1)
        grid.addWidget(numPosLabel, 6, 2)

        grid.addWidget(automateButton, 7, 0)
        grid.addWidget(self.timerValue, 7, 1)
        grid.addWidget(self.numTimes, 7, 2)

        grid.addWidget(startPosLabel, 8, 0)
        grid.addWidget(stopPosLabel, 8, 1)
        grid.addWidget(self.startPos, 9, 0)
        grid.addWidget(self.stopPos, 9, 1)

        # Connect buttons to their corresponding signals
        homeButton.clicked.connect(self.moveToHomePos)
        closeButton.clicked.connect(self.closeConnection)

        self.moveXPosEdit.returnPressed.connect(self.moveXAxis)
        self.moveYPosEdit.returnPressed.connect(self.moveYAxis)

        self.stopPos.returnPressed.connect(self.automatedWellMove)

        setHomeButton.clicked.connect(self.setHomeCoord)
        automateButton.clicked.connect(self.automateMove)

        self.setLayout(grid)
        self.setGeometry(300, 400, 400, 300)

        self.setWindowTitle("Zaber stage test")
        self.show()

    def moveToHomePos(self):
        """
        Move the stage to home position

        """
        self.progress = QProgressDialog('Completing', None, 0, 0, self)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.show()
        self.device.all_axes.home()
        QCoreApplication.processEvents()
        self.progress.cancel()
        self.currentPosition.setText("Current position (X,Y) : {} {}".format(self.XAxis.get_position(
            Units.LENGTH_MILLIMETRES), self.YAxis.get_position(Units.LENGTH_MILLIMETRES)))

    def closeConnection(self):
        """
        Close connection to the stage controller - required before quitting

        """
        self.device.connection.close()
        self.msgBox = QMessageBox.about(
            self, 'Close connection', "Closed connection to the stage")
        QApplication.instance().quit()

    def moveXAxis(self):
        """
        Move X axis to the value set in the line edit
        """
        XAxisPos = int(self.moveXPosEdit.text())
        try:
            if (XAxisPos + self.XAxis.get_position(Units.LENGTH_MILLIMETRES) < 100 or XAxisPos + self.XAxis.get_position(Units.LENGTH_MILLIMETRES) > 0):
                self.XAxis.move_relative(XAxisPos, Units.LENGTH_MILLIMETRES)
                self.currentPosition.setText("Current position (X,Y) : {} {}".format(self.XAxis.get_position(
                    Units.LENGTH_MILLIMETRES), self.YAxis.get_position(Units.LENGTH_MILLIMETRES)))
        except CommandFailedException:
            alertDialog = QMessageBox()
            alertText = QLabel("Entered value is out of limits", alertDialog)
            alertDialog.setWindowTitle("Out of Bounds")
            alertDialog.exec_()

    def moveYAxis(self):
        """
        Move Y axis to the value set in the line edit
        """
        YAxisPos = int(self.moveYPosEdit.text())
        try:
            if (YAxisPos + self.YAxis.get_position(Units.LENGTH_MILLIMETRES) < 100 or YAxisPos + self.YAxis.get_position(Units.LENGTH_MILLIMETRES) > 0):
                self.YAxis.move_relative(YAxisPos, Units.LENGTH_MILLIMETRES)
                self.currentPosition.setText("Current position (X,Y) : {} {}".format(self.XAxis.get_position(
                    Units.LENGTH_MILLIMETRES), self.YAxis.get_position(Units.LENGTH_MILLIMETRES)))
        except CommandFailedException:
            alertDialog = QMessageBox()
            alertDialog.setText("Entered value is out of limits")
            alertDialog.setWindowTitle("Out of Bounds")
            alertDialog.exec_()

    def setHomeCoord(self):
        self.homeX = self.XAxis.get_position(Units.LENGTH_MILLIMETRES)
        self.homeY = self.YAxis.get_position(Units.LENGTH_MILLIMETRES)

    def automateMove(self):
        """Automated movement sub-procudure for timer  and movement calls"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.autoXAxis)
        self.numTimesInt = int(self.numTimes.text())
        self.timer.start(int(self.timerValue.text()))

    def autoXAxis(self):
        """Automated movement of X-axis"""
        self.XAxis.move_relative(9, Units.LENGTH_MILLIMETRES)
        self.updatePosition()
        self.numTimesInt -= 1
        if (self.numTimesInt == 0):
            self.timer.stop()

    def updatePosition(self):
        """Update text of absolute position of the axis"""
        self.currentPosition.setText("Current position (X,Y) : {} {}".format(self.XAxis.get_position(
            Units.LENGTH_MILLIMETRES), self.YAxis.get_position(Units.LENGTH_MILLIMETRES)))

    def automatedWellMove(self):
        self.startPosText = self.startPos.text()
        self.stopPosText = self.stopPos.text()
        
        self.startPosInt = self.convertWellToNumber(self.startPosText)
        self.stopPosInt = self.convertWellToNumber(self.stopPosText)
        

        quo = (self.stopPosInt // 12) 

        if quo == 0:
            while self.stopPosInt != 0:
                self.stopPosInt -= 1
                self.moveWellRight()
            
        else:
            while (self.stopPosInt % 12 or self.stopPosInt % 24 or self.stopPosInt % 36 or self.stopPosInt % 96) != 0:               
                print(self.stopPosInt)
                self.moveWellRight()
                self.stopPosInt -= 1
            self.moveWellDown()

    def convertWellToNumber(self,wellName):
        """
        Convert well identifier to number
        Taken from: https://github.com/CyrusK/96-Well-Plate.py
        """
        (rowIndex, colIndex) = (0,0)

        for i in range(0, len(wellName)):
            (left, right) = (wellName[:i], wellName[i:i+1])
            if right.isdigit():
                (rowIndex, colIndex) = (left, wellName[i:])
                break

        ascii_value = ord(rowIndex) - 65

        return ascii_value*(8+(4*i)) + int(colIndex)

    def moveWellRight(self):
        self.XAxis.move_relative(9,Units.LENGTH_MILLIMETRES)
        self.updatePosition()
        
    def moveWellDown(self):
        self.XAxis.move_relative(-9*11, Units.LENGTH_MILLIMETRES)
        self.YAxis.move_relative(9, Units.LENGTH_MILLIMETRES)
        self.updatePosition()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # device = 'test'
    Library.enable_device_db_store()
    with Connection.open_serial_port("COM3") as connection:
        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))
        device = device_list[1]
        ex = Example(device)
        sys.exit(app.exec_())

    # ex = Example(device)
    # sys.exit(app.exec_())


if __name__ == "__main__":
    main()
