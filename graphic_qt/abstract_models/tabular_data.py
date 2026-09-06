import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from datetime import datetime


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float):
                return "%.2f" % value
            if isinstance(value, str):
                return  '"%s"' % value
            return value
        if role == Qt.ItemDataRole.TextAlignmentRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, int) or isinstance(value, float):
                return Qt.AlignmentFlag.AlignRight + Qt.AlignmentFlag.AlignVCenter
        if role == Qt.ItemDataRole.ForegroundRole:
            value = self._data[index.row()][index.column()]
            if (isinstance(value, int) or isinstance(value, float)) and value < 0:
                return QtGui.QColor("red")
        if role == Qt.ItemDataRole.DecorationRole:
            colors = ["#00cc00", "#00ff00", "#99ff99", "#ccff99", "#ccffcc" "#ffffff",
                      "#ffcccc", "#ff9999", "#ff6699", "#ff3399", "#ff0066"]
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime):
                return QtGui.QIcon("../asets/calendar.png")
            if isinstance(value, bool):
                if value:
                    return QtGui.QIcon('../assets/tick.png')
                return QtGui.QIcon('../assets/cross.png')

            if isinstance(value, int) or isinstance(value, float):
                value = int(value)
                value = max(-5, value)
                value = min(5, value)
                value += 5
                return QtGui.QColor(colors[value])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = [
            [True, 0.5, "String", datetime(2022, 1, 1), -5],
            [3.256, 1.75, "Hello", False, datetime(2022, 1, 2)],
            [-2, 3, "World", True, datetime(2022, 1, 3)],
            [0, 0, " ", False, datetime(2022, 1, 4)],
            [1.269, 0, "", False, datetime(2022, 1, 5)],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())


            