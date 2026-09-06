import sys
from PyQt6.QtWidgets import(QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDockWidget, QFormLayout,
                            QLineEdit, QWidget, QPushButton, QSpinBox, QMessageBox, QToolBar)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabla de Inventario")
        self.setFixedSize(800, 600)
        self.setWindowTitle("Selección de Productos")
        self.setWindowIcon(QIcon("users.png"))

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setRowCount(6)
        self.table.setHorizontalHeaderLabels(["id_producto", "nombre", "precio", "stock", "categoría", "estado"])

        

