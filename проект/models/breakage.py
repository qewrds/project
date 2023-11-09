from datetime import datetime

from PyQt5.QtCore import QByteArray, QBuffer
from PyQt5.QtGui import QPixmap


class Breakage:
    def __init__(self, place, time, description, image: QPixmap = None, id_=None):
        self._place = place
        self._time = time
        self._des = description
        self._im = image
        self._id = id_

    @property
    def place(self):
        return self._place

    @property
    def time(self):
        return self._time

    @property
    def description(self):
        return self._des

    @property
    def text(self):
        return f"{self.place}\n{self.description}"

    @property
    def image(self):
        return self._im

    @property
    def id(self):
        return self._id

    @staticmethod
    def from_db(data: tuple):
        idx, place, time, des, im_bytes = data
        im = None
        if im_bytes is not None and len(im_bytes) > 0:
            im = QPixmap()
            im.loadFromData(QByteArray(im_bytes), "PNG")
        return Breakage(place, datetime.fromtimestamp(time),
                        des, im, idx)

    def to_db(self):
        im_bytes = QByteArray()
        if self.image is not None:
            buf = QBuffer(im_bytes)
            self.image.save(buf, "PNG")
        return {"place": self.place,
                "time": self.time.timestamp(),
                "desc": self.description,
                "image_bytes": im_bytes.data(),
                "id": self.id}
