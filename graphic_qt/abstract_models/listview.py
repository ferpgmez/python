import sys
from PyQt6.QtCore import Qt, QAbstractListModel
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QListView, QWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout,
                             QVBoxLayout)
import json


class TodoModel(QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            _, text = self.todos[index.row()]
            return text
        if role == Qt.ItemDataRole.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return QIcon('../assets/tick.png')

    def rowCount(self, index):
        return len(self.todos)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("List View")

        self.todoView = QListView()
        btn_delete = QPushButton("Delete")
        btn_complete = QPushButton("Complete")
        self.todoInput = QLineEdit()
        btn_add = QPushButton("Add")

        btn_delete.clicked.connect(self.delete)
        btn_complete.clicked.connect(self.complete)
        btn_add.clicked.connect(self.add)

        self.todoView.setModel(TodoModel())

        hlayout = QHBoxLayout()
        hlayout.addWidget(btn_delete)
        hlayout.addSpacing(10)
        hlayout.addWidget(btn_complete)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.todoView)
        vlayout.addLayout(hlayout)
        vlayout.addSpacing(20)
        vlayout.addWidget(self.todoInput)
        vlayout.addWidget(btn_add)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

        self.model = TodoModel()
        self.load()
        self.todoView.setModel(self.model)

    def add(self):
        text = self.todoInput.text()
        if text:
            self.model.todos.append((False, text))
            self.model.layoutChanged.emit()
            self.todoInput.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            self.model.dataChanged.emit(index, index)
            self.todoView.clearSelection()
            self.save()

    def load(self):
        try:
            with open('todo.json', 'r') as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open('todo.json', 'w') as f:
            json.dump(self.model.todos, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



