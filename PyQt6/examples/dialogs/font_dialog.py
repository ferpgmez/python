import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QSizePolicy, QVBoxLayout, QLabel, QFontDialog
from PyQt6.QtGui import QFont


class Window(QWidget):
    def __init__(self):
        super().__init__()

        btn = QPushButton("Dialog", self)
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(self.showDialog)

        self.lbl = QLabel("Knowledge only counts when you apply it.", self)

        vbox = QVBoxLayout()
        vbox.addWidget(btn)
        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setWindowTitle("Font Dialog")
        self.setGeometry(300, 300, 300, 200)

    def showDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
