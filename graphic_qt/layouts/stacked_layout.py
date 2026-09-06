import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedLayout, QVBoxLayout,
                             QWidget)
from layout_colorwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stacked layout")

        btn_red = QPushButton("Red")
        btn_red.clicked.connect(self.activate_tab_1)

        btn_green = QPushButton("Green")
        btn_green.clicked.connect(self.activate_tab_2)

        btn_blue = QPushButton("Blue")
        btn_blue.clicked.connect(self.activate_tab_3)

        layout = QHBoxLayout()
        layout.addWidget(btn_red)
        layout.addWidget(btn_green)
        layout.addWidget(btn_blue)

        self.stackLayout = QStackedLayout()
        self.stackLayout.addWidget(Color("red"))
        self.stackLayout.addWidget(Color("green"))
        self.stackLayout.addWidget(Color("blue"))

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.stackLayout)
        main_layout.addLayout(layout)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def activate_tab_1(self):
        self.stackLayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stackLayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stackLayout.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    

