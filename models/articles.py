from db.connection import get_connection
from models.magazine import Magazine

class Article:
    def __init__(self, title, author_id, magazine_id, topic, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.topic = topic

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ?, topic = ? WHERE id = ?",
                    (self.title, self.author_id, self.magazine_id, self.topic, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id, topic) VALUES (?, ?, ?, ?)",
                    (self.title, self.author_id, self.magazine_id, self.topic)
                )
                self.id = cursor.lastrowid
            conn.commit()

    @classmethod
    def find_by_author(cls, author_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,)).fetchall()
            return [cls(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"], topic=row["topic"]) for row in rows]

    @classmethod
    def find_by_id(cls, article_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
            if row:
                return cls(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"], topic=row["topic"])
            return None

    @classmethod
    def find_by_title(cls, title):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM articles WHERE title = ?", (title,)).fetchall()
            return [cls(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"], topic=row["topic"]) for row in rows]
    @classmethod
    def find_by_magazine(cls, magazine_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,)).fetchall()
            return [cls(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"], topic=row["topic"]) for row in rows]

    def magazine(self):
        return Magazine.find_by_id(self.magazine_id)