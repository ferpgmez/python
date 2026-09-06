import sys
import random
from PyQt6.QtCore import QRect, QRectF, QSize, Qt, QTimer
from PyQt6.QtGui import QBrush, QColor, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget


class EqualizerBar(QWidget):
    def __init__(self, bars, steps):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        if isinstance(steps, list):
            self.n_steps = len(steps)
            self.steps = steps
        elif isinstance(steps, int):
            self.n_steps = steps
            self.steps = ["red"] * steps
        else:
            raise TypeError("steps must be a list or an int")

        self.n_bars = bars
        self._x_solid_percent = 0.8
        self._y_solid_percent = 0.8
        self._background_color = QColor("black")
        self._padding = 25

        self._timer = None
        self.setDecayFrequencyMs(100)
        self._decay = 10

        self._vmin = 0
        self._vmax = 100
        self._values = [0.0] * bars

    def paintEvent(self, e):
        painter = QPainter(self)

        brush = QBrush()
        brush = QBrush(self._background_color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        d_height = painter.device().height() - 2 * self._padding
        d_width = painter.device().width() - 2 * self._padding

        step_y = d_height / self.n_steps
        bar_height = step_y * self._y_solid_percent
        bar_height_space = step_y * (1 - self._x_solid_percent) / 2

        step_x = d_width / self.n_bars
        bar_width = step_x * self._x_solid_percent
        bar_width_space = step_x * (1 - self._y_solid_percent) / 2

        for b in range(self.n_bars):
            pc = (self._values[b] - self._vmin) / (self._vmax - self._vmin)
            n_steps_to_draw = int(pc * self.n_steps)
            for n in range(n_steps_to_draw):
                brush.setColor(QColor(self.steps[n]))
                rect = QRectF(
                    self._padding + step_x * b + bar_width_space,
                    self._padding + d_height - (1 + n) * step_y + bar_height_space,
                    bar_width,
                    bar_height,
                )
                painter.fillRect(rect, brush)
        painter.end()

    def sizeHint(self):
        return QSize(20, 120)

    def _trigger_refresh(self):
        self.update()

    def setDecayFrequencyMs(self, ms):
        if self._timer:
            self._timer.stop()

        if ms:
            self._timer = QTimer(self)
            self._timer.setInterval(ms)
            self._timer.timeout.connect(self._decay_beat)
            self._timer.start()

    def _decay_beat(self):
        self._values = [max(0, v - self._decay) for v in self._values]
        self.update()

    def setValues(self, v):
        self._values = v
        self.update()

    def values(self):
        return self._values

    def setRange(self, vmin, vmax):
        assert float(vmin) < float(vmax)
        self._vmin , self._vmax = float(vmin), float(vmax)

    def setColor(self, color):
        self.steps = [color] * self._bar.n_steps
        self.update()

    def setColors(self, colors):
        self.n_steps = len(colors)
        self.steps = colors
        self.update()

    def setBarPadding(self, i):
        self._padding = int(i)
        self.update()

    def setBarSolidXPercent(self, f):
        self._x_solid_percent = float(f)
        self.update()

    def setBarSolidYPercent(self, f):
        self._y_solid_percent = float(f)
        self.update()

    def setBarBackgroundColor(self, color):
        self._background_color = QColor(color)
        self.update()


class Window (QMainWindow):
    def __init__(self):
        super().__init__()

        self.equalizer = EqualizerBar(
            5,
            [
                "#0C0786",
                "#40039C",
                "#6A00A7",
                "#8F0DA3",
                "#B02A8F",
                "#CA4678",
                "#E06461",
                "#F1824C",
                "#FCA635",
                "#FCCC25",
                "#EFF821",
            ],
        )
        self.equalizer.setBarSolidYPercent(0.4)
        self.setCentralWidget(self.equalizer)

        self._timer = QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self.update_values)
        self._timer.start()

    def update_values(self):
        self.equalizer.setValues(
            [min(100, v + random.randint(0, 50) if random.randint(0, 5) > 2 else v) for v in self.equalizer.values()]
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



























