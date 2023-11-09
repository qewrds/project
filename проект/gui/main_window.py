from PyQt5.QtWidgets import QTabWidget, QMainWindow, QMenuBar

from gui.places_window import PlacesWindow
from gui.resources_panel import ResourcesPanel
from gui.breakages_panel import BreakagesPanel
from gui.resources_window import ResourcesWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Автоматы с кофе")
        self.showMaximized()

        self.c_widget = CentralWidget(self)
        self.setCentralWidget(self.c_widget)

        self.places_w = PlacesWindow(self)
        self.res_w = ResourcesWindow(self)

        menu_bar = QMenuBar()
        places_menu = menu_bar.addMenu("Изменение данных")
        places_menu.addAction("Изменение расположения")\
            .triggered.connect(self.editPlaces)
        places_menu.addAction("Изменение кофе")\
            .triggered.connect(self.editRes)
        self.setMenuBar(menu_bar)

    def refresh(self):
        self.c_widget.refresh()

    def problem(self, mes):
        self.statusBar().setStyleSheet("color : red")
        self.statusBar().showMessage(mes, 6000)

    def mes(self, mes):
        self.statusBar().setStyleSheet("color : black")
        self.statusBar().showMessage(mes, 3000)

    def editPlaces(self):
        self.places_w.show()

    def editRes(self):
        self.res_w.show()


class CentralWidget(QTabWidget):
    def __init__(self, rod):
        super().__init__(rod)

        self.res_panel = ResourcesPanel(self)
        self.addTab(self.res_panel, "Кол-во стаканчиков кофе в автоматах")

        self.breakages_panel = BreakagesPanel(self)
        self.addTab(self.breakages_panel, "Поломки")

        self.mes("Готов к работе")

    def mes(self, mes):
        self.parent().mes(mes)

    def refresh(self):
        self.res_panel.refresh()
        self.breakages_panel.refresh()
