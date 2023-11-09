from collections import defaultdict
from functools import reduce


from db.resources import ResourcesDatabase


class Reserve:
    def __init__(self):
        self._stockpile = defaultdict(dict)
        for place, res, _, warning, stock\
                in ResourcesDatabase().stocks():
            self._stockpile[place][res] = stock, stock < warning

    def places(self):
        return sorted(list(self._stockpile.keys()))

    def resources(self):
        return sorted(list(reduce(lambda x, y: x & y,
                                  map(lambda p: p.keys(), self._stockpile.values()))))

    def stock(self, place, res):
        return self._stockpile[place][res]
