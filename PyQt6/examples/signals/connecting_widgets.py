import sys
from PyQt6.QtWidgets import QApplication, QDial, QLCDNumber, QHBoxLayout, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

        lcd = QLCDNumber(self)
        dial = QDial(self)

        dial.setNotchesVisible(True)
        dial.setRange(0, 360)
        lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)

        dial.valueChanged.connect(lcd.display)

        layout = QHBoxLayout(self)
        layout.addWidget(lcd)
        layout.addWidget(dial)
        self.setLayout(layout)

        self.setWindowTitle("Dial and LCD")
        self.resize(300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
