import sqlite3

class DBManager:
    def __init__(self, db_name='app.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def get_value(self, food_name):
        self.cursor.execute("SELECT value FROM data WHERE Food_Items=?", (food_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user(userid INTEGER PRIMARY KEY, username TEXT, )")