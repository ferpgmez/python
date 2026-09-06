import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Click me")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)

        self.label = QLabel("")
        self.label.setFont(QFont("Arial", 16))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.resize(400, 300)

        self.setStyleSheet("""
        QWidget {
            background-color: #ffcc66;
        }
        QPushButton {
            background-color: #ff9933;
            color: #663300;
            border: 1px solid #663300;
            border-radius: 5px;
            height: 30px;
            text-align: center; 
        }
        QLabel {
            background-color: #ffcc66;
            color: #663300;   
        }
        """)

        self.setWindowTitle("Signals")

    def the_button_was_clicked(self):
        if self.button.isChecked():
            self.label.setText("Button is checked")
        else:
            self.label.setText("Button is not checked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

