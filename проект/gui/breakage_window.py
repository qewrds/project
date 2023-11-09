from datetime import datetime
from os import path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFormLayout, QVBoxLayout, QComboBox, QTextEdit, \
    QDateTimeEdit, QPushButton, QLabel, QFileDialog

from db.places import PlacesDatabase
from gui.centrable import Centrable
from models.breakage import Breakage


class BreakageWindow(QDialog, Centrable):
    size = (400, 200)

    def __init__(self, new=False):
        super().__init__()

        self.acc = False
        self.load_im = False

        self.setWindowTitle("Новая поломка" if new else "Поломка")
        self.resize(*BreakageWindow.size)
        self.center()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignHCenter)

        FL = QFormLayout()
        self.layout().addLayout(FL)

        self.n_place = QComboBox()
        self.n_place.addItems(PlacesDatabase().places())
        FL.addRow("Место", self.n_place)

        self.n_time = QDateTimeEdit()
        self.n_time.setDateTime(datetime.now())
        self.n_time.setMaximumDateTime(datetime.now())
        FL.addRow("Время", self.n_time)

        self.n_des = QTextEdit()
        FL.addRow("Описание", self.n_des)

        self._im = QLabel("Нет изображения")
        self._im.setScaledContents(True)
        self.im_pixmap = QPixmap()
        self.loadImage(path.join('resources', 'placeholder.png'))
        self.layout().addWidget(self._im)

        if new:
            self.select_im = QPushButton("Выбрать изображение")
            self.select_im.clicked.connect(self.selectImage)
            self.layout().addWidget(self.select_im)

        btn = QPushButton("Добавить" if new else "Поломка устранена")
        btn.clicked.connect(self.proc)
        self.layout().addWidget(btn)

    @property
    def _datetime(self):
        return datetime.fromtimestamp(self.n_time.dateTime().toSecsSinceEpoch())

    def proc(self):
        self.acc = True
        self.close()

    def freeze(self):
        self.n_place.setEnabled(False)
        self.n_time.setEnabled(False)
        self.n_des.setEnabled(False)

    def fill(self, breakage):
        self.n_place.setCurrentText(breakage.place)
        self.n_time.setDateTime(breakage.time)
        self.n_des.setText(breakage.description)
        if breakage.image is not None:
            self.im_pixmap = breakage.image

    def selectImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Изображение поломки", '.',
                                                   "Файл изображения (*.png)")
        if file_name != "":
            self.load_im = True
            self.loadImage(file_name)

    def loadImage(self, file_path):
        self.im_pixmap.load(file_path)
        self.update()

    def paintEvent(self, event):
        self._im.setPixmap(self.im_pixmap)

    def resizeEvent(self, event):
        self._im.setMaximumSize(self.width(), self.height() * 0.6)

    @staticmethod
    def getNewBreakageData():
        break_w = BreakageWindow(True)
        break_w.exec()
        if break_w.acc:
            return Breakage(break_w.n_place.currentText(),
                            break_w._datetime,
                            break_w.n_des.toPlainText(),
                            break_w.im_pixmap
                            if break_w.load_im
                            else None)

    @staticmethod
    def openFixWindow(breakage):
        break_w = BreakageWindow()
        break_w.fill(breakage)
        break_w.freeze()
        break_w.exec()
        return break_w.acc
