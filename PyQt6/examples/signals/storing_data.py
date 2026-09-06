import sys
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QApplication)
from PyQt6.QtGui import QFont


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MyApp')
        self.button_is_checked = True

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.setChecked(self.button_is_checked)
        button.clicked.connect(self.the_button_was_toggled)
        self.layout = QVBoxLayout()
        self.layout.addWidget(button)
        self.setLayout(self.layout)

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print(self.button_is_checked)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

