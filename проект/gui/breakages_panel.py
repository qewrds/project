from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton

from db.breakages import BreakagesDatabase
from gui.breakage_window import BreakageWindow


class BreakagesPanel(QWidget):
    def __init__(self, rod):
        super().__init__()
        self.rod = rod

        self.db = BreakagesDatabase()

        self.setLayout(QVBoxLayout())

        self.b_list = QListWidget()
        self.b_list.itemDoubleClicked.connect(self.BreakageWindow)
        self.layout().addWidget(self.b_list)
        self.refresh()

        btn = QPushButton("Добавить поломку")
        btn.clicked.connect(self.addBreakage)
        self.layout().addWidget(btn)

    def addBreakage(self):
        breakage = BreakageWindow.getNewBreakageData()
        if breakage is not None:
            self.db.add(breakage)
            self.rod.mes(f"Поломка в {breakage.place} добавлена")
            self.refresh()

    def refresh(self):
        self.b_list.clear()
        for breakage in self.db.breakages():
            self.b_list.addItem(BreakagesListItem(breakage))

    def BreakageWindow(self):
        breakage = self.sender().selectedItems()[0].breakage
        fix = BreakageWindow.openFixWindow(breakage)
        if fix:
            self.db.fixed(breakage)
            self.rod.mes(f"Поломка в {breakage.place} устранена")
            self.refresh()


class BreakagesListItem(QListWidgetItem):
    def __init__(self, breakage):
        super().__init__()
        self._breakage = breakage
        self.setText(breakage.text)

    @property
    def breakage(self):
        return self._breakage
