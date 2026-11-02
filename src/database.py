import sqlite3

class TriangleDatabase:
    def __init__(self, db_name: str = ":memory:"):
       
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                side1 TEXT,
                side2 TEXT,
                side3 TEXT,
                triangle_type TEXT,
                error_message TEXT
            )
        """)
        self.conn.commit()

    def add_record(self, side1: str, side2: str, side3: str, t_type: str, error: str):
        self.cursor.execute(
            "INSERT INTO triangles (side1, side2, side3, triangle_type, error_message) VALUES (?, ?, ?, ?, ?)",
            (side1, side2, side3, t_type, error)
        )
        self.conn.commit()

    def get_record(self, side1: str, side2: str, side3: str):
        self.cursor.execute(
            "SELECT triangle_type, error_message FROM triangles WHERE side1=? AND side2=? AND side3=?",
            (side1, side2, side3)
        )
        return self.cursor.fetchone()  # Вернет (type, error) или None

    def delete_record(self, side1: str, side2: str, side3: str):
        self.cursor.execute(
            "DELETE FROM triangles WHERE side1=? AND side2=? AND side3=?",
            (side1, side2, side3)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()