import sys
from random import choice

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QDial, QSlider, QLCDNumber, QCompleter,
                             QGroupBox, QVBoxLayout, QHBoxLayout,QLineEdit)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        common_fruits = [
            "apple", "banana", "orange", "pineapple", "pear", "watermelon", "cherry", "grape", "strawberry",
            "raspberry", "peach", "mango", "kiwi", "papaya", "blueberry", "blackberry", "pomegranate",
            "avocado", "kiwifruit", "cantaloupe", "mangosteen", "honeydew", "coconut", "guava", "lychee",
        ]

        self.setWindowTitle("Connecting widgets example")

        title_label = QLabel("Connecting widgets example")
        title_label.setFont(QFont("Cantarell", 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        edits_groupbox = QGroupBox("Line edits")

        search = QLineEdit()
        search.setPlaceholderText("Enter a keyword to search for...")
        search.setClearButtonEnabled(True)
        label_search = QLabel()
        search.textChanged.connect(label_search.setText)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setClearButtonEnabled(True)
        self.lbl_password = QLabel()
        self.password.textChanged.connect(self.verify_password)

        fruits = QCompleter(common_fruits)
        fruits.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        fruits_edit = QLineEdit()
        fruits_edit.setCompleter(fruits)
        fruits_edit.setClearButtonEnabled(True)
        label_fruits = QLabel()
        fruits_edit.textChanged.connect(label_fruits.setText)

        edits_layout = QVBoxLayout()
        edits_layout.addWidget(search)
        edits_layout.addWidget(label_search)
        edits_layout.addWidget(self.password)
        edits_layout.addWidget(self.lbl_password)
        edits_layout.addWidget(fruits_edit)
        edits_layout.addWidget(label_fruits)
        edits_groupbox.setLayout(edits_layout)

        sliders_groupbox = QGroupBox("Sliders")

        sld_hor = QSlider(Qt.Orientation.Horizontal)
        sld_hor.setRange(0, 100)
        sld_hor.setTickPosition(QSlider.TickPosition.TicksBelow)
        sld_hor.setSingleStep(1)
        self.lbl_sld_hor = QLabel()
        sld_hor.valueChanged.connect(self.updateHor)

        sld_ver = QSlider(Qt.Orientation.Vertical)
        sld_ver.setRange(0, 100)
        sld_ver.setTickPosition(QSlider.TickPosition.TicksRight)
        sld_ver.setSingleStep(1)
        self.lbl_sld_ver = QLabel()
        sld_ver.valueChanged.connect(self.updateVer)

        sliders_layout = QHBoxLayout()
        sliders_layout.addWidget(sld_hor)
        sliders_layout.addWidget(self.lbl_sld_hor)
        sliders_layout.addWidget(sld_ver)
        sliders_layout.addWidget(self.lbl_sld_ver)
        sliders_groupbox.setLayout(sliders_layout)

        dial_groupbox = QGroupBox("Dials")

        lcd = QLCDNumber()
        lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        dial = QDial()
        dial.setNotchesVisible(True)
        dial.setRange(0, 100)
        dial.valueChanged.connect(lcd.display)

        dial_layout = QHBoxLayout()
        dial_layout.addWidget(dial)
        dial_layout.addWidget(lcd)
        dial_groupbox.setLayout(dial_layout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(edits_groupbox)
        hlayout.addWidget(sliders_groupbox)
        hlayout.addWidget(dial_groupbox)
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(hlayout)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def verify_password(self):
        if self.lbl_password.text() == "manolito":
            self.lbl_password.setText("Successfully logged")
            self.lbl_password.setStyleSheet("color: green")
            self.lbl_password.setFont(QFont("Cantarell", 12))
        else:
            self.lbl_password.setText("Incorrect password")
            self.lbl_password.setStyleSheet("color: red")
            self.lbl_password.setFont(QFont("Cantarell", 12))

    def updateHor(self, value):
        self.lbl_sld_hor.setText(f"Horizontal: {value}")

    def updateVer(self, value):
        self.lbl_sld_ver.setText(f"Vertical: {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())







