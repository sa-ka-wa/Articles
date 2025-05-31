from db.connection import get_connection
from models.article import Article
from models.magazine import Magazine

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
            else:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cursor.lastrowid
            conn.commit()

   

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM authors WHERE name = ?", (name,)).fetchone()
            if row:
                return cls(name=row["name"], id=row["id"])
            return None

    @classmethod    
    def  find_by_id(cls, id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM authors WHERE id = ?", (id,)).fetchone()
            if row:
                return cls(name=row["name"], id=row["id"])
            return None          

    def articles(self):
        return Article.find_by_author(self.id)

    def magazines(self):
        return list({article.magazine() for article in self.articles()})
    

    def add_article(self, title, magazine_id, topic):
        """Create and save a new article by this author"""
        article = Article(title=title, author_id=self.id, magazine_id=magazine_id, topic=topic)
        article.save()
        return article

    def topic_areas(self):
        """Return a set of unique topics from this author's articles"""
        return {article.topic for article in self.articles()}


