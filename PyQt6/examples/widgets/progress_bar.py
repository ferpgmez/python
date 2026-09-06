import sys
from PyQt6.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QBasicTimer


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(10, 20, 300, 30)

        self.btn = QPushButton('Start', self)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        vbox = QVBoxLayout()
        vbox.addWidget(self.pbar)
        vbox.addWidget(self.btn)
        self.setLayout(vbox)

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step += 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


