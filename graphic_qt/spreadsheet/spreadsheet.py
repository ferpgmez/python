import sys
from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtGui import QColor, QIcon, QKeySequence, QPainter, QPixmap, QAction, QActionGroup
from PyQt6.QtWidgets import (QApplication, QColorDialog, QComboBox, QDialog, QFontDialog, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QToolBar, QVBoxLayout)
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog
from spreadsheetdelegate import SpreadsheetDelegate
from spreaddheetitem import SpreadSheetItem
from printview import PrintView
from util import encode_pos, decode_pos


class SpreadSheet(QMainWindow):

    dateFormats = ["dd/MM/yyyy", "yyyy/M/dd", "dd.MM.yyyy"]

    currentDateFormat = dateFormats[0]

    def __init__(self, rows, cols, parent=None):
        super().__init__(parent)

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.formulaInput = QLineEdit()
        self.cellLabel = QLabel(self.toolBar)
        self.cellLabel.setMinimumSize(80, 0)
        self.toolBar.addWidget(self.cellLabel)
        self.toolBar.addWidget(self.formulaInput)
        self.table = QTableWidget(rows, cols, self)
        for c in range(cols):
            character = chr(ord('A') + c)
            self.table.setHorizontalHeaderItem(c, QTableWidgetItem(self))

        self.table.setItemPrototype(self.table.item(rows - 1, cols - 1))
        self.table.setItemDelegate(SpreadsheetDelegate(self))
        self.createActions()
        self.updateColor(0)
        self.setupMenuBar()
        self.setupContents()
        self.setupContents()
        self.setupContextMenu()
        self.setCentralWidget(self.table)
        self.statusBar()
        self.table.currentItemChanged.connect(self.updateStatus)
        self.table.currentItemChanged.connect(self.updateColor)
        self.table.currentItemChanged.connect(self.updateLineEdit)
        self.table.itemChanged.connect(self.updateStatus)
        self.formulaInput.returnPressed.connect(self.returnPressed)
        self.table.itemChanged.connect(self.updateLineEdit)
        self.setWindowTitle("SpreadSheet")

    def createActions(self):
        self.cell_sumAction = QAction("Sum", self)
        self.cell_sumAction.triggered.connect(self.actionSum)

        self.cell_addAction = QAction("&Add", self)
        self.cell_addAction.setShortcut(Qt.Key.Key_Control + Qt.Key.Key_Plus)
        self.cell_addAction.triggered.connect(self.actionAdd)

        self.cell_subAction = QAction("&Subtract", self)
        self.cell_subAction.setShortcut(Qt.Key.Key_Control + Qt.Key.Key_Minus)
        self.cell_subAction.triggered.connect(self.actionSubtract)

        self.cell_mulAction = QAction("&Multiply", self)
        self.cell_mulAction.setShortcut(Qt.Key.Key_Control + Qt.Key.Key_Multiply)
        self.cell_mulAction.triggered.connect(self.actionMultiply)

        self.cell_divAction = QAction("&Divide", self)
        self.cell_divAction.setShortcut(Qt.Key.Key_Control + Qt.Key.Key_Divide)
        self.cell_divAction.triggered.connect(self.actionDivide)

        self.fontAction = QAction("&Font", self)
        self.fontAction.setShortcut(Qt.Key.Key_Control + Qt.Key.Key_F)
        self.fontAction.triggered.connect(self.selectFont)

        self.colorAction = QAction(QIcon(QPixmap(16, 16)), "Background &Color", self)
        self.colorAction.triggered.connect(self.selectColor)

        self.clearAction = QAction("&Clear", self)
        self.clearAction.setShortcut(Qt.Key.Key_Delete)
        self.clearAction.triggered.connect(self.clear)

        self.aboutSpreadSheet = QAction("&About", self)
        self.aboutSpreadSheet.triggered.connect(self.showAbout)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.setShortcut(QKeySequence.StandardKey.Quit)
        self.exitAction.triggered.connect(QApplication.instance().quit)

        self.printAction = QAction("&Print", self)
        self.printAction.setShortcut(QKeySequence.StandardKey.Print)
        self.printAction.triggered.connect(self.print_)

        self.firstSeparator = QAction(self)
        self.firstSeparator.setSeparator(True)

        self.secondSeparator = QAction(self)
        self.secondSeparator.setSeparator(True)

    def setupMenuBar(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.dateFormatMenu = self.fileMenu.addMenu("&Date Format")
        self.dateFormatGroup = QActionGroup(self)
        for f in self.dateFormats:
            action = QAction(f, self)
            action.setCheckable(True)
            action.triggered.connect(self.changeDateFormat)
            self.dateFormatGroup.addAction(action)
            if f == self.currentDateFormat:
                action.setChecked(True)

        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.exitAction)
        self.cellMenu = self.menuBar().addMenu("&Cell")
        self.cellMenu.addAction(self.cell_addAction)
        self.cellMenu.addAction(self.cell_subAction)
        self.cellMenu.addAction(self.cell_mulAction)
        self.cellMenu.addAction(self.cell_divAction)
        self.cellMenu.addAction(self.cell_sumAction)
        self.cellMenu.addSeparator()
        self.cellMenu.addAction(self.colorAction)
        self.cellMenu.addAction(self.fontAction)
        self.menuBar().addSeparator()
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenu.addAction(self.aboutSpreadSheet)

    def changeDateFormat(self):
        action = self.sender()
        oldFormat = self.currentDateFormat
        newFormat = self.currentDateFormat = action.text()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            date = QDate.fromString(item.text(), oldFormat)
            item.setText(date.toString(newFormat))

    def updateStatus(self, item):
        if item and item == self.table.currentItem():
            self.statusBar().showMessage(item.data(Qt.ItemDataRole.StatusTipRole), 1000)
            self.cellLabel.setText("Cell: (%s):" % encode_pos(self.table.row(item), self.table.column(item)))

    def updateColor(self, item):
        pixmap = QPixmap(16, 16)
        color = QColor()
        if item:
            color = item.backgroundColor()
        if not color.isValid():
            color = self.palette().base().color()
        painter = QPainter(pixmap)
        painter.fillRect(0, 0, 16, 16, color)
        lighter = color.lighter()
        painter.setPen(lighter)
        painter.drawPolyline(QPoint(0, 15), QPoint(0, 0), QPoint(15, 0))
        painter.setPen(color.darker())
        painter.drawPolyline(QPoint(1, 15), QPoint(15, 15), QPoint(15, 1))
        painter.end()
        self.colorAction.setIcon(QIcon(pixmap))

    def updateLineEdit(self, item):
        if item != self.table.currentItem():
            return
        if item:
            self.formulaInput.setText(item.data(Qt.ItemDataRole.EditRole))
        else:
            self.formulaInput.clear()

    def returnPressed(self):
        text = self.formulaInput.text()
        row = self.table.currentRow()
        col = self.table.currentColumn()
        item = self.table.item(row, col)
        if not item:
            self.table.setItem(row, col, SpreadSheetItem(text))
        else:
            item.setData(Qt.ItemDataRole.EditRole, text)

    def selectColor(self):
        item = self.table.currentItem()
        color = item and QColor(item.background()) or self.table.palette().base().color()
        color = QColorDialog.getColor(color, self)
        if not color.isValid():
            return
        selected = self.table.selectedItems()
        if not selected:
            return
        for i in selected:
            i and i.setBackground(color)
        self.updateColor(self.table.currentItem())

    def selectFont(self):
        selected = self.table.selectedItems()
        if not selected:
            return
        font, ok = QFontDialog.getFont(self.font(), self)
        if not ok:
            return
        for i in selected:
            i and i.setFont(font)

    def runInputDialog(self, title, c1Text, c2Text, opText, outText, cell1, cell2, outCell):
        rows = []
        cols = []
        for r in range(self.table.rowCount()):
            rows.append(str(r + 1))
        for c in range(self.table.columnCount()):
            cols.append(chr(ord('A') + c))
        addDialog = QDialog(self)
        addDialog.setWindowTitle(title)
        group = QGroupBox(title, addDialog)
        group.setMinimumSize(250, 100)
        cell1Label = QLabel(c1Text, group)
        cell1RowInput = QComboBox(group)
        c1Row, c1Col = decode_pos(cell1)
        cell1RowInput.addItems(rows)
        cell1RowInput.setCurrentIndex(c1Row)
        cell1colInput = QComboBox(group)
        cell1colInput.addItems(cols)
        cell1colInput.setCurrentIndex(c1Col)
        operatorLabel = QLabel(opText, group)
        operatorLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        cell2Label = QLabel(c2Text, group)
        cell2RowInput = QComboBox(group)
        c2Row, c2Col = decode_pos(cell2)
        cell2RowInput.addItems(rows)
        cell2RowInput.setCurrentIndex(c2Row)
        cell2colInput = QComboBox(group)
        cell2colInput.addItems(cols)
        cell2colInput.setCurrentIndex(c2Col)
        equalsLabel = QLabel("=", group)
        equalsLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        outLabel = QLabel(outText, group)
        outRowInput = QComboBox(group)
        outRow, outCol = decode_pos(outCell)
        outRowInput.addItems(rows)
        outRowInput.setCurrentIndex(outRow)
        outColInput = QComboBox(group)
        outColInput.addItems(cols)
        outColInput.setCurrentIndex(outCol)

        cancelButton = QPushButton("Cancel", addDialog)
        cancelButton.clicked.connect(addDialog.reject)
        okButton = QPushButton("Ok", addDialog)
        okButton.setDefault(True)
        okButton.clicked.connect(addDialog.accept)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(okButton)
        buttonsLayout.addSpacing(10)
        buttonsLayout.addWidget(cancelButton)

        dialogLayout = QVBoxLayout(addDialog)
        dialogLayout.addWidget(group)
        dialogLayout.addStretch(1)
        dialogLayout.addItem(buttonsLayout)

        cell1Layout = QHBoxLayout()
        cell1Layout.addWidget(cell1Label)
        cell1Layout.addSpacing(10)
        cell1Layout.addWidget(cell1colInput)
        cell1Layout.addWSpacing(10)
        cell1Layout.addWidget(cell1RowInput)

        cell2Layout = QHBoxLayout()
        cell2Layout.addWidget(cell2Label)
        cell2Layout.addSpacing(10)
        cell2Layout.addWidget(cell2colInput)
        cell2Layout.addWSpacing(10)
        cell2Layout.addWidget(cell2RowInput)

        











































