import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QColor

colors = ["#00cc99", "#ff66ff", "#00ccff", "#ff6600", "#996633", "#6699ff", "#ff3300", "#99ff66", "#00cc99"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Single signal")
        self.button = QPushButton("Click me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.button.setStyleSheet(f"background-color: {random.choice(colors)}")
        self.button.setText("Clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



