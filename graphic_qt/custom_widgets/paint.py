import sys
from PyQt6.QtCore import QPoint, QPointF, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel


class PaintWidget(QLabel):
    def __init__(self, width, height, background="white"):
        super().__init__()

        pixmap = QPixmap(width, height)
        painter = QPainter(pixmap)
        brush = QBrush()
        brush.setColor(QColor(background))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.fillRect(0, 0, pixmap.width(), pixmap.height(), brush)
        painter.end()
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self._pen_color = QColor("#000000")
        self._pen_width = 4

    def setPenColor(self, c):
        self._pen_color = QColor(c)

    def setPenWidth(self, w):
        self._pen_width = int(w)

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.position().x()
            self.last_y = e.position().y()
            return

        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        p = painter.pen()
        p.setWidth(self._pen_width)
        p.setColor(self._pen_color)
        painter.setPen(p)
        painter.drawLine(
            QPointF(self.last_x, self.last_y),
            QPointF(e.position().x(), e.position().y()),
        )
        painter.end()
        self.setPixmap(pixmap)

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self._flood_fill_from_event(e)

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def _flood_fill_from_event(self, e):
        image = self.pixmap().toImage()
        w, h = image.width(), image.height()
        x, y = e.position().x(), e.position().y()

        target_color = image.pixel(x, y)
        have_seen = set()
        queue = [(x, y)]

        def get_cardinal_points(have_seen, center_pos):
            points = []
            cx, cy = center_pos
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                xx, yy = cx + x, cy + y
                if 0 <= xx < w and 0 <= yy < h and (xx, yy) not in have_seen:
                    points.append((xx, yy))
                    have_seen.add((xx, yy))
            return points

        pixmap = self.pixmap()
        painter = QPainter(pixmap)
        painter.setPen(QPen(self._pen_color))

        while queue:
            x, y = queue.pop()
            if image.pixel(x, y) == target_color:
                painter.drawPoint(x, y)
                queue.extend(get_cardinal_points(have_seen, (x, y)))

        self.setPixmap(pixmap)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        paint = PaintWidget(300, 300)
        paint.setPenWidth(5)
        paint.setPenColor("#eb5160")
        self.setCentralWidget(paint)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



























