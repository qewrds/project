from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, \
    QListWidgetItem, QDialog, QFormLayout, QLineEdit

from db.places import PlacesDatabase, PlaceAlreadyExistsError
from gui.centrable import Centrable


class PlacesWindow(QWidget, Centrable):
    def __init__(self, rod):
        super().__init__()
        self.main_window = rod
        self.setWindowTitle("Изменение расположения")
        self.center()
        self.setLayout(QVBoxLayout())

        self.places_list = QListWidget()
        self.places_list.itemDoubleClicked.connect(self.DelDialog)
        self.layout().addWidget(self.places_list)
        self.upd()

        btn = QPushButton("Новое место")
        btn.clicked.connect(self.AddDialog)
        self.layout().addWidget(btn)

    def DelDialog(self):
        place = self.sender().selectedItems()[0].place
        dialog = DeletionDialog(self, place)
        dialog.exec()
        self.upd()

    def AddDialog(self):
        dialog = AddingDialog(self)
        dialog.exec()
        self.upd()

    def upd(self):
        self.places_list.clear()
        for place in PlacesDatabase().places():
            self.places_list.addItem(PlacesListItem(place))
        self.main_window.refresh()

    def mes(self, mes):
        self.main_window.mes(mes)

    def problem(self, mes):
        self.main_window.problem(mes)


class PlacesListItem(QListWidgetItem):
    def __init__(self, place):
        super().__init__()
        self._place = place
        self.setText(place)

    @property
    def place(self):
        return self._place


class DeletionDialog(QDialog):
    def __init__(self, rod, place):
        super().__init__(rod)
        self._place = place

        self.resize(300, 80)
        self.setWindowTitle(place)
        self.setLayout(QVBoxLayout())

        btn = QPushButton("Удалить место")
        btn.clicked.connect(self.now_delete)
        self.layout().addWidget(btn)

    def now_delete(self):
        PlacesDatabase().delete(self._place)
        self.mes(f"Место {self._place} удалено из БД")
        self.close()

    def mes(self, mes):
        self.parent().mes(mes)


class AddingDialog(QDialog):
    def __init__(self, rod):
        super().__init__(rod)

        self.resize(300, 120)
        self.setWindowTitle("Новое место")
        self.setLayout(QFormLayout())

        self._name_ = QLineEdit()
        self._name_.setPlaceholderText("Название")
        self.layout().addRow(self._name_)

        btn = QPushButton("Создать")
        btn.clicked.connect(self.now_add)
        self.layout().addRow(btn)

    def now_add(self):
        try:
            PlacesDatabase().add(self.name1)
            self.mes(f"Место {self.name1} добавлено в базу данных")
        except PlaceAlreadyExistsError:
            self.problem(f"Место {self.name1} уже существует")
        self.close()

    @property
    def name1(self):
        return self._name_.text()

    def problem(self, mes):
        self.parent().problem(mes)

    def mes(self, mes):
        self.parent().mes(mes)
