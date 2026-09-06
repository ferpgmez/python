import sys
from PyQt6.QtWidgets import QApplication, QWidget, QCalendarWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QDate


class Window(QWidget):
    def __init__(self):
        super().__init__()

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked.connect(self.showDate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())

        vbox = QVBoxLayout()
        vbox.addWidget(cal)
        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

    def showDate(self, date):
        self.lbl.setText(date.toString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
