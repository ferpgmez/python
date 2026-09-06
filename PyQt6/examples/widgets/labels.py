import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QMovie, QFont
from PyQt6.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()