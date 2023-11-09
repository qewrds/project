from sqlite3 import IntegrityError

from db.database import Database


class ResourcesDatabase(Database):

    def stocks(self):
        return self.execute("""SELECT p.name,
                                      r.title, r.max_quantity, r.alert_quantity,
                                      s.quantity
                               FROM stockpile AS s
                               JOIN places AS p ON s.place_id = p.id
                               JOIN resources AS r ON s.resource_id = r.id;""")\
            .fetchall()

    def deduct(self, place, resource, quantity):
        self.execute("""UPDATE stockpile SET quantity=(
                            SELECT quantity FROM stockpile WHERE place_id=(
                                SELECT id FROM places WHERE name=:place
                            ) AND resource_id=(
                                SELECT id FROM resources WHERE title=:resource
                            )) - :quantity
                        WHERE place_id=(SELECT id FROM places WHERE name=:place)
                        AND resource_id=(SELECT id FROM resources
                                         WHERE title=:resource);""",
                     {"place": place, "resource": resource, "quantity": quantity})
        self.commit()

    def supply(self, place, resource, quantity):
        self.execute("""UPDATE stockpile SET quantity=(
                            SELECT quantity FROM stockpile WHERE place_id=(
                                SELECT id FROM places WHERE name=:place
                            ) AND resource_id=(
                                SELECT id FROM resources WHERE title=:resource
                            )) + :quantity
                        WHERE place_id=(SELECT id FROM places WHERE name=:place)
                        AND resource_id=(SELECT id FROM resources
                                         WHERE title=:resource);""",
                     {"place": place, "resource": resource, "quantity": quantity})
        self.commit()

    def max_quantity(self, title):
        return self.execute("""SELECT max_quantity
                               FROM resources
                               WHERE title = ?""", (title,)).fetchone()[0]

    def izm_(self, title):
        return self.execute("""SELECT measurement
                               FROM resources
                               WHERE title = ?""", (title,)).fetchone()[0]

    def resources(self):
        return [r[0] for r
                in self.execute("""SELECT title FROM resources;""").fetchall()]

    def delete(self, title):
        self.execute("""DELETE FROM resources WHERE title=?""", (title,))
        self.commit()

    def add(self, title, max_quantity, alert_quantity, measurement):
        try:
            self.execute("""INSERT INTO resources
                            (title, max_quantity, alert_quantity, measurement)
                            VALUES (?, ?, ?, ?)""",
                         (title, max_quantity, alert_quantity, measurement))
            self._initialize_stock(title)
        except IntegrityError:
            raise ResourceAlreadyExistsError
        finally:
            self.commit()

    def _initialize_stock(self, title):
        resource_id = self.execute("""SELECT id FROM resources WHERE title=?;""",
                                   (title,)).fetchone()[0]
        places_ids = [r[0] for r in
                      self.execute("""SELECT id FROM places;""").fetchall()]
        self.executemany("""INSERT INTO stockpile (place_id, resource_id, quantity)
                                    VALUES (?, ?, ?)""",
                         [(place_id, resource_id, 0)
                          for place_id in places_ids])
        self.commit()


class ResourceAlreadyExistsError(Exception):
    pass