import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog, QPushButton


class ColorButton(QPushButton):
    colorChanged = Signal(object)

    def __init__(self, color=None):
        super().__init__()
        self.setObjectName("ColorButton")
        self._color = None
        self._default = color
        self.pressed.connect(self.onColorPicker)
        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)
        if self._color:
            self.setStyleSheet(f"#ColorButton {{background-color: {self._color};}}")
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec():
            self.setColor(dlg.currentColor().name())

    def musePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.setColor(self._default)
        return super().mousePressEvent(e)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        palette = ColorButton(color="red")
        palette.colorChanged.connect(self.show_selected_color)
        self.setCentralWidget(palette)

    @staticmethod
    def show_selected_color(c):
        print("Selected {}".format(c))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



