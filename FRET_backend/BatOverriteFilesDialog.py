from PyQt5.QtWidgets import QGridLayout,  QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys

class ask_override_files(QDialog):
    def __init__(self, parent=None):
        super(ask_override_files, self).__init__(parent)
        self.setWindowTitle('File conflict')
        self.grid = QGridLayout()
        self.resize(250, 250)
        self.setLayout(self.grid)

        self.current = 'Stop'


        radioButton = QRadioButton('Overwrite Files')
        radioButton.to_do = 'Overwrite Files'
        radioButton.toggled.connect(self.updataState)
        self.grid.addWidget(radioButton, 0, 0)

        radioButton = QRadioButton('Change Suffix')
        radioButton.to_do = 'Change Suffix'
        radioButton.toggled.connect(self.updataState)
        self.grid.addWidget(radioButton, 1, 0)

        # provide option to give new suffix
        self.suffix_box = QLineEdit()
        self.suffix_box.setPlaceholderText('NewSuffix')
        self.grid.addWidget(self.suffix_box,1,1)


        # Close with selection button
        select_button = QPushButton("OK")
        select_button.clicked.connect(self.ClickEvent)
        self.grid.addWidget(select_button, 2,0)

        # Close with stop button
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.StopPressEvent)
        self.grid.addWidget(stop_button, 2,1)

    def updataState(self):
        self.current = str(self.sender().to_do)

    def ClickEvent(self):
        # event for pressing OK button
        self.decision = self.current
        print(self.current)
        self.close()

    def StopPressEvent(self):
        # event for pressing stop button
        self.decision = 'Stop'
        self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen = ask_override_files()
    screen.show()
    sys.exit(app.exec_())