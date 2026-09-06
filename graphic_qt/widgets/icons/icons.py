import sys
from fileinput import filename

from PIL.DdsImagePlugin import item1, item2
from PyQt6.QtCore import QFileInfo, QRegularExpression, QSize, Qt
from PyQt6.QtGui import QIcon, QImage, QPalette, QPixmap, QAction, QActionGroup
from PyQt6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFileDialog, QFrame, QGridLayout, QGroupBox,
                             QHBoxLayout, QHeaderView, QItemDelegate, QLabel, QMainWindow, QMessageBox, QRadioButton,
                             QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSpinBox, QStyleFactory,
                             QStyle)


class IconSizeSpinBox(QSpinBox):
    @staticmethod
    def valueFromText(text):
        regExp = QRegularExpression("(\\d+)(\\s*[xx]\\s*\\d+)?")
        if regExp.match(text):
            return int(regExp.cap(1))
        else:
            return 0

    @staticmethod
    def textFromValue(value):
        return "%dx%d" % (value, value)


class ImageDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        comboBox = QComboBox(parent)
        if index.column() == 1:
            comboBox.addItem("Normal")
            comboBox.addItem("Active")
            comboBox.addItem("Disabled")
            comboBox.addItem("Selected")
        elif index.column() == 2:
            comboBox.addItem("Off")
            comboBox.addItem("On")

        comboBox.activated.connect(self.emitCommitData)
        return comboBox

    def setEditorData(self, editor, index):
        comboBox = editor
        if not comboBox:
            return
        pos = comboBox.findText(index.model().data(index), Qt.MatchFlag.MatchExactly)
        comboBox.setCurrentIndex(pos)

    def setModelData(self, editor, model, index):
        comboBox = editor
        if not comboBox:
            return
        model.setData(index, comboBox.currentText())

    def emitCommitData(self):
        self.commitData.emit(self.sender())


class IconPreviewArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)

        self.icon = QIcon()
        self.size = QSize()
        self.stateLabels = []
        self.modeLabels = []
        self.pixmapLabels = []

        self.stateLabels.append(self.createHeaderLabel("Off"))
        self.stateLabels.append(self.createHeaderLabel("On"))

        self.modeLabels.append(self.createHeaderLabel("Normal"))
        self.modeLabels.append(self.createHeaderLabel("Active"))
        self.modeLabels.append(self.createHeaderLabel("Disabled"))
        self.modeLabels.append(self.createHeaderLabel("Selected"))

        for j, label in enumerate(self.stateLabels):
            mainLayout.addWidget(label, j + 1, 0)

        for i, label in enumerate(self.modeLabels):
            mainLayout.addWidget(label, 0, i + 1)
            self.pixmapLabels.append([])
            for j in range(len(self.stateLabels)):
                self.pixmapLabels[i].append(self.createPixmapLabel())
                mainLayout.addWidget(self.pixmapLabels[i][j], j + 1, i + 1)

    def setIcon(self, icon):
        self.icon = icon
        self.updatePixmapLabels()

    def setSize(self, size):
        if size != self.size:
            self.size = size
            self.updatePixmapLabels()

    @staticmethod
    def createHeaderLabel(text):
        label = QLabel("<b>%s</b>" % text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    @staticmethod
    def createPixmapLabel():
        label = QLabel()
        label.setEnabled(False)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFrameShape(QFrame.Shape.Box)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        label.setAutoFillBackground(True)
        label.setMinimumSize(132, 132)
        return label

    def updatePixmapLabels(self):
        for i in range(len(self.modeLabels)):
            if i == 0:
                mode = QIcon.Mode.Normal
            elif i == 1:
                mode = QIcon.Mode.Active
            elif i == 2:
                mode = QIcon.Mode.Disabled
            else:
                mode = QIcon.Mode.Selected

            for j in range(len(self.stateLabels)):
                state = QIcon.State.Off if j == 0 else QIcon.State.On
                pixmap = self.icon.pixmap(self.size, mode, state)
                self.pixmapLabels[i][j].setPixmap(pixmap)
                self.pixmapLabels[i][j].setEnabled(not pixmap.isNull())


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.createPreviewGroupBox()
        self.createImagesGroupBox()
        self.createIconSizeGroupBox()

        self.createActions()
        self.createMenus()
        self.createContextMenu()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.previewGroupBox, 0, 0, 1, 2)
        mainLayout.addWidget(self.imagesGroupBox, 1, 0)
        mainLayout.addWidget(self.iconSizeGroupBox, 1, 1)
        self.centralWidget.setLayout(mainLayout)

        self.setWindowTitle("Icons")
        self.checkCurrentStyle()
        self.otherRadioButton.click()
        self.resize(self.minimumSizeHint())

    def about(self):
        QMessageBox.about(self, "About Icons",
                          "The <b>Icons</b> example illustrates how Qt renders an icon "
                          "in different modes (active, normal, disabled and selected) "
                          "and states (on and off) based on a set of images.")

    def changeStyle(self, checked):
        if not checked:
            return
        action = self.sender()
        style = QStyleFactory.create(action.data())
        if not style:
            return
        QApplication.setStyle(style)

        self.setButtonText(self.smallRadioButton, "Small (%d x %d)", style, QStyle.PixelMetric.PM_SmallIconSize)
        self.setButtonText(self.largeRadioButton, "Large (%d x %d)", style, QStyle.PixelMetric.PM_LargeIconSize)
        self.setButtonText(self.toolBarRadioButton, "Tool bar (%d x %d)", style, QStyle.PixelMetric.PM_ToolBarIconSize)
        self.setButtonText(self.listViewRadioButton, "List view (%d x %d)", style, QStyle.PixelMetric.PM_ListViewIconSize)
        self.setButtonText(self.iconViewRadioButton, "Icon view (%d x %d)", style, QStyle.PixelMetric.PM_IconViewIconSize)
        self.setButtonText(self.tabBarRadioButton, "Tab bar (%d x %d)", style, QStyle.PixelMetric.PM_TabBarIconSize)
        self.changeSize()

    @staticmethod
    def setButtonText(button, label, syle, metric):
        metric_value = syle.pixelMetric(metric)
        button.setText(label % (metric_value, metric_value))

    def changeSize(self, checked=True):
        if not checked:
            return
        if self.otherRadioButton.isChecked():
            extent = self.otherSpinBox.value()
        else:
            if self.smallRadioButton.isChecked():
                metric = QStyle.PixelMetric.PM_SmallIconSize
            elif self.largeRadioButton.isChecked():
                metric = QStyle.PixelMetric.PM_LargeIconSize
            elif self.toolBarRadioButton.isChecked():
                metric = QStyle.PixelMetric.PM_ToolBarIconSize
            elif self.listViewRadioButton.isChecked():
                metric = QStyle.PixelMetric.PM_ListViewIconSize
            elif self.iconViewRadioButton.isChecked():
                metric = QStyle.PixelMetric.PM_IconViewIconSize
            else:
                metric = QStyle.PixelMetric.PM_TabBarIconSize
            extent = QApplication.style().pixelMetric(metric)

        self.previewArea.setSize(QSize(extent, extent))
        self.otherSpinBox.setEnabled(self.otherRadioButton.isChecked())

    def changeIcon(self):
        icon = QIcon()
        for row in range(self.imagesTable.rowCount()):
            item0 = self.imagesTable.item(row, 0)
            item1 = self.imagesTable.item(row, 1)
            item2 = self.imagesTable.item(row, 2)

            if item0.checkState() == Qt.CheckState.Checked:
                if item1.text() == "Normal":
                    mode = QIcon.Mode.Normal
                elif item1.text() == "Active":
                    mode = QIcon.Mode.Active
                elif item1.text() == "Disabled":
                    mode = QIcon.Mode.Disabled
                else:
                    mode = QIcon.Mode.Selected

                if item2.text() == "On":
                    state = QIcon.State.On
                else:
                    state = QIcon.State.Off

                filename = item0.data(Qt.ItemDataRole.UserRole)
                image = QImage(filename)
                if not image.isNull():
                    icon.addPixmap(QPixmap.fromImage(image), mode, state)

        self.previewArea.setIcon(icon)

    def addImage(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Open image", "",
                                                    "Images (*.png *.xpm *.jpg *.bmp);;All files (*)")
        for fileName in fileNames:
            row = self.imagesTable.rowCount()
            self.imagesTable.setRowCount(row + 1)

            imagesName = QFileInfo(fileName).baseName()
            item0 = QTableWidgetItem(imagesName)
            item0.setData(Qt.ItemDataRole.UserRole, fileName)
            item0.setFlags(item0.flags() and ~Qt.ItemFlag.ItemIsEditable)

            item1 = QTableWidgetItem("Normal")
            item2 = QTableWidgetItem("Off")

            if self.guessModeStateAct.isChecked():
                if '_act' in fileName:
                    item1.setText("Active")
                elif '_dis' in fileName:
                    item1.setText("Disabled")
                elif '_sel' in fileName:
                    item1.setText("Selected")

                if '_on' in fileName:
                    item2.setText("On")

            self.imagesTable.setItem(row, 0, item0)
            self.imagesTable.setItem(row, 1, item1)
            self.imagesTable.setItem(row, 2, item2)
            self.imagesTable.openPersistentEditor(item1)
            self.imagesTable.openPersistentEditor(item2)
            item0.setCheckState(Qt.CheckState.Checked)

    def removeAllImages(self):
        self.imagesTable.setRowCount(0)
        self.changeIcon()

    def createPreviewGroupBox(self):
        self.previewGroupBox = QGroupBox("Preview")
        self.previewArea = IconPreviewArea()
        layout = QVBoxLayout()
        layout.addWidget(self.previewArea)
        self.previewGroupBox.setLayout(layout)

    def createImagesGroupBox(self):
        self.imagesGroupBox = QGroupBox("Images")

        self.imagesTable = QTableWidget()
        self.imagesTable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.imagesTable.setItemDelegate(ImageDelegate(self))

        self.imagesTable.horizontalHeader().setDefaultSectionSize(90)
        self.imagesTable.setColumnCount(3)
        self.imagesTable.setHorizontalHeaderLabels(["Image", "Mode", "State"])
        self.imagesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.imagesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.imagesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.imagesTable.verticalHeader().hide()
        self.imagesTable.itemChanged.connect(self.changeIcon)

        layout = QVBoxLayout()
        layout.addWidget(self.imagesTable)
        self.imagesGroupBox.setLayout(layout)

    def createIconSizeGroupBox(self):
        self.iconSizeGroupBox = QGroupBox("Icon size")

        self.smallRadioButton = QRadioButton()
        self.largeRadioButton = QRadioButton()
        self.toolBarRadioButton = QRadioButton()
        self.listViewRadioButton = QRadioButton()
        self.iconViewRadioButton = QRadioButton()
        self.tabBarRadioButton = QRadioButton()
        self.otherRadioButton = QRadioButton("Other:")

        self.otherSpinBox = IconSizeSpinBox()
        self.otherSpinBox.setRange(8, 128)
        self.otherSpinBox.setValue(64)

        self.smallRadioButton.toggled.connect(self.changeSize)
        self.largeRadioButton.toggled.connect(self.changeSize)
        self.toolBarRadioButton.toggled.connect(self.changeSize)
        self.listViewRadioButton.toggled.connect(self.changeSize)
        self.iconViewRadioButton.toggled.connect(self.changeSize)
        self.tabBarRadioButton.toggled.connect(self.changeSize)
        self.otherRadioButton.toggled.connect(self.changeSize)
        self.otherSpinBox.valueChanged.connect(self.changeSize)

        otherSizeLayout = QHBoxLayout()
        otherSizeLayout.addWidget(self.otherRadioButton)
        otherSizeLayout.addWidget(self.otherSpinBox)
        otherSizeLayout.addStretch()

        layout = QGridLayout()
        layout.addWidget(self.smallRadioButton, 0, 0)
        layout.addWidget(self.largeRadioButton, 1, 0)
        layout.addWidget(self.toolBarRadioButton, 2, 0)
        layout.addWidget(self.listViewRadioButton, 0, 1)
        layout.addWidget(self.iconViewRadioButton, 1, 1)
        layout.addWidget(self.tabBarRadioButton, 2, 1)
        layout.addLayout(otherSizeLayout, 3, 0, 1, 2)
        layout.setRowStretch(4, 1)
        self.iconSizeGroupBox.setLayout(layout)

    def createActions(self):
        self.addImagesAct = QAction("&Add images...", self)
        self.addImagesAct.setShortcut("Ctrl+A")
        self.addImagesAct.triggered.connect(self.addImage)

        self.removeAllImagesAct = QAction("&Remove all images", self)
        self.removeAllImagesAct.setShortcut("Ctrl+R")
        self.removeAllImagesAct.triggered.connect(self.removeAllImages)

        self.exitAct = QAction("&Exit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.triggered.connect(self.close)

        self.styleActionGroup = QActionGroup(self)
        for styleName in QStyleFactory.keys():
            action = QAction(text="%s Style" % styleName, parent=self)
            action.setCheckable(True)
            action.triggered.connect(self.changeStyle)
            action.setData(styleName)
            self.styleActionGroup.addAction(action)

        self.guessModeStateAct = QAction("&Guess Image Mode/State", self)
        self.guessModeStateAct.setCheckable(True)
        self.guessModeStateAct.setChecked(True)

        self.aboutAct = QAction("&About", self)
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QAction("&About Qt", self)
        self.aboutQtAct.triggered.connect(QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.addImagesAct)
        self.fileMenu.addAction(self.removeAllImagesAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        for action in self.styleActionGroup.actions():
            self.viewMenu.addAction(action)
        self.viewMenu.addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createContextMenu(self):
        self.imagesTable.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.imagesTable.addAction(self.addImagesAct)
        self.imagesTable.addAction(self.removeAllImagesAct)

    def checkCurrentStyle(self):
        for action in self.styleActionGroup.actions():
            styleName = action.data()
            candidate = QStyleFactory.create(styleName)
            if candidate is None:
                return
            if candidate.metaObject().className() == QApplication.style().metaObject().className():
                action.trigger()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

































