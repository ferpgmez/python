import sys
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QApplication, QBoxLayout, QCheckBox, QComboBox, QDial, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QScrollBar, QSlider, QSpinBox, QStackedWidget, QWidget)


class SliderGroup(QWidget):

    valueChanged = pyqtSignal(int)

    def __init__(self, orientation, title, parent=None):
        super().__init__(parent)

        self.slider = QSlider(orientation)
        self.slider.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)

        self.scrollBar = QScrollBar(orientation)
        self.scrollBar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.dial = QDial()
        self.dial.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.dial.setNotchesVisible(True)

        self.slider.valueChanged.connect(self.scrollBar.setValue)
        self.scrollBar.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.slider.setValue)

        self.dial.valueChanged.connect(self.valueChanged)

        if orientation == Qt.Orientation.Horizontal:
            direction = QBoxLayout.Direction.TopToBottom
        else:
            direction = QBoxLayout.Direction.LeftToRight

        slidersLayout = QBoxLayout(direction)
        slidersLayout.addWidget(self.slider)
        slidersLayout.addWidget(self.scrollBar)
        slidersLayout.addWidget(self.dial)
        self.setLayout(slidersLayout)

    def setValue(self, value):
        self.slider.setValue(value)

    def setMinimum(self, value):
        self.slider.setMinimum(value)
        self.scrollBar.setMinimum(value)
        self.dial.setMinimum(value)

    def setMaximum(self, value):
        self.slider.setMaximum(value)
        self.scrollBar.setMaximum(value)
        self.dial.setMaximum(value)

    def invertAppearance(self, invert):
        self.slider.setInvertedAppearance(invert)
        self.scrollBar.setInvertedAppearance(invert)
        self.dial.setInvertedAppearance(invert)

    def invertedKeyBindings(self, invert):
        self.slider.setInvertedControls(invert)
        self.scrollBar.setInvertedControls(invert)
        self.dial.setInvertedControls(invert)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.horizontalSliders = SliderGroup(Qt.Orientation.Horizontal, "Horizontal")
        self.verticalSliders = SliderGroup(Qt.Orientation.Vertical, "Vertical")

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.horizontalSliders)
        self.stackedWidget.addWidget(self.verticalSliders)

        self.createControls("Controls")

        self.horizontalSliders.valueChanged.connect(self.verticalSliders.setValue)
        self.verticalSliders.valueChanged.connect(self.valueSpinBox.setValue)
        self.valueSpinBox.valueChanged.connect(self.horizontalSliders.setValue)

        layout = QHBoxLayout()
        layout.addWidget(self.controlsGroup)
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

        self.minimumSpinBox.setValue(0)
        self.maximumSpinBox.setValue(20)
        self.valueSpinBox.setValue(5)

        self.setWindowTitle("Sliders")

    def createControls(self, title):
        self.controlsGroup = QGroupBox(title)

        minimumLabel = QLabel("Minimum value:")
        maximumLabel = QLabel("Maximum value:")
        valueLabel = QLabel("Current value:")

        invertAppearance = QCheckBox("Invert appearance")
        invertedKeyBindings = QCheckBox("Inverted key bindings")

        self.minimumSpinBox = QSpinBox()
        self.minimumSpinBox.setRange(-100, 100)
        self.minimumSpinBox.setSingleStep(1)

        self.maximumSpinBox = QSpinBox()
        self.maximumSpinBox.setRange(-100, 100)
        self.maximumSpinBox.setSingleStep(1)

        self.valueSpinBox = QSpinBox()
        self.valueSpinBox.setRange(-100, 100)
        self.valueSpinBox.setSingleStep(1)

        orientationCombo = QComboBox()
        orientationCombo.addItem("Horizontal slider-like widgets")
        orientationCombo.addItem("Vertical slider-like widgets")

        orientationCombo.activated.connect(self.stackedWidget.setCurrentIndex)
        self.minimumSpinBox.valueChanged.connect(self.horizontalSliders.setMinimum)
        self.minimumSpinBox.valueChanged.connect(self.verticalSliders.setMinimum)
        self.maximumSpinBox.valueChanged.connect(self.horizontalSliders.setMaximum)
        self.maximumSpinBox.valueChanged.connect(self.verticalSliders.setMaximum)
        invertAppearance.toggled.connect(self.horizontalSliders.invertAppearance)
        invertAppearance.toggled.connect(self.verticalSliders.invertAppearance)
        invertedKeyBindings.toggled.connect(self.horizontalSliders.invertedKeyBindings)
        invertedKeyBindings.toggled.connect(self.verticalSliders.invertedKeyBindings)

        controlsLayout = QGridLayout()
        controlsLayout.addWidget(minimumLabel, 0, 0)
        controlsLayout.addWidget(maximumLabel, 1, 0)
        controlsLayout.addWidget(valueLabel, 2, 0)
        controlsLayout.addWidget(self.minimumSpinBox, 0, 1)
        controlsLayout.addWidget(self.maximumSpinBox, 1, 1)
        controlsLayout.addWidget(self.valueSpinBox, 2, 1)
        controlsLayout.addWidget(invertAppearance, 0, 2)
        controlsLayout.addWidget(invertedKeyBindings, 1, 2)
        controlsLayout.addWidget(orientationCombo, 3, 0, 1, 3)

        self.controlsGroup.setLayout(controlsLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


