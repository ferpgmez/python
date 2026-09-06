import sys
from PyQt6.QtWidgets import QApplication, QColorDialog, QFrame, QPushButton, QWidget
from PyQt6.QtGui import QColor


class ColorDialog(QWidget):
    def __init__(self):
        super().__init__()

        col = QColor(0, 0, 0)
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(130, 20, 100, 100)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Color Dialog')

    def showDialog(self):
        col = QColorDialog.getColor()
        if col:
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorDialog()
    ex.show()
    sys.exit(app.exec())