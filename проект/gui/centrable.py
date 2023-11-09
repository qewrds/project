from PyQt5.QtWidgets import QDesktopWidget


class Centrable:
    def center(self):
        geo = self.frameGeometry()
        geo.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(geo.topLeft())
