import sys
from random import choice
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont

colors = ["#44cc00", "#1a66ff", "#e600e6", "#ff6666", "#00ff00", "#cc9900", "#ff3300", "#e6e600", "#0099ff"]

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong',
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0

        self.setWindowTitle('My App')
        self.button = QPushButton("Click me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.counter_label = QLabel()
        font = QFont("Cantarell", 12)
        self.counter_label.setFont(font)

        self.title_label = QLabel()
        font = QFont("Cantarell", 12)
        self.title_label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.counter_label)
        layout.addWidget(self.title_label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def the_button_was_clicked(self):
        self.n_times_clicked += 1
        new_window_title = choice(window_titles)
        self.button.setStyleSheet(f"background-color: {choice(colors)}")
        self.setWindowTitle(new_window_title)
        self.counter_label.setText(f'Clicked {self.n_times_clicked} times')

    def the_window_title_changed(self, window_title):
        self.title_label.setText(window_title)
        if window_title == 'Something went wrong':
            self.title_label.setStyleSheet('color: red')
            self.button.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
