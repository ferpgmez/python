import sys
from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtGui import QColor, QIcon, QKeySequence, QPainter, QPixmap,  QAction, QActionGroup
from PyQt6.QtWidgets import (QApplication, QColorDialog, QComboBox, QDialog, QFontDialog, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QTableWidgetItem, QTableWidget,
                             QToolBar, QVBoxLayout)
from spreadsheetdelegate import SpreadsheetDelegate
from spreadsheetitem import SpreadsheetItem
from printview import PrintView
from util import decode_pos, encode_pos


class SpreadSheet(QMainWindow):
    dateFormats = ["yyyy-MM-dd", "dd/MM/yyyy", "MM/dd/yyyy"]

    currentDateFormat = dateFormats[0]

    def __init__(self, rows, cols, parent=None):
        super().__init__(parent)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.formulaInput = QLineEdit()
        self.cellLabel = QLabel(self.toolbar)
        self.cellLabel.setMinimumSize(80, 0)
        self.toolbar.addWidget(self.cellLabel)
        self.toolbar.addWidget(self.formulaInput)
        self.table = QTableWidget(rows, cols, self)
        for c in range(cols):
            character = chr(ord('A') + c)
            self.table.setHorizontalHeaderItem(c, QTableWidgetItem(character))
        self.table.setItemPrototype(self.table.item(rows - 1, cols - 1))
        self.table.setItemDelegate(SpreadsheetDelegate(self))
        self.crateActions()
        self.updateColor(0)
        self.setUpMenuBar()
        self.setUpContents()
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
        self.cell_sumAction = QAction("sum", self)
        self.cell_sumAction.triggered.connect(self.actionSum)

        self.cell_addAction = QAction("&add", self)
        self.cell_addAction.setShortcut(Qt.Key.Key_Control | Qt.Key.Key_Plus)
        self.cell_addAction.triggered.connect(self.actionAdd)

        self.cell_subAction = QAction("&subtract", self)
        self.cell_subAction.setShortcut(Qt.Key.Key_Control | Qt.Key.Key_Minus)
        self.cell_subAction.triggered.connect(self.actionSubtract)

        self.cell_mulAction = QAction("&multiply", self)
        self.cell_mulAction.setShortcut(Qt.Key.Key_Control | Qt.Key.Key_multiply)
        self.cell_mulAction.triggered.connect(self.actionMultiply)

        self.cell_divAction = QAction("&divide", self)
        self.cell_divAction.setShortcut(Qt.Key.Key_Control | Qt.Key.Key_division)
        self.cell_divAction.triggered.connect(self.actionDivide)

        self.fontAction = QAction("&font", self)
        self.fontAction.setShortcut(Qt.Key.Key_Control | Qt.Key.Key_F)
        self.fontAction.triggered.connect(self.selectFont)

        self.colorAction = QAction(QIcon(QPixmap(16, 16)), "Background color...", self)
        self.colorAction.triggered.connect(self.selectColor)

        self.clearAction = QAction("&clear", self)
        self.clearAction.setShortcut(Qt.Key.Key_Delete)
        self.clearAction.triggered.connect(self.clear)

        self.aboutSpreadSheet = QAction("&about", self)
        self.aboutSpreadSheet.triggered.connect(self.showAbout)

        self.exitAction = QAction("&exit", self)
        self.exitAction.setShortcut(QKeySequence.StandardKey.Quit)
        self.exitAction.triggered.connect(QApplication.instance().quit)

        self.printAction = QAction("&print", self)
        self.printAction.setShortcut(QKeySequence.StandardKey.Print)
        self.printAction.triggered.connect(self.print_)

        self.firstSeparator = QAction(self)
        self.firstSeparator.setSeparator(True)

        self.secondSeparator = QAction(self)
        self.secondSeparator.setSeparator(True)

    def setupMenuBar(self):
        self.fileMenu = self.menuBar().addMenu("&file")
        self.dateFormatMenu = self.fileMenu.addMenu("&date format")
        self.dateFormatGroup = QActionGroup(self)
        for f in self.dateFormats:
            action = QAction(f, self)
            action.setCheckable(True)
            action.triggered.connect(self.changeDateFormat)
            self.dateFormatGroup.addAction(action)
            self.dateFormatMenu.addAction(action)
            if f == self.currentDateFormat:
                action.setChecked(True)
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.exitAction)
        self.cell_menu = self.menuBar().addMenu("&cell")
        self.cell_menu.addAction(self.cell_addAction)
        self.cell_menu.addAction(self.cell_subAction)
        self.cell_menu.addAction(self.cell_mulAction)
        self.cell_menu.addAction(self.cell_divAction)
        self.cell_menu.addAction(self.cell_sumAction)
        self.cell_menu.addSeparator()
        self.cell_menu.addAction(self.colorAction)
        self.cell_menu.addAction(self.fontAction)
        self.cell_menu.addSeparator()
        self.aboutMenu = self.menuBar().addMenu("&about")
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
            self.cellLabel.setText("Cell: (%s)" % encode_pos(self.table.row(item), self.table.column(item)))

    def updateColor(self, item):
        pixmap = QPixmap(16, 16)
        color = QColor()
        if item:
            color = item.backgroundColor()
        

