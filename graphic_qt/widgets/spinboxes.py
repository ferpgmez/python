import sys
from PyQt6.QtCore import QDate, QDateTime, Qt, QTime
from PyQt6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDateTimeEdit, QDoubleSpinBox, QGroupBox, QHBoxLayout,
                             QLabel, QSpinBox, QTimeEdit, QVBoxLayout, QWidget)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.createSpinBoxes()
        self.createDateTimeEdits()
        self.createDoubleSpinBoxes()

        layout = QHBoxLayout()
        layout.addWidget(self.spinBoxesGroup)
        layout.addWidget(self.editsGroup)
        layout.addWidget(self.doubleSpinBoxesGroup)
        self.setLayout(layout)
        self.setWindowTitle("SpinBoxes")

    def createSpinBoxes(self):
        self.spinBoxesGroup = QGroupBox("SpinBoxes")

        integerLabel = QLabel("Enter a value between %d and %d:" % (-20, 20))
        integerSpinBox = QSpinBox()
        integerSpinBox.setRange(-20, 20)
        integerSpinBox.setSingleStep(1)
        integerSpinBox.setValue(0)

        zoomLabel = QLabel("Enter a zoom factor between %d and %d:" % (0, 1000))
        zoomSpinBox = QSpinBox()
        zoomSpinBox.setRange(0, 1000)
        zoomSpinBox.setSingleStep(10)
        zoomSpinBox.setSuffix("%")
        zoomSpinBox.setSpecialValueText("Automatic")
        zoomSpinBox.setValue(100)

        priceLabel = QLabel("Enter a price between %d and %d:" % (0, 999))
        priceSpinBox = QSpinBox()
        priceSpinBox.setRange(0, 999)
        priceSpinBox.setSingleStep(1)
        priceSpinBox.setPrefix("$")
        priceSpinBox.setValue(99)

        spinBoxLayout = QVBoxLayout()
        spinBoxLayout.addWidget(integerLabel)
        spinBoxLayout.addWidget(integerSpinBox)
        spinBoxLayout.addWidget(zoomLabel)
        spinBoxLayout.addWidget(zoomSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(priceSpinBox)
        self.spinBoxesGroup.setLayout(spinBoxLayout)

    def createDateTimeEdits(self):
        self.editsGroup = QGroupBox("Date and time spin boxes")

        dateLabel = QLabel()
        dateEdit = QDateEdit()
        dateEdit.setDateRange(QDate(2024, 1, 1), QDate(2025, 12, 31))
        dateLabel.setText("Appointment date (between %s and %s):" %
                          (dateEdit.minimumDate().toString(Qt.DateFormat.ISODate),
                           dateEdit.maximumDate().toString(Qt.DateFormat.ISODate)))

        timeLabel = QLabel()
        timeEdit = QTimeEdit(QTime.currentTime())
        timeEdit.setTimeRange(QTime(9, 0, 0, 0), QTime(16, 30, 0, 0))
        timeLabel.setText("Appointment time (between %s and %s):" %
                          (dateEdit.minimumTime().toString(Qt.DateFormat.ISODate),
                           dateEdit.maximumTime().toString(Qt.DateFormat.ISODate)))

        self.meetingLabel = QLabel()
        self.meetingEdit = QDateTimeEdit(QDateTime.currentDateTime())
        formatLabel = QLabel("Format string for meeting date and time:")

        formatComboBox = QComboBox()
        formatComboBox.addItem('yyyy-MM-dd hh:mm:ss (zzz \'ms\')')
        formatComboBox.addItem('hh:mm:ss MM/dd/yyyy')
        formatComboBox.addItem('hh:mm:ss dd/MM/yyyy')
        formatComboBox.addItem('hh:mm:ss')
        formatComboBox.addItem('hh:mm ap')
        formatComboBox.activated.connect(self.setFormatString)
        self.setFormatString(formatComboBox.currentText())

        editsLayout = QVBoxLayout()
        editsLayout.addWidget(dateLabel)
        editsLayout.addWidget(dateEdit)
        editsLayout.addWidget(timeLabel)
        editsLayout.addWidget(timeEdit)
        editsLayout.addWidget(self.meetingLabel)
        editsLayout.addWidget(self.meetingEdit)
        editsLayout.addWidget(formatLabel)
        editsLayout.addWidget(formatComboBox)
        self.editsGroup.setLayout(editsLayout)

    def setFormatString(self, formatString):
        self.meetingEdit.setDisplayFormat(formatString)

        if self.meetingEdit.displayedSections() and QDateTimeEdit.Section.DateSections_Mask:
            self.meetingEdit.setDateRange(QDate(2024, 1, 1), QDate(2025, 12, 31))
            self.meetingLabel.setText("Meeting date (between %s and %s):" %
                                      (self.meetingEdit.minimumDate().toString(Qt.DateFormat.ISODate),
                                       self.meetingEdit.maximumDate().toString(Qt.DateFormat.ISODate)))
        else:
            self.meetingEdit.setTimeRange(QTime(0, 7, 20, 0), QTime(21, 0, 0, 0))
            self.meetingLabel.setText("Meeting time (between %s and %s):" %
                                      (self.meetingEdit.minimumTime().toString(Qt.DateFormat.ISODate),
                                       self.meetingEdit.maximumTime().toString(Qt.DateFormat.ISODate)))

    def createDoubleSpinBoxes(self):
        self.doubleSpinBoxesGroup = QGroupBox("Double spin boxes")

        precisionLabel = QLabel("Number of decimal places to show:")
        precisionSpinBox = QSpinBox()
        precisionSpinBox.setRange(0, 100)
        precisionSpinBox.setValue(2)

        doubleLabel = QLabel("Enter a value between %d and %d:" % (-20, 20))
        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setRange(-20.0, 20.0)
        self.doubleSpinBox.setSingleStep(1.0)
        self.doubleSpinBox.setValue(0.0)

        scaleLabel = QLabel("Enter a scale factor between %d and %d:" % (0, 1000))
        self.scaleSpinBox = QDoubleSpinBox()
        self.scaleSpinBox.setRange(0.0, 1000.0)
        self.scaleSpinBox.setSingleStep(10.0)
        self.scaleSpinBox.setSuffix("%")
        self.scaleSpinBox.setSpecialValueText("No scalling")
        self.scaleSpinBox.setValue(100.0)

        priceLabel = QLabel("Enter a price between %d and %d:" % (0, 1000))
        self.priceSpinBox = QDoubleSpinBox()
        self.priceSpinBox.setRange(0.0, 1000.0)
        self.priceSpinBox.setSingleStep(1.0)
        self.priceSpinBox.setPrefix("$")
        self.priceSpinBox.setValue(99.99)

        precisionSpinBox.valueChanged.connect(self.changePrecision)

        spinBoxLayout = QVBoxLayout()
        spinBoxLayout.addWidget(precisionLabel)
        spinBoxLayout.addWidget(precisionSpinBox)
        spinBoxLayout.addWidget(doubleLabel)
        spinBoxLayout.addWidget(self.doubleSpinBox)
        spinBoxLayout.addWidget(scaleLabel)
        spinBoxLayout.addWidget(self.scaleSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(self.priceSpinBox)
        self.doubleSpinBoxesGroup.setLayout(spinBoxLayout)

    def changePrecision(self, decimals):
        self.doubleSpinBox.setDecimals(decimals)
        self.scaleSpinBox.setDecimals(decimals)
        self.priceSpinBox.setDecimals(decimals)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())






