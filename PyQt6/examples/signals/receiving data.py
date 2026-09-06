import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.btn = QPushButton("Click me")
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.the_button_was_clicked)
        self.btn.clicked.connect(self.the_button_was_toggled)

        self.lbl1 = QLabel('')
        self.lbl1.setFont(QFont("Arial", 16))

        self.lbl2 = QLabel('')
        self.lbl2.setFont(QFont("Arial", 16))
        self.resize(400, 200)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.btn)
        vlayout.addWidget(self.lbl1)
        vlayout.addWidget(self.lbl2)
        self.setLayout(vlayout)

        self.setWindowTitle("Receiving data")

    def the_button_was_clicked(self):
        self.lbl1.clear()
        if self.btn.isChecked():
            self.lbl1.setText("You clicked the button!")
        else:
            self.lbl1.setText("")

    def the_button_was_toggled(self, checked):
        self.lbl2.clear()
        if checked:
            self.lbl2.setText("Checked")
        else:
            self.lbl2.setText("Unchecked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


