from PyQt5.QtWidgets import (
    QApplication, QDialog, QGridLayout, QLabel,
    QComboBox, QPushButton, QVBoxLayout
)
import sys

class ChannelSelectionWindow(QDialog):
    def __init__(self, parent=None):
        super(ChannelSelectionWindow, self).__init__(parent)
        self.setWindowTitle("Channel Selection")
        self.resize(300, 250)

        layout = QVBoxLayout()
        grid = QGridLayout()

        self.channel_dropdowns = []
        self.channel_list = ['Acceptor (1 or ||)', 'Donor (1 or ||)', 'Acceptor (2 or T)', 'Donor (2 or T)']
        self.dropdown_options = ["Channel 1", "Channel 2", "Channel 3", "Channel 4", "None"]
        self.channel_mapping = {}  # Final output: e.g. {1.0: 2.0, ...}

        # For mapping label → raw ID
        self.label_to_raw = {
            'Acceptor (1 or ||)': 1.0,
            'Donor (1 or ||)': 2.0,
            'Acceptor (2 or T)': 3.0,
            'Donor (2 or T)': 4.0
        }

        pre_selection = {
            'Acceptor (1 or ||)': 'Channel 1',
            'Donor (1 or ||)': 'Channel 2',
            'Acceptor (2 or T)': 'Channel 3',
            'Donor (2 or T)': 'Channel 4'
        }

        for i in range(4):
            label_text = self.channel_list[i]
            label = QLabel(label_text)

            dropdown = QComboBox()
            dropdown.addItems(self.dropdown_options)
            default_value = pre_selection.get(label_text, "None")
            if default_value in self.dropdown_options:
                dropdown.setCurrentIndex(self.dropdown_options.index(default_value))

            self.channel_dropdowns.append(dropdown)
            grid.addWidget(label, i, 0)
            grid.addWidget(dropdown, i, 1)

        layout.addLayout(grid)

        self.accept_button = QPushButton("Accept")
        self.accept_button.clicked.connect(self.on_accept)
        layout.addWidget(self.accept_button)

        self.setLayout(layout)

    def on_accept(self):
        # Create direct numerical mapping: e.g. 1.0 → 2.0
        self.channel_mapping = {}
        for i, label in enumerate(self.channel_list):
            dropdown_value = self.channel_dropdowns[i].currentText()
            if dropdown_value.startswith("Channel"):
                source = self.label_to_raw[label]
                target = float(dropdown_value.split()[-1])
                self.channel_mapping[source] = target

        print(self.channel_mapping)
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChannelSelectionWindow()
    window.exec_()