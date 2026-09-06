import sys
from random import choice
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QColor, QFont

colors = ["#00cc99", "#ff66ff", "#00ccff", "#ff6600", "#996633", "#6699ff", "#ff3300", "#99ff66", "#00cc99"]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = False
        self.setWindowTitle("Storing data")
        self.button = QPushButton("Click me!")
        self.button.setCheckable(True)
        self.button.setFixedSize(200, 50)
        self.button.setChecked(self.button_is_checked)
        self.button.clicked.connect(self.the_button_was_toggled)

        self.check_label = QLabel()
        font = QFont("Cantarell", 12)
        self.check_label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.check_label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def the_button_was_toggled(self, checked):
        self.button.setStyleSheet(f"background-color: {choice(colors)}")
        if checked:
            self.check_label.setText("Checked")
            self.check_label.setStyleSheet("")
        else:
            self.check_label.setText("Unchecked")
            self.check_label.setStyleSheet("color: red")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


