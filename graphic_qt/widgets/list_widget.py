import sys
from PyQt6.QtWidgets import QInputDialog, QApplication, QWidget, QListWidget, QGridLayout, QPushButton, QMainWindow
from PyQt6.QtGui import QIcon
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("List widget")
        self.setWindowIcon(QIcon('../assets/ui-menu-blue.png'))

        self.list_widget = QListWidget()
        self.list_widget.addItems(["Learn Python", "Learn C++", "Learn Java", "Learn C#"])

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add)

        insert_button = QPushButton("Insert")
        insert_button.clicked.connect(self.insert)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)

        self.load()

        layout = QGridLayout()
        layout.addWidget(self.list_widget, 0, 0, 4, 1)
        layout.addWidget(add_button, 0, 1)
        layout.addWidget(insert_button, 1, 1)
        layout.addWidget(remove_button, 3, 1)
        layout.addWidget(clear_button, 4, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add(self):
        text, ok = QInputDialog.getText(self, "Add item", "Enter text:")
        if ok and text:
            self.list_widget.addItem(text)
            self.save()

    def insert(self):
        text, ok = QInputDialog.getText(self, "Insert item", "Enter text:")
        if ok and text:
            current_row = self.list_widget.currentRow()
            self.list_widget.insertItem(current_row + 1, text)
            self.save()

    def remove(self):
        current_row = self.list_widget.currentRow()
        if current_row >= 0:
            current_item = self.list_widget.takeItem(current_row)
            del current_item
            self.save()

    def clear(self):
        self.list_widget.clear()

    def load(self):
        try:
            with open('data.json', 'r') as f:
                self.list_widget.addItems(json.load(f))
        except Exception:
            pass

    def save(self):
        with open('data.json', 'w') as f:
            json.dump([item.text() for item in self.list_widget.items(0)], f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

