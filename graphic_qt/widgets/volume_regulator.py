import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QSlider, QLabel, QMainWindow, QHBoxLayout
from PyQt6.QtGui import QPixmap


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Volume Regulator")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.setValue)

        self.label = QLabel()
        self.label.setPixmap(QPixmap("../assets/mute.png"))

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setValue(self, value):
        if value == 0:
            self.label.setPixmap(QPixmap("../assets/mute.png"))
        elif value <= 30:
            self.label.setPixmap(QPixmap("../assets/min.png"))
        elif value <= 60:
            self.label.setPixmap(QPixmap("../assets/med.png"))
        else:
            self.label.setPixmap(QPixmap("../assets/max.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



