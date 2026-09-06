from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem
from util import decode_pos


class SpreadsheetItem(QTableWidgetItem):
    def __init__(self, text=None):
        if text is not None:
            super().__init__(text)
        else:
            super().__init__()
        self.isResolving = False

    def clone(self):
        item = super().clone()
        item.isResolving = self.isResolving
        return item

    def formula(self):
        return self.data(Qt.ItemDataRole.DisplayRole)

    def data(self, role):
        if role in (Qt.ItemDataRole.EditRole, Qt.ItemDataRole.StatusTipRole):
            return self.formula()
        if role == Qt.ItemDataRole.DisplayRole:
            return self.display()
        t = str(self.display())
        try:
            number = int(t)
        except ValueError:
            number = None
        if role == Qt.ItemDataRole.ForegroundRole:
            if number is None:
                return QColor(Qt.GlobalColor.black)
            elif number < 0:
                return QColor(Qt.GlobalColor.red)
            return QColor(Qt.GlobalColor.blue)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return super().data(role)

    def setData(self, role, value):
        super().setData(role, value)
        if self.tableWidget():
            self.tableWidget().viewport().update()

    def display(self):
        if self.isResolving:
            return None
        self.isResolving = True
        result = self.computeFormula(self.formula(), self.tableWidget())
        self.isResolving = False
        return result

    def computeFormula(self, formula, widget):
        if formula is None:
            return None
        slist = formula.split(' ')
        if not slist or not widget:
            return formula
        op = slist[0].lower()
        firstRow = -1
        firstCol = -1
        secondRow = -1
        secondCol = -1
        if len(slist) > 1:
            firstRow, firstCol = decode_pos(slist[1])
        if len(slist) > 2:
            secondRow, secondCol = decode_pos(slist[2])
        start = widget.item(firstRow, firstCol)
        end = widget.item(secondRow, secondCol)
        firstVal = 0
        try:
            firstVal = start and int(start.text()) or 0
        except ValueError:
            pass
        secondVal = 0
        try:
            secondVal = end and int(end.text()) or 0
        except ValueError:
            pass
        result = None
        if op == "sum":
            sum_ = 0
            for r in range(firstRow, secondRow + 1):
                for c in range(firstCol, secondCol + 1):
                    tableItem = widget.item(r, c)
                    if tableItem and tableItem != self:
                        try:
                            sum_ += int(tableItem.text())
                        except ValueError:
                            pass
            result = sum_
        elif op == "+":
            result = firstVal + secondVal
        elif op == "-":
            result = firstVal - secondVal
        elif op == "*":
            result = firstVal * secondVal
        elif op == "/":
            if secondVal == 0:
                result = "nan"
            else:
                result = firstVal / secondVal
        elif op == "=":
            if start:
                result = start.text()
            else:
                result = formula
        return result
