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

        self.decision = 'Stop'


        radioButton = QRadioButton('Overwrite Files')
        radioButton.to_do = 'Overwrite Files'
        radioButton.toggled.connect(self.updataState)
        self.grid.addWidget(radioButton, 0, 0)

        radioButton = QRadioButton('Change Suffix')
        radioButton.to_do = 'Change Suffix'
        radioButton.toggled.connect(self.updataState)
        self.grid.addWidget(radioButton, 1, 0)

        # provide option to give new suffix
        suffix_box = QLineEdit()
        suffix_box.setPlaceholderText('NewSuffix')
        self.grid.addWidget(suffix_box,1,1)


        # Stop is the default state
        radioButton = QRadioButton('Stop')
        radioButton.to_do = 'Stop'
        radioButton.setChecked(True)
        self.current = 'Stop'
        radioButton.toggled.connect(self.updataState)
        self.grid.addWidget(radioButton,2,0)

        # Close with selection button
        select_button = QPushButton("OK")
        select_button.clicked.connect(self.ClickEvent)
        labelResult = QLabel()
        self.grid.addWidget(select_button, 3,0)

    def updataState(self):
        self.current = str(self.sender().to_do)

    def ClickEvent(self):
        self.decision = self.current

app = QApplication(sys.argv)
screen = ask_override_files()
screen.show()
sys.exit(app.exec_())