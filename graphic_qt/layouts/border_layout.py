import sys
from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QLayout, QTextBrowser, QWidget, QWidgetItem, QMainWindow


class ItemWrapper:
    def __init__(self, i, p):
        self.item = i
        self.position = p


class BorderLayout(QLayout):
    West, East, South, North, Center = range(5)
    MinimumSize, SizeHint = range(2)

    def __init__(self, parent=None, margin=None, spacing=-1):
        super().__init__(parent)

        if margin is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.list = []

    def __del__(self):
        l = self.takeAt(0)
        while l is not None:
            l = self.takeAt(0)

    def addItem(self, item):
        self.add(item, self.West)

    def addWidget(self, widget, position):
        self.add(QWidgetItem(widget), position)

    def expandingDirections(self):
        return Qt.Orientation.Horizontal | Qt.Orientation.Vertical

    def hasHeightForWidth(self):
        return False

    def count(self):
        return len(self.list)

    def itemAt(self, index):
        if index < len(self.list):
            return self.list[index].item
        return None

    def minimumSize(self):
        return self.calculateSize(self.MinimumSize)

    def setGeometry(self, rect):
        center = None
        eastWidth = 0
        westWidth = 0
        nortHeight = 0
        southHeight = 0
        centerHeight = 0
        super().setGeometry(rect)

        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position
            if position == self.West:
                item.setGeometry(QRect(rect.x(), nortHeight, rect.width(), item.sizeHint().height()))
                nortHeight += item.geometry().height() + self.spacing()
            elif position == self.South:
                item.setGeometry(QRect(item.geometry().x(), item.geometry().y(), rect.width(), item.sizeHint().height()))
                southHeight += item.geometry().height() + self.spacing()
                item.setGeometry(QRect(rect.x(), rect.y() + rect.height() - southHeight + self.spacing(),
                                      item.geometry().width(), item.geometry().height()))
            elif position == self.Center:
                center = wrapper
        centerHeight = rect.height() - nortHeight - southHeight
        for wrapper in self.list:
            item = wrapper.item
            position = wrapper.position
            if position == self.West:
                item.setGeometry(QRect(rect.x(), nortHeight, item.geometry().width(), centerHeight))
                westWidth += item.geometry().width() + self.spacing()
            elif position == self.East:
                item.setGeometry(QRect(item.geometry().x(), item.geometry().y(), item.geometry().width(), centerHeight))
                eastWidth += item.geometry().width() + self.spacing()
                item.setGeometry(QRect(rect.x() + rect.width() - eastWidth + self.spacing(),
                                       nortHeight, item.geometry().width(), item.geometry().height()))
        if center:
            center.item.setGeometry(QRect(westWidth, nortHeight, rect.width() - westWidth - eastWidth, centerHeight))

    def sizeHint(self):
        return self.calculateSize(self.SizeHint)

    def takeAt(self, index):
        if 0 <= index <= len(self.list):
            layoutStruct = self.list.pop(index)
            return layoutStruct.item()
        return None

    def add(self, item, position):
        self.list.append(ItemWrapper(item, position))

    def calculateSize(self, sizeType):
        totalSize = QSize()
        for wrapper in self.list:
            position = wrapper.position
            itemSize = QSize()
            if sizeType == self.MinimumSize:
                itemSize = wrapper.item.minimumSize()
            else:
                itemSize = wrapper.item.sizeHint()

            if position in (self.North, self.South, self.Center):
                totalSize.setHeight(totalSize.height() + itemSize.height())
            if position in (self.West, self.East, self.Center):
                totalSize.setWidth(totalSize.width() + itemSize.width())
        return totalSize


class Window(QWidget):
    def __init__(self):
        super().__init__()

        centralWidget = QTextBrowser()
        centralWidget.setPlainText("Central widget")
        layout = BorderLayout()
        layout.addWidget(centralWidget, BorderLayout.Center)

        label_n = self.createLabel("North")
        layout.addWidget(label_n, BorderLayout.North)

        label_w = self.createLabel("West")
        layout.addWidget(label_w, BorderLayout.West)

        layout_e1 = self.createLabel("East 1")
        layout.addWidget(layout_e1, BorderLayout.East)

        layout_e2 = self.createLabel("East 2")
        layout.addWidget(layout_e2, BorderLayout.East)

        layout_s = self.createLabel("South")
        layout.addWidget(layout_s, BorderLayout.South)

        self.setLayout(layout)
        self.setWindowTitle("Border layout")

    @staticmethod
    def createLabel(text):
        label = QLabel(text)
        label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        return label


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())














