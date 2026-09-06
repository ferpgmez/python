from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableView


class PrintView(QTableView):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def print_(self, printer):
        self.resize(printer.width(), printer.height())
        self.render(printer)