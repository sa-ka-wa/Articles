from db.connection import get_connection
from models.article import Article

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            conn.commit()

    @classmethod
    def find_by_id(cls, magazine_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,)).fetchone()
            if row:
                return cls(name=row["name"], category=row["category"], id=row["id"])
            return None
    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM magazines WHERE name = ?", (name,)).fetchone()
            if row:
                return cls(name=row["name"], category=row["category"], id=row["id"])
            return None

    @classmethod
    def find_by_category(cls,category):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM magazines WHERE category = ?", (category,)).fetchall()
            return [cls(name=row["name"], category=row["category"], id=row["id"]) for row in rows]




    def articles(self):
        return Article.find_by_magazine(self.id)

    def contributors(self):
        # Return unique Author objects who contributed articles to this magazine
        authors = {article.author() for article in self.articles()}
        return list(authors)

    def article_titles(self):
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        # Alias for contributors, or add extra logic if needed
        return self.contributors()