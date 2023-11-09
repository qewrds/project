from db.database import Database
from models.breakage import Breakage


class BreakagesDatabase(Database):
    def add(self, breakage):
        self.execute("""INSERT INTO breakages (place_id, time, description, image)
                     VALUES ((SELECT id FROM places WHERE name=:place),
                              :time, :desc, :image_bytes)""",
                     breakage.to_db())
        self.commit()

    def breakages(self):
        return [Breakage.from_db(entry) for entry in
                self.execute("""SELECT b.id, p.name, b.time, b.description, b.image
                                FROM breakages AS b JOIN places AS p
                                ON b.place_id = p.id;""").fetchall()]

    def fixed(self, breakage):
        self.execute("""DELETE FROM breakages WHERE id=?""", (breakage.id,))
        self.commit()
