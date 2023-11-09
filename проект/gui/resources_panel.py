from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget,\
    QTableWidgetItem, QPushButton

from db.resources import ResourcesDatabase
from gui.resource_dialog import ResourceDialog
from models.reserve import Reserve


class ResourcesPanel(QWidget):
    warning_color = QColor("Red")

    def __init__(self, rod):
        super().__init__()
        self.rod = rod
        self.setLayout(QVBoxLayout())

        self.table = QTableWidget()
        self.layout().addWidget(self.table)

        add_res = QPushButton("Добавить в автомат кофе")
        add_res.clicked.connect(self.add_)
        self.layout().addWidget(add_res)

        del_res = QPushButton("Достать из автомата стакан кофе")
        del_res.clicked.connect(self.deduct)
        self.layout().addWidget(del_res)

        self.upd()

    def add_(self):
        place, res, kolvo = ResourceDialog.add_res()
        if all((place, res, kolvo)):
            ResourcesDatabase().supply(place, res, kolvo)
            self.rod.mes(f"Добавлено {kolvo} "
                                     f"{ResourcesDatabase().izm_(res)} "
                                     f"{res} в {place}")
        self.upd()

    def deduct(self):
        place, res, quantity = ResourceDialog.del_res()
        if all((place, res, quantity)):
            ResourcesDatabase().deduct(place, res, quantity)
            self.rod.mes(f"Убрано {quantity} "
                                     f"{ResourcesDatabase().izm_(res)} "
                                     f"{res} из {place}")
        self.upd()

    def refresh(self):
        self.upd()

    def upd(self):
        self.reser = Reserve()
        self.table.setColumnCount(len(self.reser.resources()))
        self.table.setHorizontalHeaderLabels(self.reser.resources())
        self.table.setRowCount(len(self.reser.places()))
        self.table.setVerticalHeaderLabels(self.reser.places())
        for row, place in enumerate(self.reser.places()):
            for col, res in enumerate(self.reser.resources()):
                stock, warning = self.reser.stock(place, res)
                item = QTableWidgetItem(str(stock))
                if warning:
                    item.setForeground(ResourcesPanel.warning_color)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)
        self.table.resizeColumnsToContents()

        self.table.resizeRowsToContents()
