import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QMainWindow, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap, QMovie
from PyQt6.QtCore import Qt, QSize


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Labels")

        self.message = QLabel("Hello!")
        self.message.setFont(QFont("Cantarell", 30))
        self.message.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.image = QLabel()
        self.image.setPixmap(QPixmap("../assets/foto1.png"))
        self.image.setFixedSize(QSize(400, 300))

        self.video = QLabel()
        movie = QMovie("../assets/video2.gif")
        self.video.setMovie(movie)
        self.video.setFixedSize(QSize(400, 300))
        movie.start()

        button = QPushButton("Click me!")
        button.clicked.connect(self.button_clicked)

        hlayout = QHBoxLayout()
        hlayout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.message)
        vlayout.addWidget(self.image)
        vlayout.addWidget(self.video)
        vlayout.addLayout(hlayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

    def button_clicked(self):
        self.setStyleSheet(
            "background: #663300;"
            "color: #FFFFFF;"
        )

        self.message.setText("Surprise!")
        self.image.setPixmap(QPixmap("../assets/foto2.png"))
        self.movie = QMovie("../assets/video1.gif")
        self.video.setMovie(self.movie)
        self.movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec())

































