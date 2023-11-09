from sqlite3 import IntegrityError

from db.database import Database


class PlaceAlreadyExistsError(Exception):
    pass


class PlacesDatabase(Database):
    def places(self):
        return [place for _, place
                in self.execute("""SELECT id, name FROM places""").fetchall()]

    def add(self, name):
        try:
            self.execute("""INSERT INTO places (name)
                            VALUES (?)""", (name,))
            self._initialize_stock(name)
        except IntegrityError:
            raise PlaceAlreadyExistsError
        finally:
            self.commit()

    def _initialize_stock(self, name):
        place_id = self.execute("""SELECT id FROM places WHERE name=?;""",
                                (name,)).fetchone()[0]
        resources_ids = [r[0] for r in
                         self.execute("""SELECT id FROM resources;""").fetchall()]
        self.executemany("""INSERT INTO stockpile (place_id, resource_id, quantity)
                            VALUES (?, ?, ?)""",
                         [(place_id, resource_id, 0)
                          for resource_id in resources_ids])
        self.commit()

    def delete(self, name):
        self.execute("""DELETE FROM places WHERE name=?""", (name,))
        self.commit()
