from enum import Enum

from PyQt5.QtWidgets import QDialog, QComboBox, QVBoxLayout, QPushButton, QSpinBox

from db.resources import ResourcesDatabase
from models.reserve import Reserve


class ResourceDialog(QDialog):
    class Types(Enum):
        ADD = 0
        DEL = 1

    def __init__(self, dialog_type: Types):
        super().__init__()
        self.acc = False
        self.type = dialog_type
        self.setWindowTitle("Автомат")
        self.setLayout(QVBoxLayout())
        self.resize(350, 150)

        res = Reserve()

        self._place = QComboBox()
        self._place.addItems(res.places())
        self.layout().addWidget(self._place)

        self._res = QComboBox()
        self._res.addItems(res.resources())
        self.layout().addWidget(self._res)

        self.num = QSpinBox()
        self._res.currentTextChanged.connect(self.upd)
        self._place.currentTextChanged.connect(self.upd)
        self.layout().addWidget(self.num)

        self.acc_btn = QPushButton(
            "Добавить" if dialog_type is ResourceDialog.Types.ADD else "Списать")
        self.acc_btn.clicked.connect(self.accp)
        self.layout().addWidget(self.acc_btn)

        self.upd()

    def accp(self):
        self.acc = True
        self.close()

    def upd(self):
        self.num.setMinimum(1)
        now_reserve, _ = Reserve().stock(self.place, self.resource)
        max_reserve = ResourcesDatabase().max_quantity(self.resource)
        if self.type is ResourceDialog.Types.ADD:
            max_value = max_reserve - now_reserve
        else:
            max_value = now_reserve
        self.num.setMaximum(max_value)
        if max_value == 0:
            self.acc_btn.setDisabled(True)
        else:
            self.acc_btn.setEnabled(True)

    @property
    def place(self):
        return self._place.currentText()

    @property
    def resource(self):
        return self._res.currentText()

    @property
    def quantity(self):
        return self.num.value()

    @staticmethod
    def add_res():
        wind = ResourceDialog(ResourceDialog.Types.ADD)
        wind.exec()
        if wind.acc:
            return wind.place, wind.resource, wind.quantity
        return None, None, None

    @staticmethod
    def del_res():
        wind = ResourceDialog(ResourceDialog.Types.DEL)
        wind.exec()
        if wind.acc:
            return wind._place.currentText(),\
                   wind._res.currentText(),\
                   wind.num.value()
        return None, None, None
