# 'GUI to get the input files and tracking dir for the on the fly burst version
#  Expected files are:
#  1. Root of the folder that shall be tracked (the one in which the .ht3 files will be inserted) /path/target_folder
#  2. A file containing the settings (excel?!) *.csv vs. *.xls
#  3. First correction file *.hhd
#  4. Second correction file *.hhd'


# PyQT imports
from PyQt5.QtWidgets import QGridLayout,  QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys

class File_DD_Dialog(QDialog):

    def __init__(self, parent=None):
        super(File_DD_Dialog, self).__init__(parent)
        self.setWindowTitle("Drag and Drop")
        self.setAcceptDrops(True)
        self.grid = QGridLayout()
        self.resize(250,200)


        # total 4 elements for 200 pixels -> boxes y coords -> 1. 1-50, 2. 51-101, 3. 102-152

        # build fields
        self.file1Widget = QLineEdit(self)
        self.file1Widget.setPlaceholderText('Select tracking folder')
        self.grid.addWidget(self.file1Widget,0,0)

        # build fields
        self.file2Widget = QLineEdit(self)
        self.file2Widget.setPlaceholderText('Select settings file')
        self.grid.addWidget(self.file2Widget,1,0)

        # build fields
        self.file3Widget = QLineEdit(self)
        self.file3Widget.setPlaceholderText('Select first hhd file')
        self.grid.addWidget(self.file3Widget,2,0)

        # build fiels
        self.file4Widget = QLineEdit(self)
        self.file4Widget.setPlaceholderText('Select second hhd file ')
        self.grid.addWidget(self.file4Widget,3,0)

        # Close with selection button
        self.select_button = QPushButton("OK")
        self.select_button.clicked.connect(self.ok_button_pressed)
        self.labelResult = QLabel()
        self.grid.addWidget(self.select_button, 10, 0, 1,2)

        # Buttons for file dialogs

        # First define a Folder Icon
        pixmapi = getattr(QStyle, 'SP_DirOpenIcon')
        icon = self.style().standardIcon(pixmapi)

        # File 1 Button
        self.file1Button = QPushButton('')
        self.file1Button.setIcon(icon)
        self.file1Button.clicked.connect(self.folder_button1_select)
        self.grid.addWidget(self.file1Button, 0,1)

        # File 2 Button
        self.file2Button = QPushButton('')
        self.file2Button.setIcon(icon)
        self.file2Button.clicked.connect(self.folder_button2_select)
        self.grid.addWidget(self.file2Button, 1,1)

        # File 3 Button
        self.file3Button = QPushButton('')
        self.file3Button.setIcon(icon)
        self.file3Button.clicked.connect(self.folder_button3_select)
        self.grid.addWidget(self.file3Button, 2,1)

        # file 4 Button
        self.file4Button = QPushButton('')
        self.file4Button.setIcon(icon)
        self.file4Button.clicked.connect(self.folder_button3_select)
        self.grid.addWidget(self.file4Button, 3,1)

        self.setLayout(self.grid)

    def folder_button1_select(self):
        self.first_file = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder")
        try: # if nothing selected the empty var won't have an index and the program will return (same below)
            self.file1Widget.setText(self.first_file)
        except IndexError:
            return

    def folder_button2_select(self):
        self.first_file = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select File", "", "*.csv;;*.xls")
        try:
            self.file2Widget.setText(self.first_file[0][0])
        except IndexError:
            return

    def folder_button3_select(self):
        self.first_file = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select File", "", "*.hhd")
        try:
            self.file3Widget.setText(self.first_file[0][0])
        except IndexError:
            return

    def folder_button4_select(self):
        self.first_file = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select File", "", "*.hhd")
        try:
            self.file4Widget.setText(self.first_file[0][0])
        except IndexError:
            return


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        # Define vertical coordinates for accepted boxes in a given file widget position
        # it does scale with the window size therefore coordinates as ranges are defined

        self.ycoord_range_pos1 = \
            [self.file1Widget.pos().y()+self.file1Widget.size().height()+10,
             self.file1Widget.pos().y()-self.file1Widget.size().height()-10]
        self.ycoord_range_pos2 = \
            [self.file2Widget.pos().y()+self.file2Widget.size().height()+10,
             self.file2Widget.pos().y()-self.file2Widget.size().height()-10]
        self.ycoord_range_pos3 = \
            [self.file3Widget.pos().y()+self.file3Widget.size().height()+10,
             self.file3Widget.pos().y()-self.file3Widget.size().height()-10]
        self.ycoord_range_pos4 = \
            [self.file4Widget.pos().y() + self.file4Widget.size().height() + 10,
             self.file4Widget.pos().y() - self.file4Widget.size().height() - 10]

        files = [u.toLocalFile() for u in event.mimeData().urls()]

        if event.pos().y() <= self.ycoord_range_pos1[0] and event.pos().y() > self.ycoord_range_pos1[1]:
            if files[0].endswith('.ht3'): # only if correct ht3 file type
                self.file1Widget.setText(files[0])
        elif event.pos().y() <= self.ycoord_range_pos2[0] and event.pos().y() >=  self.ycoord_range_pos2[1]:
            if files[0].endswith('.hhd'): # only if correct hhd file type
                self.file2Widget.setText(files[0])
        elif event.pos().y() <= self.ycoord_range_pos3[0] and event.pos().y() >= self.ycoord_range_pos3[1]:
            if files[0].endswith('.hhd'): # only if correct hhd file type
                self.file3Widget.setText(files[0])
        elif event.pos().y() <= self.ycoord_range_pos4[0] and event.pos().y() >= self.ycoord_range_pos4[1]:
            if files[0].endswith('.hhd'):  # only if correct hhd file type
                self.file4Widget.setText(files[0])

    def ok_button_pressed(self):
        # Store the selected file path's in a dictionary
        self.file_dir_dict = dict()
        self.file_dir_dict['Tracker'] = self.file1Widget.text()
        self.file_dir_dict['Settings'] = self.file2Widget.text()
        self.file_dir_dict['HHD1'] = self.file3Widget.text()
        self.file_dir_dict['HHD2'] = self.file4Widget.text()

        self.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationDisplayName("OTF_pyBat")
    #app.setWindowIcon(QtGui.QIcon('requirements/batIcon.png'))
    w = File_DD_Dialog()
    w.setWindowTitle('OTF-Bat')
    w.show()
    sys.exit(app.exec_())

