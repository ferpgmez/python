import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("../assets/lock.png"))

        heading = QLabel("Wellcome back")
        heading.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        heading.setObjectName("heading")

        subheading = QLabel("Please enter your email and password to login")
        subheading.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        subheading.setObjectName("subheading")

        self.email = QLineEdit(self)
        self.email.setPlaceholderText("Enter your email")
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Login")

        layout = QVBoxLayout(self)
        layout.addWidget(heading)
        layout.addWidget(subheading)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(self.btn_login)
        layout.addStretch()
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("login.qss").read_text())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

