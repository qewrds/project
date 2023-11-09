from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidgetItem, \
    QListWidget, QDialog, QLineEdit, QSpinBox, QFormLayout

from db.resources import ResourcesDatabase, ResourceAlreadyExistsError
from gui.centrable import Centrable


class ResourcesWindow(QWidget, Centrable):
    def __init__(self, rod):
        super().__init__()
        self.window = rod
        self.setWindowTitle("Изменение типов кофе")
        self.center()
        self.setLayout(QVBoxLayout())

        self.res_list = QListWidget()
        self.res_list.itemDoubleClicked.connect(self.DelDialog)
        self.layout().addWidget(self.res_list)
        self.upd()

        btn = QPushButton("Новый тип кофе")
        btn.clicked.connect(self.AddDialog)
        self.layout().addWidget(btn)

    def DelDialog(self):
        res = self.sender().selectedItems()[0].resource
        dialog = DeletionDialog(self, res)
        dialog.exec()
        self.upd()

    def AddDialog(self):
        dialog = AddingDialog(self)
        dialog.exec()
        self.upd()

    def upd(self):
        self.res_list.clear()
        for resource in ResourcesDatabase().resources():
            self.res_list.addItem(ResourcesListItem(resource))
        self.window.refresh()

    def mes(self, mes):
        self.window.mes(mes)

    def problem(self, mes):
        self.window.problem(mes)


class ResourcesListItem(QListWidgetItem):
    def __init__(self, res):
        super().__init__()
        self._res = res
        self.setText(res)

    @property
    def resource(self):
        return self._res


class DeletionDialog(QDialog):
    def __init__(self, rod, res):
        super().__init__(rod)
        self._res = res

        self.resize(300, 80)
        self.setWindowTitle(res)
        self.setLayout(QVBoxLayout())

        btn = QPushButton("Удалить тип кофе")
        btn.clicked.connect(self.now_delete)
        self.layout().addWidget(btn)

    def now_delete(self):
        ResourcesDatabase().delete(self._res)
        self.mes(f"Кофе {self._res} удалено из базы данных")
        self.close()

    def mes(self, mes):
        self.parent().mes(mes)


class AddingDialog(QDialog):
    def __init__(self, rod):
        super().__init__(rod)

        self.resize(300, 120)
        self.setWindowTitle("Новый тип кофе")
        self.setLayout(QFormLayout())

        self.name = QLineEdit()
        self.name.setPlaceholderText("Название нового кофе")
        self.layout().addRow(self.name)

        self.max_kol = QSpinBox()
        self.max_kol.setMinimum(1)
        self.max_kol.setMaximum(2 ** 16)
        self.layout().addRow("Максимальный запас", self.max_kol)

        self.warning_kol = QSpinBox()
        self.warning_kol.setMinimum(1)
        self.warning_kol.setMaximum(2 ** 16)
        self.max_kol.valueChanged.connect(self.upd)
        self.layout().addRow("Граница допустимого запаса", self.warning_kol)

        self.izm = QLineEdit()
        self.izm.setPlaceholderText("Единицы измерения")
        self.layout().addRow(self.izm)

        btn = QPushButton("Создать")
        btn.clicked.connect(self.now_add)
        self.layout().addRow(btn)

        self.upd()

    def now_add(self):
        try:
            ResourcesDatabase().add(self.name1, self.max_kol_,
                                        self.warning_kol_, self.izm_)
            self.mes(f"Кофе {self.name1} добавлено в БД")
        except ResourceAlreadyExistsError:
            self.problem(f"Кофе {self.name1} уже существует!")
        self.close()

    def upd(self):
        self.warning_kol.setMaximum(self.max_kol.value())

    def mes(self, mes):
        self.parent().mes(mes)

    def problem(self, mes):
        self.parent().problem(mes)

    @property
    def name1(self):
        return self.name.text()

    @property
    def max_kol_(self):
        return self.max_kol.value()

    @property
    def warning_kol_(self):
        return self.warning_kol.value()

    @property
    def izm_(self):
        return self.izm.text()
